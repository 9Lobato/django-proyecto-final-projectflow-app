# apps\projects\views.py sirve para:
# gestionar las vistas relacionadas con proyectos
# controlar el acceso de los usuarios a los proyectos
# y gestionar acciones como crear, editar, eliminar, archivar y seguir proyectos

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import IntegerField
from django.db.models.functions import Cast, Substr
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
# Imports internos de proyecto/apps
from apps.core.utils.navigation import get_previous_next
from apps.projects.permissions import get_user_role, user_can_archive_project, user_can_change_owner, user_can_create_project, user_can_delete_project, user_can_edit_project, user_can_view_project
from apps.projects.querysets import get_projects_queryset
from apps.projects.to_template import to_template
from apps.projects.utils import prepare_project_for_user
from apps.tasks.models import Task
from .forms import ProjectForm
from .models import Project, ProjectFollow, ProjectTemplate


# muestra los proyectos disponibles para el usuario
@login_required
def project_list(request):

  projects = get_projects_queryset()

  user = request.user
  is_owner = user.is_superuser
  is_manager = user.is_staff and not user.is_superuser

  my_projects = []
  external_projects = []

  for p in projects:

    prepare_project_for_user(p, user)

    if is_owner:
      my_projects.append(p)

    elif is_manager:

      if p.is_assigned or p.is_followed:
        my_projects.append(p)
      else:
        external_projects.append(p)

    else:
      if p.is_assigned:
        my_projects.append(p)

  sections = [
    ("Mis proyectos", my_projects),
  ]

  if is_manager:
    sections.append(
      ("Disponible a seguir", external_projects)
    )

  return render(request, "projects/project_list.html", {
    "sections": sections,
    "can_create_project": user_can_create_project(user),
  })


# muestra y procesa el formulario de edición de un proyecto
@login_required
def project_update(request, pk):

  project = get_projects_queryset().get(pk=pk)

  user = request.user

  is_manager = (
      user.is_staff and
      not user.is_superuser)

  is_assigned = project.assignments.filter(user=user).exists()

  is_followed = ProjectFollow.objects.filter(
      user=user,
      project=project
  ).exists()

  has_access = user_can_view_project(user, project)

  readonly = (
      project.is_archived
      or (is_manager and not (is_assigned or is_followed))
  )
  
  user_role = get_user_role(request.user, project)
  can_change_owner = user_can_change_owner(request.user, project)
  can_edit = (
    user_can_edit_project(user, project)
    and not readonly
  )

  def apply_role_restrictions(form, user_role, readonly=False):

    if readonly:
      for field in form.fields.values():
        field.disabled = True
      return

    form.fields["template"].disabled = True

    if user_role == "MEMBER":

      form.fields["code"].disabled = True
      form.fields["name"].disabled = True
      form.fields["description"].disabled = True

    elif user_role == "MANAGER":

      form.fields["code"].disabled = True
      form.fields["name"].disabled = True

  owners = User.objects.filter(
    project_assignments__project=project,
    project_assignments__role__name="OWNER"
  ).distinct()

  if request.method == "POST" and "clear" in request.POST:
    return redirect(f'{reverse("project_create")}?year={project.code[:2]}')
  
  if request.method == "POST":

    form = ProjectForm(request.POST, instance=project)
    apply_role_restrictions(form, user_role, readonly=readonly)

    if form.is_valid():

      project = form.save()

      owner_id = request.POST.get("owner")

      if owner_id and can_change_owner:
        try:
          new_owner = User.objects.get(pk=owner_id)
          project.owner = new_owner
          project.save()
        except User.DoesNotExist:
          pass

      next_url = request.POST.get("next")

      if not next_url or next_url == "None":
        next_url = None

      if "save" in request.POST:
        return redirect(next_url) if next_url else redirect("project_list")

      return redirect("project_update", pk=project.pk)
    
  else:

    form = ProjectForm(
      instance=project,
      initial={"template": project.template}
    )

    apply_role_restrictions(
      form,
      user_role,
      readonly=readonly
    )
  
  next_url = request.GET.get("next")

  if not next_url or next_url == "None":
    next_url = None

  year = project.code[:2]
  
  projects = [
    p for p in get_projects_queryset().filter(code__startswith=year)
    if user_can_view_project(request.user, p)]

  previous_project, next_project = get_previous_next(projects, project)

  return render(request, "projects/project_form.html", {
    "form": form,
    "project": project,
    "mode": "edit",
    "next": next_url,
    "project_list_url": reverse("project_list"),
    "previous_project": previous_project,
    "next_project": next_project,
    "can_edit": can_edit,
    "readonly": readonly,
    "can_change_owner": can_change_owner,
    "user_role": user_role,
    "templates": ProjectTemplate.objects.all(),
    "owners": owners,})


# crea un nuevo proyecto a partir del formulario
@login_required
def project_create(request):

  user = request.user

  if not user_can_create_project(user):
    return render(request, "common/403.html", status=403)

  if request.method == "POST":

    form = ProjectForm(request.POST)

    if form.is_valid():

      project = form.save(commit=False)
      project.owner = user

      template = form.cleaned_data.get("template")

      if template:

        project.template = template

      project.save()

      if template:

        for t in template.tasks.all():

          Task.objects.create(
            project=project,
            title=t.title,
            description=t.description,
            priority=t.priority,
            created_by=request.user,
          )

      next_url = request.POST.get("next")

      if "save" in request.POST:
        return redirect(next_url) if next_url else redirect("project_list")

      return redirect("project_update", pk=project.pk)

  else:

    year = request.GET.get("year")
    
    if not year:
    
      year = timezone.now().strftime("%y")

    last_project = Project.objects.filter(
      code__startswith=year
    ).annotate(
      num=Cast(Substr("code", 4, 3), IntegerField())
    ).order_by("-num").first()

    if last_project:
      new_number = last_project.num + 1
    else:
      new_number = 1

    form = ProjectForm(initial={
      "code": f'{year}-{new_number:03d}'
    })

  return render(request, "projects/project_form.html", {
    "form": form,
    "mode": "create",
    "project_list_url": reverse("project_list"),
    "project": None,
    "previous_project": None,
    "next_project": None,
    "user_role": "OWNER",
    "templates": ProjectTemplate.objects.all(),})


# elimina un proyecto si el usuario tiene permiso
@login_required
def project_delete(request, pk):

  project = get_object_or_404(Project, pk=pk)

  # Bloqueo por permisos
  if not user_can_delete_project(request.user, project):

    return render(request, "common/403.html", status=403)
  
  next_url = request.GET.get("next")

  if request.method == "POST":

    project.delete()

    return redirect(next_url) if next_url else redirect("project_list")

  return render(request, "common/confirm_delete.html", {
    "type": "proyecto",
    "name": project.name,
    "project": project,
    "gender": "el",})


# convierte un proyecto existente en una plantilla
@login_required
def project_to_template(request, pk):

  project = get_object_or_404(Project, pk=pk)

  to_template(project)

  return redirect("project_update", pk=project.pk)


# archiva o desarchiva un proyecto
@login_required
def project_archive_toggle(request, pk):

  project = get_object_or_404(Project, pk=pk)

  if not user_can_archive_project(request.user, project):
    return render(request, "common/403.html", status=403)
  
  if project.is_archived:
    project.unarchive()
  else:
    project.archive()

  return redirect(request.META.get("HTTP_REFERER", "project_list"))


# comprueba si un usuario sigue un proyecto
def is_following_project(user, project):
  return ProjectFollow.objects.filter(
    user=user,
    project=project
  ).exists()


# permite seguir o dejar de seguir un proyecto
@login_required
def project_follow_toggle(request, pk):

  project = get_object_or_404(Project, pk=pk)

  if not (request.user.is_staff and not request.user.is_superuser):
    return redirect("project_list")

  follow = ProjectFollow.objects.filter(
    user=request.user,
    project=project
  ).first()

  if follow:
    follow.delete()
  else:
    ProjectFollow.objects.create(
      user=request.user,
      project=project
    )

  return redirect(request.META.get("HTTP_REFERER", "project_list"))
