# apps\reports\admin.py sirve para:
# configurar la administración de los modelos de informes desde el panel de Django

# Librerías estándar de Python
from django.contrib import admin
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
# Imports internos de proyecto/apps
from .models import ProjectProgressSnapshot


# CONFIGURACIÓN ADMINISTRATIVA: registra y configura los snapshots de progreso
@admin.register(ProjectProgressSnapshot)
class ProjectProgressSnapshotAdmin(admin.ModelAdmin):

  list_display = (
    "project",
    "month",
    "completion_percentage",
    "is_interpolated",
  )
