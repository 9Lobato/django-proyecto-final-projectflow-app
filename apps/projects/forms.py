# apps\projects\forms.py sirve para:
# definir los formularios utilizados para crear y editar proyectos
# y permitir seleccionar una plantilla de proyecto al crear un proyecto

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django import forms
# Imports internos de proyecto/apps
from .models import Project, ProjectTemplate


# define el formulario para crear y editar proyectos
class ProjectForm(forms.ModelForm):
    
  template = forms.ModelChoiceField(
    queryset=ProjectTemplate.objects.all(),
    required=False,
    label="Template",
    widget=forms.Select(
      attrs={"class": "form-select"}))

  class Meta:
    model = Project
    fields = [
      "code",
      "name",
      "description",
      "template"]

    widgets = {
      "code": forms.TextInput(attrs={"class": "form-control"}),
      "name": forms.TextInput(attrs={"class": "form-control", "maxlength": 40,}),
      "description": forms.Textarea(attrs={
        "class": "form-control", 
        "rows": 23,
        "style": "resize: vertical; overflow-y: auto;",}),}
