# apps\tasks\utils.py sirve para:
# detectar las menciones de usuarios en un texto
# y obtener los usuarios correspondientes de la base de datos

# Librerías estándar de Python
import re
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib.auth.models import User
# Imports internos de proyecto/apps


# UTILIDAD: obtiene los usuarios mencionados mediante @usuario en un texto
def get_mentioned_users(text):

  usernames = re.findall(r"@(\w+)", text)

  return User.objects.filter(username__in=usernames)
