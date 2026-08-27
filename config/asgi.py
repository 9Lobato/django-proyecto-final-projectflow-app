# config/asgi.py sirve para:
# configurar la entrada ASGI del proyecto Django
# y exponer la aplicación para servidores compatibles con ASGI

# Librerías estándar de Python
import os
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
# Imports internos de proyecto/apps
from django.core.asgi import get_asgi_application

"""
ASGI config for ProjectFlow project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

# Define el módulo de configuración de Django y crea la aplicación ASGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_asgi_application()
