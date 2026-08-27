# apps\reports\management\commands\seed_demo.py sirve para:
# ejecutar en orden la creación de todos los datos necesarios
# para generar una base de datos completa de demostración

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.core.management.base import BaseCommand
# Imports internos de proyecto/apps
from apps.reports.demo.users import create_users
from apps.reports.demo.roles import create_roles
from apps.reports.demo.projects import create_projects
from apps.reports.demo.assignments import create_assignments
from apps.reports.demo.tasks import create_tasks
from apps.reports.demo.comments import create_comments
from apps.reports.demo.snapshots import create_snapshots
from apps.reports.demo.templates import create_templates


# comando de Django que ejecuta la generación completa de datos demo
class Command(BaseCommand):
  help = "Genera una base de datos completa para demostración"

  def handle(self, *args, **options):

    self.stdout.write("Creando usuarios...")
    create_users()

    self.stdout.write("Creando roles...")
    create_roles()

    self.stdout.write("Creando proyectos...")
    create_projects()

    self.stdout.write("Creando asignaciones...")
    create_assignments()

    self.stdout.write("Creando tareas...")
    create_tasks()

    self.stdout.write("Creando templates...")
    create_templates()

    self.stdout.write("Creando comentarios...")
    create_comments()

    self.stdout.write("Creando snapshots...")
    create_snapshots()

    self.stdout.write(self.style.SUCCESS("Base de datos de demostración creada.")
    )
