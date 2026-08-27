# apps\projects\permissions.py sirve para:
# centralizar la lógica de permisos de usuarios sobre proyectos y tareas
# determinar qué acciones puede realizar cada usuario según su rol
# y controlar el acceso de usuarios asignados o seguidores de proyectos

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
# Imports internos de proyecto/apps
from .models import Assignment, ProjectFollow


# matriz de permisos disponibles para cada rol
ROLE_PERMISSIONS = {
    
  "OWNER": {
    "view_project": True,
    "create_project": True,
    "edit_project": True,
    "delete_project": True,
    "archive_project": True,
    "manage_users": True,
    "change_owner": True,

    "view_task": True,
    "create_task": True,
    "edit_task": True,
    "delete_task": True,
    "assign_task": True,},

  "MANAGER": {
    "view_project": True,
    "create_project": False,
    "edit_project": True,
    "delete_project": False,
    "archive_project": False,
    "manage_users": True,
    "change_owner": False,

    "view_task": True,
    "create_task": True,
    "edit_task": True,
    "delete_task": True,
    "assign_task": True,},

  "MEMBER": {
    "view_project": True,
    "create_project": False,
    "edit_project": False,
    "delete_project": False,
    "archive_project": False,
    "manage_users": False,
    "change_owner": False,

    "view_task": True,
    "create_task": False,
    "edit_task": False, # MEMBER no tiene permiso general de edición, pero puede editar descripción y estado de sus tareas asignadas.
    "delete_task": False,
    "assign_task": False,}}


# obtiene el rol que tiene un usuario dentro de un proyecto
def get_user_role(user, project):

  if user.is_superuser:
    return "OWNER"

  assignment = Assignment.objects.filter(
    user=user,
    project=project
  ).select_related("role").first()

  if not assignment:
    return None

  return assignment.role.name


# comprueba si el rol del usuario tiene un permiso determinado
def has_permission(user, project, permission_key):

  role = get_user_role(user, project)

  if not role:
    return False

  permissions = ROLE_PERMISSIONS.get(role)

  if not permissions:
    return False

  return permissions.get(permission_key, False)


# comprueba si el usuario puede visualizar un proyecto
def user_can_view_project(user, project):

  # Owner
  if user.is_superuser:
    return True

  # Miembro del proyecto
  if Assignment.objects.filter(
    user=user,
    project=project
  ).exists():
    return True

  # Manager que sigue el proyecto
  if ProjectFollow.objects.filter(
    user=user,
    project=project
  ).exists():
    return True

  return False


# comprueba si el usuario puede crear proyectos
def user_can_create_project(user, project=None):
  if user.is_superuser:
    return True
  return has_permission(user, project, "create_project")


# comprueba si el usuario puede editar un proyecto
def user_can_edit_project(user, project):

  if user.is_superuser:
    return True

  if ProjectFollow.objects.filter(
    user=user,
    project=project
  ).exists():
    return False

  role = get_user_role(user, project)

  return role in ["OWNER", "MANAGER"]


# comprueba si el usuario puede eliminar un proyecto
def user_can_delete_project(user, project):
  if user.is_superuser:
    return True
  return has_permission(user, project, "delete_project")


# comprueba si el usuario puede archivar un proyecto
def user_can_archive_project(user, project):
  if user.is_superuser:
    return True
  return has_permission(user, project, "archive_project")


# comprueba si el usuario puede gestionar los usuarios de un proyecto
def user_can_manage_project(user, project):
  if user.is_superuser:
    return True
  return has_permission(user, project, "manage_users")


# comprueba si el usuario puede cambiar el propietario de un proyecto
def user_can_change_owner(user, project):
  if user.is_superuser:
    return True
  return has_permission(user, project, "change_owner")


# comprueba si el usuario puede visualizar las tareas de un proyecto
def user_can_view_task(user, task):
  if user.is_superuser:
    return True
  project = task.project
  # Usuario asignado al proyecto
  if Assignment.objects.filter(
    user=user,
    project=project
  ).exists():
    return True
  # Usuario siguiendo el proyecto
  if ProjectFollow.objects.filter(
    user=user,
    project=project
  ).exists():
    return True
  return False


# comprueba si el usuario puede crear tareas en un proyecto
def user_can_create_task(user, project):
  if project.is_archived:
      return False
  if user.is_superuser:
    return True
  return has_permission(user, project, "create_task")


# comprueba si el usuario puede editar una tarea
def user_can_edit_task(user, task):
  if user.is_superuser:
    return True
  role = get_user_role(user, task.project)

  # Owner y Manager pueden editar todo
  if role in ["OWNER", "MANAGER"]:
    return True

  # Member sólo sus tareas
  if role == "MEMBER":
    return task.assigned_to == user
  return False


# comprueba si el usuario puede duplicar una tarea en un proyecto
def user_can_duplicate_task(user, project):
  if user.is_superuser:
    return True
  return has_permission(user, project, "create_task")


# comprueba si el usuario puede eliminar una tarea
def user_can_delete_task(user, task):
  if user.is_superuser:
    return True
  return has_permission(user, task.project, "delete_task")


# comprueba si el usuario puede asignar una tarea a un usuario
def user_can_assign_task(user, task):
  if user.is_superuser:
    return True
  return has_permission(user, task.project, "assign_task")


# determina el nivel de acceso del usuario a un proyecto
def get_project_access_mode(user, project):

  if user.is_superuser:
    return "EDIT"

  role = get_user_role(user, project)

  if role in ["OWNER", "MANAGER"]:
    return "EDIT"

  if role == "MEMBER":
    return "EDIT"

  if ProjectFollow.objects.filter(
    user=user,
    project=project
  ).exists():
    return "READONLY"

  return "DENY"


# determina el nivel de acceso del usuario a una tarea
def get_task_access_mode(user, task):

  if user.is_superuser:
    return "EDIT"

  project = task.project
  role = get_user_role(user, project)

  if role in ["OWNER", "MANAGER"]:
    return "EDIT"

  if role == "MEMBER":
    if task.assigned_to == user:
      return "EDIT"
    return "READONLY"

  if ProjectFollow.objects.filter(
    user=user,
    project=project
  ).exists():
    return "READONLY"

  return "DENY"
