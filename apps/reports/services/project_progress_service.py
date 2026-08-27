# apps\reports\services\project_progress_service.py sirve para:
# calcular, reconstruir y devolver el progreso histórico y actual
# de los proyectos mediante snapshots mensuales

# Librerías estándar de Python
from calendar import monthrange
from datetime import date
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.utils import timezone
# Imports internos de proyecto/apps
from apps.projects.models import Project
from apps.reports.models import ProjectProgressSnapshot


# HELPER PRIVADO: genera los meses del informe desde el mes de creación del primer proyecto
# hasta el mes actual
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


# MÉTRICAS DE PROYECTOS: calcula el progreso de un proyecto para una fecha concreta
def calculate_project_progress(project, reference_date):
    """
    Calcula el progreso de un proyecto para una fecha concreta.

    Reglas:

    - Antes de existir el proyecto -> None.
    - Las tareas eliminadas no participan.
    - Las tareas canceladas no participan.
    - El mes actual utiliza el estado actual.
    - En histórico:
        * Las tareas con completed_at histórico se consideran
          parte del proyecto aunque created_at sea posterior.
        * Las tareas normales utilizan created_at para determinar
          cuándo empezaron a existir.
        * El porcentaje histórico se calcula sobre todas las
          tareas que forman parte del proyecto en ese período.
    """

    project_start = project.created_at.date()

    if reference_date < project_start:
      return None

    tasks = project.tasks.filter(
      deleted_at__isnull=True,
    )

    today = timezone.now().date()

    is_current_period = (
      reference_date.year == today.year
      and reference_date.month == today.month
    )

    # --------------------------------------------------
    # Mes actual
    # --------------------------------------------------

    if is_current_period:

      total_tasks = 0
      completed_tasks = 0

      for task in tasks:

        if task.status == "CANCELLED":
          continue

        task_created = task.created_at.date()

        if task_created > reference_date:
          continue

        total_tasks += 1

        if task.status == "DONE":
          completed_tasks += 1

      if total_tasks == 0:
        return 0

      return round(
        completed_tasks / total_tasks * 100
      )

    # --------------------------------------------------
    # Histórico
    # --------------------------------------------------

    valid_tasks = []

    for task in tasks:

      if task.status == "CANCELLED":
        continue

      created_date = task.created_at.date()

      completed_date = (
        task.completed_at.date()
        if task.completed_at
        else None
      )

      # La tarea existe en esa fecha
      if created_date <= reference_date:
        valid_tasks.append(task)

    if not valid_tasks:
      return 0

    total_tasks = len(valid_tasks)

    completed_tasks = sum(
      1
      for task in valid_tasks
      if (
        task.completed_at
        and task.completed_at.date() <= reference_date
      )
    )

    return round(
      completed_tasks / total_tasks * 100
    )


# MÉTRICAS DE PROYECTOS: devuelve el progreso actual real del proyecto
def get_current_project_progress(project):
  """
  Devuelve el progreso actual real del proyecto.
  """

  today = timezone.now().date()

  return calculate_project_progress(
    project=project,
    reference_date=today,
  )


# SNAPSHOTS: actualiza el snapshot correspondiente al mes actual
def update_current_month_snapshots():

  today = timezone.now().date()
  current_month = today.replace(day=1)

  projects = (
    Project.objects
    .filter(
      is_archived=False,
    )
    .prefetch_related("tasks")
  )

  for project in projects:

    completion_percentage = calculate_project_progress(
      project=project,
      reference_date=today,
    )

    if completion_percentage is None:
      continue

    ProjectProgressSnapshot.objects.update_or_create(
      project=project,
      month=current_month,
      defaults={
        "completion_percentage": completion_percentage,
        "is_interpolated": False,
      },
    )


# SNAPSHOTS: reconstruye los snapshots históricos de un proyecto
def rebuild_project_snapshots(project):
  """
  Reconstruye todos los snapshots históricos de un proyecto.

  - Empieza en el mes de creación del proyecto.
  - Para proyectos activos llega hasta el mes actual.
  - Para proyectos archivados llega hasta el mes de archivo.
  - El mes de archivo se calcula exactamente en archived_at.
  - Los meses posteriores al archivo no se crean.
  """

  project_start = project.created_at.date()

  start_month = project_start.replace(
    day=1,
  )

  archive_date = None
  end_month = None

  if project.archived_at:

    archive_date = project.archived_at.date()

    end_month = archive_date.replace(
      day=1,
    )

  else:

    today = timezone.now().date()

    end_month = today.replace(
      day=1,
    )

  existing_snapshots = {
    snapshot.month: snapshot
    for snapshot in ProjectProgressSnapshot.objects.filter(
      project=project,
    )
  }

  year = start_month.year
  month = start_month.month

  while (
    year < end_month.year
    or (
      year == end_month.year
      and month <= end_month.month
    )
  ):

    snapshot_month = date(
      year,
      month,
      1,
    )

    # --------------------------------------------------
    # Mes de archivo
    # --------------------------------------------------

    if (
      archive_date is not None
      and snapshot_month == end_month
    ):

      reference_date = archive_date

    # --------------------------------------------------
    # Mes actual de un proyecto activo
    # --------------------------------------------------

    elif (
      archive_date is None
      and snapshot_month == end_month
    ):

      reference_date = timezone.now().date()

    # --------------------------------------------------
    # Mes histórico normal
    # --------------------------------------------------

    else:

      last_day = monthrange(
        year,
        month,
      )[1]

      reference_date = date(
        year,
        month,
        last_day,
      )

    calculated_percentage = (
      calculate_project_progress(
        project=project,
        reference_date=reference_date,
      )
    )

    completion_percentage = (
      calculated_percentage
      if calculated_percentage is not None
      else 0
    )

    snapshot = existing_snapshots.get(
      snapshot_month,
    )

    if snapshot is None:

      ProjectProgressSnapshot.objects.create(
        project=project,
        month=snapshot_month,
        completion_percentage=completion_percentage,
        is_interpolated=False,
      )

    else:

      snapshot.completion_percentage = (
        completion_percentage
      )

      snapshot.is_interpolated = False

      snapshot.save(
        update_fields=[
          "completion_percentage",
          "is_interpolated",
        ]
      )

    month += 1

    if month > 12:
      month = 1
      year += 1


# DATOS DEL DASHBOARD: obtiene los snapshots necesarios para el gráfico de progreso
def get_progress_snapshots():

  months = _get_report_months()

  snapshots = list(
    ProjectProgressSnapshot.objects
    .select_related("project")
    .filter(
      month__in=months,
    )
    .order_by(
      "project__code",
      "month",
    )
  )

  snapshot_dict = {
    (
      snapshot.project.code,
      snapshot.month,
    ): snapshot.completion_percentage
    for snapshot in snapshots
  }

  project_codes = sorted({
    snapshot.project.code
    for snapshot in snapshots
  })

  datasets = []

  for project_code in project_codes:

    data = []

    finished = False

    for month in months:

      if finished:

        data.append(None)
        continue

      percentage = snapshot_dict.get(
        (project_code, month),
        None,
      )

      data.append(percentage)

      # Cuando el proyecto llega al 100%,
      # dejamos de mostrar la línea en los meses posteriores.
      if percentage == 100:

        finished = True

    datasets.append(
      {
        "label": project_code,
        "data": data,
      }
    )

  return {
    "progress_labels": [
      month.strftime("%b %Y")
      for month in months
    ],
    "progress_datasets": datasets,
  }
