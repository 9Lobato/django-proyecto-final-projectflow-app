# Manual funcional de ProjectFlow

## 1. Introducción

ProjectFlow es una aplicación web para la gestión de proyectos y tareas.

La aplicación permite:

- Gestionar proyectos.
- Gestionar tareas.
- Organizar tareas mediante un tablero Kanban.
- Asignar usuarios a proyectos y tareas.
- Aplicar filtros y búsquedas.
- Seguir proyectos.
- Archivar proyectos.
- Consultar informes.
- Utilizar un workflow de seguimiento del proyecto.
- Trabajar con diferentes idiomas.
- Gestionar las funcionalidades según el rol del usuario.

La aplicación utiliza Django como backend y combina páginas renderizadas por Django con interfaces dinámicas desarrolladas mediante React.

---

## 2. Acceso a la aplicación

El acceso se realiza mediante la pantalla de inicio de sesión.

El usuario debe introducir sus credenciales para acceder a las funcionalidades protegidas de ProjectFlow.

Una vez autenticado, la aplicación mantiene la sesión mediante el sistema de autenticación de Django.

Si el usuario intenta acceder a una sección protegida sin haber iniciado sesión, será redirigido al login.

---

## 3. Navegación

La navegación principal se encuentra en la barra superior de la aplicación.

Dependiendo del usuario y de sus permisos, pueden aparecer diferentes opciones.

Entre ellas:

- Inicio.
- Workflow / guía.
- Proyectos.
- Tareas.
- Kanban.
- Informes.
- Gestión.
- Cambio de idioma.
- Cierre de sesión.

Las opciones disponibles pueden variar según el rol y los permisos del usuario.

La navegación se obtiene dinámicamente desde el backend para mantener la información relacionada con el usuario autenticado.

---

## 4. Inicio / Workflow

La sección /start/ proporciona una guía de trabajo para el usuario.

El workflow está organizado en pasos que pueden marcarse como completados.

El usuario puede:

- Consultar los diferentes pasos.
- Marcar un paso como completado.
- Desmarcar un paso.
- Continuar el workflow en diferentes momentos.

El progreso se guarda asociado al usuario.

Persistencia del workflow

El estado de los pasos se almacena en el backend mediante WorkflowProgress.

Por este motivo, los pasos marcados permanecen:

- Después de recargar la página.
- Después de cerrar sesión.
- Después de volver a iniciar sesión.

El progreso no depende únicamente del navegador o del almacenamiento local.

El funcionamiento general es:

Usuario
   ↓
Workflow
   ↓
React
   ↓
API Django
   ↓
WorkflowProgress
   ↓
Base de datos

---

## 5. Proyectos

La sección de proyectos permite consultar los proyectos a los que el usuario tiene acceso.

Los proyectos muestran información relevante como:

- Nombre.
- Código.
- Descripción.
- Responsable.
- Tareas.
- Estado.
- Información relacionada con asignaciones y seguimiento.

Los proyectos se organizan según la relación del usuario con ellos.

## 5.1. Búsqueda de proyectos

La lista de proyectos dispone de búsqueda.

El usuario puede introducir texto para localizar proyectos por:

- Nombre.
- Descripción.

La búsqueda se ejecuta sobre los proyectos disponibles para el usuario.

Al eliminar el texto de búsqueda se recupera la lista normal de proyectos.

Si una búsqueda no devuelve resultados, se muestra el mensaje correspondiente indicando que no existen proyectos para los valores buscados.

---

## 6. Gestión de proyectos

Los usuarios con permisos suficientes pueden realizar operaciones de gestión sobre los proyectos.

Entre las operaciones disponibles se encuentran:

- Crear proyectos.
- Editar proyectos.
- Eliminar proyectos.
- Archivar y desarchivar proyectos.
- Convertir proyectos en plantillas cuando corresponda.

Las operaciones están protegidas mediante los permisos definidos en Django.

Un usuario no puede realizar una operación simplemente modificando la interfaz del navegador si no dispone de autorización en el backend.

---

## 7. Seguimiento de proyectos

Los usuarios que tienen permisos para ello pueden seguir un proyecto.

El seguimiento permite mantener un proyecto identificado como relevante para el usuario.

El usuario puede:

- Seguir un proyecto.
- Dejar de seguirlo.
- Consultar visualmente su estado de seguimiento.

El estado de seguimiento se almacena en la base de datos y permanece después de recargar la página.

---

## 8. Archivado de proyectos

Los proyectos pueden archivarse cuando el usuario dispone de los permisos necesarios.

El archivado permite retirar un proyecto del flujo habitual de trabajo sin eliminar necesariamente toda su información.

También es posible desarchivar un proyecto cuando corresponda.

Las operaciones de archivado se validan en Django.

---

## 9. Tareas

La sección de tareas permite consultar y gestionar las tareas asociadas a los proyectos.

Las tareas pueden contener información como:

- Título.
- Descripción.
- Proyecto.
- Responsable.
- Creador.
- Estado.
- Prioridad.
- Tipo de entrega.
- Fechas relevantes.

La información visible depende de los permisos y de la relación del usuario con los proyectos correspondientes.

---

## 10. Búsqueda de tareas

La lista de tareas permite buscar por texto.

La búsqueda se realiza sobre:

- Título.
- Descripción.

Los resultados se actualizan mostrando únicamente las tareas que coinciden con los valores buscados.

Al eliminar la búsqueda se recupera la lista normal de tareas.

---

## 11. Filtros de tareas

La sección de tareas permite utilizar diferentes filtros.

Entre ellos:

- Creador.
- Responsable.
- Estado.
- Tipo de entrega.
- Prioridad.

Los filtros pueden utilizarse individualmente o combinados.

Por ejemplo, es posible filtrar simultáneamente por:

Estado = IN_PROGRESS
Prioridad = HIGH

En este caso únicamente se muestran las tareas que cumplen ambas condiciones.

Los filtros pueden eliminarse individualmente para recuperar progresivamente los resultados.

---

## 12. Kanban

El Kanban permite visualizar las tareas organizadas por estado.

Las columnas representan los diferentes estados de trabajo.

El usuario puede consultar las tareas de forma visual y moverlas entre columnas cuando la operación esté permitida.

La interfaz Kanban utiliza React para proporcionar una interacción dinámica.

---

## 13. Drag & Drop en Kanban

Las tareas pueden desplazarse mediante drag & drop.

El usuario puede:

- Seleccionar una tarea.
- Arrastrarla.
- Colocarla sobre una columna válida.
- Confirmar visualmente el nuevo estado.
- El backend actualiza la tarea.

El cambio de estado se guarda en la base de datos.

Por tanto, después de recargar la página la tarea mantiene el nuevo estado.

---

## 14. Transiciones de estado

No todas las transiciones entre estados están permitidas.

El sistema valida las transiciones antes de modificar la tarea.

Cuando una transición no es válida:

- La interfaz indica que el destino no es válido.
- La tarea no cambia de estado.
- El estado anterior permanece.
- La información persistida en la base de datos no se modifica.

Las reglas de transición se aplican en el backend.

---

## 15. Copiar tareas

El Kanban permite copiar una tarea a otro proyecto cuando el usuario dispone de los permisos necesarios.

El flujo es:

1. Seleccionar la acción de copiar.
2. Elegir el proyecto de destino permitido.
3. Confirmar la operación.
4. Django crea la nueva tarea.
5. La tarea original permanece sin modificaciones.

La tarea copiada aparece en el proyecto de destino.

La autorización para copiar una tarea se comprueba en Django.

---

## 16. Búsqueda en Kanban

El Kanban dispone de búsqueda de tareas.

La búsqueda permite localizar tareas por texto sin abandonar la vista del tablero.

Los resultados se reflejan en las diferentes columnas manteniendo la estructura del Kanban.

Al eliminar la búsqueda se recuperan las tareas correspondientes a la vista normal.

---

## 17. Roles y permisos

ProjectFlow utiliza diferentes roles para controlar el acceso a proyectos y operaciones.

Los roles principales son:

- OWNER
- MANAGER
- MEMBER

Cada rol dispone de diferentes capacidades.

Las reglas detalladas de permisos se encuentran documentadas en:

docs/02 Permisos.md

Los permisos se comprueban en el backend Django.

La interfaz puede ocultar o mostrar acciones dependiendo de las capacidades del usuario, pero esta presentación no sustituye la validación del backend.

---

## 18. Informes

La aplicación dispone de una sección de informes.

Los informes permiten consultar información agregada relacionada con los proyectos y las tareas.

El acceso y la información disponible dependen de los permisos del usuario.

---

## 19. Gestión

Los usuarios con permisos administrativos pueden acceder a las funcionalidades de gestión disponibles en la aplicación.

Estas funcionalidades permiten administrar determinados elementos de ProjectFlow según el rol y las autorizaciones correspondientes.

Las operaciones administrativas están protegidas por Django.

---

## 20. Internacionalización

ProjectFlow dispone de soporte para diferentes idiomas.

El usuario puede cambiar el idioma desde la navegación de la aplicación.

Al cambiar el idioma:

- Se actualizan los textos traducibles.
- La navegación se adapta al idioma seleccionado.
- El usuario puede volver posteriormente al idioma anterior.

Actualmente se utiliza el sistema de internacionalización de Django.

---

## 21. Cierre de sesión

El usuario puede cerrar la sesión mediante la opción correspondiente de la navegación.

Al cerrar sesión:

- La sesión autenticada deja de estar disponible.
- Las páginas protegidas requieren volver a iniciar sesión.
- El usuario es redirigido a la pantalla de login.

Los datos persistentes asociados al usuario no se eliminan al cerrar sesión.

Esto incluye, entre otros datos, el progreso guardado del workflow.

---

## 22. Seguridad

Las operaciones que modifican información están protegidas mediante Django.

La aplicación utiliza:

- Autenticación.
- Sesiones.
- Control de permisos.
- Protección CSRF.
- Validaciones en el backend.

Las APIs utilizadas por React forman parte del mismo sistema de seguridad.

React no sustituye las comprobaciones de seguridad realizadas por Django.

---

## 23. Comportamiento general del frontend

Las funcionalidades integradas con React permiten actualizar determinadas partes de la interfaz de forma dinámica.

El frontend React se comunica con Django mediante APIs JSON.

De forma simplificada:

Usuario
   ↓
Interfaz React
   ↓
Petición HTTP
   ↓
API Django
   ↓
Validación / lógica de negocio
   ↓
Base de datos
   ↓
Respuesta JSON
   ↓
React
   ↓
Actualización de la interfaz

Las páginas que todavía utilizan templates Django continúan funcionando mediante el flujo tradicional de Django.

---

## 24. Resumen funcional

Las principales funcionalidades actuales de ProjectFlow son:

Funcionalidad               Disponible
Login / logout                  Sí
Navegación según usuario	      Sí
Workflow                        Sí
Persistencia del workflow       Sí
Gestión de proyectos            Sí
Búsqueda de proyectos           Sí
Seguimiento de proyectos	      Sí
Archivado de proyectos          Sí
Gestión de tareas               Sí
Búsqueda de tareas              Sí
Filtros de tareas               Sí
Kanban                          Sí
Drag & Drop                     Sí
Validación de transiciones	    Sí
Copia de tareas                 Sí
Búsqueda en Kanban              Sí
Informes                        Sí
Gestión                         Sí
Internacionalización            Sí
Control de permisos             Sí

---

## 25. Flujo general de trabajo

Un flujo habitual de uso de ProjectFlow puede ser:

1. Iniciar sesión
        ↓
2. Consultar el workflow
        ↓
3. Seleccionar un proyecto
        ↓
4. Consultar sus tareas
        ↓
5. Filtrar o buscar tareas
        ↓
6. Trabajar con las tareas
        ↓
7. Utilizar el Kanban
        ↓
8. Actualizar estados
        ↓
9. Seguir o archivar proyectos
        ↓
10. Consultar informes
        ↓
11. Cerrar sesión

El progreso del workflow y los cambios realizados sobre proyectos y tareas se mantienen en el backend cuando la operación correspondiente ha sido completada correctamente.

---

## 26. Conclusión

ProjectFlow proporciona una plataforma integrada para la gestión de proyectos y tareas.

La aplicación combina:

- Django para backend, seguridad, permisos y persistencia.
- React para las interfaces dinámicas.
- Vite para el desarrollo y compilación del frontend.
- Django Templates y recursos estáticos para las partes que continúan utilizando la arquitectura tradicional.

El usuario puede gestionar proyectos y tareas, trabajar con el Kanban, realizar búsquedas y filtros, seguir y archivar proyectos, utilizar el workflow y consultar informes, siempre dentro de los permisos asociados a su usuario.
