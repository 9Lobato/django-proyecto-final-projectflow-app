# apps\reports\demo\comments.py sirve para:
# generar los comentarios y solicitudes de demostración asociados a las tareas de los proyectos,
# utilizando los usuarios, roles y catálogos definidos para la demo

# Librerías estándar de Python
import random
from datetime import timedelta
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.db import transaction
# Imports internos de proyecto/apps
from apps.tasks.models import TaskComment
from apps.projects.models import Project
from apps.reports.demo.projects import PROJECTS
from apps.reports.demo.catalogs.comments_catalog import COMMENTS_CATALOG
from apps.reports.demo.catalogs.project_roles import OWNER, MANAGER, MEMBER


# HELPER PRIVADO: obtiene los usuarios del proyecto agrupados por rol
def _project_members(project):

  members = {
    OWNER: [],
    MANAGER: [],
    MEMBER: [],
  }

  assignments = (
    project.assignments
    .select_related(
      "user",
      "role",
    )
  )

  for assignment in assignments:

    members[
      assignment.role.name
    ].append(
      assignment.user
    )

  return members


# HELPER PRIVADO: busca una tarea del proyecto a partir de los datos del catálogo y devuelve None si no existe
def _find_task(project, comment_data):

  filters = {"title": comment_data["task"]}

  if "task_sequence" in comment_data:
    filters["sequence_number"] = comment_data["task_sequence"]

  try:
    return project.tasks.get(**filters)

  except project.tasks.model.DoesNotExist:
    return None

  except project.tasks.model.MultipleObjectsReturned:
    raise Exception(
      f'Existe más de una tarea '{comment_data["task"]}' '
      f'en el proyecto {project.code}. '
      f'Añade task_sequence al catálogo.'
    )


# HELPER PRIVADO: selecciona aleatoriamente un autor entre los usuarios que tienen el rol indicado en el catálogo
def _resolve_author(members, comment_data):

  role_members = members[comment_data["author_role"]]

  if not role_members:
    raise Exception(f'No existen usuarios con rol {comment_data["author_role"]}')

  return random.choice(role_members)


# HELPER PRIVADO: construye el texto del comentario y añade una mención a un usuario del rol indicado cuando corresponde
def _build_comment_text(members, comment_data):

  text = comment_data["text"]

  mentions_role = comment_data.get("mentions_role")

  if not mentions_role:
    return text

  mentioned_members = members[mentions_role]

  if not mentioned_members:
    raise Exception(f'No existen usuarios con rol {mentions_role}')

  mentioned_user = random.choice(mentioned_members)

  return (
    f'{text} @{mentioned_user.username}'
  )


# HELPER PRIVADO: calcula la fecha de creación del comentario a partir de la fecha
# de creación del proyecto y del día indicado en el catálogo
def _build_comment_date(project, comment_data):

  day = comment_data.get("day", 0)

  return (project.created_at + timedelta(days=day))


# HELPER PRIVADO: crea y guarda un comentario o solicitud de demostración a partir
# de los datos definidos en el catálogo
def _create_comment(project, comment_data, members):

  task = _find_task(project, comment_data)

  if not task:
    return

  author = _resolve_author(members, comment_data)

  text = _build_comment_text(members, comment_data)

  comment = TaskComment(
    task=task,
    user=author,
    text=text,
    type=comment_data["type"],
    request_kind=comment_data.get("request_kind", ""),
    resolved=comment_data.get("resolved", False),
  )

  comment.created_at = _build_comment_date(project, comment_data)

  if comment.resolved:

    days = comment_data.get("resolved_days_after", 0)
    comment.resolved_at = (comment.created_at + timedelta(days=days))

  comment.save()


# genera los comentarios y solicitudes de demostración para todos
# los proyectos definidos en el catálogo
@transaction.atomic
def create_comments():

  TaskComment.objects.all().delete()

  projects = {
    project.code: project
    for project in Project.objects.all()
  }

  for project_data in PROJECTS:

    project = projects.get(project_data["code"])

    if not project:
      raise Exception(f'No existe el proyecto {project_data["code"]}')

    catalog = COMMENTS_CATALOG[project_data["type"]]
    members = _project_members(project)

    for comment_data in catalog:

      _create_comment(project, comment_data, members)
