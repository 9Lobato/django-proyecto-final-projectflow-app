# apps\projects\to_template.py sirve para:
# convertir un proyecto existente en una plantilla reutilizable
# copiando sus datos y las tareas asociadas

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
# Imports internos de proyecto/apps
from apps.projects.models import ProjectTemplate, TaskTemplate
from apps.tasks.models import Task


# convierte un proyecto y sus tareas en una plantilla de proyecto
def to_template(project, name=None):

  template = ProjectTemplate.objects.create(
    name=name or project.name,
    description=project.description or "",
    generated_from=project.code)

  tasks = Task.objects.filter(project=project)

  for task in tasks:
    TaskTemplate.objects.create(
      template=template,
      title=task.title,
      description=task.description or "",
      priority=task.priority)

  project.template = template
  project.save(update_fields=["template"])

  return template
