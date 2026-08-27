# apps\kanban\apps.py sirve para:
# configurar la aplicación kanban dentro del proyecto Django

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.apps import AppConfig
# Imports internos de proyecto/apps


# configuración de la aplicación kanban
class KanbanConfig(AppConfig):
  default_auto_field = "django.db.models.BigAutoField"
  name = "apps.kanban"
