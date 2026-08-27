# apps\projects\admin.py sirve para:
# registrar y configurar los modelos de la aplicación en el panel de administración de Django
# y personalizar la gestión de proyectos, roles, asignaciones, plantillas y usuarios

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
# Imports internos de proyecto/apps
from .models import Assignment, Project, ProjectTemplate, Role, TaskTemplate


# configura la visualización del modelo Role en el admin
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):

  list_display = (
    "id",
    "name",)

  ordering = ("name",)

# configura la visualización del modelo Project en el admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

  list_display = (
#    "id",
    "code",
    "name",
#    "description",
    "owner",
    "created_at",
    "updated_at",)

  search_fields = (
    "code",
    "name",
    "description",)

  ordering = ("-code",)

# configura la visualización del modelo Assignment en el admin
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

  list_display = (
#    "id",
    "project_code",
    "project_name",
#    "project",
    "user",
    "role",
    "assigned_at",)

  list_filter = (
    "user",
    "role",
    "project",)

  search_fields = (
    "project__code",
    "project__name",)

  ordering = ("-project__code", "user__username",)

  def project_code(self, obj):
    return obj.project.code

  project_code.short_description = "Code"

  def project_name(self, obj):
    return obj.project.name

  project_name.short_description = "Name"


# elimina del admin las configuraciones originales de User y Group
# para sustituir la configuración de User por una personalizada
admin.site.unregister(User)
admin.site.unregister(Group)


# configura la visualización personalizada de User en el admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
  list_display = (
    "username",
    "project_roles",
#    "email",
    "is_superuser",
    "is_staff",)
  
  ordering = ("username",)

  def project_roles(self, obj):

    assignments = Assignment.objects.filter(
      user=obj
    ).select_related(
      "project",
      "role")

    return ", ".join([
      f'{a.project.code} ({a.role.name})'
      for a in assignments])

  project_roles.short_description = "Project Roles"


# permite gestionar las tareas de una plantilla desde el admin
class TaskTemplateInline(admin.TabularInline):
  model = TaskTemplate
  extra = 0


# configura la gestión de plantillas de proyecto en el admin
@admin.register(ProjectTemplate)
class ProjectTemplateAdmin(admin.ModelAdmin):
  inlines = [TaskTemplateInline]
