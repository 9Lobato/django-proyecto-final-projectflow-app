# apps\projects\urls.py sirve para:
# definir las URLs de la aplicación projects y asociarlas con las vistas correspondientes

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.urls import path
# Imports internos de proyecto/apps
from . import views


urlpatterns = [
  # Listar proyectos
  path("", views.project_list, name="project_list"),
  # Editar proyecto
  path("<int:pk>/edit/", views.project_update, name="project_update"),
  # Crear proyecto
  path("create/", views.project_create, name="project_create"),
  # Eliminar proyecto
  path("<int:pk>/delete/", views.project_delete, name="project_delete"),
  # Convertir proyecto a plantilla
  path("<int:pk>/to-template/", views.project_to_template, name="project_to_template"),
  # Archivar o desarchivar proyecto
  path("<int:pk>/archive/", views.project_archive_toggle, name="project_archive_toggle"),
  # Seguir o dejar de seguir un proyecto
  path("<int:pk>/follow/", views.project_follow_toggle, name="project_follow_toggle"),
]
