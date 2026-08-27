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
  # Cambiar estado de una tarea
  path("move/", views.move_task, name="kanban_move"),
  # Copiar tarea a otro proyecto
  path("copy/", views.copy_task, name="kanban_copy"),
]
