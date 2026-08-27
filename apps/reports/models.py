# apps\reports\models.py sirve para:
# definir los modelos de datos utilizados por la aplicación de informes

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.db import models
# Imports internos de proyecto/apps
from apps.projects.models import Project


# MODELO DE INFORMES: almacena el progreso mensual de un proyecto 
class ProjectProgressSnapshot(models.Model):

  project = models.ForeignKey(
    Project,
    on_delete=models.CASCADE,
    related_name="progress_snapshots",
  )

  month = models.DateField()

  completion_percentage = models.PositiveSmallIntegerField(
    default=0
  )

  is_interpolated = models.BooleanField(default=False)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    unique_together = ("project", "month")
