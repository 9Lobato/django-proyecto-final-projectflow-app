# apps\kanban\urls.py sirve para:
# definir las URLs de la aplicación kanban
# y asociarlas con las vistas correspondientes

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.urls import path
# Imports internos de proyecto/apps
from . import views


urlpatterns = [
  # Mostrar tablero kanban
  path("", views.board, name="kanban"),
  # Django → JSON → frontend
  path("api/", views.kanban_api, name="kanban_api"),
  # Cambiar estado de una tarea Django → modifica BD
  path("move/", views.move_task, name="kanban_move"),
  # Copiar tarea a otro proyecto Django → modifica BD
  path("copy/", views.copy_task, name="kanban_copy"),
]
