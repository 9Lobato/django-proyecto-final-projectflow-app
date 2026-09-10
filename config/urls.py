# config/urls.py sirve para:
# definir las rutas principales del proyecto Django
# y conectar cada URL con las vistas o rutas de las aplicaciones correspondientes

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
# Imports internos de proyecto/apps
from apps.core.forms import CustomLoginForm


urlpatterns = [
  # API global para React
  path("api/", include("apps.core.urls")),
  # Rutas de la aplicación principal
  path('', include('apps.home.urls')),
  # Inicio de sesión
  path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=CustomLoginForm), name='login'),
  # Cierre de sesión
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  # Rutas de proyectos
  path('projects/', include('apps.projects.urls')),
  # Rutas de tareas
  path('tasks/', include('apps.tasks.urls')),
  # Rutas del tablero Kanban
  path("kanban/", include("apps.kanban.urls")),
  # Rutas de informes
  path("report/", include("apps.reports.urls")),
  # Rutas de gestión administrativa de la aplicación
  path('manage/', include('apps.manage.urls')),
  # Panel de administración de Django
  path('admin/', admin.site.urls),
  # Cambiar idioma
  path("i18n/", include("django.conf.urls.i18n")),
]
