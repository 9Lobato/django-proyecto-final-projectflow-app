# apps\reports\demo\roles.py sirve para:
# crear o recuperar los roles necesarios para los datos de demostración
# y devolverlos organizados por nombre

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
# Imports internos de proyecto/apps
from apps.projects.models import Role
from apps.reports.demo.catalogs.project_roles import ROLES

# crea o recupera los roles definidos en el catálogo y los devuelve organizados por nombre
def create_roles():

  roles = {}

  for name in ROLES:
    role, _ = Role.objects.get_or_create(name=name)
    roles[name] = role

  return roles
