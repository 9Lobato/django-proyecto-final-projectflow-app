# apps\tasks\views.py sirve para:
# gestionar las peticiones HTTP relacionadas con las tareas y sus comentarios, incluyendo listar, crear, editar,
# duplicar y eliminar tareas, aplicar filtros y permisos de acceso, gestionar comentarios y solicitudes,
# y devolver las respuestas HTML o JSON correspondientes

# Librerías estándar de Python
from urllib.parse import urlencode
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Case, Count, IntegerField, Q, Value, When
from django.db.models.functions import Cast, Substr
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse
# Imports internos de proyecto/apps
from apps.core.utils.navigation import get_previous_next
from apps.projects.models import Assignment, Project, Role
from apps.projects.permissions import user_can_view_task,user_can_edit_task, user_can_create_task, user_can_duplicate_task, user_can_delete_task, get_user_role, get_task_access_mode
from apps.reports.services.project_progress_service import rebuild_project_snapshots
from .forms import TaskCommentForm, TaskForm
from .models import Task, TaskComment
from .utils import get_mentioned_users


# Listar, filtrar y mostrar las tareas accesibles para el usuario
@login_required
def task_list(request):

  project = request.GET.get("project") or None
  followed_projects = Project.objects.filter(followers__user=request.user)
  assigned_projects = Project.objects.filter(assignments__user=request.user)

  if request.user.is_superuser:
    allowed_projects = Project.objects.all()
  elif project:
    allowed_projects = Project.objects.filter(pk=project)
  else:
    allowed_projects = (assigned_projects | followed_projects).distinct()

  tasks = (
    Task.objects
    .select_related(
      "project",
      "created_by",
      "assigned_to",
    )
    .filter(project__in=allowed_projects, deleted_at__isnull=True)
    .annotate(
      watchers_count=Count("watchers", distinct=True),

      comments_count=Count(
        "comments",
        filter=Q(comments__type=TaskComment.COMMENT),
        distinct=True,
      ),

      my_comments_count=Count(
        "comments",
        filter=Q(
          comments__type=TaskComment.COMMENT,
          comments__user=request.user,
        ),
        distinct=True,
      ),

      requests_count=Count(
        "comments",
        filter=Q(comments__type=TaskComment.REQUEST),
        distinct=True,
      ),

      my_requests_count=Count(
        "comments",
        filter=Q(
          comments__type=TaskComment.REQUEST,
          comments__user=request.user,
        ),
        distinct=True,
      ),
    )
  )

  base_tasks = tasks

  created_by_users = User.objects.filter(
    project_assignments__role__name__in=["OWNER", "MANAGER"]
  ).distinct()

  assigned_to_users = User.objects.filter(
    project_assignments__isnull=False
  ).distinct()

  created_by = request.GET.get("created_by") or None
  assigned_to = request.GET.get("assigned_to") or None
  status = request.GET.getlist("status")
  delivery = request.GET.getlist("delivery")
  priority = request.GET.getlist("priority")
  search = request.GET.get("search") or None

  if created_by:
    tasks = tasks.filter(created_by_id=created_by)

  if assigned_to == "unassigned":
    tasks = tasks.filter(assigned_to__isnull=True)
  elif assigned_to:
    tasks = tasks.filter(assigned_to_id=assigned_to)

  if status:
    tasks = tasks.filter(status__in=status)

  today = timezone.localdate()

  if delivery:

    q = Q()

    if "NO_LIMIT" in delivery:
      q |= (
        Q(due_at__isnull=True)
        | Q(status__in=["DONE", "CANCELLED"])
      ) & Q(
        project__is_archived=False
      )

    if "ARCHIVED" in delivery:
      q |= Q(
        project__is_archived=True
      )

    if "OVERDUE" in delivery:
      q |= Q(
        due_at__lt=timezone.now(),
        status__in=[
          "TODO",
          "IN_PROGRESS",
        ],
        project__is_archived=False,
      )

    if "ON_TIME" in delivery:
      q |= Q(
        due_at__gte=timezone.now(),
        status__in=[
          "TODO",
          "IN_PROGRESS",
        ],
        project__is_archived=False,
      )

    tasks = tasks.filter(q)

  if priority:
    tasks = tasks.filter(priority__in=priority)

  if search:
    tasks = tasks.filter(
      Q(title__icontains=search)
      | Q(description__icontains=search)
    )

  if project:
    tasks = tasks.filter(project_id=project)

  tasks = (
    tasks
    .annotate(
      status_order=Case(
        When(status="IN_PROGRESS", then=Value(1)),
        When(status="TODO", then=Value(2)),
        When(status="CANCELLED", then=Value(3)),
        When(status="DONE", then=Value(4)),
        output_field=IntegerField(),
      )
    )
    .order_by("project__code", "status_order", "id")
    .distinct()
  )

  project_ids = set(
    tasks.values_list("project_id", flat=True)
  )

  projects = (
    Project.objects
    .filter(id__in=project_ids)
    .annotate(
      project_year=Cast(
        Substr("code", 1, 2),
        IntegerField()
      ),
      project_number=Cast(
        Substr("code", 4, 3),
        IntegerField()
      ),
    )
    .order_by(
      "-project_year",
      "-project_number"
    )
  )

  for p in projects:
    p.task_count = (
      base_tasks
      .filter(project_id=p.id)
      .values("pk")
      .distinct()
      .count()
    )

    p.filtered_task_count = (
      tasks
      .filter(project_id=p.id)
      .values("pk")
      .distinct()
      .count()
    )

  followed_set = set()

  if not project:
    followed_set = set(followed_projects.values_list("id", flat=True))

  for p in projects:
    p.is_followed = p.id in followed_set
    p.can_create_task = user_can_create_task(request.user, p)

  filter_open = any([
    created_by,
    assigned_to,
    status,
    delivery,
    priority,
    search,
  ]) or request.GET.get("keep_open") == "1"

  task_filters_active = any([
    created_by,
    assigned_to,
    status,
    delivery,
    priority,
    search,
  ])

  all_tasks_exist = base_tasks.exists()

  visible_tasks_exist = (
    base_tasks
    .filter(project__assignments__user=request.user)
    .exists()
    if not request.user.is_superuser
    else all_tasks_exist
  )

  filtered_tasks_exist = tasks.exists()

  return render(
    request,
    "tasks/task_list.html",
    {
      "tasks": tasks,
      "projects": projects,
      "created_by_users": created_by_users,
      "assigned_to_users": assigned_to_users,
      "created_selected": created_by,
      "assigned_selected": assigned_to,
      "status_selected": status,
      "delivery_selected": delivery,
      "priority_selected": priority,
      "search_value": search,
      "filter_open": filter_open,
      "filters_active": task_filters_active,
      "today": today,
      "all_tasks_exist": all_tasks_exist,
      "visible_tasks_exist": visible_tasks_exist,
      "filtered_tasks_exist": filtered_tasks_exist,
    },
  )


# Editar una tarea y gestionar sus comentarios y solicitudes
@login_required
def task_update(request, pk):

  task = get_object_or_404(Task, pk=pk, deleted_at__isnull=True)

  old_status = task.status

  next_url = request.GET.get("next")

  if not next_url or next_url == "None":
    next_url = None

  mode = get_task_access_mode(request.user, task)

  if mode == "DENY":
    return render(request, "common/403.html", status=403)

  readonly = (mode == "READONLY" or task.project.is_archived)

  user_role = get_user_role(request.user, task.project)

  is_follow_only = (
    task.project.followers.filter(user=request.user).exists()
    and not task.project.assignments.filter(user=request.user).exists()
  )

  can_edit = user_can_edit_task(request.user, task)

  can_comment = (
    not readonly
    and mode == "EDIT"
    and not is_follow_only
  )

  comment_locked = not can_comment

  if request.method == "POST":

    if "save_task" in request.POST or "apply" in request.POST:

      if not can_edit:
        return render(request, "common/403.html", status=403)

      form = TaskForm(request.POST, instance=task, user=request.user, readonly=readonly, user_role=user_role, project=task.project)

      if form.is_valid():

        task = form.save(commit=False)
        task.update_status(old_status)

        rebuild_project_snapshots(task.project)

        if "save_task" in request.POST:
          return redirect(next_url) if next_url else redirect("task_list")

        if next_url:
          return redirect(
            f"{reverse('task_update', kwargs={'pk': task.pk})}?{urlencode({'next': next_url})}"
          )

        return redirect("task_update", pk=task.pk)
      
      return redirect("task_update", pk=task.pk)

    elif "send_notification" in request.POST:

      if not can_comment:
        return render(request, "common/403.html", status=403)

      comment_form = TaskCommentForm(
        request.POST,
        user=request.user,
        readonly=readonly,
        is_follow_only=is_follow_only or readonly
      )

      if comment_form.is_valid():
        comment = comment_form.save(commit=False)

        comment.type = TaskComment.COMMENT
        comment.request_kind = ""

        if user_role in ["OWNER", "MANAGER"]:
            comment.type = comment_form.cleaned_data["type"]
            comment.request_kind = comment_form.cleaned_data["request_kind"]

        comment.task = task
        comment.user = request.user
        comment.save()

        mentioned_users = get_mentioned_users(comment.text)
        member_role = Role.objects.get(name="MEMBER")

        for user in mentioned_users:
          task.watchers.add(user)

          Assignment.objects.get_or_create(
            user=user,
            project=task.project,
            defaults={"role": member_role}
          )
      
      return redirect("task_update", pk=task.pk)

    return redirect("task_update", pk=task.pk)

  else:

    form = TaskForm(instance=task, user=request.user, readonly=readonly, user_role=user_role, project=task.project)

    comment_form = TaskCommentForm(
      user=request.user,
      readonly=readonly,
      is_follow_only=is_follow_only or readonly
    )

  # navegación
  project_tasks = Task.objects.filter(
    project=task.project
  ).order_by("id")

  project_tasks = [
    t for t in project_tasks
    if user_can_view_task(request.user, t)
  ]

  previous_task, next_task = get_previous_next(project_tasks, task)
  
  comments = list(task.comments.select_related("user"))

  for comment in comments:
    is_owner = user_role == "OWNER"
    is_manager = user_role == "MANAGER"
    is_author = comment.user == request.user
    author_role = get_user_role(comment.user, task.project)

    if is_owner:
      comment.can_delete = True
    elif is_manager:
      comment.can_delete = is_author or author_role == "MEMBER"
    else:
      comment.can_delete = is_author

  return render(request, "tasks/task_form.html", {
    "form": form,
    "task": task,
    "comments": comments,
    "project": task.project,
    "mode": "edit",
    "user_role": user_role,
    "previous_task": previous_task,
    "next_task": next_task,
    "can_edit_task": can_edit,
    "can_create_task": user_can_create_task(request.user, task.project),
    "can_duplicate_task": user_can_duplicate_task(request.user, task.project),
    "can_delete_task": user_can_delete_task(request.user, task) and not task.project.is_archived,
    "comment_form": comment_form,
    "comment_locked": comment_locked,
    "can_comment": can_comment,
    "is_follow_only": is_follow_only,
    "readonly": readonly,
    "next": next_url,
  })


# Crear una nueva tarea dentro de un proyecto
@login_required
def task_create(request, project_id):

  project = get_object_or_404(Project, id=project_id)

  next_url = request.POST.get("next") or request.GET.get("next")

  if not next_url or next_url == "None":
      next_url = None

  user_role = get_user_role(request.user, project)

  if not user_can_create_task(request.user, project):
    return render(request, "common/403.html", status=403)

  if request.method == "POST":

    if "clear" in request.POST:
      url = request.path

      if next_url:
          url += "?" + urlencode({"next": next_url})

      return redirect(url)

    form = TaskForm(request.POST, user=request.user, user_role=user_role, is_create=True, project=project)

    if form.is_valid():

      new_task = form.save(commit=False)
      new_task.initialize_new_task(request.user)

      rebuild_project_snapshots(new_task.project)

      if "apply" in request.POST:

        if next_url:
          return redirect(
            f"{reverse('task_update', kwargs={'pk': new_task.pk})}?{urlencode({'next': next_url})}"
          )

        return redirect("task_update", pk=new_task.pk)

      return redirect(next_url) if next_url else redirect("task_list")

  else:

    form = TaskForm(
      initial={"project": project.pk},
      user=request.user,
      user_role=user_role,
      is_create=True,
      project=project,
    )

  return render(request, "tasks/task_form.html", {
    "form": form,
    "task": None,
    "project": project,
    "mode": "create",
    "user_role": user_role,
    "previous_task": None,
    "next_task": None,
    "can_edit_task": user_can_create_task(request.user, project),
    "can_delete_task": False,
    "can_create_task": user_can_create_task(request.user, project),
    "comment_form": TaskCommentForm(user=request.user, readonly=True),
    "user": request.user,
    "next": next_url,})


# Duplicar una tarea existente dentro de su proyecto
@login_required
def task_duplicate(request, pk):

  task = get_object_or_404(Task, pk=pk, deleted_at__isnull=True)

  next_url = request.POST.get("next") or request.GET.get("next")

  if not next_url or next_url == "None":
    next_url = None

  if not user_can_duplicate_task(request.user, task.project):
    return render(request, "common/403.html", status=403)

  user_role = get_user_role(request.user, task.project)

  if request.method == "POST":

    form = TaskForm(request.POST, user=request.user, user_role=user_role, is_create=True, project=task.project)

    if form.is_valid():

      new_task = form.save(commit=False)
      new_task.initialize_new_task(request.user)

      rebuild_project_snapshots(new_task.project)

      if "apply" in request.POST:

        if next_url:
          return redirect(
            f"{reverse('task_update', kwargs={'pk': new_task.pk})}?{urlencode({'next': next_url})}"
          )

        return redirect("task_update", pk=new_task.pk)

      return redirect(next_url) if next_url else redirect("task_list")
  
  form = TaskForm(
    initial={
      "project": task.project.pk,
      "title": task.title,
      "description": task.description,
    },
    user=request.user,
    user_role=user_role,
    is_create=True,
    project=task.project
  )

  projects = Project.objects.filter(
    assignments__user=request.user
  ).distinct()

  return render(request, "tasks/task_form.html", {
    "form": form,
    "task": task,
    "project": task.project,
    "mode": "duplicate",
    "user_role": user_role,
    "projects": projects,
    "previous_task": None,
    "next_task": None,
    "can_edit_task": True,
    "can_delete_task": False,
    "can_create_task": user_can_create_task(request.user, task.project),
    "next": next_url,
  })


# Eliminar una tarea mediante borrado lógico
@login_required
def task_delete(request, pk):
  task = get_object_or_404(Task, pk=pk)
  # Un proyecto archivado es solo lectura
  if task.project.is_archived:
    return render(request, "common/403.html", status=403)
  # Bloqueo por permisos
  if not user_can_delete_task(request.user, task):
    return render(request, "common/403.html", status=403)
  next_url = request.GET.get("next")
  if not next_url or next_url == "None":
    next_url = None
  if request.method == "POST":
    task.soft_delete()
    rebuild_project_snapshots(task.project)
    return redirect(next_url) if next_url else redirect("task_list")
  return render(request, "common/confirm_delete.html", {
    "type": "tarea",
    "name": task.title,
    "task": task,
    "gender": "la",
    "next": next_url,
  })


# Eliminar un comentario o solicitud de una tarea
@login_required
def delete_comment(request, pk):
  comment = get_object_or_404(TaskComment, pk=pk)
  next_url = request.GET.get("next")
  if not comment.can_delete(request.user):
    return render(
      request,
      "common/403.html",
      {
        "next": next_url,
      },
      status=403,
    )
  if request.method == "POST":
    comment.delete()
    if next_url:
      return redirect(next_url)
    return redirect("home")
  return render(request, "common/confirm_delete.html", {
    "type": "solicitud",
    "name": comment.text[:80],
    "gender": "la",
    "next": next_url,
  })


# Actualizar el tipo de una solicitud de tarea
@login_required
def update_request_kind(request, pk):
  comment = get_object_or_404(TaskComment, pk=pk)
  if request.method != "POST":
    return JsonResponse({"ok": False}, status=405)
  if comment.type != TaskComment.REQUEST:
    return JsonResponse({"ok": False}, status=400)
  comment.request_kind = request.POST.get("value")
  comment.save()
  return JsonResponse({"ok": True})


# Resolver o reabrir una solicitud de tarea
@login_required
def update_comment_status(request, pk):
  if request.method != "POST":
    return JsonResponse({"success": False}, status=405)
  comment = get_object_or_404(TaskComment, pk=pk)
  if comment.type != TaskComment.REQUEST:
    return JsonResponse({"success": False}, status=400)
  # Resolver
  if not comment.resolved:
    if not comment.can_resolve(request.user):
      return JsonResponse({"success": False}, status=403)
    comment.resolved = True
    comment.resolved_at = timezone.now()
    status = "RESOLVED"
  # Reabrir
  else:
    if not comment.can_reopen(request.user):
      return JsonResponse({"success": False}, status=403)
    comment.resolved = False
    comment.resolved_at = None
    status = "OPEN"
  comment.save()
  return JsonResponse({
    "success": True,
    "status": status,
    "resolved_at": (
      timezone.localtime(comment.resolved_at).strftime("%d/%m/%y %H:%M")
      if comment.resolved_at else ""
    ),
    "can_reopen": comment.can_reopen(request.user),
    "can_resolve": comment.can_resolve(request.user),
  })
