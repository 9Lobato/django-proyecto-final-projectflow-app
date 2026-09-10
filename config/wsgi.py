# config/wsgi.py sirve para:
# configurar la entrada WSGI del proyecto Django
# y exponer la aplicación para servidores compatibles con WSGI

# Librerías estándar de Python
import os
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
# Imports internos de proyecto/apps
from django.core.wsgi import get_wsgi_application


"""
WSGI config for ProjectFlow project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

# Define el módulo de configuración de Django y crea la aplicación WSGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
