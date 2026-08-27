# apps\reports\urls.py sirve para:
# definir las rutas de la aplicación de informes y asociarlas con sus vistas

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.urls import path
# Imports internos de proyecto/apps
from . import views


urlpatterns = [
  # Mostrar dashboard dashboard de informes
  path("", views.report, name="report"),
  # Exportar el informe en formato PDF
  path("export/pdf/", views.report_export_pdf, name="report_export_pdf"),
  # Exportar el informe en formato Excel
  path("export/xls/", views.report_export_xls, name="report_export_xls"),
]
