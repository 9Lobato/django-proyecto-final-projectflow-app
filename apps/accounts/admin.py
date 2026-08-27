# apps\accounts\admin.py sirve para:
# configurar qué modelos de la aplicación aparecen y cómo se gestionan
# desde el panel de administración de Django

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib import admin
# Imports internos de proyecto/apps
from .models import Profile


# configuración de visualización del perfil de usuario en el admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = (
    "id",
    "user",
    "bio",
    "avatar",
    "created_at",)
