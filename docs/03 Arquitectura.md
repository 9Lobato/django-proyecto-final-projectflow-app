# 03. Arquitectura de ProjectFlow

## 1. Introducción

ProjectFlow es una aplicación web desarrollada con Django como backend y React + Vite como frontend integrado.

La aplicación mantiene la arquitectura y lógica de negocio principal en Django, incluyendo:

- Autenticación y sesiones.
- Modelos y acceso a base de datos.
- Permisos y autorización.
- Gestión de proyectos.
- Gestión de tareas.
- Kanban.
- Seguimiento y archivado de proyectos.
- Internacionalización.
- APIs internas utilizadas por el frontend React.

React se utiliza para construir e integrar las interfaces que requieren una interacción más dinámica, mientras que Django continúa proporcionando determinadas páginas renderizadas mediante templates y los servicios backend de la aplicación.

Por tanto, ProjectFlow no es una SPA completamente independiente de Django. Se trata de una arquitectura híbrida en la que Django continúa siendo el núcleo de la aplicación y React consume determinados endpoints JSON proporcionados por Django.

---

## 2. Arquitectura general

La arquitectura puede representarse de la siguiente manera:

                         ProjectFlow
                              │
                ┌─────────────┴─────────────┐
                │                           │
             Django                    React + Vite
             Backend                    Frontend
                │                           │
                │                    Componentes JSX
                │                    Estado de interfaz
                │                    Peticiones a API
                │                           │
                └─────────────┬─────────────┘
                              │
                       APIs / HTTP
                              │
                           Django
                              │
                    ┌─────────┴─────────┐
                    │                   │
                 Modelos              Lógica
                  / ORM              de negocio
                    │                   │
                    └─────────┬─────────┘
                              │
                          Base de datos

La comunicación entre React y Django se realiza mediante peticiones HTTP.

React puede solicitar o modificar información mediante endpoints JSON de Django, mientras que Django mantiene el acceso a los modelos y a la base de datos.

---

## 3. Backend Django

Django constituye el núcleo del backend de ProjectFlow.

Entre sus responsabilidades se encuentran:

- Gestión de usuarios y autenticación.
- Gestión de sesiones.
- Control de permisos.
- Validación de operaciones.
- Lógica de negocio.
- Acceso a la base de datos mediante Django ORM.
- Generación de determinadas páginas HTML.
- Exposición de APIs JSON para el frontend React.
- Gestión de CSRF.
- Internacionalización.

La estructura principal del backend se organiza mediante aplicaciones Django independientes.

apps/
├── accounts/
├── core/
├── home/
├── kanban/
├── projects/
├── reports/
└── tasks/

config/
├── settings.py
├── urls.py
├── wsgi.py
└── ...

Cada aplicación agrupa funcionalidades relacionadas y mantiene separadas las responsabilidades del sistema.

---

## 4. Frontend React + Vite

La parte React del proyecto se encuentra dentro del directorio:

frontend/
├── src/
│   ├── components/
│   │   ├── Kanban.jsx
│   │   ├── Navbar.jsx
│   │   ├── Start.jsx
│   │   └── Workflow.jsx
│   │
│   ├── styles/
│   │   ├── kanban.css
│   │   └── start.css
│   │
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
│
├── vite.config.js
├── package.json
└── ...

## 4.1. Responsabilidades principales

React se encarga principalmente de:

- Renderizar componentes interactivos.
- Gestionar el estado de la interfaz.
- Responder a acciones del usuario.
- Realizar peticiones a las APIs de Django.
- Actualizar la interfaz sin necesidad de recargar toda la página.
- Gestionar determinadas interacciones del Kanban y del workflow.

Vite proporciona el entorno de desarrollo y el proceso de compilación del frontend.

---

## 5. Integración entre Django y React

Django y React se integran mediante HTTP.

El frontend React realiza peticiones a endpoints proporcionados por Django, principalmente mediante respuestas JSON.

Por ejemplo:

React
  │
  │ GET /api/navbar/
  ▼
Django
  │
  ├── autenticación
  ├── permisos
  ├── consultas
  └── lógica de negocio
  │
  ▼
JSON
  │
  ▼
React
  │
  ▼
Actualización de la interfaz

Esta separación permite que React gestione la experiencia de usuario mientras Django mantiene el control de los datos y las reglas de negocio.

---

## 6. APIs internas

Las APIs internas se encuentran principalmente bajo:

/api/

Actualmente existen endpoints utilizados para funcionalidades como:

/api/navbar/
/api/workflow/
/projects/archive/api/
/projects/follow/api/
/kanban/api/
/kanban/move/
/kanban/copy/

Estas rutas son atendidas por Django y permiten que el frontend interactúe con el backend sin depender exclusivamente de páginas HTML renderizadas.

Las APIs siguen utilizando la autenticación y autorización proporcionadas por Django.

---

## 7. Flujo de una petición

Dependiendo de la funcionalidad, una petición puede seguir diferentes recorridos.

## 7.1. Página renderizada por Django

Para una página tradicional:

Usuario
   ↓
URL
   ↓
config/urls.py
   ↓
urls.py de la aplicación
   ↓
views.py
   ↓
Permisos / QuerySets / Services
   ↓
Models / ORM
   ↓
Base de datos
   ↓
Contexto
   ↓
Template Django
   ↓
HTML
   ↓
Navegador

## 7.2. Petición desde React

Cuando una funcionalidad React necesita información del backend:

Usuario
   ↓
Componente React
   ↓
Petición HTTP
   ↓
API Django
   ↓
View
   ↓
Permisos / lógica de negocio
   ↓
Models / ORM
   ↓
Base de datos
   ↓
Respuesta JSON
   ↓
React
   ↓
Actualización de la interfaz

De esta forma, React no accede directamente a la base de datos.

---

## 8. Gestión de permisos

Los permisos se mantienen en el backend Django.

React puede recibir información sobre las capacidades del usuario para adaptar la interfaz, pero la autorización real de las operaciones corresponde a Django.

Por ejemplo:

React
  │
  │ solicitud de modificación
  ▼
Django
  │
  ├── usuario autenticado
  ├── permisos
  ├── rol
  └── reglas de negocio
  │
  ▼
Operación permitida / rechazada

Esto evita depender de controles exclusivamente visuales en el frontend.

Un usuario no obtiene permisos adicionales simplemente modificando el código o el estado de React.

---

## 9. Persistencia de datos

La persistencia de los datos se realiza mediante Django ORM.

La estructura general es:

React / Django Templates
          ↓
       Views
          ↓
   Lógica de negocio
          ↓
      Django ORM
          ↓
      Base de datos

React no almacena los datos principales de la aplicación como fuente de verdad.

Los proyectos, tareas, usuarios, asignaciones, estados y demás información persistente pertenecen al backend y a la base de datos.

---

## 10. Persistencia del workflow

El progreso del workflow es persistente y está asociado al usuario.

La interfaz React obtiene el estado mediante:

/start/
   ↓
React
   ↓
GET /api/workflow/
   ↓
WorkflowProgress
   ↓
Base de datos

Cuando el usuario marca o desmarca un paso:

React
   ↓
POST /api/workflow/
   ↓
WorkflowProgress.checks
   ↓
Base de datos

El modelo utilizado es:

WorkflowProgress
├── user
└── checks

Cada usuario dispone de un único registro de progreso mediante una relación OneToOneField.

Esto permite que el estado del workflow:

- Se mantenga después de recargar la página.
- Se mantenga después de cerrar sesión.
- Se recupere al volver a iniciar sesión.
- Sea independiente del navegador utilizado por el usuario.

El backend es, por tanto, la fuente de verdad del progreso persistente del workflow.

---

## 11. Sesiones y autenticación

La autenticación continúa siendo gestionada por Django.

El flujo general es:

Usuario
   ↓
/login/
   ↓
Django Authentication
   ↓
Sesión Django
   ↓
Usuario autenticado

Las peticiones realizadas desde React utilizan la sesión de Django y las medidas de protección CSRF correspondientes.

React no sustituye el sistema de autenticación de Django.

---

## 12. Kanban

El Kanban combina la interfaz dinámica del frontend con la lógica de negocio del backend.

De forma simplificada:

Usuario
   ↓
Kanban React
   ↓
Drag & Drop
   ↓
API Django
   ↓
Validación de permisos
   ↓
Cambio de estado
   ↓
Base de datos
   ↓
Respuesta
   ↓
Actualización del Kanban

Las operaciones que modifican información persistente se validan en Django antes de actualizar la base de datos.

Esto permite controlar tanto las transiciones válidas como los permisos del usuario.

---

## 13. Estructura del proyecto

La estructura general de ProjectFlow queda organizada de la siguiente manera:

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
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
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
│
├── static/
│
├── locale/
│
├── manage.py
│
└── requirements.txt

apps/

Contiene las aplicaciones Django y la lógica funcional del backend.

config/

Contiene la configuración global del proyecto Django.

frontend/

Contiene el código fuente del frontend React y la configuración de Vite.

templates/

Contiene las plantillas HTML utilizadas por Django.

static/

Contiene recursos estáticos del proyecto, incluyendo CSS y JavaScript que siguen siendo utilizados por las partes Django-rendered de la aplicación.

locale/

Contiene los archivos de traducción utilizados por Django.

---

## 14. Separación de responsabilidades

ProjectFlow mantiene una separación clara entre frontend y backend.

React

Se encarga principalmente de:

- Presentación dinámica.
- Componentes.
- Estado de interfaz.
- Interacciones del usuario.
- Comunicación con las APIs.

Django

Se encarga principalmente de:

- Autenticación.
- Autorización.
- Reglas de negocio.
- Validación.
- Persistencia.
- ORM.
- APIs.
- Templates Django.
- Seguridad.

Base de datos

Se encarga de almacenar la información persistente de la aplicación.

La regla general es:

Interfaz → React
Reglas de negocio → Django
Datos persistentes → Base de datos

---

## 15. Principios arquitectónicos

La arquitectura de ProjectFlow sigue los siguientes principios:

1. Django es la autoridad sobre los datos y permisos.
2. React se utiliza para mejorar la interacción y dinamismo de la interfaz.
3. El frontend no accede directamente a la base de datos.
4. Las operaciones persistentes pasan por Django.
5. La autorización se valida en el backend.
6. Las APIs proporcionan una interfaz clara entre React y Django.
7. La aplicación mantiene compatibilidad con páginas renderizadas por Django.
8. La información persistente no depende exclusivamente del estado del navegador.
9. La lógica de negocio debe permanecer fuera de los componentes React cuando afecte a la seguridad o integridad de los datos.
10. Cada aplicación Django mantiene separadas sus responsabilidades funcionales.

---

## 16. Resumen

La arquitectura actual de ProjectFlow combina Django y React de forma integrada:

                         USUARIO
                            │
                ┌───────────┴───────────┐
                │                       │
        Django Templates          React + Vite
                │                       │
                └───────────┬───────────┘
                            │
                         HTTP/API
                            │
                          Django
                            │
                 ┌──────────┴──────────┐
                 │                     │
              Permisos             Lógica de
              Seguridad             negocio
                 │                     │
                 └──────────┬──────────┘
                            │
                         Django ORM
                            │
                       BASE DE DATOS

Django continúa siendo el núcleo de la aplicación y mantiene la responsabilidad sobre autenticación, permisos, lógica de negocio y persistencia.

React + Vite proporciona una interfaz moderna y dinámica para las partes integradas del proyecto.

Esta arquitectura permite evolucionar progresivamente la interfaz hacia React sin tener que reemplazar toda la estructura existente de Django.
