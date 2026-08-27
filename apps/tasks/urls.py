# apps\tasks\urls.py sirve para:
# definir las rutas de la aplicación tasks
# y asociarlas con las vistas encargadas de listar,
# crear, editar, duplicar y eliminar tareas,
# además de gestionar los comentarios y solicitudes de las tareas

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.urls import path
# Imports internos de proyecto/apps
from . import views


urlpatterns = [
  # Listar todas las tareas
  path("", views.task_list, name="task_list"),
  # Editar tarea
  path("<int:pk>/edit/", views.task_update, name="task_update"),
  # Duplicar tarea
  path("<int:pk>/duplicate/", views.task_duplicate, name="task_duplicate"),
  # Crear tarea de proyecto
  path("project/<int:project_id>/create/", views.task_create, name="task_create"),
  # Eliminar tarea
  path("<int:pk>/delete/", views.task_delete, name="task_delete"),
  # Eliminar una notificación
  path("comments/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
  # Actualizar tipo de notificación
  path("comments/<int:pk>/request-kind/", views.update_request_kind,name="update_request_kind"),
  # Actualizar estado notificación
  path("comments/<int:pk>/status/", views.update_comment_status, name="update_comment_status"),
]
