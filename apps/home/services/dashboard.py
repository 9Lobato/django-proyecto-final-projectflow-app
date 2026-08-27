# apps\home\services\dashboard.py sirve para:
# preparar los datos necesarios para mostrar el dashboard principal
# según el usuario actual y sus permisos

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.db.models import Count, Exists, IntegerField, OuterRef, Q
from django.db.models.functions import Cast, Substr
# Imports internos de proyecto/apps
from apps.projects.models import Assignment, Project, ProjectTemplate
from apps.projects.querysets import get_projects_queryset
from apps.tasks.services.inbox import get_user_inbox


# prepara los datos necesarios para el dashboard del usuario
def get_dashboard_context(user):

  is_owner = (
    user.is_superuser
    or Assignment.objects.filter(
      user=user,
      role__name="OWNER",
    ).exists()
  )

  projects = get_projects_queryset()

  if is_owner:
    dashboard_projects = projects
  else:
    dashboard_projects = (
      projects
      .filter(
        Q(assignments__user=user) |
        Q(followers__user=user)
      )
      .distinct()
    )

  inbox = get_user_inbox(user, dashboard_projects)

  followed = Project.objects.filter(
    followers__user=user,
    pk=OuterRef("pk")
  )

  if is_owner:
    dashboard_projects = (
      projects
      .annotate(is_followed=Exists(followed))
    )
  else:
    dashboard_projects = (
      projects
      .filter(
        Q(assignments__user=user) |
        Q(followers__user=user)
      )
      .distinct()
      .annotate(is_followed=Exists(followed))
    )

  notification_projects = []

  project_qs = (
    Project.objects
    .filter(
      id__in=inbox.values_list(
        "task__project_id",
        flat=True
      ).distinct()
    )
    .annotate(
      is_followed=Exists(followed),
      project_year=Cast(Substr("code", 1, 2), IntegerField()),
      project_number=Cast(Substr("code", 4, 3), IntegerField()),
    )
    .order_by(
      "-project_year",
      "-project_number",
    )
  )

  for project in project_qs:

    notifications = inbox.filter(
      task__project=project
    ).select_related(
      "task"
    ).order_by(
      "task__sequence_number",
      "-created_at"
    )

    for comment in notifications:
      comment.can_delete_request_user = comment.can_delete_request(user)
      comment.can_resolve_user = comment.can_resolve(user)
      comment.can_reopen_user = comment.can_reopen(user)
      comment.can_delete_user = comment.can_delete(user)

    project.notifications = notifications
    notification_projects.append(project)

  templates = (
    ProjectTemplate.objects
    .annotate(
      projects_count=Count("projects"),
      tasks_count=Count("tasks"),
    )
    .order_by(
      "-projects_count",
      "-generated_from",
    )
  )

  return {
    "dashboard_projects": dashboard_projects,
    "notification_projects": notification_projects,
    "templates": templates,
  }
