# apps\reports\services\pdf.py sirve para:
# generar los informes PDF a partir de plantillas HTML

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.template.loader import render_to_string
# Imports internos de proyecto/apps
from .dashboard import build_report_dashboard
from .metrics import project_summary, user_summary


# HELPER PRIVADO: renderiza una plantilla HTML con el contexto recibido
def _render_pdf(template, context):

  html = render_to_string(template, context)

  return html


# INFORME DASHBOARD: genera el contenido HTML del informe general
def build_dashboard_pdf():

  context = build_report_dashboard()

  return _render_pdf("reports/dashboard.html", context)


# INFORME PROYECTO: genera el contenido HTML del informe de un proyecto
def build_project_pdf(project):

  context = project_summary(project)

  return _render_pdf("reports/project.html", context)


# INFORME USUARIO: genera el contenido HTML del informe de un usuario
def build_user_pdf(user):

  context = user_summary(user)

  return _render_pdf("reports/user.html", context)
