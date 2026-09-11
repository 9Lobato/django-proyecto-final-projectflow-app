# apps\accounts\models.py sirve para:
# gestionar información adicional de los usuarios del sistema
# extender el modelo User de Django
# almacenar datos de perfil como biografía o avatar
# mantener separada la lógica de autenticación y la de perfil de usuario

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib.auth.models import User
from django.db import models
# Imports internos de proyecto/apps


# perfil con información adicional asociada a un usuario
class Profile(models.Model):

  user = models.OneToOneField(User, on_delete=models.CASCADE)

  bio = models.TextField(blank=True, null=True)

  avatar = models.ImageField(
    upload_to="avatars/",
    blank=True,
    null=True
  )

  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.user.username


# progreso del workflow asociado al usuario
class WorkflowProgress(models.Model):

  user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name="workflow_progress"
  )

  checks = models.JSONField(default=dict, blank=True)

  def __str__(self):
    return f"Workflow: {self.user.username}"
