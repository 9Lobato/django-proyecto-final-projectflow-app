# apps\manage\forms.py sirve para:
# definir los formularios utilizados en la gestión de usuarios y plantillas aplicar estilos
# Bootstrap a los campos de los formularios y gestionar los formularios de tareas asociadas a las plantillas

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
# Imports internos de proyecto/apps
from apps.projects.models import ProjectTemplate, TaskTemplate


# aplica clases CSS de Bootstrap a los campos de los formularios
class BootstrapFormMixin:

  def apply_bootstrap(self):
    for field in self.fields.values():
      widget = field.widget

      if isinstance(widget, forms.CheckboxInput):
        widget.attrs["class"] = "form-check-input"

      elif isinstance(widget, forms.Select):
        widget.attrs["class"] = "form-select"

      else:
        widget.attrs["class"] = "form-control"


# formulario para crear y editar usuarios
class UserEditForm(BootstrapFormMixin, forms.ModelForm):

  class Meta:
    model = User
    fields = ["username", "first_name", "last_name", "email", "is_active", "is_staff", "is_superuser", "date_joined", "last_login",]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.apply_bootstrap()

    for field_name in ["date_joined", "last_login"]:
        if field_name in self.fields:
            self.fields[field_name].disabled = True


# formulario para crear y editar plantillas de proyectos
class ProjectTemplateForm(BootstrapFormMixin, forms.ModelForm):

  class Meta:
    model = ProjectTemplate
    fields = [
      "name",
      "description",
      "perfect_for",
    ]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.apply_bootstrap()

    self.fields["description"].widget.attrs.update({
      "rows": 14
    })


# formulario para crear y editar tareas de una plantilla
class TaskTemplateForm(BootstrapFormMixin, forms.ModelForm):

  class Meta:
    model = TaskTemplate
    fields = [
      "title",
      "description",
      "priority",
    ]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.apply_bootstrap()

    self.fields["description"].widget.attrs.update({"rows": 3})
  
  def clean_title(self):
    title = self.cleaned_data.get("title")

    if not title:
      raise forms.ValidationError("Título obligatorio")
    
    return title


# conjunto de formularios para gestionar las tareas de una plantilla
TaskTemplateFormSet = inlineformset_factory(
  ProjectTemplate,
  TaskTemplate,
  form=TaskTemplateForm,
  extra=0,
  can_delete=True,
)
