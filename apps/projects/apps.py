# apps\projects\apps.py sirve para:
# configurar la aplicación projects dentro del proyecto Django

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.apps import AppConfig
# Imports internos de proyecto/apps


# configura la aplicación projects
class ProjectsConfig(AppConfig):
  default_auto_field = "django.db.models.BigAutoField"
  name = "apps.projects"
