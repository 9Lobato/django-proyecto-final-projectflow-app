# apps\tasks\admin.py sirve para:
# registrar el modelo Task en el panel de administración de Django
# gestionar tareas desde /admin sin construir interfaz propia

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib import admin
# Imports internos de proyecto/apps
from .models import Task


# CONFIGURACIÓN ADMINISTRATIVA: registra y configura el modelo Task en el admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

  list_display = (
    "id",
    "project",
    "title",
    "created_by",
    "assigned_to",
    "status",
    "priority",)

  list_editable = (
    "project",
    "assigned_to",
    "status",
    "priority",)

  list_filter = (
    "project",
    "status",
    "priority",
    "created_by",
    "assigned_to",)

  search_fields = (
    "title",
    "description",)

  ordering = ("-id", )
