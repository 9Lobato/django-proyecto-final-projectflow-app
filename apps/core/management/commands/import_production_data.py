# apps\core\management\import_production_data.py sirve para:
# importar importar los datos iniciales de ProjectFlow en el entorno de producción.

# Librerías estándar de Python
from pathlib import Path
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
# Imports internos de proyecto/apps


class Command(BaseCommand):
  help = "Importa los datos locales de ProjectFlow en producción."

  def handle(self, *args, **options):
    User = get_user_model()

    # Si los datos ya fueron importados, no hacemos nada.
    if User.objects.filter(username="SLobato").exists():
      self.stdout.write(
        "Los datos de producción ya están importados."
      )
      return

    fixture = Path("production_data.json")

    if not fixture.exists():
      self.stdout.write(
        self.style.ERROR(
          "No se encontró production_data.json"
        )
      )
      return

    # Elimina el superusuario temporal creado en Render.
    User.objects.exclude(username="SLobato").filter(
      is_superuser=True
    ).delete()

    self.stdout.write(
      "Superusuarios temporales eliminados."
    )

    call_command(
      "loaddata",
      str(fixture),
      verbosity=1,
    )

    self.stdout.write(
      self.style.SUCCESS(
        "Datos de producción importados correctamente."
      )
    )
