# apps\core\urls.py sirve para:
# definir las URLs de la aplicación core

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.urls import path
# Imports internos de proyecto/apps
from . import views


urlpatterns = [
  path("navbar/", views.navbar_api, name="navbar_api"),
  path("workflow/", views.workflow_api, name="workflow_api"),
]
