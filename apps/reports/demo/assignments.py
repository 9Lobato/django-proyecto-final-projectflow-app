# apps\reports\demo\assignments.py sirve para:
# definir las asignaciones de usuarios y roles para los proyectos
# de demostración y crear dichas asignaciones en la base de datos

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.db import transaction
from django.contrib.auth.models import User
# Imports internos de proyecto/apps
from apps.projects.models import Project, Assignment, Role


# catálogo de asignaciones de usuarios por proyecto y rol
ASSIGNMENTS = [
  {
    "project": "23-001",
    "members": [
      ("ALopez", "OWNER"),
      ("DMartin", "MANAGER"),
      ("JSanz", "MEMBER"),
      ("LMoreno", "MEMBER"),
    ],
  },
  {
    "project": "23-002",
    "members": [
      ("CGarcia", "OWNER"),
      ("ERuiz", "MANAGER"),
      ("MGil", "MEMBER"),
      ("PNavarro", "MEMBER"),
    ],
  },
  {
    "project": "24-001",
    "members": [
      ("ALopez", "OWNER"),
      ("DMartin", "MANAGER"),
      ("JSanz", "MEMBER"),
      ("MGil", "MEMBER"),
    ],
  },
  {
    "project": "24-002",
    "members": [
      ("CGarcia", "OWNER"),
      ("ERuiz", "MANAGER"),
      ("LMoreno", "MEMBER"),
    ],
  },
  {
    "project": "24-003",
    "members": [
      ("ALopez", "OWNER"),
      ("DMartin", "MANAGER"),
      ("PNavarro", "MEMBER"),
      ("JSanz", "MEMBER"),
    ],
  },
  {
    "project": "25-001",
    "members": [
      ("CGarcia", "OWNER"),
      ("ERuiz", "MANAGER"),
      ("JSanz", "MEMBER"),
      ("LMoreno", "MEMBER"),
    ],
  },
  {
    "project": "25-002",
    "members": [
      ("ALopez", "OWNER"),
      ("DMartin", "MANAGER"),
      ("MGil", "MEMBER"),
      ("PNavarro", "MEMBER"),
    ],
  },
  {
    "project": "25-003",
    "members": [
      ("CGarcia", "OWNER"),
      ("ERuiz", "MANAGER"),
      ("JSanz", "MEMBER"),
    ],
  },
  {
    "project": "26-001",
    "members": [
      ("ALopez", "OWNER"),
      ("DMartin", "MANAGER"),
      ("LMoreno", "MEMBER"),
      ("MGil", "MEMBER"),
    ],
  },
  {
    "project": "26-002",
    "members": [
      ("CGarcia", "OWNER"),
      ("ERuiz", "MANAGER"),
      ("PNavarro", "MEMBER"),
      ("JSanz", "MEMBER"),
    ],
  },
  {
    "project": "26-003",
    "members": [
      ("ALopez", "OWNER"),
      ("DMartin", "MANAGER"),
      ("MGil", "MEMBER"),
    ],
  },
  {
    "project": "26-004",
    "members": [
      ("CGarcia", "OWNER"),
      ("ERuiz", "MANAGER"),
      ("LMoreno", "MEMBER"),
      ("PNavarro", "MEMBER"),
    ],
  },
]

# crea o actualiza las asignaciones de usuarios a proyectos
# utilizando el rol indicado en el catálogo de demostración
@transaction.atomic
def create_assignments():
  users = {
    user.username: user
    for user in User.objects.all()
  }
  roles = {
    role.name: role
    for role in Role.objects.all()
  }
  projects = {
    project.code: project
    for project in Project.objects.all()
  }
  Assignment.objects.all().delete()
  for data in ASSIGNMENTS:
    project = projects.get(data["project"])
    if not project:
      raise Exception(f'Proyecto {data["project"]} no existe.')

    for username, role_name in data["members"]:
      user = users.get(username)
      if not user:
        raise Exception(f'Usuario {username} no existe.')
      role = roles.get(role_name)
      if not role:
        raise Exception(f'Rol {role_name} no existe.')

      Assignment.objects.update_or_create(
        project=project,
        user=user,
        defaults={
          "role": role,
        },
      )
