# apps\core\forms.py sirve para:
# definir formularios personalizados y reutilizables
# relacionados con la aplicación core

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django import forms
from django.contrib.auth.forms import AuthenticationForm
# Imports internos de proyecto/apps


# formulario personalizado para el inicio de sesión
class CustomLoginForm(AuthenticationForm):

  username = forms.CharField(
    widget=forms.TextInput(attrs={
      "class": "form-control",
      "style": "width: 220px;"}))

  password = forms.CharField(
    widget=forms.PasswordInput(attrs={
      "class": "form-control",
      "style": "width: 220px;"}))
