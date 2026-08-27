# apps\tasks\services\inbox.py sirve para:
# consultar los comentarios y la actividad relacionados con las tareas de los proyectos

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
# Imports internos de proyecto/apps
from apps.tasks.models import TaskComment


# SERVICIO: obtiene los comentarios de la bandeja de entrada del usuario
def get_user_inbox(user, projects):
  return (
    TaskComment.objects
    .filter(
      task__project__is_archived=False,
      task__project__in=projects
    )
    .select_related("task", "task__project", "user")
    .distinct()
    .order_by("-created_at")
  )


# SERVICIO: obtiene la actividad relacionada con las tareas y sus proyectos
def get_user_activity(user):
  return (
    TaskComment.objects
    .select_related("task", "task__project", "user")
  )
