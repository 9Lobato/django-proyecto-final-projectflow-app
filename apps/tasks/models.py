# apps\tasks\models.py sirve para:
# definir las tareas y comentarios asociados a los proyectos
# controlar estados, prioridades, fechas y tiempos de las tareas
# gestionar asignaciones, seguimiento y eliminación lógica de tareas
# calcular información relacionada con planificación, plazos y progreso
# y controlar los comentarios, solicitudes y menciones de las tareas

# Librerías estándar de Python
import re
from datetime import timedelta
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
# Imports internos de proyecto/apps
from apps.projects.models import Project


# MODELO DE TAREAS: representa una tarea dentro de un proyecto
class Task(models.Model):

  sequence_number = models.PositiveIntegerField(
    null=True,
    blank=True
  )

  title = models.CharField(max_length=149)

  description = models.TextField(
    blank=True,
    null=True)

  project = models.ForeignKey(
    Project,
    on_delete=models.CASCADE,
    related_name="tasks")

  created_by = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="created_tasks")
    
  created_at = models.DateTimeField(
    default=timezone.now)

  deleted_at = models.DateTimeField(
    null=True,
    blank=True)

  updated_at = models.DateTimeField(
    auto_now=True)

  assigned_to = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="assigned_tasks")
  
  watchers = models.ManyToManyField(
    User,
    blank=True,
    related_name="watched_tasks")

  STATUS_CHOICES = [
    ("TODO", "To do"),
    ("IN_PROGRESS", "In progress"),
    ("DONE", "Done"),
    ("CANCELLED", "Cancelled"),]

  status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default="TODO")

  PRIORITY_CHOICES = [
    ("LOW", "Low"),
    ("MEDIUM", "Medium"),
    ("HIGH", "High"),]

  priority = models.CharField(
    max_length=20,
    choices=PRIORITY_CHOICES,
    default="MEDIUM")
  
  time_estimated = models.PositiveIntegerField(
    null=True,
    blank=True,)

  due_at = models.DateTimeField(
    null=True,
    blank=True)

  started_at = models.DateTimeField(
    null=True,
    blank=True)

  completed_at = models.DateTimeField(
    null=True,
    blank=True)

  cancelled_at = models.DateTimeField(
    null=True,
    blank=True)

  elapsed_minutes = models.PositiveIntegerField(
    default=0)

  active_started_at = models.DateTimeField(
    null=True,
    blank=True)

  remaining_minutes = models.IntegerField(
    null=True,
    blank=True
  )

  frozen_at = models.DateTimeField(
    null=True,
    blank=True)
  
  @property
  def is_overdue(self):

    delta = self.remaining_delta

    return (delta is not None and delta.total_seconds() < 0)
  
  @property
  def is_on_time(self):

    delta = self.remaining_delta

    return (delta is not None and delta.total_seconds() >= 0)

  def __str__(self):
    return self.title

  @property
  def is_deleted(self):
    return self.deleted_at is not None

  def soft_delete(self):

    if self.deleted_at:
      return

    self.deleted_at = timezone.now()

    self.active_started_at = None
    
    self.frozen_at = self.frozen_at or timezone.now()

    self.save(update_fields=[
      "deleted_at",
      "active_started_at",
      "frozen_at",
      "updated_at",
    ])

  @property
  def planning_offset(self):

    if not self.due_at or not self.time_estimated:
      return None

    reference = self.reference_time

    if reference is None:
      return None

    planned_start = (
      self.due_at -
      timedelta(days=self.time_estimated)
    )

    delta = reference - planned_start

    return delta.total_seconds() / 86400

  @property
  def planning_offset_abs(self):

    value = self.planning_offset

    if value is None:
      return None

    return abs(value)

  @property
  def reference_time(self):

    if self.project.is_archived:
      return self.project.archived_at or timezone.now()

    if self.status in ["DONE", "CANCELLED"]:
      return self.frozen_at or timezone.now()

    return timezone.now()
  
  @property
  def remaining_delta(self):

    if self.project.is_archived:
      return None

    if self.status in ["DONE", "CANCELLED"]:
      return None

    if not self.due_at:
      return None

    return self.due_at - timezone.now()

  @property
  def remaining_status(self):

    if self.project.is_archived:
      return "ARCHIVED"

    if self.status in ["DONE", "CANCELLED"]:
      return "NO_LIMIT"

    if not self.due_at:
      return "NO_LIMIT"

    if self.due_at < timezone.now():
      return "OVERDUE"

    return "ON_TIME"

  @property
  def time_remaining(self):

    status = self.remaining_status

    if status == "ARCHIVED":
      return "Archivada"

    if status == "NO_LIMIT":
      return None

    if status == "OVERDUE":
      return -1

    delta = self.remaining_delta

    return delta.total_seconds() / 86400
  
  @property
  def timeline_total(self):

    if not self.due_at or not self.created_at:
      return None

    total_minutes = (
      self.due_at - self.created_at
    ).total_seconds() / 60

    return max(total_minutes, 1)

  @property
  def timeline_estimated_start_percent(self):

    if not self.due_at:
      return 0

    if not self.timeline_total:
      return 0

    if not self.time_estimated:
      return 0

    created = timezone.localtime(self.created_at)

    estimated_start = (
      self.due_at -
      timedelta(days=self.time_estimated)
    )

    elapsed_minutes = (
        estimated_start - created
    ).total_seconds() / 60

    percent = elapsed_minutes * 100 / self.timeline_total

    return min(max(percent, 0), 100)

  @property
  def timeline_estimated_percent(self):

    if not self.timeline_total:
      return 0

    if not self.time_estimated:
      return 0

    estimated_minutes = self.time_estimated * 1440

    percent = estimated_minutes * 100 / self.timeline_total

    return min(max(percent, 0), 100)

  @property
  def timeline_today_percent(self):

    if not self.timeline_total:
      return 0

    created = timezone.localtime(self.created_at).date()

    current_date = timezone.localtime(self.reference_time).date()

    elapsed_days = (current_date - created).days

    elapsed_minutes = elapsed_days * 1440

    percent = elapsed_minutes * 100 / self.timeline_total

    return min(max(percent, 0), 100)
  
  def stop_timers(self):
    if self.frozen_at:
      return

    now = timezone.now()

    if self.active_started_at:
      elapsed = now - self.active_started_at
      elapsed_minutes = max(int(elapsed.total_seconds() / 60), 0)
      self.elapsed_minutes += elapsed_minutes

    if self.due_at:
      remaining_minutes = int((self.due_at - now).total_seconds() / 60)
      self.remaining_minutes = max(remaining_minutes, 0)
    else:
      self.remaining_minutes = None

    self.active_started_at = None
    self.frozen_at = now
  
  def unstop_timers(self):

    now = timezone.now()

    if (
      self.remaining_minutes is not None
      and self.remaining_minutes > 0
    ):
      self.due_at = now + timedelta(
        minutes=self.remaining_minutes
      )

    self.active_started_at = now

    self.remaining_minutes = None
    self.frozen_at = None

  def handle_status_change(self, old_status):

    new_status = self.status

    if old_status == new_status:
      return

    now = timezone.now()

    # TODO -> IN_PROGRESS
    if (
      old_status == "TODO" and new_status == "IN_PROGRESS"
    ):
      if self.started_at is None:
        self.started_at = now

      if self.active_started_at is None:
        self.active_started_at = now

      return

    # TODO -> CANCELLED
    if (
      old_status == "TODO" and new_status == "CANCELLED"
    ):
      self.cancelled_at = now
      self.stop_timers()
      return

    # IN_PROGRESS -> DONE
    if (
      old_status == "IN_PROGRESS" and new_status == "DONE"
    ):
      self.completed_at = now
      self.stop_timers()
      return
    
    # IN_PROGRESS -> CANCELLED
    if (
      old_status == "IN_PROGRESS" and new_status == "CANCELLED"
    ):
      self.cancelled_at = now
      self.stop_timers()
      return

    # DONE -> IN_PROGRESS
    if (
      old_status == "DONE" and new_status == "IN_PROGRESS"
    ):
      self.completed_at = None
      self.unstop_timers()
      return

    # CANCELLED -> TODO
    if (
      old_status == "CANCELLED" and new_status == "TODO"
    ):
      self.cancelled_at = None
      if self.remaining_minutes is not None:
        self.due_at = timezone.now() + timedelta(
          minutes=self.remaining_minutes
        )
      self.remaining_minutes = None
      self.frozen_at = None
      return

    # CANCELLED -> IN_PROGRESS
    if (
      old_status == "CANCELLED"
      and new_status == "IN_PROGRESS"
    ):
      self.cancelled_at = None
      self.unstop_timers()
      return

  @property
  def is_planned(self):
    return self.due_at is not None

  def initialize_timers(self):

    if self.status != "IN_PROGRESS":
      return

    now = timezone.now()

    self.started_at = now
    self.active_started_at = now
  
  def initialize_new_task(self, user):

    self.created_by = user
    self.initialize_timers()
    self.save()
    self.watchers.add(user)

  def save(self, *args, **kwargs):

    if self.sequence_number is None:
      last_number = Task.objects.filter(
        project=self.project
      ).aggregate(
        models.Max("sequence_number")
      )["sequence_number__max"]

      self.sequence_number = (last_number or 0) + 1

    if self.pk:

      old_task = Task.objects.get(pk=self.pk)

      if old_task.due_at != self.due_at:
        self.remaining_minutes = None

    super().save(*args, **kwargs)
  
  def update_status(self, old_status):

    self.handle_status_change(old_status)
    self.save()


# MODELO DE COMENTARIOS: representa comentarios y solicitudes asociados a una tarea
class TaskComment(models.Model):

  COMMENT = "COMMENT"
  REQUEST = "REQUEST"

  TYPE_CHOICES = [
    (COMMENT, "Comentario"),
    (REQUEST, "Solicitud"),
  ]

  REQUEST_KIND_CHOICES = [
    ("IMMEDIATE", "Inmediata"),
    ("SCHEDULED", "Programada"),
    ("ROUTINE", "Rutinaria"),
    ("MITIGATION", "Revisión"),
    ("IMPROVEMENT", "Mejora"),
    ("OPTIONAL", "Opcional"),
    ("DELEGATED", "Delegada"),
  ]

  task = models.ForeignKey(Task, related_name="comments", on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  text = models.TextField()
  created_at = models.DateTimeField(default=timezone.now)

  type = models.CharField(
    max_length=10,
    choices=TYPE_CHOICES,
    default=COMMENT,
  )

  request_kind = models.CharField(
    max_length=20,
    choices=REQUEST_KIND_CHOICES,
    blank=True,
  )

  resolved = models.BooleanField(default=False)

  resolved_at = models.DateTimeField(null=True, blank=True)

  @property
  def mentions(self):
    return re.findall(r"@([A-Za-z0-9_]+)", self.text)
  
  def get_mentioned_users(self):
    return User.objects.filter(username__in=self.mentions)
  
  @property
  def mentions_string(self):
    if not self.mentions:
      return "NONE"
    return ",".join(self.mentions)
  
  def can_resolve(self, user):
    return (
      self.type == self.REQUEST
      and not self.resolved
      and user in self.get_mentioned_users()
    )

  def can_reopen(self, user):
    return (
      self.type == self.REQUEST
      and self.resolved
      and self.user == user
    )
  
  def can_delete_request(self, user):
    return (
      self.type == self.REQUEST
      and self.user == user
      and not self.resolved
    )
  
  def can_delete(self, user):
    project = self.task.project
    is_author = self.user == user
    is_owner = getattr(project, "owner", None) == user
    is_manager = project.assignments.filter(
      user=user,
      role__name="MANAGER"
    ).exists()
    if self.type == self.REQUEST:
      # Nunca se puede borrar una solicitud resuelta
      if self.resolved:
        return False
      # El autor puede eliminarla mientras siga abierta
      if is_author:
        return True
      # Owner y Manager también pueden eliminar solicitudes abiertas
      if is_owner or is_manager:
        return True
      return False
    return is_author or is_owner or is_manager

  class Meta:
    ordering = ["-created_at"]
