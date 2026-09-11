# 04. Convenciones de desarrollo de ProjectFlow

## 1. Objetivo

Este documento define las convenciones utilizadas durante el desarrollo de ProjectFlow.

El proyecto combina:

- Django para backend y lógica de negocio.
- React para la interfaz dinámica.
- Vite para desarrollo y compilación del frontend.
- HTML/CSS/JavaScript para las partes de la aplicación que continúan utilizando templates y recursos estáticos de Django.

El objetivo de estas convenciones es mantener un código organizado, predecible y fácil de mantener.

---

## 2. Estructura general

La estructura principal del proyecto se divide en backend y frontend:

ProjectFlow/
│
├── apps/
│   ├── accounts/
│   ├── core/
│   ├── home/
│   ├── kanban/
│   ├── projects/
│   ├── reports/
│   └── tasks/
│
├── config/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── styles/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── templates/
├── static/
├── locale/
├── manage.py
└── requirements.txt

La separación principal es:

Backend  → Django
Frontend → React + Vite

---

## 3. Convenciones Django

## 3.1. Aplicaciones

Las funcionalidades del backend se agrupan en aplicaciones Django independientes.

Ejemplos:

- accounts: usuarios y perfiles.
- core: funcionalidades comunes y APIs generales.
- home: página principal.
- kanban: tablero Kanban y operaciones relacionadas.
- projects: proyectos, seguimiento y archivado.
- reports: informes.
- tasks: gestión y filtrado de tareas.

Cada aplicación debe contener únicamente la lógica relacionada con su responsabilidad.

---

## 4. Modelos

Los modelos se definen en models.py dentro de la aplicación correspondiente.

Ejemplo:

class WorkflowProgress(models.Model):
  user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name="workflow_progress",
  )

  checks = models.JSONField(default=dict, blank=True)

Convenciones

- Utilizar nombres descriptivos.
- Mantener los modelos relacionados con su aplicación.
- Utilizar relaciones Django (ForeignKey, OneToOneField, ManyToManyField) cuando corresponda.
- Evitar almacenar información persistente únicamente en el frontend.
- Utilizar __str__() para facilitar la identificación de los objetos en Django.
- Crear y aplicar migraciones después de modificar los modelos.

---

## 5. Views y URLs

Las URLs se definen en el urls.py de cada aplicación y se incluyen desde config/urls.py.

Las views deben encargarse de:

- Recibir la petición.
- Validar autenticación y permisos.
- Obtener o modificar los datos necesarios.
- Devolver HTML o JSON según corresponda.

Las operaciones de negocio importantes no deben depender exclusivamente del frontend.

---

## 6. APIs JSON

Las APIs utilizadas por React se agrupan bajo /api/.

Ejemplos:

/api/navbar/
/api/workflow/
/kanban/api/
/kanban/move/
/kanban/copy/
/projects/archive/api/
/projects/follow/api/

Convenciones

- Utilizar respuestas JSON para las APIs consumidas por React.
- Utilizar métodos HTTP coherentes con la operación.
- Utilizar GET para obtener información.
- Utilizar POST para operaciones que modifican información cuando corresponda.
- Validar siempre permisos en Django.
- No confiar en que React haya ocultado una acción para considerar que está autorizada.
- Mantener los endpoints relacionados con su aplicación Django.

---

## 7. QuerySets

Las consultas complejas o reutilizables pueden centralizarse en querysets.py.

Ejemplo:

apps/projects/querysets.py

Esto permite separar las consultas de la lógica de presentación y evitar repetir filtros complejos en diferentes views.

Cuando sea apropiado se deben utilizar:

- select_related()
- prefetch_related()
- annotate()
- Q()
- filtros del ORM

para mantener las consultas eficientes y legibles.

---

## 8. Permisos y seguridad

La autorización se realiza en el backend.

Las comprobaciones de permisos deben permanecer en Django aunque React controle visualmente qué acciones puede realizar un usuario.

Ejemplo conceptual:

React muestra acción
        ↓
Usuario ejecuta acción
        ↓
Django recibe petición
        ↓
Django comprueba permisos
        ↓
Operación permitida / rechazada

Las operaciones que modifican datos deben estar protegidas mediante las comprobaciones correspondientes de autenticación, autorización y CSRF.

---

## 9. Convenciones React

## 9.1. Componentes

Los componentes React se almacenan en:

frontend/src/components/

Ejemplos:

Kanban.jsx
Navbar.jsx
Start.jsx
Workflow.jsx

Los nombres de componentes utilizan PascalCase.

Ejemplo:

function Workflow() {
  // ...
}

Los componentes deben representar una responsabilidad clara.

Cuando una parte de la interfaz pueda mantenerse como componente independiente, debe evitarse concentrar toda la lógica en un único componente.

## 9.2. Archivos JSX

Los componentes React utilizan la extensión:

.jsx

Ejemplo:

frontend/src/components/Workflow.jsx

Los archivos principales del frontend son:

frontend/src/App.jsx
frontend/src/main.jsx

main.jsx constituye el punto de entrada de React.

App.jsx organiza la aplicación React y sus componentes principales.

---

## 10. Estado en React

El estado React debe utilizarse principalmente para controlar información necesaria para la interfaz.

Ejemplos:

- Elementos seleccionados.
- Estado visual de un componente.
- Elementos abiertos o cerrados.
- Resultados cargados desde una API.
- Estados temporales de interacción.

El estado de React no debe considerarse la fuente de verdad de los datos persistentes de la aplicación.

Para información que debe sobrevivir a una recarga o a una nueva sesión, la fuente de verdad debe ser el backend Django.

---

## 11. Comunicación con Django

Los componentes React se comunican con Django mediante peticiones HTTP.

Ejemplo conceptual:

Componente React
       ↓
fetch()
       ↓
API Django
       ↓
JSON
       ↓
Estado React
       ↓
Renderizado

Las peticiones deben utilizar las rutas API existentes en Django en lugar de acceder directamente a la base de datos.

React nunca debe conectarse directamente a SQLite ni a otro sistema de persistencia utilizado por Django.

---

## 12. Persistencia

Debe distinguirse entre estado de interfaz y datos persistentes.

Estado de interfaz

Puede permanecer únicamente en React cuando no sea necesario conservarlo.

Ejemplos:

Modal abierto
Filtro visual temporal
Elemento seleccionado
Panel expandido

Datos persistentes

Deben almacenarse en Django y en la base de datos.

Ejemplos:

Proyectos
Tareas
Estados de tareas
Asignaciones
Seguimientos
WorkflowProgress

La regla general es:

Estado temporal → React
Datos persistentes → Django / Base de datos

---

## 13. Workflow

El estado de los pasos completados del workflow se persiste en Django.

React obtiene el estado mediante:

GET /api/workflow/

y guarda los cambios mediante:

POST /api/workflow/

El modelo utilizado es:

WorkflowProgress
├── user
└── checks

Por tanto, los checks del workflow no deben implementarse como información persistente exclusivamente en localStorage.

El flujo esperado es:

Usuario
   ↓
React
   ↓
API Django
   ↓
WorkflowProgress
   ↓
Base de datos

Esto permite conservar el progreso después de recargar la página y después de cerrar y volver a iniciar sesión.

---

## 14. Vite

Vite se utiliza como herramienta de desarrollo y compilación del frontend React.

La configuración se encuentra en:

frontend/vite.config.js

Durante el desarrollo, Vite proporciona el servidor del frontend y configura el acceso al backend Django mediante proxy.

La configuración debe permitir que React pueda comunicarse con Django manteniendo correctamente la sesión y las peticiones protegidas por CSRF.

Para generar la versión de producción del frontend se utiliza:

npm run build

El resultado se genera en:

frontend/dist/

Este directorio no forma parte del código fuente y se mantiene fuera del control de versiones cuando así lo establece .gitignore.

---

## 15. CSS

Los estilos específicos de React se encuentran principalmente en:

frontend/src/styles/

Ejemplos:

frontend/src/styles/kanban.css
frontend/src/styles/start.css

Los estilos globales se encuentran en:

frontend/src/index.css

Convenciones

- Utilizar nombres descriptivos.
- Mantener los estilos específicos de un componente separados cuando sea razonable.
- Evitar duplicar reglas CSS.
- Mantener los estilos globales únicamente para reglas realmente globales.
- No introducir estilos inline salvo que exista una razón clara.

Los estilos utilizados por las páginas Django tradicionales continúan en el sistema de archivos estáticos del proyecto.

---

## 16. JavaScript heredado de Django

ProjectFlow conserva determinados archivos JavaScript dentro de:

static/js/

Estos archivos pertenecen a las partes de la aplicación que continúan utilizando las interfaces Django existentes.

La existencia de estos archivos no implica que React deba utilizarlos.

Cuando una funcionalidad haya sido integrada en React, su lógica correspondiente debe mantenerse dentro del frontend React siempre que sea posible.

La coexistencia de ambos sistemas es intencionada:

Django templates
  ↓
static/js/

React
  ↓
frontend/src/

---

## 17. Internacionalización

ProjectFlow utiliza el sistema de internacionalización de Django.

Los archivos de traducción se encuentran en:

locale/

Las cadenas traducibles deben mantenerse preparadas para el sistema de traducción correspondiente.

Cuando una funcionalidad React dependa de textos proporcionados por Django, debe evitarse duplicar innecesariamente las traducciones existentes.

---

## 18. Nombres y estilo

Python

Se utiliza snake_case:

project_list
workflow_api
project_archive_toggle

Las clases utilizan PascalCase:

WorkflowProgress
Project
Task
JavaScript / React

Las variables y funciones utilizan camelCase:

workflowChecks
handleDrop
loadProjects

Los componentes utilizan PascalCase:

Navbar
Kanban
Workflow
Start

Los archivos de componentes utilizan normalmente el mismo nombre que el componente:

Navbar.jsx
Kanban.jsx
Workflow.jsx

---

## 19. Comentarios

Los comentarios deben utilizarse cuando aporten información útil sobre:

- Decisiones de implementación.
- Comportamientos que no sean evidentes.
- Integraciones entre Django y React.
- Restricciones técnicas.
- Soluciones a comportamientos específicos.

No se deben añadir comentarios que simplemente describan una línea de código evidente.

Ejemplo útil:

# progreso del workflow asociado al usuario
class WorkflowProgress(models.Model):
  ...

Debe evitarse comentar de forma excesiva código cuyo comportamiento sea evidente por sí mismo.

---

## 20. Git

Los cambios deben mantenerse organizados en commits relacionados con una funcionalidad o corrección concreta.

Ejemplos de tipos utilizados:

feat: nueva funcionalidad
fix: corrección
docs: documentación
chore: tareas de mantenimiento

Los archivos generados automáticamente o dependientes del entorno local no deben incluirse en el repositorio.

Entre ellos:

.env
db.sqlite3
__pycache__/
node_modules/
frontend/dist/

según las reglas establecidas en .gitignore.

---

## 21. Principio general de separación

La regla principal para mantener la arquitectura organizada es:

Django
→ datos
→ seguridad
→ permisos
→ lógica de negocio
→ persistencia
→ APIs

React
→ componentes
→ interacción
→ estado de interfaz
→ presentación
→ comunicación con APIs

Vite
→ desarrollo
→ servidor frontend
→ compilación

React puede controlar cómo se presenta una funcionalidad, pero Django mantiene el control sobre lo que el usuario puede hacer y sobre qué información se guarda.

---

## 22. Resumen

Las convenciones actuales de ProjectFlow reflejan una arquitectura híbrida Django + React.

La aplicación no pretende duplicar la lógica entre frontend y backend. La responsabilidad principal se mantiene separada:

             PROJECTFLOW
                  │
        ┌─────────┴─────────┐
        │                   │
      Django              React
        │                   │
   Reglas de negocio    Interfaz
   Seguridad            Componentes
   Permisos             Estado visual
   Persistencia         Interacción
   APIs                 Peticiones HTTP
        │                   │
        └─────────┬─────────┘
                  │
               HTTP/JSON

El backend Django es la fuente de verdad para los datos y permisos, mientras que React proporciona una interfaz dinámica para las funcionalidades integradas.

Las partes que todavía utilizan templates y JavaScript estático de Django pueden coexistir con React sin que ambas arquitecturas tengan que mezclarse innecesariamente.
