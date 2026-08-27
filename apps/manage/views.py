# apps\manage\views.py sirve para:
# gestionar las vistas de administración de usuarios, roles, equipos de proyectos y plantillas
# y controlar las acciones permitidas según el usuario y el estado del proyecto

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
# Imports internos de proyecto/apps
from apps.core.utils.navigation import get_previous_next
from apps.manage.forms import ProjectTemplateForm, TaskTemplateFormSet, UserEditForm
from apps.projects.models import Assignment, Project, ProjectFollow, ProjectTemplate, Role
from apps.projects.permissions import get_user_role


# lista usuarios
@login_required
def manage(request):

  users = User.objects.all().order_by("username")

  for user in users:

    user.can_delete = (
      not user.project_assignments.exists()
      and not user.is_superuser
      and user != request.user
    )

  roles = Role.objects.all().order_by("name")

  role_counts = {
    "OWNER": Role.objects.get(name="OWNER").assignment_set.count(),
    "MANAGER": Role.objects.get(name="MANAGER").assignment_set.count(),
    "MEMBER": Role.objects.get(name="MEMBER").assignment_set.count(),
  }

  return render(request, "manage/manage.html", {
    "users": users,
    "roles": roles,
    "role_counts": role_counts})


# edita usuarios
@login_required
def user_update(request, pk):

  user = get_object_or_404(User, pk=pk)

  users = User.objects.order_by("username")

  previous_user, next_user = get_previous_next(users, user)

  if request.method == "POST":
    form = UserEditForm(request.POST, instance=user)

    if form.is_valid():
      user = form.save()

      if "apply" in request.POST:
        return redirect("user_update", pk=user.pk)

      return redirect("manage")

  else:
    form = UserEditForm(instance=user)

  return render(
    request,
    "manage/user_form.html",
    {
      "form": form,
      "mode": "edit",
      "previous_user": previous_user,
      "next_user": next_user,
    },
  )


# crea usuarios
@login_required
def user_create(request):

  if request.method == "POST":
    form = UserEditForm(request.POST)

    if form.is_valid():
      user = form.save()

      if "apply" in request.POST:
        return redirect("user_update", pk=user.pk)

      return redirect("manage")

  else:
    form = UserEditForm()

  return render(
    request,
    "manage/user_form.html",
    {
      "form": form,
      "mode": "create",
      "previous_user": None,
      "next_user": None,
    },
  )


# elimina usuarios
@login_required
def user_delete(request, pk):

  user = get_object_or_404(User, pk=pk)

  blocked = False
  reason = None

  if user == request.user:
    blocked = True
    reason = "es tu propio usuario."

  elif user.is_superuser:
    blocked = True
    reason = "los superusuarios están protegidos."

  elif user.project_assignments.exists():
    blocked = True
    reason = "tiene proyectos o tareas asignadas."

  if blocked:
    return render(request, "common/confirm_delete.html", {
      "type": "usuario",
      "name": user.username,
      "gender": "el",
      "blocked": True,
      "reason": reason,
    })

  if request.method == "POST":
    user.delete()
    return redirect("manage")

  return render(request, "common/confirm_delete.html", {
    "type": "usuario",
    "name": user.username,
    "gender": "el",
    "blocked": False,
  })


# activa o desactiva a un usuario
@login_required
def user_toggle_active(request, pk):

  user = get_object_or_404(User, pk=pk)

  if user == request.user:
    return redirect("manage")

  user.is_active = not user.is_active
  user.save()

  return redirect("manage")


# Mostrar los usuarios asociados a un determinado rol
@login_required
def role_detail(request, role_name):

  roles = Role.objects.order_by("name")

  current_role = get_object_or_404(Role, name=role_name.upper())

  previous_role, next_role = get_previous_next(
    roles,
    current_role,
  )

  assignments = (
    Assignment.objects
    .select_related("user", "project", "role")
    .filter(role__name=role_name.upper())
    .order_by(
      "user__username",
      "-project__code",
    )
  )

  users_with_projects = []

  for assignment in assignments:
    user = assignment.user
    existing_user = next(
      (
        item
        for item in users_with_projects
        if item["user"].pk == user.pk
      ),
      None,
    )

    if existing_user is None:
      users_with_projects.append({
        "user": user,
        "projects": [
          assignment.project
        ],
      })
    else:
      existing_user["projects"].append(
        assignment.project
      )

  return render(
    request,
    "manage/role_detail.html",
    {
      "role_name": role_name.upper(),
      "users_with_projects": users_with_projects,
      "previous_role": previous_role,
      "next_role": next_role,
    }
  )


# muestra los usuarios que forman parte del equipo de un proyecto
@login_required
def project_team(request, pk):

  projects = Project.objects.order_by("code")

  project = get_object_or_404(projects, pk=pk)

  previous_project, next_project = get_previous_next(projects, project)

  assignments = (
    Assignment.objects
    .filter(project=project)
    .select_related("user", "role")
    .order_by("role__name", "user__username")
  )

  role = get_user_role(request.user, project)

  is_followed = ProjectFollow.objects.filter(
    project=project,
    user=request.user,
  ).exists()

  can_manage_team = (
    role in ["OWNER", "MANAGER"]
    and not project.is_archived
    and not is_followed
  )

  return render(
    request,
    "manage/project_team.html",
    {
      "project": project,
      "assignments": assignments,
      "previous_project": previous_project,
      "next_project": next_project,
      "role": role,
      "can_manage_team": can_manage_team,
      "from_report": request.GET.get("from") == "report",
    }
  )


# añade un usuario al equipo de un proyecto con un rol determinado
@login_required
def team_include(request, pk):

  project = get_object_or_404(Project, pk=pk)

  role = get_user_role(request.user, project)

  is_followed = ProjectFollow.objects.filter(
    project=project,
    user=request.user,
  ).exists()

  if role not in ["OWNER", "MANAGER"] or project.is_archived or is_followed:
    return render(request, "common/403.html", status=403)

  if role == "OWNER":
    roles = Role.objects.all().order_by("name")
  else:
    roles = Role.objects.filter(name="MEMBER")

  assigned_users = Assignment.objects.filter(
    project=project
  ).values_list("user_id", flat=True)

  available_users = User.objects.exclude(
    id__in=assigned_users
  ).order_by("username")

  if request.method == "POST":

    user_id = request.POST.get("user")
    role_name = request.POST.get("role")

    if role == "MANAGER" and role_name != "MEMBER":
      return render(request, "common/403.html", status=403)

    user = get_object_or_404(User, pk=user_id)
    role_obj = get_object_or_404(Role, name=role_name)

    Assignment.objects.create(
      user=user,
      project=project,
      role=role_obj,
    )

    return redirect("project_team", pk=project.pk)

  return render(
    request,
    "manage/team_include.html",
    {
      "project": project,
      "users": available_users,
      "roles": roles,
    },
  )


# muestra las plantillas de proyectos disponibles
@login_required
def templates(request):

  templates = (
    ProjectTemplate.objects
    .annotate(
      projects_count=Count("projects"),
      tasks_count=Count("tasks"),
    )
    .order_by(
      "-projects_count",
      "-generated_from",
    )
  )

  return render(
    request,
    "manage/templates.html",
    {
      "templates": templates,
    },
  )


# elimina un usuario del equipo de un proyecto
@login_required
def team_exclude(request, pk, user_id):

  project = get_object_or_404(Project, pk=pk)

  role = get_user_role(request.user, project)

  is_followed = ProjectFollow.objects.filter(
    project=project,
    user=request.user,
  ).exists()

  if role not in ["OWNER", "MANAGER"] or project.is_archived or is_followed:
    return render(request, "common/403.html", status=403)

  assignment = get_object_or_404(
    Assignment,
    project=project,
    user_id=user_id,
  )

  if request.method == "POST":

    assignment.delete()

    return redirect("project_team", pk=project.pk)

  return render(
    request,
    "common/confirm_delete.html",
    {
      "type": "miembro del equipo",
      "name": assignment.user.username,
      "gender": "el",
    },
  )


# crea una nueva plantilla de proyecto y sus tareas
@login_required
def template_create(request):

  if request.method == "POST":

    form = ProjectTemplateForm(request.POST)
    formset = TaskTemplateFormSet(request.POST)

    if form.is_valid() and formset.is_valid():

      template = form.save()

      formset.instance = template
      formset.save()

      if "apply" in request.POST:
        return redirect(
          "template_update",
          pk=template.pk)

      return redirect("templates")

  else:

    form = ProjectTemplateForm()

    formset = TaskTemplateFormSet()

  return render(request, "manage/template_form.html", {
      "form": form,
      "formset": formset,
      "mode": "create",
      "template_obj": None,
      "previous_template": None,
      "next_template": None,
    },
  )


# edita una plantilla de proyecto y sus tareas
@login_required
def template_update(request, pk):

  template = get_object_or_404(
    ProjectTemplate,
    pk=pk,
  )

  templates = ProjectTemplate.objects.order_by("name")

  previous_template, next_template = get_previous_next(
    templates,
    template,
  )
  
  form = ProjectTemplateForm(instance=template)
  formset = TaskTemplateFormSet(instance=template, queryset=template.tasks.order_by("-id"))

  if request.method == "POST":

    form = ProjectTemplateForm(request.POST, instance=template)
    formset = TaskTemplateFormSet(request.POST, instance=template, queryset=template.tasks.order_by("-id"))

    if form.is_valid() and formset.is_valid():

      form.save()
      formset.save()

      if "apply" in request.POST:
        return redirect("template_update", pk=template.pk)

      return redirect("templates")

  return render(request, "manage/template_form.html", {
    "form": form,
    "formset": formset,
    "mode": "edit",
    "template_obj": template,
    "previous_template": previous_template,
    "next_template": next_template,
  })


# elimina una plantilla de proyecto
@login_required
def template_delete(request, pk):

  template = get_object_or_404(ProjectTemplate, pk=pk)

  if template.projects.exists():
    return render(request, "common/confirm_delete.html", {
      "type": "plantilla",
      "name": template.name,
      "gender": "la",
      "blocked": True,
      "reason": "está siendo usada en algún proyecto."
    })

  if request.method == "POST":
    template.delete()
    return redirect("templates")

  return render(request, "common/confirm_delete.html", {
    "type": "plantilla",
    "name": template.name,
    "gender": "la",
    "blocked": False,
  })
