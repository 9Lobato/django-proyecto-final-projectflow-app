# apps\reports\views.py sirve para:
# gestionar las vistas de informes y preparar los datos para su visualización y exportación

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# Imports internos de proyecto/apps
from apps.reports.services.dashboard import build_report_dashboard
from apps.reports.services.export import export_pdf, export_xls


# VISTA DE INFORMES: muestra el dashboard de informes
@login_required
def report(request):

  context = build_report_dashboard()

  context["report_data"] = {
    "status_labels": context["status_labels"],
    "status_data": context["status_data"],
    "months": context["months"],
    "projects_month": context["projects_month"],
    "archived_months": context["archived_months"],
    "projects_archived_month": context["projects_archived_month"],
    "user_labels": context["user_labels"],
    "user_tasks": context["user_tasks"],
    "participation_labels": context["participation_labels"],
    "participation_data": context["participation_data"],
    "productivity_labels": context["productivity_labels"],
    "productivity_data": context["productivity_data"],
    "delivery_labels": context["delivery_labels"],
    "delivery_data": context["delivery_data"],
    "priority_labels": context["priority_labels"],
    "priority_data": context["priority_data"],
    "progress_labels": context["progress_labels"],
    "progress_datasets": context["progress_datasets"],
    "projects_created_codes": context["projects_created_codes"],
    "projects_archived_codes": context["projects_archived_codes"],
  }

  return render(request, "reports/report.html", context)


# VISTA DE EXPORTACIÓN: devuelve el informe en formato PDF
@login_required
def report_export_pdf(request):

  return export_pdf()


# VISTA DE EXPORTACIÓN: devuelve el informe en formato Excel
@login_required
def report_export_xls(request):

  return export_xls()
