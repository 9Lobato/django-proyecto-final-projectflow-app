# 03. Arquitectura de ProjectFlow

## 1. Introducción

ProjectFlow es una aplicación web desarrollada con Django para la gestión de proyectos y tareas.

La arquitectura del proyecto está organizada por funcionalidades mediante aplicaciones Django independientes.

Las principales áreas funcionales son:

- Gestión de usuarios y autenticación.
- Proyectos.
- Tareas.
- Kanban.
- Informes.
- Gestión administrativa.
- Dashboard y página inicial.

La estructura de la aplicación busca separar:

- Configuración global del proyecto;
- Funcionalidades de negocio;
- Acceso a datos;
- Lógica de permisos;
- Servicios;
- Vistas;
- Plantillas;
- Archivos estáticos;
- Internacionalización.

La aplicación sigue principalmente el patrón de arquitectura MTV de Django:

- **Model** → modelos y acceso a datos.
- **Template** → presentación HTML.
- **View** → coordinación entre petición, lógica y respuesta.

El objetivo de esta arquitectura es mantener separadas las responsabilidades de cada módulo y facilitar el mantenimiento y evolución de la aplicación. Además, el proyecto incorpora una capa de servicios y módulos específicos para consultas y permisos.

---

## 2. Estructura general del proyecto

La estructura principal del proyecto es:

ProjectFlow/
│
├── apps/
│   ├── accounts/ # Relacionada con los usuarios y la administración del modelo de usuario
│   ├── core/     # Contiene elementos reutilizables o transversales de la aplicación
│   ├── home/     # Controla el Dashboard y la página inicial
│   ├── kanban/   # Proporciona el tablero visual de tareas
│   ├── manage/   # Contiene funcionalidades de gestión administrativa de la aplicación
│   ├── projects/ # Contiene la lógica principal relacionada con los proyectos
│   ├── reports/  # Contiene la funcionalidad de informes y métricas
│   └── tasks/    # Gestiona las tareas de los proyectos
│
├── config/
│   ├── settings.py # Contiene la configuración principal de Django
│   ├── urls.py     # Define las rutas principales del proyecto
│   ├── asgi.py     # ?
│   └── wsgi.py     # ?
│
├── templates/
│   ├── common/
│   ├── home/
│   ├── kanban/
│   ├── manage/
│   ├── projects/
│   ├── reports/
│   ├── registration/
│   └── tasks/
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
├── locale/
│   ├── en/
│   └── es/
│
├── manage.py
├── requirements.txt
└── db.sqlite3

---

## 3. Configuración del proyecto

La carpeta config/ contiene la configuración global de Django.

Contiene la configuración principal de la aplicación:

- Aplicaciones instaladas;
- Middleware;
- Base de datos;
- Plantillas;
- Archivos estáticos;
- Internacionalización;
- Autenticación;
- Configuración de Django.

También es el punto donde se registra la estructura general de ProjectFlow.

## 4. Aplicaciones Django

ProjectFlow utiliza varias aplicaciones Django para separar las distintas áreas funcionales.

### Accounts

Gestiona los aspectos relacionados con los usuarios y la administración de usuarios de Django.

### Core

Contiene funcionalidades compartidas por diferentes partes de la aplicación.

### Home

Gestiona la página inicial y el dashboard de ProjectFlow.

## 5. Aplicación projects

La aplicación projects contiene la lógica principal relacionada con los proyectos.

Su estructura incluye:

apps/projects/
├── admin.py
├── apps.py
├── forms.py
├── models.py       # Define los modelos relacionados con los proyectos.
├── permissions.py  # Centraliza la lógica de permisos.
├── querysets.py    # Centraliza consultas reutilizables relacionadas con proyectos.
├── to_template.py
├── urls.py
├── utils.py
└── views.py        # Contiene las vistas relacionadas con listado de proyectos, creación, edición, eliminación, archivado, detalle, gestión del equipo y plantillas.

## 6. Aplicación projects

La aplicación tasks gestiona las tareas de los proyectos.

Su estructura incluye:

apps/tasks/
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── services/
│└── inbox.py
├── urls.py
├── utils.py
└── views.py

## 7. Aplicación kanban

La aplicación kanban proporciona la vista Kanban de las tareas.

Su estructura es:

apps/kanban/
├── apps.py
├── urls.py
└── views.py

## 8. Aplicación reports

La aplicación reports concentra la funcionalidad de informes y análisis.

Su estructura es:

apps/reports/
├── models.py
├── views.py
├── urls.py
├── services/
│├── dashboard.py
│├── export.py
│├── metrics.py
│├── pdf.py
│└── project_progress_service.py
└── demo/

## 9. Aplicación manage

La aplicación manage proporciona las funcionalidades administrativas propias de ProjectFlow.

Está relacionada principalmente con la gestión de:

- Usuarios;
- Proyectos;
- Equipos;
- Roles.

Su estructura es:

apps/manage/
├── forms.py
├── urls.py
└── views.py

## 10. Plantillas

Las plantillas HTML se encuentran en templates/

Están organizadas por funcionalidad:

templates/
├── common/
├── home/
├── kanban/
├── manage/
├── projects/
├── reports/
├── registration/
└── tasks/

Además existe una plantilla base templates/base.html

## 11. Archivos estáticos

Las plantillas HTML se encuentran en static/

Se dividen en:

static/
├── css/
├── js/
└── img/

Los archivos css y js están organizados en carpetas según sus funcionalidades.

## 12. Flujo de una petición

El flujo general de una petición HTTP es:

Usuario
   │
   ▼
  URL
   │
   ▼
config/urls.py
   │
   ▼
urls.py de la aplicación
   │
   ▼
views.py
   │
   ├── permissions.py
   ├── querysets.py
   ├── services/
   └── models.py
   │
   ▼
Contexto
   │
   ▼
Template HTML
   │
   ▼
Respuesta HTTP

## 13. Separación de responsabilidades

ProjectFlow intenta mantener una separación clara entre las diferentes responsabilidades.

| Archivo         | Responsabilidad                                                                         |
| --------------- | --------------------------------------------------------------------------------------- |
| models.py       | Representar y persistir los datos                                                       |
| views.py        | Recibir la petición, controlar el flujo y devolver la respuesta                         |
| forms.py        | Validar y procesar los datos introducidos por el usuario                                |
| querysets.py    | Centralizar consultas complejas o reutilizables                                         |
| permissions.py  | Determinar qué acciones puede realizar cada usuario                                     |

| Carpeta         | Responsabilidad                                                                         |
| --------------- | --------------------------------------------------------------------------------------- |
| services/       | Contener lógica de negocio o procesos que no deberían estar directamente en las vistas  |
| templates/      | Representar visualmente los datos recibidos del backend                                 |
| static/js/      | Gestionar interacciones del navegador y comportamiento dinámico de la interfaz          |

## 14. Acceso y permisos

El control de acceso se basa principalmente en los roles:

OWNER
MANAGER
MEMBER

El rol se determina en función de la relación del usuario con el proyecto.

Además, un usuario puede seguir un proyecto sin formar parte de su equipo.

Esto permite diferenciar entre:

Usuario asignado
        │
        └── acceso según su rol

Usuario seguidor
        │
        └── acceso de solo lectura

La lógica detallada de permisos se documenta en:

02 Permisos.md

## 15. Dashboard

El dashboard utiliza una combinación de consultas y servicios para construir la información que necesita cada usuario.

El flujo principal es:

home()
   │
   ▼
get_dashboard_context(user)
   │
   ├── proyectos
   ├── notificaciones
   ├── tareas
   └── plantillas
   │
   ▼
templates/home/home.html

El dashboard no obtiene directamente toda la información desde la plantilla.

La preparación de datos se realiza previamente en apps/home/services/dashboard.py

## 16. Internacionalización

ProjectFlow utiliza el sistema de internacionalización de Django.

Las traducciones se almacenan en:

locale/
├── en/
│   └── LC_MESSAGES/
│       └── django.po
└── es/
    └── LC_MESSAGES/
        └── django.po

Las cadenas traducibles se marcan en las plantillas mediante {% load i18n %} y {% translate "Texto" %}

El cambio de idioma se realiza mediante la vista set_language de Django.

La internacionalización se utiliza de forma selectiva para los elementos que necesitan traducción.

## 17. Base de datos

ProjectFlow utiliza Django ORM para acceder a la base de datos.

Las aplicaciones definen sus modelos y Django gestiona las migraciones correspondientes.

Las migraciones se encuentran dentro de cada aplicación:

apps/
└── <app>/
    └── migrations/

Las migraciones permiten evolucionar el esquema de la base de datos de forma controlada.

Los archivos de migración no contienen lógica de negocio de la aplicación, sino cambios estructurales del modelo de datos.

## 18. Entorno de ejecución

El proyecto utiliza un entorno virtual de Python env/

Este directorio contiene las dependencias instaladas y no forma parte del código fuente de ProjectFlow.

Por este motivo:

- No se documenta como parte de la arquitectura funcional;
- No debe incluirse en el control de versiones;
- No debe procesarse al generar traducciones;
- Sus paquetes no deben modificarse manualmente.

Las dependencias utilizadas por el proyecto se registran en requirements.txt

## 19. Principios utilizados

La arquitectura de ProjectFlow sigue principalmente estos principios:

- Separación de responsabilidades

Cada módulo intenta encargarse de una responsabilidad concreta.

- Reutilización

Las consultas y reglas comunes se centralizan en módulos reutilizables.

Ejemplos:

querysets.py
permissions.py
services/

- Modularidad

Cada aplicación Django representa una parte funcional de ProjectFlow.

- Bajo acoplamiento

Las aplicaciones se comunican mediante modelos, servicios y funciones bien definidas evitando duplicar lógica.

- Seguridad

Las operaciones sensibles se protegen mediante:

- Autenticación;
- Permisos;
- Comprobaciones de rol;
- Restricciones a nivel de proyecto;
- Protección CSRF de Django.

## 20. Resumen de la arquitectura

La arquitectura de ProjectFlow puede resumirse de la siguiente manera:

                    ┌─────────────────────┐
                    │       Usuario       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Django URLs      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Views         │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        Permissions       Querysets         Services
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Models        │
                    │     Django ORM      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Database       │
                    └─────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Templates      │
                    │   HTML + Bootstrap  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   CSS + JavaScript  │
                    └─────────────────────┘

En conjunto, ProjectFlow utiliza Django como núcleo de la aplicación, separando la lógica funcional en aplicaciones independientes y utilizando services, querysets y permissions para evitar concentrar toda la lógica en las vistas.
