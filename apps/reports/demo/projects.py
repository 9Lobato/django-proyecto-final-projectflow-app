# apps\reports\demo\projects.py sirve para:
# definir el catálogo de proyectos de demostración y crear o actualizar dichos proyectos en la base de 
# datos con sus propietarios, fechas, estado de archivado y datos de progreso

# Librerías estándar de Python
from datetime import datetime, time
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction
# Imports internos de proyecto/apps
from apps.projects.models import Project
from apps.reports.demo.catalogs.project_types import WEB, ERP, BI, MOBILE, INFRASTRUCTURE, SECURITY, AUTOMATION


# catálogo de proyectos de demostración
PROJECTS = [
  {
    "code": "23-001",
    "name": "Portal de Clientes",
    "description": "Nuevo portal web para clientes.",
    "owner": "ALopez",
    "type": WEB,
    "created": "2023-09-15",
    "archived": "2024-05-18",
    "last_percentage": 100,
    "last_date": "2024-05-18",
  },
  {
    "code": "23-002",
    "name": "Migración ERP",
    "description": "Migración del ERP corporativo.",
    "owner": "CGarcia",
    "type": ERP,
    "created": "2023-10-02",
    "archived": None,
    "last_percentage": 100,
    "last_date": "2024-11-01",
  },
  {
    "code": "24-001",
    "name": "Dashboard BI",
    "description": "Paneles de negocio para dirección.",
    "owner": "ALopez",
    "type": BI,
    "created": "2024-01-10",
    "archived": None,
    "last_percentage": 100,
    "last_date": "2025-03-01",
  },
  {
    "code": "24-002",
    "name": "Web Corporativa",
    "description": "Rediseño de la web corporativa.",
    "owner": "CGarcia",
    "type": WEB,
    "created": "2024-05-01",
    "archived": "2025-05-18",
    "last_percentage": 100,
    "last_date": "2025-05-18",
  },
  {
    "code": "24-003",
    "name": "Aplicación Android",
    "description": "Aplicación móvil para clientes.",
    "owner": "ALopez",
    "type": MOBILE,
    "created": "2024-10-15",
    "archived": None,
    "last_percentage": 100,
    "last_date": "2025-08-01",
  },
  {
    "code": "25-001",
    "name": "Aplicación iOS",
    "description": "Versión iOS de la aplicación móvil.",
    "owner": "CGarcia",
    "type": MOBILE,
    "created": "2025-02-05",
    "archived": "2026-01-10",
    "last_percentage": 100,
    "last_date": "2026-01-10",
  },
  {
    "code": "25-002",
    "name": "CRM Comercial",
    "description": "Nuevo CRM para el departamento comercial.",
    "owner": "ALopez",
    "type": ERP,
    "created": "2025-04-18",
    "archived": None,
    "last_percentage": 100,
    "last_date": "2026-01-01",
  },
  {
    "code": "25-003",
    "name": "ISO 27001",
    "description": "Adecuación de procesos de seguridad.",
    "owner": "CGarcia",
    "type": SECURITY,
    "created": "2025-09-12",
    "archived": None,
    "last_percentage": 50,
    "last_date": "2026-08-01",
  },
  {
    "code": "26-001",
    "name": "Integración SAP",
    "description": "Integración con SAP mediante API.",
    "owner": "ALopez",
    "type": INFRASTRUCTURE,
    "created": "2026-01-28",
    "archived": "2026-08-01",
    "last_percentage": 100,
    "last_date": "2026-08-01",
  },
  {
    "code": "26-002",
    "name": "Gestión de Inventario",
    "description": "Sistema de inventario y logística.",
    "owner": "CGarcia",
    "type": INFRASTRUCTURE,
    "created": "2026-04-08",
    "archived": None,
    "last_percentage": 25,
    "last_date": "2026-08-01",
  },
  {
    "code": "26-003",
    "name": "Portal RRHH",
    "description": "Portal interno para empleados.",
    "owner": "ALopez",
    "type": WEB,
    "created": "2026-06-06",
    "archived": None,
    "last_percentage": 17,
    "last_date": "2026-08-01",
  },
  {
    "code": "26-004",
    "name": "Automatización Facturación",
    "description": "Automatización de procesos contables.",
    "owner": "CGarcia",
    "type": AUTOMATION,
    "created": "2026-06-20",
    "archived": None,
    "last_percentage": 0,
    "last_date": "2026-08-01",
  },
]

# crea o actualiza los proyectos de demostración en la base de datos utilizando los datos
# definidos en el catálogo de proyectos de demostración
@transaction.atomic
def create_projects():

  owners = {
    user.username: user
    for user in User.objects.all()
  }

  for data in PROJECTS:

    owner = owners.get(data["owner"])

    if not owner:
      raise Exception(f'No existe el usuario {data["owner"]}')

    project, _ = Project.objects.update_or_create(
      code=data["code"],
      defaults={
        "name": data["name"],
        "description": data["description"],
        "owner": owner,
      },
    )

    created_date = datetime.strptime(
      data["created"],
      "%Y-%m-%d",
    ).date()

    project.created_at = timezone.make_aware(
      datetime.combine(
        created_date,
        time(9, 30),
      )
    )

    if data["archived"]:

      archived_datetime = timezone.make_aware(
        datetime.combine(
          datetime.strptime(
            data["archived"],
            "%Y-%m-%d"
          ).date(),
          time(17, 30)
        )
      )

      project.is_archived = True
      project.archived_at = archived_datetime
      project.updated_at = archived_datetime

    else:

      project.is_archived = False
      project.archived_at = None

    project.save(
      update_fields=[
        "created_at",
        "updated_at",
        "is_archived",
        "archived_at",
      ]
    )
