# apps\home\context_processors.py sirve para:
# proporcionar a las plantillas información sobre el flujo de trabajo
# disponible para el usuario según su rol

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.urls import reverse
# Imports internos de proyecto/apps
from apps.projects.models import Assignment


# prepara el flujo de trabajo que se muestra al usuario según su rol
def workflow_context(request):
  if not request.user.is_authenticated:
    return {}
  if request.user.is_superuser:
    role = "OWNER"
  else:
    assignment = (
      Assignment.objects
      .filter(user=request.user)
      .select_related("role")
      .order_by("role__name")
      .first()
    )
    role = (
      assignment.role.name
      if assignment and assignment.role
      else "MEMBER"
    )
  workflows = {
    "OWNER": [
      {
        "title": "En Gestión",
        "items": [
          "Cree los usuarios necesarios de la app.",
          "Gestione los roles de cada usuario para cada proyecto.",
        ],
        "url": "manage",
      },
      {
        "title": "En Proyectos",
        "items": [
          "Cree proyectos nuevos y defina sus datos.",
          "Elimine proyectos y archive proyectos finalizados.",
          "Cree plantillas de proyectos archivados.",
        ],
        "url": "project_list",
      },
      {
        "title": "En Tareas",
        "items": [
          "Filtre y visualice las tareas y sus datos para los diferentes proyectos.",
          "Cree y gestione comentarios y solicitudes de tarea.",
        ],
        "url": "task_list",
      },
      {
        "title": "En Dashboard",
        "items": [
          "Gestione las plantillas de proyectos utilizadas en la creación de proyectos.",
          "Gestione los usuarios de los equipos de cada proyecto.",
          "Manténgase informado de nuevas notificaciones.",
        ],
        "url": "home",
      },
      {
        "title": "En Kanban",
        "items": [
          "Visualice y guíe el desarrollo de proyectos.",
          "Cambie el estado, prioridades y tiempos de tareas.",
          "Duplique o copie tareas entre proyectos.",
        ],
        "url": "kanban",
      },
      {
        "title": "En Informes",
        "items": [
          "Consulte el análisis de datos de proyectos y usuarios.",
          "Exporte informes a PDF y Excel.",
        ],
        "url": "report",
      },
    ],
    "MANAGER": [
      {
        "title": "En Proyectos",
        "items": [
          "Visualice los proyectos que le han sido asignados.",
          "Visualice los proyectos de otros managers disponibles para seguir.",
        ],
        "url": "project_list",
      },
      {
        "title": "En Tareas",
        "items": [
          "Gestione las tareas de proyectos asignados.",
          "Cree comentarios y solicitudes de tareas a resolver.",
          "Mencione a otros usuarios para la resolución de solicitudes.",
        ],
        "url": "task_list",
      },
      {
        "title": "En Dashboard",
        "items": [
          "Gestione los usuarios de los equipos de los proyectos asignados.",
          "Manténgase informado de nuevas notificaciones.",
        ],
        "url": "home",
      },
      {
        "title": "En Kanban",
        "items": [
          "Visualice y gestione el desarrollo temporal de proyectos asignados.",
          "Cambie el estado, prioridades y tiempos de tareas.",
          "Duplique o copie tareas de proyectos seguidos a proyectos asignados.",
        ],
        "url": "kanban",
      },
      {
        "title": "En Informes",
        "items": [
          "Consulte el análisis de datos de proyectos asignados y usuarios.",
          "Exporte informes a PDF y Excel.",
        ],
        "url": "report",
      },
    ],
    "MEMBER": [
      {
        "title": "En Proyectos",
        "items": [
          "Visualice los proyectos que le han sido asignados.",
        ],
        "url": "project_list",
      },
      {
        "title": "En Tareas",
        "items": [
          "Gestione las tareas de proyectos asignados.",
          "Cree comentarios y solicitudes de tareas a resolver.",
          "Mencione a otros usuarios para la resolución de solicitudes.",
        ],
        "url": "task_list",
      },
      {
        "title": "En Dashboard",
        "items": [
          "Gestione los usuarios de los equipos de los proyectos asignados.",
          "Manténgase informado de nuevas notificaciones.",
        ],
        "url": "home",
      },
      {
        "title": "En Kanban",
        "items": [
          "Visualice el desarrollo de proyectos.",
          "Cambie el estado de tareas asignadas.",
        ],
        "url": "kanban",
      },
    ],
  }
  workflow_steps = workflows[role]
  for step in workflow_steps:
    step["href"] = reverse(step["url"])
  return {
    "workflow_role": role,
    "workflow_steps": workflow_steps,
  }
