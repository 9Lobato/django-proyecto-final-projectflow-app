# apps\reports\demo\catalogs\comments_catalog.py sirve para:
# definir el catálogo de comentarios y solicitudes de demostración asociados a cada tipo de proyecto,
# incluyendo autor, fecha, tarea, tipo de comentario, solicitud, menciones y resolución

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
# Imports internos de proyecto/apps
from .comment_types import COMMENT, REQUEST
from .project_roles import OWNER, MANAGER, MEMBER
from .project_types import WEB, ERP, BI, MOBILE, INFRASTRUCTURE, SECURITY, AUTOMATION
from .request_kinds import IMMEDIATE, SCHEDULED, ROUTINE, MITIGATION, IMPROVEMENT, OPTIONAL, DELEGATED


# catálogo de comentarios y solicitudes por tipo de proyecto
COMMENTS_CATALOG = {
  WEB: [
    {
      "day": 45,
      "task": "Implementación Login",
      "task_order": 6,
      "author_role": MEMBER,
      "type": COMMENT,
      "text": "Backend terminado.",
    },
    {
      "day": 47,
      "task": "Implementación Login",
      "task_order": 6,
      "author_role": MANAGER,
      "type": COMMENT,
      "text": "Revisa el control de sesiones.",
    },
    {
      "day": 50,
      "task": "Implementación Login",
      "task_order": 6,
      "author_role": OWNER,
      "type": REQUEST,
      "request_kind": IMPROVEMENT,
      "mentions_role": MEMBER,
      "text": "Por favor revisa la autenticación.",
    },
    {
      "day": 60,
      "task": "Implementación Login",
      "task_order": 6,
      "author_role": OWNER,
      "type": REQUEST,
      "request_kind": OPTIONAL,
      "mentions_role": MEMBER,
      "text": "Añade documentación del login.",
      "resolved": True,
      "resolved_days_after": 5,
    },
  ],
  ERP: [
    # Pendiente
  ],
  BI: [
    # Pendiente
  ],
  MOBILE: [
    # Pendiente
  ],
  INFRASTRUCTURE: [
    # Pendiente
  ],
  SECURITY: [
    # Pendiente
  ],
  AUTOMATION: [
    # Pendiente
  ],
}
