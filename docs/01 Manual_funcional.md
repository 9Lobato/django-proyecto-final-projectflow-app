# Manual funcional de ProjectFlow

## 1. Introducción

ProjectFlow es una aplicación web para la gestión de proyectos, tareas y equipos de trabajo.

La aplicación permite:

- Gestionar proyectos;
- Gestionar tareas;
- Organizar tareas mediante un tablero Kanban;
- Consultar informes;
- Gestionar usuarios y equipos;
- Recibir y gestionar notificaciones;
- Utilizar plantillas de proyectos;
- Trabajar con diferentes roles y permisos;
- Seguir proyectos para consultar su evolución.

El acceso y las acciones disponibles dependen del rol del usuario y de su relación con cada proyecto.

---

## 2. Usuarios y roles

ProjectFlow utiliza tres roles principales:

* OWNER: responsable de la administración y gestión completa.
* MANAGER: responsable de la gestión operativa de los proyectos.
* MEMBER: usuario que participa en el trabajo del proyecto.

Los superusuarios de Django se consideran automáticamente como OWNER.

---

## 3. Inicio de sesión

Los usuarios deben autenticarse para acceder a las funcionalidades de ProjectFlow.

La aplicación dispone de:

- Página de inicio de sesión;
- Cierre de sesión;
- Identificación del usuario autenticado;
- Selección de la página inicial según el rol.

### Página inicial según el rol

| Rol     | Página inicial  |
|---------|-----------------|
| Owner   | Gestión         |
| Manager | Proyectos       |
| Member  | Dashboard       |

Si un usuario no tiene una asignación de proyecto que determine su rol, se utiliza MEMBER como rol por defecto para determinar la página inicial.

---

## 4. Dashboard

El Dashboard constituye la página principal de trabajo para los usuarios que acceden a ella.

Su contenido se adapta al usuario y a los proyectos con los que tiene relación.

El Dashboard proporciona principalmente:

- Proyectos disponibles para el usuario;
- Notificaciones relacionadas con sus proyectos;
- Información sobre plantillas de proyectos.

### 4.1 Proyectos

Los superusuarios pueden acceder a todos los proyectos.

Para el resto de usuarios, el Dashboard muestra los proyectos en los que están asignados o son seguidores.

Los proyectos se presentan junto con información calculada sobre sus tareas, como el número total de tareas y las tareas completadas.

### 4.2 Notificaciones

El Dashboard agrupa las notificaciones por proyecto.

Las acciones disponibles sobre una notificación dependen de los permisos del usuario.

Entre las operaciones contempladas por el sistema se encuentran:

- Eliminar una solicitud;
- Resolver una solicitud;
- Reabrir una solicitud;
- Eliminar una notificación.

### 4.3 Plantillas

El Dashboard también muestra las plantillas de proyectos.

Para cada plantilla se dispone de información sobre:

- Número de proyectos asociados;
- Número de tareas asociadas.

Las plantillas se ordenan dando prioridad a las que tienen un
mayor número de proyectos asociados.

---

## 5. Proyectos

La sección de proyectos permite consultar y gestionar los proyectos a los que el usuario tiene acceso.

Los proyectos contienen información relacionada con:

- Propietario;
- Miembros o asignaciones;
- Tareas;
- Seguidores;
- Plantilla de origen;
- Estado de archivado.

Las operaciones que puede realizar cada usuario dependen de su rol.

---

## 6. Tareas

Las tareas pertenecen a un proyecto y representan unidades de trabajo.

Los usuarios pueden consultar las tareas de los proyectos a los que tienen acceso.

Dependiendo del rol y de la asignación de la tarea, un usuario puede:

- Crear tareas;
- Editar tareas;
- Eliminar tareas;
- Asignar tareas a usuarios.

Los miembros tienen un acceso más limitado y pueden editar sus propias tareas asignadas.

---

## 7. Kanban

El tablero Kanban proporciona una representación visual de las tareas de un proyecto.

Las tareas se organizan según su estado de trabajo.

El objetivo del tablero es facilitar:

- La visualización del trabajo pendiente;
- La identificación del estado actual de cada tarea;
- El seguimiento del progreso;
- La gestión visual del flujo de trabajo.

Las operaciones disponibles dependen de los permisos del usuario.

---

## 8. Informes

La sección de informes proporciona información agregada sobre los proyectos y sus tareas.

Está orientada principalmente al seguimiento y análisis del trabajo realizado.

Entre la información que puede proporcionar se encuentran:

- Tareas;
- Estados;
- Usuarios;
- Progreso de proyectos;
- Métricas de actividad.

Los informes están disponibles para los roles que tengan acceso a esta funcionalidad.

---

## 9. Gestión

La sección de gestión proporciona funcionalidades administrativas de ProjectFlow.

Está destinada principalmente a usuarios con permisos de administración.

Permite gestionar elementos relacionados con:

- Usuarios;
- Proyectos;
- Equipos;
- Plantillas;
- Asignaciones.

Las operaciones disponibles dependen del rol del usuario.

---

## 10. Seguimiento de proyectos

Los usuarios pueden seguir proyectos.

Seguir un proyecto permite consultar información del mismo sin necesidad de estar asignado directamente a él.

Los usuarios que siguen un proyecto pueden disponer de acceso de solo lectura cuando no tienen una asignación dentro del proyecto.

---

## 11. Archivado de proyectos

Los proyectos pueden ser archivados por usuarios con los permisos correspondientes.

Un proyecto archivado continúa formando parte de la aplicación, pero determinadas operaciones quedan restringidas.

Por ejemplo, no se pueden crear nuevas tareas en un proyecto archivado.

---

## 12. Internacionalización

ProjectFlow incorpora soporte para traducciones mediante el sistema de internacionalización de Django.

Las traducciones se gestionan mediante archivos .po situados en:

locale/
├── en/
│ └── LC_MESSAGES/
│   └── django.po
└── es/
  └── LC_MESSAGES/
    └── django.po

Las cadenas traducibles se marcan en las plantillas mediante las herramientas de internacionalización de Django.

El idioma puede seleccionarse desde el menú correspondiente de la aplicación.

## 13. Resumen de funcionalidades

| Funcionalidad         | Descripción                                           |
|-----------------------|-------------------------------------------------------|
| Inicio de sesión      | Autenticación de usuarios                             |
| Dashboard             | Vista general personalizada                           |
| Proyectos             | Consulta y gestión de proyectos                       |
| Tareas                | Gestión del trabajo de los proyectos                  |
| Kanban                | Visualización del flujo de tareas                     |
| Informes              | Análisis y métricas                                   |
| Gestión               | Administración de usuarios, proyectos y plantillas    |
| Seguimiento           | Consulta de proyectos seguidos                        |
| Plantillas            | Creación y reutilización de estructuras de proyectos  |
| Internacionalización  | Soporte para diferentes idiomas                       |

---

## 14. Arquitectura funcional

Desde el punto de vista funcional, ProjectFlow puede representarse de la siguiente manera:

                         ProjectFlow
                              │
          ┌───────────────────┼────────────────────┐
          │                   │                    │
      Dashboard           Proyectos             Gestión
          │                   │                    │
          │              ┌────┴──────┐             │
          │              │           │             │
          │            Tareas   Seguimiento    Usuarios
          │              │                     Equipos
          │           Kanban                   Plantillas
          │
          └───────── Informes

El acceso a cada funcionalidad está condicionado por los permisos del usuario.
