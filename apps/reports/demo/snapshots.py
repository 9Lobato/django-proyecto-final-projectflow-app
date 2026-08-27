# apps\reports\demo\snapshots.py sirve para:
# generar los snapshots mensuales de progreso de los proyectos de demostración

# Librerías estándar de Python
from calendar import monthrange
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.db import transaction
from django.utils import timezone
# Imports internos de proyecto/apps
from apps.reports.models import ProjectProgressSnapshot
from apps.projects.models import Project
from apps.reports.demo.projects import PROJECTS
from apps.reports.services.project_progress_service import calculate_project_progress


# HELPER PRIVADO: recorre los meses entre una fecha inicial y una fecha final
def _iter_months(start_month, end_month):

  month = start_month

  while month <= end_month:

    yield month

    if month.month == 12:

      month = month.replace(
        year=month.year + 1,
        month=1,
      )

    else:

      month = month.replace(
        month=month.month + 1,
      )


# HELPER PRIVADO: devuelve el primer día del mes de una fecha
def _month_start(value):

  return value.replace(
    day=1,
  )


# HELPER PRIVADO: devuelve el último día del mes indicado
def _month_end(month):

  last_day = monthrange(
    month.year,
    month.month,
  )[1]

  return month.replace(
    day=last_day,
  )


# HELPER PRIVADO: determina hasta qué mes se deben generar snapshots para un proyecto
def _project_snapshot_end(project):

  today = timezone.now().date()

  current_month = _month_start(today)

  if project.archived_at:

    archived_month = _month_start(
      project.archived_at.date()
    )

    return min(
      archived_month,
      current_month,
    )

  return current_month


# genera los snapshots mensuales de progreso para todos los proyectos de demostración
@transaction.atomic
def create_snapshots():

  ProjectProgressSnapshot.objects.all().delete()

  projects = {
    project.code: project
    for project in Project.objects.all()
  }

  today = timezone.now().date()

  for project_data in PROJECTS:

    project = projects.get(
      project_data["code"]
    )

    if not project:
      raise Exception(
        f'No existe el proyecto {project_data["code"]}'
      )

    project_start = _month_start(
      project.created_at.date()
    )

    project_end = _project_snapshot_end(
      project
    )

    if project_start > project_end:
      continue

    for month in _iter_months(
      project_start,
      project_end,
    ):

      archive_month = (
        _month_start(
          project.archived_at.date()
        )
        if project.archived_at
        else None
      )

      if (
        archive_month is not None
        and month == archive_month
      ):
        reference_date = project.archived_at.date()

      else:
        reference_date = _month_end(month)

      reference_date = min(
        reference_date,
        today,
      )

      progress = calculate_project_progress(
        project=project,
        reference_date=reference_date,
      )

      if progress is None:
        continue

      ProjectProgressSnapshot.objects.create(
        project=project,
        month=month,
        completion_percentage=progress,
        is_interpolated=False,
      )
