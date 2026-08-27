# apps\tasks\forms.py sirve para:
# definir los formularios de creación y edición de tareas y comentarios,
# incluyendo sus campos, restricciones y permisos según el usuario y el proyecto

# Librerías estándar de Python
from datetime import datetime
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
# Imports internos de proyecto/apps
from .models import Task, TaskComment
from apps.projects.permissions import get_user_role


# FORMULARIO DE TAREAS: gestiona la creación y edición de tareas según el usuario y el proyecto
class TaskForm(forms.ModelForm):

  def __init__(self, *args, user=None, readonly=False, user_role=None, is_create=False, project=None, **kwargs):
    super().__init__(*args, **kwargs)

    if readonly:
      for field in self.fields.values():
        field.disabled = True
      return

    if not is_create:
      self.fields["project"].disabled = True

    if project is None:
      project = getattr(self.instance, "project", None)

    # ======================================================
    # Filtrar usuarios asignables
    # ======================================================

    if project is None:
        self.fields["assigned_to"].queryset = User.objects.none()

    else:
        current_role = get_user_role(user, project) if user else None

        if current_role == "OWNER":
            allowed_users = (
                User.objects
                .filter(project_assignments__project=project)
                .distinct()
            )
        else:
            allowed_users = (
                User.objects
                .filter(project_assignments__project=project)
                .exclude(
                    project_assignments__project=project,
                    project_assignments__role__name="OWNER",
                )
                .distinct()
            )

        self.fields["assigned_to"].queryset = allowed_users

    # ======================================================
    # Restricciones MEMBER
    # ======================================================

    if user_role == "MEMBER":

      editable = set() if is_create else {"description", "status"}

      for name, field in self.fields.items():
        if name not in editable:
          field.disabled = True

    # ======================================================
    # Tareas finalizadas/canceladas
    # ======================================================

    if self.instance and self.instance.pk:

      if self.instance.status in ["DONE", "CANCELLED"]:

        self.fields["time_estimated"].disabled = True
        self.fields["due_at"].disabled = True

  def clean_due_at(self):
    due_at = self.cleaned_data.get("due_at")

    if due_at:
      due_at = timezone.make_aware(
        datetime.combine(
          due_at,
          datetime.max.time()
        )
      )

    return due_at

  class Meta:
    model = Task
  
    fields = [
      "project",
      "title",
      "description",
      "priority",
      "status",
      "assigned_to",
      "time_estimated",
      "due_at",]

    widgets = {
      "project": forms.Select(attrs={"class": "form-select"}),
      "title": forms.TextInput(attrs={"class": "form-control", "maxlength": 40,}),
      "description": forms.Textarea(attrs={
        "class": "form-control", 
        "rows": 12,
        "style": "resize: vertical; overflow-y: auto;",}),
      "priority": forms.Select(attrs={"class": "form-select"}),
      "status": forms.Select(attrs={"class": "form-select"}),
      "assigned_to": forms.Select(attrs={"class": "form-select"}),
      "time_estimated": forms.NumberInput(attrs={"class": "form-control text-end", "min": 0}),
      "due_at": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}),}


# FORMULARIO DE COMENTARIOS: gestiona la creación y edición de comentarios y solicitudes de tareas
class TaskCommentForm(forms.ModelForm):

  class Meta:
    model = TaskComment
    fields = ["text", "type", "request_kind"]

    widgets = {
      "text": forms.Textarea(attrs={
        "class": "form-control",
        "id": "commentText",
        "rows": 1,
        "placeholder": "Escribe la descripción aquí ...",
      }),
      "type": forms.Select(attrs={
        "class": "form-select"
      }),
      "request_kind": forms.Select(attrs={
        "class": "form-select"
      }),
    }

  def __init__(self, *args, user=None, readonly=False, is_follow_only=False, **kwargs):
    super().__init__(*args, **kwargs)

    if readonly or is_follow_only:
      for field in self.fields.values():
        field.disabled = True
        field.widget.attrs["disabled"] = True
        field.widget.attrs["readonly"] = True
      return

    if user:
      self.user = user

      if not user.groups.filter(name__in=["MANAGER", "OWNER"]).exists():
        self.fields["type"].initial = TaskComment.COMMENT
        self.fields["request_kind"].disabled = True
