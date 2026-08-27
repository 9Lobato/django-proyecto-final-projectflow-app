# apps\core\context_processors.py sirve para:
# proporcionar información sobre el rol del usuario
# a todas las plantillas de Django

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
# Imports internos de proyecto/apps
from apps.projects.models import Assignment


# determina los roles del usuario actual para las plantillas
def user_role(request):

  if not request.user.is_authenticated:
    return {
      "is_owner": False,
      "is_manager": False,
    }

  is_owner = (
    request.user.is_superuser
    or Assignment.objects.filter(
      user=request.user,
      role__name="OWNER",
    ).exists()
  )

  is_manager = (
    request.user.is_superuser
    or Assignment.objects.filter(
      user=request.user,
      role__name="MANAGER",
    ).exists()
  )

  return {
    "is_owner": is_owner,
    "is_manager": is_manager,
  }
