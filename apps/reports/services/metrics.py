# apps\reports\services\metrics.py sirve para:
# calcular y devolver las métricas de proyectos, tareas y usuarios
# utilizadas por el dashboard y los informes

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.utils import timezone
# Imports internos de proyecto/apps


# HELPER PRIVADO: calcula la media de una colección de valores ignorando los valores nulos
def _average(values):

  values = [
    value
    for value in values
    if value is not None
  ]

  if not values:
    return None

  return round(
    sum(values) / len(values),
    1,
  )


# HELPER PRIVADO: devuelve únicamente los días de retraso positivos
def _positive_delay(task):

  delay = task_delay_days(task)

  if delay is None:
    return None

  return max(delay, 0)


# MÉTRICAS DE PROYECTOS: progreso
def project_completion(tasks):

  valid_tasks = [
    task
    for task in tasks
    if task.status != "CANCELLED"
  ]

  total = len(valid_tasks)

  if total == 0:
    return 0

  completed = sum(
    1
    for task in valid_tasks
    if task.status == "DONE"
  )

  return round(completed / total * 100)


# MÉTRICAS DE PROYECTOS: porcentaje de entregas en plazo
def project_delivery(tasks):

  completed = [
    task
    for task in tasks
    if task.status == "DONE"
  ]

  total = len(completed)

  if total == 0:
    return 0

  on_time = sum(
    1
    for task in completed
    if (
      task.completed_at
      and task.due_at
      and task.completed_at <= task.due_at
    )
  )

  return round(on_time / total * 100)


# MÉTRICAS DE PROYECTOS: media de tiempo de resolución
def project_average_resolution(tasks):

  return _average(
    task_resolution_days(task)
    for task in tasks
    if task.started_at
    and task.completed_at
  )


# MÉTRICAS DE PROYECTOS: media de tiempo de retardo
def project_average_delay(tasks):

  return _average(
    _positive_delay(task)
    for task in tasks
    if task.due_at
    and task.completed_at
  )


# MÉTRICAS DE PROYECTOS: salud general
def project_health(tasks):

  completion = project_completion(tasks)

  delivery = project_delivery(tasks)

  delay = project_average_delay(tasks)

  if delay is None:
    delay = 0

  delay = min(delay, 10)

  score = (completion * 0.5 + delivery * 0.3 + (10 - delay) * 2)

  return round(score)


# MÉTRICAS DE PROYECTOS: porcentaje de tareas asignadas
def project_assignment(tasks):

  total = len(tasks)

  if total == 0:
    return 0

  assigned = sum(
    1
    for task in tasks
    if task.assigned_to
  )

  return round(
    assigned / total * 100
  )


# MÉTRICAS DE PROYECTOS: planificación vs realidad
def project_planning_accuracy(tasks):

  values = [
    task.planning_offset_abs
    for task in tasks
    if task.due_at
    and task.time_estimated
  ]

  return _average(values)


# MÉTRICAS DE PROYECTOS: usuarios asignados al proyecto
def project_users(tasks):

  users = {}

  for task in tasks:
    if task.assigned_to:
      users[task.assigned_to.id] = task.assigned_to.username

  return {
    "count": len(users),
    "names": sorted(users.values()),
  }


# MÉTRICAS DE PROYECTOS: tareas activas
def project_active(tasks):

  return sum(
    1
    for task in tasks
    if task.status in (
      "TODO",
      "IN_PROGRESS",
    )
  )


# MÉTRICAS DE PROYECTOS: tareas completadas
def project_completed(tasks):

  return sum(
    1
    for task in tasks
    if task.status == "DONE"
  )


# MÉTRICAS DE PROYECTOS: tareas vencidas
def project_overdue(tasks):

  return sum(
    1
    for task in tasks
    if (
      task.status in (
        "TODO",
        "IN_PROGRESS",
      )
      and task.due_at
      and task.due_at < timezone.now()
    )
  )


# MÉTRICAS DE PROYECTOS: tareas canceladas
def project_cancelled(tasks):

  return sum(
    1
    for task in tasks
    if task.status == "CANCELLED"
  )


# MÉTRICAS DE PROYECTOS: resumen de métricas del proyecto
def project_metrics(project):

  tasks = list(project.tasks.filter(deleted_at__isnull=True))
  total = len(tasks)
  completion = project_completion(tasks)
  delivery = project_delivery(tasks)
  average_resolution = project_average_resolution(tasks)
  average_delay = project_average_delay(tasks)
  health = project_health(tasks)
  assignment = project_assignment(tasks)
  accuracy = project_planning_accuracy(tasks)
  users = project_users(tasks)
  pending = project_active(tasks)
  completed = project_completed(tasks)
  overdue = project_overdue(tasks)
  cancelled = project_cancelled(tasks)

  return {
    "total": total,
    "completion": completion,
    "delivery": delivery,
    "average_resolution": average_resolution,
    "average_delay": average_delay,
    "health": health,
    "assignment": assignment,
    "accuracy": accuracy,
    "users": users,
    "pending": pending,
    "completed": completed,
    "overdue": overdue,
    "cancelled": cancelled,
  }


# MÉTRICAS DE PROYECTOS: resumen completo del proyecto
def project_summary(project):

  data = project_metrics(project)

  return {
    "id": project.id,
    "code": project.code,
    "name": project.name,
    "is_archived": project.is_archived,
    "total_tasks": data["total"],
    "completed_tasks": data["completed"],
    "delivery": data["delivery"],
    "average_resolution": data["average_resolution"],
    "average_delay": data["average_delay"],
    "health": data["health"],
    "assignment_percentage": data["assignment"],
    "planning_accuracy": data["accuracy"],
    "users": data["users"]["count"],
    "user_names": "<br>".join(data["users"]["names"]),
    "pending_tasks": data["pending"],
    "completion_percentage": data["completion"],
    "overdue": data["overdue"],
    "cancelled": data["cancelled"],
  }


# MÉTRICAS DE TAREAS: días que se tarda en finalizar una tarea
def task_resolution_days(task):

  if not task.started_at:
    return None

  if not task.completed_at:
    return None

  delta = (
    task.completed_at -
    task.started_at
  )

  return delta.total_seconds() / 86400


# MÉTRICAS DE TAREAS: días de retraso de una tarea
def task_delay_days(task):

  if not task.due_at:
    return None

  if not task.completed_at:
    return None

  delta = (
    task.completed_at -
    task.due_at
  )

  return round(
    delta.total_seconds() / 86400,
    1,
  )


# MÉTRICAS DE TAREAS: resumen de métricas de una tarea
def task_metrics(task):

  resolution = task_resolution_days(task)
  delay = task_delay_days(task)

  return {
    "resolution": resolution,
    "delay": delay,
  }


# MÉTRICAS DE TAREAS: resumen completo de una tarea
def task_summary(task):

  data = task_metrics(task)

  return {
    "id": task.id,
    "title": task.title,
    "resolution_days": data["resolution"],
    "delay_days": data["delay"],
  }


# MÉTRICAS DE USUARIOS: tiempo medio de resolución
def user_average_resolution(tasks):

  return _average(
    task_resolution_days(task)
    for task in tasks
    if (
      task.status == "DONE"
      and task.started_at
      and task.completed_at
    )
  )


# MÉTRICAS DE USUARIOS: retraso medio
def user_average_delay(tasks):

  return _average(
    _positive_delay(task)
    for task in tasks
    if (
      task.status == "DONE"
      and task.due_at
    )
  )


# MÉTRICAS DE USUARIOS: tareas en plazo
def user_on_time(tasks):

  return sum(
    1
    for task in tasks
    if (
      task.status in ("DONE", "CANCELLED")
      or task.due_at is None
      or (
        task.status in ("TODO", "IN_PROGRESS")
        and task.due_at >= timezone.now()
      )
    )
  )


# MÉTRICAS DE USUARIOS: entrega del usuario
def user_delivery(tasks):

  completed = [
    task
    for task in tasks
    if task.status == "DONE"
  ]

  total = len(completed)

  if total == 0:
    return 0

  on_time = sum(
    1
    for task in completed
    if (
      task.completed_at
      and task.due_at
      and task.completed_at <= task.due_at
    )
  )

  return round(on_time / total * 100)


# MÉTRICAS DE USUARIOS: salud del usuario
def user_health(tasks, productivity):

  delivery = user_delivery(tasks)

  delay = user_average_delay(tasks)

  if delay is None:
    delay = 0

  delay = min(delay, 10)

  score = (
    productivity * 0.6 + delivery * 0.2 + (10 - delay) * 2
  )

  return round(score)


# MÉTRICAS DE USUARIOS: resumen de métricas del usuario
def user_metrics(user):

  tasks = list(
    user.assigned_tasks.filter(
      project__is_archived=False,
      deleted_at__isnull=True,
    )
  )

  active = sum(
    1
    for task in tasks
    if (
      task.status in ("TODO", "IN_PROGRESS")
      and (
        task.due_at is None
        or task.due_at >= timezone.now()
      )
    )
  )

  completed = sum(
    1
    for task in tasks
    if task.status == "DONE"
  )

  overdue = sum(
    1
    for task in tasks
    if (
      task.status in (
        "TODO",
        "IN_PROGRESS",
      )
      and task.due_at
      and task.due_at < timezone.now()
    )
  )

  cancelled = sum(
    1
    for task in tasks
    if task.status == "CANCELLED"
  )

  archived = sum(
    1
    for task in user.assigned_tasks.all()
    if (
      task.project.is_archived
      and task.deleted_at is None
    )
  )

  on_time = user_on_time(tasks)

  if active + completed:
    productivity = round(
      completed / (active + completed) * 100
    )
  else:
    productivity = 0

  delivery = user_delivery(tasks)

  average_resolution = user_average_resolution(tasks)

  average_delay = user_average_delay(tasks)

  health = user_health(
    tasks,
    productivity,
  )

  return {
    "active": active,
    "completed": completed,
    "cancelled": cancelled,
    "archived": archived,
    "overdue": overdue,
    "on_time": on_time,
    "productivity": productivity,
    "delivery": delivery,
    "average_resolution": average_resolution,
    "average_delay": average_delay,
    "health": health,
  }


# MÉTRICAS DE USUARIOS: resumen completo del usuario
def user_summary(user):

  data = user_metrics(user)

  assignment = (
    user.project_assignments
    .select_related("role")
    .first()
  )

  role = assignment.role.get_name_display() if assignment else "-"
  role_code = assignment.role.name if assignment else "MEMBER"

  project_count = user.project_assignments.filter(
    project__is_archived=False
  ).count()

  task_count = (
    data["active"] +
    data["completed"] +
    data["cancelled"]
  )

  return {
    "id": user.id,
    "username": user.username,
    "active_tasks": data["active"],
    "completed_tasks": data["completed"],
    "cancelled_tasks": data["cancelled"],
    "archived_tasks": data["archived"],
    "overdue_tasks": data["overdue"],
    "on_time_tasks": data["on_time"],
    "productivity": data["productivity"],
    "delivery": data["delivery"],
    "average_resolution": data["average_resolution"],
    "average_delay": data["average_delay"],
    "project_count": project_count,
    "task_count": task_count,
    "role": role,
    "role_code": role_code,
  }
