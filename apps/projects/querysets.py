# apps\projects\querysets.py sirve para:
# centralizar consultas reutilizables relacionadas con proyectos
# y preparar los datos necesarios para mostrar los proyectos
# con sus tareas, asignaciones y estadísticas

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.db.models import Count, IntegerField, Q
from django.db.models.functions import Cast, Substr
# Imports internos de proyecto/apps
from .models import Project


# obtiene un queryset de proyectos con sus relaciones y estadísticas
def get_projects_queryset(search=None):
  queryset = (
    Project.objects
    .select_related("owner", "template")
    .prefetch_related("assignments", "tasks")
    .annotate(
      total_tasks=Count("tasks"),
      completed_tasks=Count("tasks", filter=Q(tasks__status="DONE")),
      project_year=Cast(Substr("code", 1, 2), IntegerField()),
      project_number=Cast(Substr("code", 4, 3), IntegerField()),
    )
  )

  if search:
    queryset = queryset.filter(
      Q(name__icontains=search) |
      Q(description__icontains=search)
    )

  return queryset.order_by("-project_year", "-project_number")
