# apps\accounts\apps.py sirve para:
# configurar la aplicación accounts y proporcionar a Django
# información sobre su configuración

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.apps import AppConfig
# Imports internos de proyecto/apps


class AccountsConfig(AppConfig):
  default_auto_field = "django.db.models.BigAutoField"
  name = "apps.accounts"
