# apps\kanban\views.py sirve para:
# gestionar las vistas del tablero Kanban
# mostrar los proyectos y sus tareas organizadas por estado
# y gestionar acciones como mover y copiar tareas

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
# Imports internos de proyecto/apps
from apps.projects.models import Project
from apps.projects.permissions import user_can_create_task, user_can_edit_task, user_can_view_task
from apps.projects.utils import prepare_project_for_user
from apps.tasks.models import Task


# muestra el tablero Kanban con los proyectos y sus tareas
@login_required
def board(request):

  user = request.user

  if user.is_superuser:

    projects = (
      Project.objects
      .all()
      .order_by("-code")
    )

  else:

    assigned_projects = Project.objects.filter(
      assignments__user=user
    )

    followed_projects = Project.objects.filter(
      followers__user=user
    )

    projects = (
      assigned_projects |
      followed_projects
    ).distinct().order_by("-code")

  data = []

  for project in projects:

    prepare_project_for_user(project, user)

    tasks = Task.objects.filter(project=project)

    task_data = []

    for task in tasks:
      task_data.append({
        "task": task,
        "can_move": user_can_edit_task(user, task),
      })

    data.append({
      "project": project,
      "todo": [
        item for item in task_data
        if item["task"].status == "TODO"
      ],
      "progress": [
        item for item in task_data
        if item["task"].status == "IN_PROGRESS"
      ],
      "done": [
        item for item in task_data
        if item["task"].status == "DONE"
      ],
      "cancelled": [
        item for item in task_data
        if item["task"].status == "CANCELLED"
      ],
    })

  return render(request, "kanban/kanban.html", {
    "board": data
  })


# mueve una tarea entre los estados permitidos del tablero Kanban
@require_POST
@login_required
def move_task(request):

  task_id = request.POST.get("task_id")
  new_status = request.POST.get("status")

  VALID_STATUS = {
    "TODO",
    "IN_PROGRESS",
    "DONE",
    "CANCELLED",
  }

  ALLOWED_MOVES = {
    "TODO": {
      "IN_PROGRESS",
      "CANCELLED",
    },
    "IN_PROGRESS": {
      "TODO",
      "DONE",
      "CANCELLED",
    },
    "DONE": {
      "IN_PROGRESS",
    },
    "CANCELLED": {
      "TODO",
      "IN_PROGRESS",
    },
  }

  try:

    task = Task.objects.get(
      id=task_id,
      deleted_at__isnull=True,
    )

    # Permiso para mover la tarea
    if not user_can_edit_task(request.user, task):
      return JsonResponse(
        {
          "success": False,
          "error": "No tienes permiso para mover esta tarea.",
        },
        status=403,
      )

    # Estado válido
    if new_status not in VALID_STATUS:
      return JsonResponse(
        {
          "success": False,
          "error": "Estado no válido.",
        },
        status=400,
      )

    # Transición permitida
    if new_status not in ALLOWED_MOVES.get(task.status, set()):
      return JsonResponse(
        {
          "success": False,
          "error": "Movimiento no permitido.",
        },
        status=400,
      )

    # Una tarea planificada no puede volver a TODO
    if (
      task.is_planned
      and task.status == "IN_PROGRESS"
      and new_status == "TODO"
    ):
      return JsonResponse(
        {
          "success": False,
          "error": (
            "Una tarea planificada no puede volver a "
            "'To do'. Elimina primero la planificación."
          ),
        },
        status=400,
      )

    old_status = task.status

    task.status = new_status
    task.update_status(old_status)

    return JsonResponse({
      "success": True
    })

  except Task.DoesNotExist:

    return JsonResponse(
      {
        "success": False,
        "error": "La tarea no existe.",
      },
      status=404,
    )
    

# copia una tarea a otro proyecto si el usuario tiene permisos
@require_POST
@login_required
def copy_task(request):

  task_id = request.POST.get("task_id")
  project_id = request.POST.get("project_id")

  try:

    original_task = Task.objects.get(id=task_id)

    if not user_can_view_task(request.user, original_task):
      return JsonResponse(
        {"success": False},
        status=403,
      )

    new_project = Project.objects.get(id=project_id)

    if not user_can_create_task(request.user, new_project):
      return JsonResponse(
        {"success": False},
        status=403,
      )

    new_task = Task.objects.create(
      title=original_task.title,
      description=original_task.description,
      priority=original_task.priority,
      project=new_project,
      status="TODO",
      created_by=request.user,
    )

    return JsonResponse({
      "success": True,
      "task_id": new_task.id
    })

  except (Task.DoesNotExist, Project.DoesNotExist):
    return JsonResponse(
      {"success": False},
      status=404
    )
