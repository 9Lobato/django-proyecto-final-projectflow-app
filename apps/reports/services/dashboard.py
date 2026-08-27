# apps\reports\services\dashboard.py sirve para:
# recopilar y preparar los datos necesarios para el dashboard de informes,
# incluyendo métricas generales, tareas, proyectos y estadísticas del equipo

# Librerías estándar de Python
from datetime import date
import math
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
# Imports internos de proyecto/apps
from apps.projects.models import Project
from apps.reports.services import metrics
from apps.reports.services.project_progress_service import get_progress_snapshots
from apps.tasks.models import Task


# Etiquetas de los estados de las tareas para mostrar en el dashboard
STATUS_LABELS = {
  "TODO": "To do",
  "IN_PROGRESS": "In progress",
  "DONE": "Done",
  "CANCELLED": "Cancelled",
}


# Pesos para calcular la participación según el rol: proyectos asignados y tareas ejecutadas
ROLE_WEIGHTS = {
  "OWNER":   (0.85, 0.15),
  "MANAGER": (0.70, 0.30),
  "MEMBER":  (0.30, 0.70),
}


# HELPER PRIVADO: obtiene los usuarios con sus estadísticas de tareas
def _get_report_users():

  return (
    User.objects
    .annotate(
      active_tasks=Count(
        "assigned_tasks",
        filter=(
          Q(
            assigned_tasks__status__in=[
              "TODO",
              "IN_PROGRESS",
            ]
          )
          & Q(assigned_tasks__project__is_archived=False)
          & (
            Q(assigned_tasks__due_at__isnull=True)
            | Q(assigned_tasks__due_at__gte=timezone.now())
          )
        ),
      ),
      completed_tasks=Count(
        "assigned_tasks",
        filter=Q(
          assigned_tasks__status="DONE",
        ),
      ),
      overdue_tasks=Count(
        "assigned_tasks",
        filter=Q(
          assigned_tasks__status__in=[
            "TODO",
            "IN_PROGRESS",
          ],
          assigned_tasks__due_at__lt=timezone.now(),
          assigned_tasks__project__is_archived=False,
        ),
      ),
    )
    .prefetch_related("assigned_tasks")
    .order_by("username")
  )


# HELPER PRIVADO: genera los meses del informe desde el mes de creación del primer
# proyecto hasta el mes actual
def _get_report_months():

  today = timezone.now().date()

  first_project = (
    Project.objects
    .order_by("created_at")
    .first()
  )

  if not first_project:
    return []

  first_month = first_project.created_at.date().replace(
    day=1,
  )

  current_month = today.replace(
    day=1,
  )

  months = []

  year = first_month.year
  month = first_month.month

  while (
    year < current_month.year
    or (
      year == current_month.year
      and month <= current_month.month
    )
  ):

    months.append(
      date(year, month, 1)
    )

    month += 1

    if month > 12:
      month = 1
      year += 1

  return months


# HELPER PRIVADO: resumen general del dashboard
def _get_summary_data():

  total_projects = (
    Project.objects
    .count()
  )

  active_projects = (
    Project.objects
    .filter(
      is_archived=False,
    )
    .count()
  )

  archived_projects = (
    Project.objects
    .filter(
      is_archived=True,
    )
    .count()
  )

  total_tasks = (
    Task.objects
    .filter(
      project__is_archived=False,
      deleted_at__isnull=True,
    )
    .count()
  )

  active_tasks = (
    Task.objects
    .filter(
      project__is_archived=False,
      deleted_at__isnull=True,
      status__in=[
        "TODO",
        "IN_PROGRESS",
      ],
    )
    .count()
  )

  completed_tasks = (
    Task.objects
    .filter(
      project__is_archived=False,
      deleted_at__isnull=True,
      status="DONE",
    )
    .count()
  )

  cancelled_tasks = (
    Task.objects
    .filter(
      project__is_archived=False,
      deleted_at__isnull=True,
      status="CANCELLED",
    )
    .count()
  )

  total_users = User.objects.count()

  completed_percentage = 0

  if total_tasks:
    completed_percentage = round(
      completed_tasks /
      total_tasks *
      100
    )

  return {
    "total_projects": total_projects,
    "active_projects": active_projects,
    "archived_projects": archived_projects,

    "total_tasks": total_tasks,
    "active_tasks": active_tasks,
    "completed_tasks": completed_tasks,
    "cancelled_tasks": cancelled_tasks,

    "total_users": total_users,
    "completed_percentage": completed_percentage,
  }


# HELPER PRIVADO: distribución de tareas por estado
def _get_task_status_data():

  status_order = [
    "TODO",
    "IN_PROGRESS",
    "DONE",
    "CANCELLED",
  ]

  tasks_by_status = (
    Task.objects
    .filter(
      project__is_archived=False,
      deleted_at__isnull=True,
    )
    .values("status")
    .annotate(total=Count("id"))
  )

  status_dict = {
    item["status"]: item["total"]
    for item in tasks_by_status
  }

  return {
    "status_labels": [
      STATUS_LABELS[status]
      for status in status_order
    ],
    "status_data": [
      status_dict.get(status, 0)
      for status in status_order
    ],
  }


# HELPER PRIVADO: entrega de tareas
def _get_task_delivery_data():

  now = timezone.now()

  delivery_dict = {
    "NO_LIMIT": 0,
    "ON_TIME": 0,
    "OVERDUE": 0,
  }

  tasks = (
    Task.objects
    .filter(
      project__is_archived=False,
      deleted_at__isnull=True,
    )
  )

  for task in tasks:

    # Sin límite
    if (
      task.due_at is None
      or task.status in [
        "DONE",
        "CANCELLED",
      ]
    ):
      delivery_dict["NO_LIMIT"] += 1

    # Vencidas
    elif (
      task.due_at < now
      and task.status in [
        "TODO",
        "IN_PROGRESS",
      ]
    ):
      delivery_dict["OVERDUE"] += 1

    # En plazo
    elif (
      task.due_at >= now
      and task.status in [
        "TODO",
        "IN_PROGRESS",
      ]
    ):
      delivery_dict["ON_TIME"] += 1


  order = [
    "NO_LIMIT",
    "ON_TIME",
    "OVERDUE",
  ]

  return {
    "delivery_labels": [
      "Sin límite",
      "En plazo",
      "Vencidas",
    ],
    "delivery_data": [
      delivery_dict[item]
      for item in order
    ],
  }


# HELPER PRIVADO: prioridad de tareas
def _get_task_priority_data():

  tasks_by_priority = (
    Task.objects
    .filter(
      project__is_archived=False,
      deleted_at__isnull=True,
    )
    .values("priority")
    .annotate(total=Count("id"))
  )

  priority_dict = {
    item["priority"]: item["total"]
    for item in tasks_by_priority
  }

  priority_order = [
    "HIGH",
    "MEDIUM",
    "LOW",
  ]

  return {
    "priority_labels": [
      "Alta",
      "Media",
      "Baja",
    ],
    "priority_data": [
      priority_dict.get(priority, 0)
      for priority in priority_order
    ],
  }


# HELPER PRIVADO: creación de proyectos
def _get_project_creation_data():

  months = _get_report_months()

  if not months:
    return {
      "months": [],
      "projects_month": [],
      "projects_created_codes": [],
    }

  first_month = months[0]

  projects_by_month = (
    Project.objects
    .filter(
      created_at__date__gte=first_month
    )
    .annotate(
      month=TruncMonth("created_at")
    )
    .values("month")
    .annotate(
      total=Count("id")
    )
    .order_by("month")
  )

  month_dict = {
    item["month"].date(): item["total"]
    for item in projects_by_month
  }

  codes_by_month = {}

  projects = (
    Project.objects
    .filter(
      created_at__date__gte=first_month
    )
    .annotate(
      month=TruncMonth("created_at")
    )
    .order_by("created_at")
  )

  for project in projects:

    month = project.month.date()

    if month not in codes_by_month:
      codes_by_month[month] = []

    codes_by_month[month].append(
      project.code
    )

  return {
    "months": [
      month.strftime("%b %Y")
      for month in months
    ],
    "projects_month": [
      month_dict.get(month, 0)
      for month in months
    ],
    "projects_created_codes": [
      codes_by_month.get(month, [])
      for month in months
    ],
  }


# HELPER PRIVADO: proyectos archivados por mes
def _get_project_archived_data():

  months = _get_report_months()

  if not months:
    return {
      "archived_months": [],
      "projects_archived_month": [],
      "projects_archived_codes": [],
    }

  first_month = months[0]

  projects_by_month = (
    Project.objects
    .filter(
      archived_at__isnull=False,
      archived_at__date__gte=first_month,
    )
    .annotate(
      month=TruncMonth("archived_at")
    )
    .values("month")
    .annotate(total=Count("id"))
    .order_by("month")
  )

  month_dict = {
    item["month"].date(): item["total"]
    for item in projects_by_month
  }

  codes_by_month = {}

  projects = (
    Project.objects
    .filter(
      archived_at__isnull=False,
      archived_at__date__gte=first_month,
    )
    .annotate(
      month=TruncMonth("archived_at")
    )
    .order_by("archived_at")
  )

  for project in projects:

    month = project.month.date()

    if month not in codes_by_month:
      codes_by_month[month] = []

    codes_by_month[month].append(
      project.code
    )

  return {
    "archived_months": [
      month.strftime("%b %Y")
      for month in months
    ],
    "projects_archived_month": [
      month_dict.get(month, 0)
      for month in months
    ],
    "projects_archived_codes": [
      codes_by_month.get(month, [])
      for month in months
    ],
  }


# HELPER PRIVADO: estadísticas de usuarios
def _get_user_workload():

  users = _get_report_users()

  return {
    "user_labels": [
      user.username
      for user in users
    ],
    "user_tasks": [
      user.active_tasks
      for user in users
    ],
  }


# HELPER PRIVADO: productividad de usuarios
def _get_user_productivity():

  users = _get_report_users()

  productivity_labels = []
  productivity_data = []

  for user in users:

    summary = metrics.user_summary(user)

    productivity_labels.append(
      summary["username"]
    )

    productivity_data.append(
      summary["productivity"]
    )

  return {
    "productivity_labels": productivity_labels,
    "productivity_data": productivity_data,
  }


# HELPER PRIVADO: análisis de proyectos
def _get_project_statistics():

  projects = (
    Project.objects
    .prefetch_related("tasks")
    .order_by("-code")
  )

  project_statistics = []

  for project in projects:

    summary = metrics.project_summary(project)

    project_statistics.append(summary)

  return {
    "project_statistics": project_statistics,
  }


# HELPER PRIVADO: estado del equipo
def _get_team_statistics():

  users = _get_report_users()

  team_statistics = [
    metrics.user_summary(user)
    for user in users
  ]

  max_projects = max(
    (u["project_count"] for u in team_statistics),
    default=1,
  )

  max_tasks = max(
    (u["task_count"] for u in team_statistics),
    default=1,
  )

  for user in team_statistics:

    project_score = (
      math.sqrt(user["project_count"]) /
      math.sqrt(max_projects) * 100
      if max_projects else 0
    )

    task_score = (
      math.sqrt(user["task_count"]) /
      math.sqrt(max_tasks) * 100
      if max_tasks else 0
    )

    project_weight, task_weight = ROLE_WEIGHTS.get(
      user["role_code"],
      (0.4, 0.6),
    )

    user["participation"] = round(
      project_score * project_weight +
      task_score * task_weight
    )

    user["workload"] = (
      round(user["task_count"] / max_tasks * 100)
      if max_tasks else 0
    )

  return {
    "team_statistics": team_statistics,
    "participation_labels": [u["username"] for u in team_statistics],
    "participation_data": [u["participation"] for u in team_statistics],
    "productivity_labels": [u["username"] for u in team_statistics],
    "productivity_data": [u["productivity"] for u in team_statistics],
  }


# HELPER PRIVADO: construye el contexto con las métricas generales y de tareas
def _build_general_context():

  context = {}

  context.update(_get_summary_data())
  context.update(_get_task_status_data())
  context.update(_get_task_delivery_data())
  context.update(_get_task_priority_data())

  return context


# HELPER PRIVADO: construye el contexto con las métricas y evolución de proyectos
def _build_project_context():

  context = {}

  context.update(_get_project_creation_data())
  context.update(_get_project_archived_data())

  progress_context = get_progress_snapshots()

  context.update(progress_context)
  context.update(
    _get_project_statistics()
  )

  return context


# HELPER PRIVADO: construye el contexto con las estadísticas y métricas del equipo
def _build_team_context():

  context = {}

  context.update(_get_user_workload())
  context.update(_get_user_productivity())
  context.update(_get_team_statistics())

  return context


# Construye y devuelve todos los datos necesarios para el dashboard de informes
def build_report_dashboard():

  context = {}

  context.update(_build_general_context())
  context.update(_build_project_context())
  context.update(_build_team_context())

  context["report_months"] = _get_report_months()

  return context
