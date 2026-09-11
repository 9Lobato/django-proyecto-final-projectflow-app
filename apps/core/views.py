# apps\core\views.py sirve para:
# proporcionar datos globales de la aplicación
# necesarios para los componentes React

# Librerías estándar de Python
import json
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import gettext
# Imports internos de proyecto/apps
from apps.projects.models import Assignment
from apps.accounts.models import WorkflowProgress


# devuelve a React los datos necesarios para el navbar
def navbar_api(request):
  if not request.user.is_authenticated:
    return JsonResponse(
      {
        "authenticated": False,
      },
      status=401,
    )

  user = request.user

  is_owner = (
    user.is_superuser
    or Assignment.objects.filter(
      user=user,
      role__name="OWNER",
    ).exists()
  )

  is_manager = (
    user.is_superuser
    or Assignment.objects.filter(
      user=user,
      role__name="MANAGER",
    ).exists()
  )

  return JsonResponse({
    "authenticated": True,
    "username": user.username,
    "is_owner": is_owner,
    "is_manager": is_manager,
    "language": request.LANGUAGE_CODE,
    "languages": [
      {
        "code": code,
        "name": name,
      }
      for code, name in settings.LANGUAGES
    ],
    "translations": {
      "projects": gettext("Proyectos"),
      "tasks": gettext("Tareas"),
      "kanban": gettext("Kanban"),
      "report": gettext("Informe"),
      "manage": gettext("Gestión"),
      "logout": gettext("Salir"),
      "search": gettext("Buscar"),
      "search_placeholder": gettext("Buscar en proyectos..."),
    },
  })


@login_required
def workflow_api(request):
  user = request.user

  if request.method == "GET":
    workflow_progress, _ = WorkflowProgress.objects.get_or_create(
      user=user
    )
    workflow_checks = workflow_progress.checks

  elif request.method == "POST":
    try:
      data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
      return JsonResponse(
        {"success": False, "error": "Datos inválidos."},
        status=400,
      )

    workflow_checks = data.get("checks", {})

    if not isinstance(workflow_checks, dict):
      return JsonResponse(
        {"success": False, "error": "Checks inválidos."},
        status=400,
      )

    workflow_progress, _ = WorkflowProgress.objects.get_or_create(user=user)
    workflow_progress.checks = workflow_checks
    workflow_progress.save(update_fields=["checks"])

  else:
    return JsonResponse(
      {"success": False, "error": "Método no permitido."},
      status=405,
    )

  if user.is_superuser:
    role = "OWNER"
  else:
    assignment = (
      Assignment.objects
      .filter(user=user)
      .select_related("role")
      .order_by("role__name")
      .first()
    )

    if assignment and assignment.role:
      role = assignment.role.name
    else:
      role = "MEMBER"

  workflows = {
    "OWNER": [
      {
        "title": "En Gestión",
        "items": [
          "Cree los usuarios necesarios de la app.",
          "Gestione los roles de cada usuario para cada proyecto.",
        ],
        "url": "/manage/",
      },
      {
        "title": "En Proyectos",
        "items": [
          "Cree proyectos nuevos y defina sus datos.",
          "Elimine proyectos y archive proyectos finalizados.",
          "Cree plantillas de proyectos archivados.",
        ],
        "url": "/projects/",
      },
      {
        "title": "En Tareas",
        "items": [
          "Filtre y visualice las tareas y sus datos para los diferentes proyectos.",
          "Cree y gestione comentarios y solicitudes de tarea.",
        ],
        "url": "/tasks/",
      },
      {
        "title": "En Dashboard",
        "items": [
          "Gestione las plantillas de proyectos utilizadas en la creación de proyectos.",
          "Gestione los usuarios de los equipos de cada proyecto.",
          "Manténgase informado de nuevas notificaciones.",
        ],
        "url": "/",
      },
      {
        "title": "En Kanban",
        "items": [
          "Visualice y guíe el desarrollo de proyectos.",
          "Cambie el estado, prioridades y tiempos de tareas.",
          "Duplique o copie tareas entre proyectos.",
        ],
        "url": "/kanban/",
      },
      {
        "title": "En Informes",
        "items": [
          "Consulte el análisis de datos de proyectos y usuarios.",
          "Exporte informes a PDF y Excel.",
        ],
        "url": "/report/",
      },
    ],
    "MANAGER": [
      {
        "title": "En Proyectos",
        "items": [
          "Visualice los proyectos que le han sido asignados.",
          "Visualice los proyectos de otros managers disponibles para seguir.",
        ],
        "url": "/projects/",
      },
      {
        "title": "En Tareas",
        "items": [
          "Gestione las tareas de proyectos asignados.",
          "Cree comentarios y solicitudes de tareas a resolver.",
          "Mencione a otros usuarios para la resolución de solicitudes.",
        ],
        "url": "/tasks/",
      },
      {
        "title": "En Dashboard",
        "items": [
          "Gestione los usuarios de los equipos de los proyectos asignados.",
          "Manténgase informado de nuevas notificaciones.",
        ],
        "url": "/",
      },
      {
        "title": "En Kanban",
        "items": [
          "Visualice y gestione el desarrollo temporal de proyectos asignados.",
          "Cambie el estado, prioridades y tiempos de tareas.",
          "Duplique o copie tareas de proyectos seguidos a proyectos asignados.",
        ],
        "url": "/kanban/",
      },
      {
        "title": "En Informes",
        "items": [
          "Consulte el análisis de datos de proyectos asignados y usuarios.",
          "Exporte informes a PDF y Excel.",
        ],
        "url": "/report/",
      },
    ],
    "MEMBER": [
      {
        "title": "En Proyectos",
        "items": [
          "Visualice los proyectos que le han sido asignados.",
        ],
        "url": "/projects/",
      },
      {
        "title": "En Tareas",
        "items": [
          "Gestione las tareas de proyectos asignados.",
          "Cree comentarios y solicitudes de tareas a resolver.",
          "Mencione a otros usuarios para la resolución de solicitudes.",
        ],
        "url": "/tasks/",
      },
      {
        "title": "En Dashboard",
        "items": [
          "Gestione los usuarios de los equipos de los proyectos asignados.",
          "Manténgase informado de nuevas notificaciones.",
        ],
        "url": "/",
      },
      {
        "title": "En Kanban",
        "items": [
          "Visualice el desarrollo de proyectos.",
          "Cambie el estado de tareas asignadas.",
        ],
        "url": "/kanban/",
      },
    ],
  }

  return JsonResponse({
    "workflow_role": role,
    "workflow_steps": workflows[role],
    "workflow_checks": workflow_checks,
  })
