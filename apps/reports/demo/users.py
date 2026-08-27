# apps\reports\demo\users.py sirve para:
# definir los usuarios de demostración y crearlos o actualizarlos
# en la base de datos

# Librerías estándar de Python
from django.contrib.auth.models import User
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.db import transaction
# Imports internos de proyecto/apps


# catálogo de usuarios de demostración
USERS = [
  # username, first_name, last_name, is_superuser, is_staff
  ("SLobato",  "Sergi",  "Lobato",   True,  True),   # Owner sistema
  ("ALopez",   "Ana",    "López",    False, False),  # Owner proyecto
  ("CGarcia",  "Carlos", "García",   False, False),  # Owner proyecto
  ("DMartin",  "David",  "Martín",   False, True),   # Manager
  ("ERuiz",    "Elena",  "Ruiz",     False, True),   # Manager
  ("JSanz",    "Javier", "Sanz",     False, False),  # Member
  ("LMoreno",  "Laura",  "Moreno",   False, False),  # Member
  ("MGil",     "Marta",  "Gil",      False, False),  # Member
  ("PNavarro", "Pablo",  "Navarro",  False, False),  # Member
]


# crea o actualiza los usuarios de demostración en la base de datos y devuelve 
# los usuarios organizados por nombre de usuario
@transaction.atomic
def create_users():

  users = {}

  for username, first_name, last_name, is_superuser, is_staff in USERS:

    user, created = User.objects.update_or_create(
      username=username,
      defaults={
        "first_name": first_name,
        "last_name": last_name,
        "email": f"{username.lower()}@demo.local",
        "is_staff": is_staff,
        "is_superuser": is_superuser,
        "is_active": True,
      },
    )

    user.set_password("demo")
    user.save()

    users[username] = user

  return users
