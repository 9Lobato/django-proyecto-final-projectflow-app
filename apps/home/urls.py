# apps\home\urls.py sirve para:
# definir las URLs de la aplicación home y asociarlas
# con las vistas que deben ejecutarse

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.urls import path
# Imports internos de proyecto/apps
from . import views


urlpatterns = [
  # Mostrar dashboard principal
  path("", views.home, name="home"),
  # Determinar la página inicial según rol de usuario
  path("start/", views.start, name="start"),
]
