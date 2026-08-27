# apps\reports\demo\tasks.py sirve para:
# generar las tareas de demostración de los proyectos, asignándolas a usuarios,
# calculando sus fechas y estableciendo su estado y progreso

# Librerías estándar de Python
import random
from datetime import timedelta, datetime
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.db import transaction
from django.utils import timezone
# Imports internos de proyecto/apps
from apps.tasks.models import Task
from apps.projects.models import Project
from apps.reports.demo.projects import PROJECTS
from apps.reports.demo.catalogs.tasks_catalog import TASK_CATALOG
from apps.reports.demo.catalogs.project_roles import OWNER, MANAGER, MEMBER
from apps.reports.demo.catalogs.task_status import TODO, IN_PROGRESS, DONE, CANCELLED
from apps.reports.demo.catalogs.demo_settings import WORKDAY_MINUTES


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


# HELPER PRIVADO: calcula las fechas de creación, inicio, vencimiento, finalización, cancelación y eliminación de una tarea
def _build_task_dates(project, task_data, status, completion_date=None):

  now = timezone.now()

  created_after_days = task_data.get(
    "created_after_days",
    0,
  )

  start_after_days = task_data.get(
    "start_after_days",
    created_after_days,
  )

  completed_after_days = task_data.get(
    "completed_after_days",
  )

  if completion_date is not None:
    completed_after_days = None

  # --------------------------------------------------------
  # Si una tarea DONE no tiene una fecha histórica explícita,
  # generamos una fecha progresiva según su orden dentro
  # del proyecto.
  #
  # Esto permite que el gráfico de progreso muestre una
  # evolución real en lugar de una línea horizontal.
  # --------------------------------------------------------

  delete_after_days = task_data.get(
    "delete_after_days",
  )

  cancel_after_days = task_data.get(
    "cancel_after_days",
  )

  created_at = (
    project.created_at
    + timedelta(days=created_after_days)
  )

  started_at = (
    project.created_at
    + timedelta(days=start_after_days)
  )

  estimate = task_data.get(
    "estimate",
    1,
  )

  due_at = (
    started_at
    + timedelta(days=estimate)
  )

  completed_at = None
  cancelled_at = None
  deleted_at = None

  if completion_date is not None:

    completed_at = completion_date

  elif completed_after_days is not None:

    completed_at = (
      project.created_at
      + timedelta(days=completed_after_days)
    )

  if cancel_after_days is not None:

    cancelled_at = (
      project.created_at
      + timedelta(days=cancel_after_days)
    )

  if delete_after_days is not None:

    deleted_at = (
      project.created_at
      + timedelta(days=delete_after_days)
    )

  # --------------------------------------------------------
  # Las tareas no pueden existir antes de la creación
  # del proyecto.
  # --------------------------------------------------------

  created_at = min(
    created_at,
    now,
  )

  started_at = max(
    started_at,
    created_at,
  )

  # --------------------------------------------------------
  # Las fechas de finalización/cancelación/eliminación
  # no pueden quedar en el futuro.
  # --------------------------------------------------------

  if completed_at is not None:

    # Nunca completar una tarea después del archivo
    # del proyecto.
    if project.archived_at:

      completed_at = min(completed_at, project.archived_at)

    else:

      completed_at = min(completed_at, now)

    completed_at = max(completed_at, started_at)

  if cancelled_at is not None:

    cancelled_at = min(cancelled_at, now)
    cancelled_at = max(cancelled_at, started_at)

  if deleted_at is not None:

    deleted_at = min(deleted_at, now)
    deleted_at = max(deleted_at, created_at)

  # --------------------------------------------------------
  # Solo los estados correspondientes tienen fechas
  # de ejecución/finalización.
  # --------------------------------------------------------

  if status == TODO:

    started_at = None
    completed_at = None
    cancelled_at = None

  elif status == IN_PROGRESS:

    completed_at = None
    cancelled_at = None

  elif status == DONE:

    cancelled_at = None

    if completed_at is None:

      completed_at = min(
        started_at,
        now,
      )

  elif status == CANCELLED:

    completed_at = None

    if cancelled_at is None:

      cancelled_at = min(
        started_at,
        now,
      )

  return {
    "created_at": created_at,
    "started_at": started_at,
    "due_at": due_at,
    "completed_at": completed_at,
    "deleted_at": deleted_at,
    "cancelled_at": cancelled_at,
  }


# HELPER PRIVADO: devuelve el propietario del proyecto
def _project_owner(project):

  return project.owner


# HELPER PRIVADO: calcula una fecha progresiva de finalización para las tareas completadas del proyecto
def _get_completion_date(project, project_data, task_data, done_index, total_done):

  last_date_string = project_data.get(
    "last_date"
  )

  if not last_date_string:
    return None

  last_date = datetime.strptime(
    last_date_string,
    "%Y-%m-%d",
  ).date()

  start_date = project.created_at.date()

  total_days = (
    last_date - start_date
  ).days

  if total_done <= 1:

    completion_date = last_date

  else:

    progress = (
      done_index / (total_done - 1)
    )

    completion_date = (
      start_date
      + timedelta(
        days=round(
          total_days * progress
        )
      )
    )

  return timezone.make_aware(
    datetime.combine(
      completion_date,
      datetime.min.time(),
    )
  )


# HELPER PRIVADO: crea una tarea de demostración con su usuario asignado, estado, fechas y datos de progreso
def _create_task(project, project_data, task_data, members, is_done, done_count, done_index=None):

  role_members = members[task_data["role"]]

  if not role_members:
    raise Exception(
      f'El proyecto {project.code} no tiene usuarios '
      f'con rol {task_data["role"]}'
    )

  assigned_to = random.choice(role_members)

  status = _resolve_status(task_data, is_done)

  completion_date = None

  if (status == DONE and done_index is not None):

    completion_date = _get_completion_date(
      project=project,
      project_data=project_data,
      task_data=task_data,
      done_index=done_index,
      total_done=done_count,
    )

  dates = _build_task_dates(
    project=project,
    task_data=task_data,
    status=status,
    completion_date=completion_date,
  )

  started_at = None

  if status != TODO:

    started_at = dates["started_at"]

  due_at = (
    dates["due_at"]
    if task_data.get("planned", True)
    else None
  )

  task = Task.objects.create(
    project=project,
    title=task_data["title"],
    description=task_data["description"],
    priority=task_data["priority"],
    created_by=_project_owner(project),
    assigned_to=assigned_to,
    time_estimated=task_data["estimate"],
    created_at=dates["created_at"],
    started_at=started_at,
    due_at=due_at,
    status=status,
  )

  if status == DONE:

    task.completed_at = dates["completed_at"]

    if task.completed_at is None:

      task.completed_at = dates["started_at"]

    task.frozen_at = task.completed_at

    task.elapsed_minutes = (task.time_estimated * WORKDAY_MINUTES)

  elif status == CANCELLED:

    task.cancelled_at = (
      dates["cancelled_at"]
      or dates["started_at"]
    )

    task.frozen_at = task.cancelled_at

  elif status == IN_PROGRESS:

    task.active_started_at = (dates["started_at"])

  task.deleted_at = dates["deleted_at"]

  task.save()


# HELPER PRIVADO: calcula cuántas tareas deben quedar completadas según el porcentaje de progreso del proyecto
def _get_done_count(project, project_data, total_tasks):

  target_percentage = project_data.get(
    "last_percentage",
    0,
  )

  target_done_count = round(
    total_tasks * target_percentage / 100
  )

  return min(
    target_done_count,
    total_tasks,
  )


# HELPER PRIVADO: determina el estado de una tarea a partir de su configuración y de si debe estar completada
def _resolve_status(task_data, is_done):

  if is_done:

    return DONE

  if task_data.get("cancel_after_days") is not None:

    return CANCELLED

  return random.choice(
    [TODO, IN_PROGRESS]
  )


# HELPER PRIVADO: selecciona las primeras tareas del catálogo respetando su orden y limitando su cantidad
def _select_tasks(catalog):

  number_of_tasks = min(
    10,
    len(catalog),
  )

  return sorted(
    catalog,
    key=lambda task: task["order"],
  )[:number_of_tasks]


# genera las tareas de demostración para todos los proyectos definidos en el catálogo
@transaction.atomic
def create_tasks():

  Task.objects.all().delete()

  projects = {
    project.code: project
    for project in Project.objects.all()
  }

  ordered_project_data = sorted(
    PROJECTS,
    key=lambda project_data: project_data["created"],
    reverse=True,
  )

  for project_data in ordered_project_data:

    project = projects.get(
      project_data["code"]
    )

    if not project:
      raise Exception(
        f'No existe el proyecto {project_data["code"]}'
      )

    catalog = TASK_CATALOG[
      project_data["type"]
    ]

    members = _project_members(
      project
    )

    selected_tasks = _select_tasks(
      catalog
    )

    done_count = _get_done_count(
      project=project,
      project_data=project_data,
      total_tasks=len(selected_tasks),
    )

    done_index = 0

    for index, task_data in enumerate(selected_tasks):

      is_done = index < done_count

      if is_done:

        current_done_index = done_index
        done_index += 1

      else:

        current_done_index = None

      _create_task(
        project=project,
        project_data=project_data,
        task_data=task_data,
        members=members,
        is_done=is_done,
        done_count=done_count,
        done_index=current_done_index,
      )
