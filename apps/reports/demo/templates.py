# apps\reports\demo\templates.py sirve para:
# generar las plantillas de demostración a partir de proyectos existentes y crear plantillas 
# independientes con tareas predefinidas

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
# Imports internos de proyecto/apps
from apps.projects.models import Project, ProjectTemplate, TaskTemplate
from apps.projects.to_template import to_template


# códigos de proyectos demo utilizados como origen para generar plantillas automáticamente
TEMPLATE_PROJECTS = [
  "26-003",
  "24-002",
  "23-001",
]


# crea las plantillas de demostración a partir de proyectos existentes y de plantillas definidas 
# directamente
def create_templates():

  ProjectTemplate.objects.all().delete()

  # Templates generados desde proyectos demo
  for code in TEMPLATE_PROJECTS:
    project = Project.objects.get(code=code)
    to_template(project)

  # Templates creados directamente
  create_standalone_templates()


# crea plantillas de proyecto independientes con sus tareas predefinidas, sin utilizar un 
# proyecto existente como origen
def create_standalone_templates():

  template = ProjectTemplate.objects.create(
    name="Nuevo proyecto de software",
    description=(
      "Plantilla para proyectos de desarrollo de aplicaciones "
      "y soluciones software."
    ),
    perfect_for=(
      "Proyectos de desarrollo de aplicaciones web, "
      "móviles o de escritorio."
    ),
  )

  TaskTemplate.objects.create(
    template=template,
    title="Definir requisitos",
    description=(
      "Recopilar y documentar los requisitos funcionales "
      "y técnicos del proyecto."
    ),
    priority="HIGH",
  )

  TaskTemplate.objects.create(
    template=template,
    title="Diseñar la solución",
    description=(
      "Definir la arquitectura y el diseño general "
      "de la solución."
    ),
    priority="HIGH",
  )

  TaskTemplate.objects.create(
    template=template,
    title="Implementar la solución",
    description=(
      "Desarrollar las funcionalidades previstas "
      "en el proyecto."
    ),
    priority="HIGH",
  )

  TaskTemplate.objects.create(
    template=template,
    title="Realizar pruebas",
    description=(
      "Verificar el funcionamiento de la solución "
      "y corregir los errores encontrados."
    ),
    priority="MEDIUM",
  )

  TaskTemplate.objects.create(
    template=template,
    title="Preparar la puesta en producción",
    description=(
      "Preparar el despliegue y comprobar que el "
      "entorno de producción está correctamente configurado."
    ),
    priority="MEDIUM",
  )

  template = ProjectTemplate.objects.create(
    name="Implantación ISO 27001",
    description=(
      "Plantilla para proyectos de implantación y "
      "preparación de una organización para ISO 27001."
    ),
    perfect_for=(
      "Proyectos de seguridad de la información, "
      "cumplimiento y certificación."
    ),
  )

  TaskTemplate.objects.create(
    template=template,
    title="Analizar el estado actual",
    description=(
      "Evaluar la situación actual de la organización "
      "respecto a los requisitos de ISO 27001."
    ),
    priority="HIGH",
  )

  TaskTemplate.objects.create(
    template=template,
    title="Definir el alcance del SGSI",
    description=(
      "Determinar el alcance del Sistema de Gestión "
      "de Seguridad de la Información."
    ),
    priority="HIGH",
  )

  TaskTemplate.objects.create(
    template=template,
    title="Realizar análisis de riesgos",
    description=(
      "Identificar activos, amenazas, vulnerabilidades "
      "y riesgos de seguridad."
    ),
    priority="HIGH",
  )

  TaskTemplate.objects.create(
    template=template,
    title="Definir controles de seguridad",
    description=(
      "Seleccionar y documentar los controles necesarios "
      "para tratar los riesgos identificados."
    ),
    priority="MEDIUM",
  )

  TaskTemplate.objects.create(
    template=template,
    title="Preparar documentación",
    description=(
      "Preparar las políticas, procedimientos y registros "
      "necesarios para el SGSI."
    ),
    priority="MEDIUM",
  )

  TaskTemplate.objects.create(
    template=template,
    title="Preparar auditoría",
    description=(
      "Revisar el cumplimiento de los requisitos y "
      "preparar la organización para la auditoría."
    ),
    priority="MEDIUM",
  )
