# apps\home\views.py sirve para:
# gestionar las vistas principales de la aplicación home
# y determinar qué contenido o página inicial debe mostrar cada usuario

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
# Imports internos de proyecto/apps
from apps.home.services.dashboard import get_dashboard_context
from apps.projects.models import Assignment


# muestra el dashboard principal del usuario
@login_required
def home(request):
  context = get_dashboard_context(request.user)
  return render(request, "home/home.html", context)

# determina la página inicial del usuario según su rol
@login_required
def start(request):

  if request.user.is_superuser:
    selected_role = "OWNER"
  else:
    assignment = (
      Assignment.objects
      .filter(user=request.user)
      .select_related("role")
      .order_by("role__name")
      .first()
    )

    if assignment:
      selected_role = assignment.role.name
    else:
      selected_role = "MEMBER"


  if selected_role == "OWNER":
    start_url = reverse("manage")
  elif selected_role == "MANAGER":
    start_url = reverse("project_list")
  else:
    start_url = reverse("home")


  return render(request, "home/start.html", {
    "selected_role": selected_role,
    "start_url": start_url,
  })
