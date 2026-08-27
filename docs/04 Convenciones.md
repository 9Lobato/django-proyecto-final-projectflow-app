# 04. Convenciones de ProjectFlow

## 1. Introducción

Este documento define las convenciones utilizadas en ProjectFlow para mantener un código:

- consistente;
- legible;
- mantenible;
- modular;
- fácil de ampliar.

Las convenciones se aplican principalmente a:

- Python;
- Django;
- HTML;
- CSS;
- JavaScript;
- documentación.

El objetivo no es imponer reglas innecesarias, sino mantener una estructura coherente a medida que el proyecto crece.

Estas convenciones deben utilizarse como guía durante el desarrollo y mantenimiento del proyecto.

Cuando una situación concreta no esté contemplada en este documento, se debe priorizar:

1. la claridad del código;
2. la coherencia con el código existente;
3. la separación de responsabilidades;
4. la reutilización;
5. la facilidad de mantenimiento.

## 2. Estructura de archivos

Las funcionalidades deben colocarse en la aplicación Django que corresponda a su responsabilidad.

Actualmente ProjectFlow está dividido principalmente en:

apps/
├── accounts/ # Gestiona los elementos relacionados con usuarios y cuentas.
├── core/     # Contiene funcionalidades compartidas por diferentes partes de la aplicación.
├── home/     # Gestiona la página inicial y el dashboard.
├── kanban/   # Gestiona el tablero Kanban.
├── manage/   # Gestiona las funcionalidades administrativas propias de ProjectFlow.
├── projects/ # Gestiona proyectos, plantillas, asignaciones, seguidores y permisos relacionados con proyectos.
├── reports/  # Gestiona informes, métricas, estadísticas y funcionalidades relacionadas con reporting.
└── tasks/    # Gestiona tareas y funcionalidades relacionadas con ellas.

Cada aplicación representa una responsabilidad funcional concreta.

La estructura general del proyecto se divide principalmente en:

ProjectFlow/
├── apps/             # ?
├── config/           # Configuración principal del proyecto Django
├── docs/             # ?
├── env/              # ?
├── locale/           # Archivos de internacionalización
├── static/           # Archivos CSS, JavaScript e imágenes
├── templates/        # Plantillas HTML
├── db.sqlite3        # Base de datos
├── manage.py         # ?
└── requirements.txt  # Paquetes necesarios para el funcionamiento de la aplicación.

## 3. Convenciones de nombres

ProjectFlow utiliza nombres descriptivos y consistentes para facilitar la lectura del código y localizar rápidamente cada componente.

## 3.1. Python

Los archivos Python utilizan nombres en minúsculas y, cuando contienen varias palabras, se separan mediante guion bajo (`snake_case`).

Ejemplos:

views.py
models.py
querysets.py
context_processors.py
project_progress_service.py
seed_demo.py

Las funciones también utilizan snake_case y deben describir claramente la acción que realizan..

Ejemplos:

get_dashboard_context()
get_projects_queryset()
user_can_edit_project()
get_project_access_mode()

Las clases utilizan PascalCase.

Ejemplos:

Project
ProjectTemplate
Assignment
CustomLoginForm

Las constantes utilizan normalmente letras mayúsculas y guiones bajos.

Ejemplo:

ROLE_PERMISSIONS = {...}

## 3.2. Django

Las aplicaciones Django utilizan nombres en minúsculas y descriptivos:

accounts
core
home
kanban
manage
projects
reports
tasks

Los modelos utilizan PascalCase y nombres en singular:

Project
Task
Assignment
ProjectTemplate
ProjectFollow

Las funciones de las vistas utilizan snake_case:

def home(request):
def start(request):

Los nombres de las URLs (name) utilizan snake_case y deben ser descriptivos.

Ejemplos:

name="project_list"
name="task_list"
name="set_language"

Cuando una URL pertenece claramente a una entidad o funcionalidad concreta, se mantiene una nomenclatura coherente con el resto de la aplicación.

## 3.3. HTML y plantillas Django

Los archivos HTML utilizan nombres en minúsculas y snake_case cuando es necesario separar palabras.

Ejemplos:

home.html
project_list.html
project_form.html
task_list.html
task_form.html
project_team.html
role_detail.html

Los fragmentos reutilizables utilizan normalmente un nombre descriptivo y pueden comenzar por _.

Ejemplos:

{{ dashboard_projects }}
{{ notification_projects }}
{{ templates }}
{{ workflow_steps }}

Los bloques de plantilla deben utilizar nombres claros y coherentes:

{% block content %}
{% endblock %}

## 3.4. CSS

Los archivos CSS utilizan nombres en minúsculas y snake_case o nombres descriptivos coherentes con la funcionalidad.

Ejemplos:

tables.css
workflow.css
text.css
kanban.css
project_list.css
template_form.css
report.css
task_list.css

Las clases CSS deben describir la función o el componente al que pertenecen.

Ejemplos:

class="workflow-arrow"
class="workflow-panel"
class="navbar-brand"

Se debe evitar utilizar nombres excesivamente genéricos cuando puedan provocar conflictos con otros componentes.

## 3.5. JavaScript

Los archivos JavaScript utilizan nombres en minúsculas y, cuando es necesario, palabras separadas mediante guion bajo.

Ejemplos:

workflow.js
form_changes.js
template_selector.js
project_list.js
kanban_layout.js
task_form.js

Las funciones utilizan camelCase.

Ejemplos:

updateWorkflow()
handleProjectChange()
loadTasks()

Las variables también utilizan camelCase:

projectId
taskList
workflowSteps
currentIndex

Las constantes pueden utilizar UPPER_SNAKE_CASE cuando representan valores que no deberían modificarse:

const MAX_ITEMS = 10;

## 3.6. Variables y parámetros

Los nombres deben describir qué representa el dato.

Se deben evitar nombres excesivamente genéricos como:

x
data
obj
value
thing

cuando existe una alternativa más descriptiva.

Es preferible:

project
task
user
assignment
notification
project_queryset

En funciones, los parámetros deben mantener una nomenclatura coherente:

def get_user_role(user, project):
def user_can_edit_project(user, project):
def user_can_edit_task(user, task):

## 3.7. Permisos y roles

Los roles utilizan nombres en mayúsculas:

OWNER
MANAGER
MEMBER

Los identificadores de permisos utilizan snake_case y siguen el patrón:

acción_entidad

Ejemplos:

view_project
create_project
edit_project
delete_project
archive_project
manage_users
change_owner

view_task
create_task
edit_task
delete_task
assign_task

Esta nomenclatura permite identificar rápidamente qué acción controla cada permiso.

## 3.8. Estados

Los estados internos utilizados por la aplicación deben utilizar identificadores consistentes.

Cuando representan valores internos del sistema, se recomienda utilizar mayúsculas.

Ejemplos:

DONE
OWNER
MANAGER
MEMBER
EDIT
READONLY
DENY

El texto mostrado al usuario puede ser diferente del identificador interno.

Por ejemplo:

DONE → Completada
READONLY → Solo lectura
DENY → Sin acceso

De esta forma se separa la lógica interna de la presentación de la interfaz.

## 3.9. Nombres de consultas y servicios

Las funciones que obtienen datos suelen comenzar por get_.

Ejemplos:

get_dashboard_context()
get_projects_queryset()
get_user_inbox()
get_project_access_mode()
get_task_access_mode()

Las funciones que comprueban permisos o condiciones utilizan nombres que expresan claramente la condición.

Ejemplos:

has_permission()
user_can_view_project()
user_can_create_project()
user_can_edit_task()

Las funciones deben evitar nombres ambiguos como:

check()
process()
handle()
do_action()

salvo que el contexto haga que su significado sea completamente evidente.

## 3.10. Nombres de documentación

Los documentos del proyecto utilizan numeración para mantener un orden lógico.

Ejemplo:

docs/
├── 01 Manual_funcional.md
├── 02 Permisos.md
├── 03 Arquitectura.md
└── 04 Convenciones.md

Los nombres de los documentos deben describir claramente su contenido.

La numeración permite identificar rápidamente el propósito de cada documento y mantener un orden coherente dentro de la documentación del proyecto.

## 4. Convenciones de Django

ProjectFlow sigue una estructura basada en las convenciones habituales de Django, procurando mantener separadas las responsabilidades de las vistas, modelos, consultas, formularios, servicios y plantillas.

El objetivo es evitar que una única parte de la aplicación concentre demasiada lógica y facilitar el mantenimiento del proyecto.

## 4.1. Aplicaciones Django

Cada aplicación debe representar una funcionalidad o área de responsabilidad concreta.

En ProjectFlow se utilizan principalmente:

accounts/
core/
home/
kanban/
manage/
projects/
reports/
tasks/

La lógica debe colocarse en la aplicación que sea responsable de ella.

Por ejemplo:

projects/
  models.py
  views.py
  forms.py
  permissions.py
  querysets.py

La lógica relacionada con proyectos debe permanecer principalmente dentro de projects.

La lógica relacionada con tareas debe permanecer principalmente dentro de tasks.

Esto evita crear dependencias innecesarias entre aplicaciones.

## 4.2. Modelos

Los modelos se definen en models.py y representan las entidades principales de la aplicación.

Los nombres de los modelos utilizan PascalCase y singular.

Ejemplos:

Project
Task
Assignment
ProjectTemplate
ProjectFollow

Los modelos deben contener principalmente:

- Definición de campos;
- Relaciones entre entidades;
- Restricciones;
- Propiedades directamente relacionadas con la entidad;
- Comportamiento propio del modelo cuando sea apropiado.

Debe evitarse colocar en los modelos lógica de negocio excesivamente compleja que pueda reutilizarse desde diferentes partes de la aplicación.

## 4.3. Vistas

Las vistas se encuentran normalmente en views.py.

Su responsabilidad principal es:

- Recibir la petición;
- Comprobar el acceso cuando corresponda;
- Obtener o preparar los datos necesarios;
- Llamar a servicios o funciones auxiliares;
- Devolver una respuesta o renderizar una plantilla.

Por ejemplo:

@login_required
def home(request):
  context = get_dashboard_context(request.user)
  return render(request, "home/home.html", context)

La vista debe evitar concentrar grandes cantidades de lógica de negocio.

Cuando una operación empieza a ser compleja o reutilizable, debe trasladarse a una función auxiliar, servicio o módulo especializado.

## 4.4. Servicios

Las operaciones que requieren una lógica de negocio más elaborada pueden colocarse en módulos services.

Ejemplo:

apps/
└── home/
  └── services/
    └── dashboard.py

En ProjectFlow, los servicios se utilizan para preparar datos o ejecutar operaciones que no deberían estar directamente dentro de una vista.

Por ejemplo:

get_dashboard_context(user)

También existen servicios relacionados con reporting:

apps/reports/services/
├── dashboard.py
├── export.py
├── metrics.py
├── pdf.py
└── project_progress_service.py

Los servicios deben tener una responsabilidad clara y evitar convertirse en módulos que acumulen funcionalidades no relacionadas.

## 4.5. QuerySets y consultas

Las consultas reutilizables relacionadas con una entidad pueden centralizarse en módulos querysets.py.

En ProjectFlow, por ejemplo:

apps/projects/querysets.py

Contiene:

get_projects_queryset()

Esta función centraliza una consulta que incluye:

- relaciones;
- estadísticas;
- anotaciones;
- ordenación.

Esto evita repetir consultas complejas en diferentes vistas.

Cuando una consulta se utiliza únicamente una vez y es sencilla, puede permanecer directamente en la vista o servicio correspondiente.

Cuando una consulta se reutiliza o tiene una lógica significativa, es preferible centralizarla.

## 4.6. Formularios

Los formularios Django se encuentran en forms.py.

Los formularios deben encargarse principalmente de:

definir campos;
validar datos introducidos por el usuario;
aplicar reglas de validación relacionadas con el formulario;
preparar los datos para ser utilizados por la vista.

Ejemplos:

apps/core/forms.py
apps/manage/forms.py
apps/projects/forms.py
apps/tasks/forms.py

La lógica de permisos no debe depender únicamente de los formularios.

Los permisos deben comprobarse también en la lógica de aplicación correspondiente para evitar que un usuario pueda saltarse las restricciones enviando una petición directamente.

## 4.7. Permisos

La lógica de permisos relacionada con proyectos y tareas se centraliza principalmente en:

apps/projects/permissions.py

Se utilizan funciones descriptivas como:

user_can_view_project()
user_can_create_project()
user_can_edit_project()
user_can_delete_project()

user_can_view_task()
user_can_create_task()
user_can_edit_task()
user_can_delete_task()
user_can_assign_task()

También existe una matriz centralizada de permisos:

ROLE_PERMISSIONS

Los permisos deben comprobarse mediante las funciones correspondientes en lugar de repetir manualmente la misma lógica en diferentes vistas.

Esto permite mantener un único punto de control para las reglas de acceso.

## 4.8. URLs

Cada aplicación debe definir sus propias URLs cuando tenga rutas propias.

Ejemplos:

apps/home/urls.py
apps/projects/urls.py
apps/tasks/urls.py
apps/kanban/urls.py
apps/reports/urls.py
apps/manage/urls.py

Las URLs principales del proyecto se incluyen desde:

config/urls.py

La configuración principal debe encargarse de conectar las aplicaciones, mientras que cada aplicación mantiene sus propias rutas.

Ejemplo:

path("projects/", include("apps.projects.urls"))
path("tasks/", include("apps.tasks.urls"))
path("kanban/", include("apps.kanban.urls"))

Los nombres de las URLs deben ser descriptivos y utilizar snake_case.

Ejemplo:

name="project_list"
name="task_list"
name="set_language"

En las plantillas y vistas se debe utilizar el nombre de la URL mediante url o reverse en lugar de escribir rutas manualmente.

Ejemplo:

{% url 'project_list' %}

o:

reverse("project_list")

## 4.9. Context processors

Los datos que deben estar disponibles de forma global en diferentes plantillas pueden prepararse mediante context_processors.py.

ProjectFlow utiliza esta estructura en determinadas aplicaciones:

apps/core/context_processors.py
apps/home/context_processors.py

Los context processors deben utilizarse únicamente para datos que realmente necesiten estar disponibles de forma global.

No se debe utilizar un context processor para cargar grandes cantidades de datos innecesariamente en todas las páginas.

## 4.10. Plantillas

Las plantillas HTML se encuentran principalmente en:

templates/

Las plantillas se organizan por funcionalidad:

templates/
├── home/
├── kanban/
├── manage/
├── projects/
├── reports/
├── tasks/
└── registration/

La plantilla base común se encuentra en:

templates/base.html

Las páginas que comparten la estructura general deben utilizar:

{% extends "base.html" %}

La plantilla base contiene elementos comunes como:

- navegación;
- búsqueda;
- contenido principal;
- widget de flujo de trabajo;
- recursos CSS y JavaScript comunes.

## 4.11. Plantillas parciales

Los componentes reutilizables pueden mantenerse como plantillas parciales.

Ejemplos:

templates/kanban/includes/_card.html
templates/projects/includes/_project_card.html
templates/reports/includes/_summary_cards.html

Las plantillas parciales deben utilizarse cuando un componente:

- se reutiliza;
- tiene una estructura suficientemente compleja;
- mejora la legibilidad de la plantilla principal.

No es necesario crear un parcial para cada pequeño fragmento HTML.

## 4.12. Contexto de las plantillas

Las vistas y servicios deben proporcionar al template únicamente los datos que necesita.

Por ejemplo:

return {
    "dashboard_projects": dashboard_projects,
    "notification_projects": notification_projects,
    "templates": templates,
}

Los nombres del contexto deben ser descriptivos y coherentes con el contenido.

Debe evitarse utilizar nombres genéricos como:

- "context"
- "data"
- "items"

cuando sea posible utilizar un nombre más específico.

## 4.13. Autenticación

Las vistas que requieren un usuario autenticado deben utilizar mecanismos de protección de Django.

Por ejemplo:

from django.contrib.auth.decorators import login_required

y:

@login_required
def home(request):
  ...

Las páginas públicas, como el inicio de sesión, deben permanecer accesibles sin autenticación cuando corresponda.

La comprobación de autenticación y la comprobación de permisos son conceptos diferentes:

Autenticación
    ↓
¿El usuario ha iniciado sesión?

Autorización
    ↓
¿El usuario tiene permiso para realizar esta acción?

Ambas comprobaciones deben aplicarse cuando sea necesario.

## 4.14. Acceso mediante ORM

Las consultas a la base de datos deben realizarse preferentemente mediante el ORM de Django.

Ejemplo:

Assignment.objects.filter(
  user=user,
  project=project
)

Debe evitarse utilizar SQL directamente salvo que exista una necesidad concreta que justifique su utilización.

Cuando sea posible, se deben aprovechar herramientas del ORM como:

select_related()
prefetch_related()
filter()
exclude()
annotate()
exists()
Count()
Q()
Exists()

Esto permite mantener las consultas integradas con el modelo de Django y facilita su mantenimiento.

## 4.15. Optimización de consultas

Cuando una vista necesita acceder a relaciones de modelos, debe evitarse realizar consultas innecesarias repetidamente.

Para relaciones de tipo ForeignKey o OneToOne se puede utilizar:

select_related()

Para relaciones ManyToMany o relaciones inversas se puede utilizar:

prefetch_related()

Ejemplo:

Project.objects.select_related(
  "owner",
  "template"
).prefetch_related(
  "assignments",
  "tasks"
)

Las consultas deben optimizarse especialmente en páginas que muestran listas de proyectos, tareas o usuarios.

## 4.16. Migraciones

Las migraciones deben generarse mediante Django:

python manage.py makemigrations

y aplicarse mediante:

python manage.py migrate

No se deben modificar manualmente las migraciones ya aplicadas salvo que exista una razón técnica clara.

Los cambios en los modelos deben generar nuevas migraciones.

Ejemplo:

0001_initial.py
0002_...
0003_...

Las migraciones forman parte de la evolución del esquema de la base de datos.

## 4.17. Internacionalización

Cuando una cadena de texto de la interfaz deba traducirse, se utilizará el sistema de internacionalización de Django.

En las plantillas:

{% load i18n %}

{% translate "Proyectos" %}

En Python pueden utilizarse las funciones de traducción de Django cuando corresponda.

Los archivos de traducción se almacenan en:

locale/
├── en/
│ └── LC_MESSAGES/
│   └── django.po
└── es/
  └── LC_MESSAGES/
    └── django.po

Las cadenas traducibles deben marcarse explícitamente.

No se deben traducir automáticamente textos que formen parte de identificadores internos, nombres de variables, estados o claves de configuración.

## 4.18. Separación de responsabilidades

Como regla general:

Modelos
    ↓
Representan datos y relaciones

QuerySets
    ↓
Centralizan consultas reutilizables

Servicios
    ↓
Preparan datos y ejecutan lógica de negocio

Permisos
    ↓
Determinan qué puede hacer cada usuario

Vistas
    ↓
Coordinan la petición y la respuesta

Templates
    ↓
Presentan los datos al usuario

JavaScript
    ↓
Gestiona la interacción en el navegador

Cuando una función empieza a asumir responsabilidades de varias capas, debe revisarse si parte de esa lógica debería trasladarse a otro módulo.

El objetivo es mantener cada componente con una responsabilidad clara y evitar vistas, modelos o servicios excesivamente grandes.

## 5. Roles y permisos

Los roles y permisos se centralizan para mantener un único criterio de autorización en ProjectFlow.

Los roles principales son:

OWNER
MANAGER
MEMBER

La matriz principal de permisos se encuentra en:

apps/projects/permissions.py

y se define mediante:

ROLE_PERMISSIONS

Los permisos utilizan nombres descriptivos en `snake_case`, por ejemplo:

view_project
create_project
edit_project
delete_project
archive_project
manage_users
change_owner

view_task
create_task
edit_task
delete_task
assign_task

Las comprobaciones deben realizarse mediante funciones específicas como:

user_can_view_project()
user_can_create_project()
user_can_edit_project()
user_can_delete_project()

user_can_view_task()
user_can_create_task()
user_can_edit_task()
user_can_delete_task()
user_can_assign_task()

Se debe evitar repetir manualmente la misma lógica de permisos en diferentes vistas.

La autenticación y la autorización deben mantenerse diferenciadas:

Autenticación
    ↓
¿El usuario está identificado?

Autorización
    ↓
¿El usuario puede realizar esta acción?

Las reglas de permisos deben mantenerse coherentes con la funcionalidad real de cada rol.

## 6. Consultas a base de datos

Las consultas a la base de datos deben realizarse preferentemente mediante el ORM de Django.

Ejemplo:

Assignment.objects.filter(
  user=user,
  project=project
)

Las consultas reutilizables o suficientemente complejas deben centralizarse en módulos especializados.

Por ejemplo:

apps/projects/querysets.py

donde se encuentra:

get_projects_queryset()

Las consultas deben utilizar nombres descriptivos y expresar claramente qué información obtienen.

Se recomienda utilizar las herramientas del ORM de Django cuando sean apropiadas:

filter()
exclude()
select_related()
prefetch_related()
annotate()
exists()
Count()
Q()
Exists()

Cuando una consulta accede repetidamente a relaciones, se debe valorar el uso de `select_related()` o `prefetch_related()` para evitar consultas innecesarias.

No se debe utilizar SQL directo salvo que exista una necesidad concreta que justifique su utilización.

## 7. Plantillas HTML

Las plantillas HTML se encuentran principalmente dentro de:

templates/

y se organizan por funcionalidad:

templates/
├── home/
├── kanban/
├── manage/
├── projects/
├── reports/
├── tasks/
└── registration/

La plantilla común es:

templates/base.html

Las páginas que compartan la estructura general deben heredar de ella:

{% extends "base.html" %}

Las plantillas deben centrarse principalmente en la presentación de los datos.

La lógica de negocio compleja no debe trasladarse al HTML.

Los componentes reutilizables pueden convertirse en plantillas parciales.

Ejemplos:

templates/kanban/includes/_card.html
templates/projects/includes/_project_card.html
templates/reports/includes/_summary_cards.html

## 8. CSS

Los archivos CSS se organizan principalmente por funcionalidad.

Ejemplo:

static/css/
├── base/
├── common/
├── kanban/
├── projects/
├── report/
└── tasks/

Los nombres de los archivos deben ser descriptivos:

tables.css
workflow.css
text.css
kanban.css
project_list.css
template_form.css
report.css
task_list.css

Las clases CSS deben describir el componente o función al que pertenecen.

Ejemplos:

workflow-arrow
workflow-panel
navbar-brand

Se deben evitar nombres excesivamente genéricos que puedan provocar conflictos.

## 9. JavaScript

Los archivos JavaScript se encuentran principalmente en:

static/js/

y se organizan por funcionalidad.

Ejemplo:

static/js/
├── base/
├── common/
├── home/
├── kanban/
├── manage/
├── projects/
├── report/
└── tasks/

Los nombres de los archivos deben ser descriptivos:

workflow.js
form_changes.js
template_selector.js
project_list.js
kanban_layout.js
task_form.js

Las funciones utilizan `camelCase`:

updateWorkflow()
handleProjectChange()
loadTasks()

Las variables también utilizan `camelCase`:

projectId
taskList
workflowSteps
currentIndex

Las constantes pueden utilizar `UPPER_SNAKE_CASE` cuando representan valores que no deberían modificarse:

const MAX_ITEMS = 10;

El JavaScript debe encargarse principalmente de la interacción del navegador y no duplicar innecesariamente reglas de negocio que ya existen en Django.

## 10. Comentarios

Los comentarios deben utilizarse para explicar decisiones, contexto o comportamientos que no sean evidentes a partir del código.

Se deben evitar comentarios que simplemente repitan lo que hace una línea de código.

Es preferible:

"# Se utiliza el primer rol asignado para determinar la página inicial.

que:

"# Obtiene assignment.
assignment = ...

Los comentarios deben mantenerse actualizados cuando se modifica el código.

Los comentarios obsoletos deben eliminarse.

## 11. Formato y sangría

El código debe mantener una sangría consistente.

En Python se utiliza una sangría de cuatro espacios por nivel:

def get_project(user):
  if user.is_authenticated:
    return project

No se deben mezclar tabulaciones y espacios.

Las estructuras complejas deben dividirse cuando esto mejore la legibilidad.

En HTML, CSS y JavaScript se debe mantener una indentación coherente con el código existente del proyecto.

## 12. Separación de responsabilidades

Cada componente debe tener una responsabilidad clara.

La distribución general de responsabilidades es:

Modelos
    ↓
Datos, relaciones y comportamiento propio de la entidad

QuerySets
    ↓
Consultas reutilizables

Servicios
    ↓
Preparación de datos y lógica de negocio

Permisos
    ↓
Autorización de acciones

Vistas
    ↓
Coordinación de petición y respuesta

Templates
    ↓
Presentación

JavaScript
    ↓
Interacción en el navegador

Se debe evitar que una vista, modelo o servicio acumule responsabilidades que pertenecen a otras capas.

## 13. Reutilización

Antes de implementar una funcionalidad nueva, se debe comprobar si ya existe una función, servicio, consulta, plantilla parcial o componente que pueda reutilizarse.

Ejemplos:

get_projects_queryset()
get_dashboard_context()
get_user_inbox()
user_can_edit_project()
user_can_edit_task()

También pueden reutilizarse:

plantillas parciales
funciones JavaScript
estilos CSS
context processors

La reutilización debe mejorar la coherencia sin crear abstracciones innecesariamente complejas.

## 14. Evitar duplicación

Debe evitarse duplicar la misma lógica en diferentes partes del proyecto.

Por ejemplo, una regla de permisos no debería implementarse de forma diferente en varias vistas si puede centralizarse en:

apps/projects/permissions.py

Una consulta compleja que se utiliza en varias partes puede centralizarse en:

apps/projects/querysets.py

Cuando se detecte código duplicado, se debe valorar si puede extraerse una función, servicio, consulta o componente reutilizable.

No se debe crear una abstracción únicamente para eliminar unas pocas líneas si el resultado hace el código menos claro.

## 15. Estados y valores internos

Los estados y valores internos deben utilizar identificadores consistentes.

Los valores internos pueden utilizar mayúsculas cuando representan estados, roles o modos de acceso:

DONE
OWNER
MANAGER
MEMBER
EDIT
READONLY
DENY

El identificador interno no tiene por qué coincidir con el texto mostrado al usuario.

Por ejemplo:

DONE     → Completada
READONLY → Solo lectura
DENY     → Sin acceso

Esto permite separar la lógica interna de la presentación de la interfaz.

Los estados no deben cambiarse arbitrariamente porque pueden estar utilizados por modelos, consultas, permisos, vistas, plantillas o JavaScript.

## 16. Textos visibles para el usuario

Los textos que aparecen en la interfaz deben ser claros, coherentes y consistentes.

Se deben mantener criterios comunes para acciones similares.

Los textos visibles deben diferenciarse de los identificadores internos.

Cuando una cadena deba traducirse, debe utilizarse el sistema de internacionalización de Django.

En plantillas:

{% load i18n %}
{% translate "Proyectos" %}

Los nombres de variables, claves de permisos y estados internos no deben traducirse.

## 17. Documentación

La documentación del proyecto se mantiene dentro de:

docs/

Los documentos principales utilizan numeración:

docs/
├── 01 Manual_funcional.md
├── 02 Permisos.md
├── 03 Arquitectura.md
└── 04 Convenciones.md

Cada documento debe tener un objetivo claramente definido.

La documentación debe mantenerse actualizada cuando cambie de forma significativa la arquitectura, los permisos, las convenciones o el funcionamiento de la aplicación.

## 18. Archivos generados y entorno virtual

El entorno virtual de Python se encuentra en:

env/

El entorno virtual contiene dependencias instaladas y no forma parte de la lógica propia de ProjectFlow.

No se debe modificar código dentro de:

env/

Los archivos de caché como:

__pycache__/
*.pyc

son archivos generados y no deben considerarse código fuente.

Los archivos generados o específicos del entorno local no deben formar parte de la documentación ni del código fuente del proyecto cuando no sean necesarios.

## 19. Internacionalización

ProjectFlow utiliza el sistema de internacionalización de Django.

Las cadenas traducibles deben marcarse explícitamente.

En plantillas:

{% load i18n %}
{% translate "Proyectos" %}

Los archivos de traducción se encuentran en:

locale/
├── en/
│   └── LC_MESSAGES/
│       └── django.po
└── es/
    └── LC_MESSAGES/
        └── django.po

Para generar mensajes de traducción de plantillas HTML se utiliza:

python manage.py makemessages -l es -e html --ignore='env'

El entorno virtual debe quedar excluido para evitar incorporar cadenas procedentes de Django o de sus dependencias.

Las traducciones compiladas se generan mediante:

django-admin compilemessages

Los identificadores internos, nombres de variables, estados y claves de configuración no deben traducirse.

## 20. Seguridad

Las comprobaciones de acceso no deben depender únicamente de la interfaz.

Ocultar un botón en una plantilla no constituye una comprobación de seguridad suficiente.

Las acciones protegidas deben comprobar los permisos también en el servidor.

Por ejemplo:

¿Puede el usuario editar el proyecto?
        ↓
user_can_edit_project()
        ↓
permitir o rechazar la acción

Las vistas que requieren autenticación deben utilizar los mecanismos de autenticación de Django:

@login_required
def home(request):
  ...

Los datos enviados por el usuario deben validarse antes de utilizarlos.

No se deben confiar las restricciones de seguridad únicamente al navegador, HTML o JavaScript.

## 21. Cambios en el proyecto

Los cambios deben realizarse de forma incremental y procurando afectar únicamente a los componentes necesarios.

Antes de modificar una funcionalidad, se debe identificar:

¿Qué aplicación es responsable?
¿Qué vista interviene?
¿Qué modelo o consulta utiliza?
¿Qué plantilla se muestra?
¿Qué permisos afectan a la acción?
¿Existe JavaScript relacionado?

Cuando se modifiquen modelos, deben generarse las migraciones correspondientes.

Cuando se modifiquen traducciones, deben actualizarse los archivos .po y compilarse cuando sea necesario.

Cuando se modifiquen permisos, debe revisarse el comportamiento de los roles afectados.

Los cambios importantes deben reflejarse también en la documentación correspondiente.

## 22. Regla general

La regla principal de ProjectFlow es mantener el código:

Claro
    ↓
Coherente
    ↓
Separado por responsabilidades
    ↓
Reutilizable cuando tenga sentido
    ↓
Fácil de mantener

Ante varias soluciones técnicamente válidas, se debe priorizar la que:

1. sea más fácil de entender;
2. respete la arquitectura existente;
3. mantenga separadas las responsabilidades;
4. evite duplicación innecesaria;
5. sea sencilla de modificar en el futuro.

Las convenciones no deben convertirse en una restricción que complique innecesariamente el código.

Cuando exista una razón técnica para apartarse de una convención, debe priorizarse la solución más clara y mantenible y, si el cambio es relevante, documentarse la decisión.
