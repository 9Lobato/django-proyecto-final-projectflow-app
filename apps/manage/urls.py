# apps\manage\urls.py sirve para:
# definir las URLs de la aplicación manage y asociarlas con las vistas correspondientes

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.urls import path
# Imports internos de proyecto/apps
from . import views


urlpatterns = [
  # Listar usuarios
  path("", views.manage, name="manage"),
  # Editar un usuario
  path("users/<int:pk>/edit/", views.user_update, name="user_update"),
  # Crear un usuario
  path("users/create/", views.user_create, name="user_create"),
  # Eliminar un usuario
  path("users/<int:pk>/delete/", views.user_delete, name="user_delete"),
  # Activar o desactivar un usuario
  path("users/<int:pk>/toggle/", views.user_toggle_active, name="user_toggle"),
  # Mostrar usuarios de un determinado rol
  path("roles/<str:role_name>/", views.role_detail, name="role_detail"),
  # Mostrar el equipo de trabajo de un proyecto
  path("projects/<int:pk>/team/", views.project_team, name="project_team"),
  # Incluir un usuario en el equipo de un proyecto
  path("projects/<int:pk>/team/include/", views.team_include, name="team_include"),
  # Excluir un usuario del equipo de un proyecto
  path("projects/<int:pk>/team/exclude/<int:user_id>/", views.team_exclude, name="team_exclude"),
  # Listar plantillas
  path("templates/", views.templates, name="templates"),
  # Crear una plantilla
  path("templates/create/", views.template_create, name="template_create"),
  # Editar una plantilla
  path("templates/<int:pk>/edit/", views.template_update, name="template_update"),
  # Eliminar una plantilla
  path("templates/<int:pk>/delete/", views.template_delete, name="template_delete"),
]
