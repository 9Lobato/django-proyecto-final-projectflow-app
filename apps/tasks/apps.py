# apps\tasks\apps.py sirve para:
# configurar la aplicación tasks dentro del proyecto Django

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.apps import AppConfig
# Imports internos de proyecto/apps


# CONFIGURACIÓN DE LA APP: define la configuración de la aplicación tasks
class TasksConfig(AppConfig):
  default_auto_field = "django.db.models.BigAutoField"
  name = "apps.tasks"
