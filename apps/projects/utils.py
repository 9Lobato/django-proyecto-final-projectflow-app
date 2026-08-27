# apps\projects\utils.py sirve para:
# preparar la información de un proyecto que necesita la interfaz
# según el usuario que está consultando el proyecto

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
# Imports internos de proyecto/apps
from .models import Assignment, ProjectFollow
from .permissions import get_user_role


# prepara los datos de un proyecto según el usuario actual
def prepare_project_for_user(project, user):

  project.user_role = get_user_role(user, project)

  project.is_assigned = Assignment.objects.filter(
    user=user,
    project=project
  ).exists()

  project.is_followed = ProjectFollow.objects.filter(
    user=user,
    project=project
  ).exists()

  is_manager = (user.is_staff and not user.is_superuser)

  project.can_follow = (is_manager and not project.is_assigned)

  manager_assignment = (
    Assignment.objects
    .select_related("user")
    .filter(
      project=project,
      role__name="MANAGER"
    )
    .first()
  )

  project.manager = manager_assignment.user if manager_assignment else None

  return project
