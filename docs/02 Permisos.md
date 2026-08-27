# 02. Permisos de ProjectFlow

## 1. Introducción

ProjectFlow utiliza un sistema de permisos basado principalmente en el rol que un usuario tiene dentro de un proyecto.

Existen tres roles:

* `OWNER`
* `MANAGER`
* `MEMBER`

Además, los superusuarios de Django reciben automáticamente el tratamiento de `OWNER`.

Los permisos se aplican tanto a proyectos como a tareas.

---

## 2. Roles

### OWNER

El `OWNER` tiene el nivel de control más elevado.

Puede:

- Consultar proyectos;
- Crear proyectos;
- Editar proyectos;
- Eliminar proyectos;
- Archivar proyectos;
- Gestionar usuarios;
- Cambiar el propietario;
- Consultar tareas;
- Crear tareas;
- Editar tareas;
- Eliminar tareas;
- Asignar tareas.

---

### MANAGER

El `MANAGER` tiene permisos de gestión operativa.

Puede:

- Consultar proyectos;
- Editar proyectos;
- Gestionar usuarios;
- Consultar tareas;
- Crear tareas;
- Editar tareas;
- Eliminar tareas;
- Asignar tareas.

No puede:

- Crear proyectos;
- Eliminar proyectos;
- Archivar proyectos;
- Cambiar el propietario.

---

### MEMBER

El `MEMBER` participa en el trabajo del proyecto con permisos más limitados.

Puede:

- Consultar proyectos;
- Consultar tareas;
- Editar sus propias tareas asignadas.

No puede:

- Crear proyectos;
- Editar proyectos;
- Eliminar proyectos;
- Archivar proyectos;
- Gestionar usuarios;
- Cambiar el propietario;
- Crear tareas;
- Eliminar tareas;
- Asignar tareas.

---

## 3. Matriz general de permisos

| Permiso             | OWNER | MANAGER |     MEMBER     |
| ------------------- | ----- | ------- | -------------- |
| Ver proyecto        |   Sí  |    Sí   |       Sí       |
| Crear proyecto      |   Sí  |    No   |       No       |
| Editar proyecto     |   Sí  |    Sí   |       No       |
| Eliminar proyecto   |   Sí  |    No   |       No       |
| Archivar proyecto   |   Sí  |    No   |       No       |
| Gestionar usuarios  |   Sí  |    Sí   |       No       |
| Cambiar propietario |   Sí  |    No   |       No       |
| Ver tarea           |   Sí  |    Sí   |       Sí       |
| Crear tarea         |   Sí  |    Sí   |       No       |
| Editar tarea        |   Sí  |    Sí   | Solo asignadas |
| Eliminar tarea      |   Sí  |    Sí   |       No       |
| Asignar tarea       |   Sí  |    Sí   |       No       |

---

## 4. Acceso a proyectos

Además de los permisos concretos, ProjectFlow determina un modo de acceso para cada usuario.

Existen tres modos:

EDIT
READONLY
DENY

### EDIT

El usuario puede interactuar con el proyecto.

Este modo corresponde a:

* `OWNER`;
* `MANAGER`;
* `MEMBER` asignado al proyecto;
* superusuarios.

El modo `EDIT` no significa que el usuario pueda realizar todas las operaciones. Las acciones concretas siguen dependiendo de los permisos de su rol.

---

### READONLY

El usuario puede consultar el proyecto, pero no modificarlo.

Por ejemplo, un usuario que sigue un proyecto sin estar asignado a él puede acceder en modo `READONLY`.

---

### DENY

El usuario no tiene acceso al proyecto.

Se aplica cuando el usuario no tiene ninguna relación válida con el proyecto.

---

## 5. Acceso a tareas

El acceso a las tareas se determina según el rol, la asignación y la relación del usuario con el proyecto.

### OWNER

Tiene acceso de edición a las tareas.

### MANAGER

Tiene acceso de edición a las tareas.

### MEMBER

El comportamiento depende de la asignación:

MEMBER
  │
  ├── tarea asignada al usuario
  │ └── EDIT
  │
  └── tarea asignada a otro usuario
    └── READONLY


### Seguidor del proyecto

Un usuario que sigue el proyecto sin estar asignado a él dispone de acceso de solo lectura a sus tareas.

### Usuario sin relación

Un usuario que no está asignado al proyecto ni lo sigue no tiene acceso a sus tareas.

---

## 6. Creación de tareas

La creación de tareas está permitida para:

* `OWNER`;
* `MANAGER`.

Los `MEMBER` no tienen permiso general para crear tareas.

Además, un proyecto archivado no permite crear nuevas tareas.

---

## 7. Edición de tareas

Los `OWNER` y `MANAGER` pueden editar las tareas del proyecto.

Los `MEMBER` solamente pueden editar las tareas que tienen asignadas.

Por tanto:

OWNER
  → puede editar cualquier tarea

MANAGER
  → puede editar cualquier tarea

MEMBER
  → puede editar únicamente sus tareas asignadas

---

## 8. Asignación de tareas

La asignación de tareas está permitida para:

* `OWNER`;
* `MANAGER`.

Los `MEMBER` no pueden asignar tareas.

---

## 9. Gestión de usuarios

La gestión de usuarios dentro de los proyectos está permitida para:

* `OWNER`;
* `MANAGER`.

Los `MEMBER` no tienen permisos de gestión de usuarios.

---

## 10. Propietario del proyecto

Cambiar el propietario de un proyecto es una operación reservada al `OWNER`.

Los `MANAGER` y `MEMBER` no pueden realizar esta operación.

---

## 11. Eliminación y archivado

### Eliminar proyecto

Permitido para:

* `OWNER`.

No permitido para:

* `MANAGER`;
* `MEMBER`.

### Archivar proyecto

Permitido para:

* `OWNER`.

No permitido para:

* `MANAGER`;
* `MEMBER`.

---

## 12. Superusuarios

Los superusuarios de Django reciben automáticamente el rol `OWNER`.

Esto significa que las comprobaciones de permisos los tratan como usuarios con acceso completo.

---

## 13. Resumen de niveles de acceso

### Proyecto

                        ┌───────────────┐
                        │    PROYECTO   │
                        └───────┬───────┘
                                │
              ┌─────────────────┼───────────┐
              │                 │           │
            EDIT             READONLY      DENY
              │                 │           │
       ┌──────┼──────┐          │           │
       │      │      │          │           │
     OWNER MANAGER MEMBER   FOLLOWER   SIN RELACIÓN
                     │
                  asignado

### Tarea

                        ┌──────────────┐
                        │     TAREA    │
                        └───────┬──────┘
                                │
              ┌─────────────────┼───────────┐
              │                 │           │
            EDIT             READONLY      DENY
              │                 │           │
       ┌──────┼──────┐          │           │
       │      │      │          │           │
     OWNER MANAGER MEMBER   FOLLOWER   SIN RELACIÓN
                     │
               tarea asignada

---

## 14. Regla fundamental

Los permisos de ProjectFlow deben entenderse en dos niveles:

1. **Rol:** determina qué operaciones puede realizar el usuario.
2. **Relación con el proyecto o tarea:** determina sobre qué elementos puede realizar esas operaciones.

Por tanto, disponer de un determinado rol no implica automáticamente tener acceso a todos los proyectos de la aplicación.

El sistema combina ambos factores para determinar el acceso final.
