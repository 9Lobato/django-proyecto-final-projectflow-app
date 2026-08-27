# apps\projects\models.py sirve para:
# definir los modelos principales de proyectos, roles y asignaciones de usuarios
# gestionar plantillas de proyectos y tareas
# gestionar el seguimiento y el archivado de proyectos

# Librerías estándar de Python
from datetime import timedelta
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
# Imports internos de proyecto/apps


# define los roles disponibles dentro de un proyecto
class Role(models.Model):

  ROLE_CHOICES = [
    ("OWNER", "Owner"),
    ("MANAGER", "Manager"),
    ("MEMBER", "Member"),]

  name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

  def __str__(self):
    return self.name


# define los proyectos y gestiona su archivado y recuperación
class Project(models.Model):

  code = models.CharField(
    max_length=6,
    unique=True,
    validators=[
      RegexValidator(
        regex=r"^\d{2}-\d{3}$",
        message="El código debe tener formato YY-000")])

  name = models.CharField(max_length=136)
  description = models.TextField(blank=True, null=True)
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_projects")
  
  template = models.ForeignKey(
    "ProjectTemplate",
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name="projects"
  )

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_archived = models.BooleanField(default=False, verbose_name="Archivado")
  archived_at = models.DateTimeField(null=True, blank=True)

  def __str__(self):
    return f'{self.code} - {self.name}'

  def archive(self):

    if self.is_archived:
      return

    now = timezone.now()

    self.is_archived = True
    self.archived_at = now

    for task in self.tasks.exclude(status__in=["DONE", "CANCELLED"]):
      task.stop_timers()
      task.save(update_fields=[
        "elapsed_minutes",
        "remaining_minutes",
        "active_started_at",
        "frozen_at",
      ])

    self.save(update_fields=["is_archived", "archived_at"])

  def unarchive(self):

    if self.archived_at:
      paused_time = timezone.now() - self.archived_at
    else:
      paused_time = timedelta()

    for task in self.tasks.exclude(status__in=["DONE", "CANCELLED"]):

      if task.due_at:
        task.due_at += paused_time

      task.unstop_timers()

      task.save(update_fields=[
        "due_at",
        "remaining_minutes",
        "active_started_at",
        "frozen_at",
      ])

    self.is_archived = False
    self.archived_at = None

    self.save(update_fields=["is_archived", "archived_at"])


# relaciona usuarios con proyectos y les asigna un rol
class Assignment(models.Model):
  
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_assignments")
  project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="assignments")
  role = models.ForeignKey(Role, on_delete=models.CASCADE)
  assigned_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ("user", "project")

  def __str__(self):
    return f'{self.user.username} - {self.project.name} ({self.role.name})'


# define las plantillas reutilizables de proyectos
class ProjectTemplate(models.Model):
  name = models.CharField(max_length=40)
  description = models.TextField(blank=True)
  perfect_for = models.TextField(blank=True, help_text="Uso orientativo del template")
  generated_from = models.CharField(
    max_length=6,
    blank=True,
    null=True)

  def __str__(self):
    return self.name


# define las tareas incluidas en una plantilla de proyecto
class TaskTemplate(models.Model):
  template = models.ForeignKey(ProjectTemplate, related_name="tasks", on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  description = models.TextField(blank=True, default="")

  PRIORITY_CHOICES = [
    ("LOW", "Low"),
    ("MEDIUM", "Medium"),
    ("HIGH", "High"),
  ]

  priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="MEDIUM")

  def __str__(self):
    return self.title


# relaciona usuarios con los proyectos que siguen
class ProjectFollow(models.Model):
  project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="followers")
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_projects")
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ("project", "user")

  def __str__(self):
    return f'{self.user.username} follows {self.project.name}'
