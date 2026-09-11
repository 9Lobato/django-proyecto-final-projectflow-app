# 02. Permisos y roles de ProjectFlow

## 1. Introducción

ProjectFlow utiliza un sistema de roles y permisos para controlar el acceso de los usuarios a proyectos, tareas y operaciones de gestión.

Los permisos se aplican principalmente en el backend Django.

El frontend puede adaptar la interfaz según las capacidades del usuario, pero la interfaz no constituye el mecanismo de autorización.

La regla fundamental es:

Interfaz → informa y limita visualmente
Backend  → autoriza o rechaza

Un usuario no obtiene permisos adicionales modificando la interfaz o realizando directamente una petición HTTP.

---

## 2. Roles principales

ProjectFlow utiliza tres roles principales dentro de los proyectos:

- OWNER
- MANAGER
- MEMBER

El rol determina las operaciones que el usuario puede realizar sobre un proyecto y sus tareas.

---

## 3. Owner

El OWNER es el propietario del proyecto.

Dispone del mayor nivel de control sobre el proyecto dentro del sistema de permisos de ProjectFlow.

Entre sus capacidades se encuentran, según la operación:

- Consultar el proyecto.
- Gestionar el proyecto.
- Gestionar sus tareas.
- Gestionar asignaciones.
- Realizar operaciones de administración del proyecto.
- Modificar o eliminar el proyecto cuando la operación esté permitida.
- Gestionar el estado de archivado.
- Utilizar las funcionalidades disponibles para la gestión del proyecto.

Las operaciones concretas continúan estando validadas por Django.

---

## 4. Manager

El MANAGER es un usuario con responsabilidades de gestión dentro de un proyecto.

Puede realizar las operaciones de gestión que correspondan a su rol y a su asignación al proyecto.

Entre sus capacidades se encuentran:

- Consultar el proyecto.
- Consultar y gestionar tareas según sus permisos.
- Participar en la gestión del proyecto.
- Realizar operaciones Kanban permitidas.
- Seguir proyectos cuando la lógica de ProjectFlow lo permite.
- Utilizar las funcionalidades disponibles para gestores.

El backend comprueba que el usuario tenga realmente el rol necesario antes de ejecutar una operación.

---

## 5. Member

El MEMBER es un usuario que participa en un proyecto.

Dispone de acceso a las funcionalidades correspondientes a su participación en el proyecto.

Puede, según las reglas de la aplicación:

- Consultar el proyecto.
- Consultar las tareas disponibles.
- Trabajar con las tareas que tiene permitido modificar.
- Utilizar el Kanban.
- Realizar transiciones de tareas permitidas.
- Utilizar las funcionalidades de consulta disponibles para miembros.

Las operaciones que requieren permisos superiores no están disponibles para un MEMBER.

---

## 6. Acceso a proyectos

El acceso a un proyecto depende de la relación del usuario con dicho proyecto.

Un usuario puede tener acceso por diferentes motivos, entre ellos:

- Ser propietario.
- Estar asignado al proyecto.
- Tener un rol de gestión.
- Disponer de permisos administrativos.

La aplicación determina los proyectos visibles para cada usuario antes de mostrar la información.

Por tanto:

Usuario
   ↓
Relación con proyecto
   ↓
Rol / permisos
   ↓
Proyectos accesibles

---

## 7. Acceso a tareas

El acceso a las tareas está relacionado con el acceso al proyecto al que pertenecen.

Las tareas no deben considerarse accesibles únicamente porque exista una URL o endpoint que permita localizarlas.

Django comprueba la relación del usuario con el proyecto y los permisos correspondientes.

De esta forma:

Usuario
   ↓
Acceso al proyecto
   ↓
Permisos sobre el proyecto/tarea
   ↓
Tarea accesible

---

## 8. Crear proyectos

La creación de proyectos está limitada a los usuarios que disponen de permisos para realizar esta operación.

La autorización se realiza en Django.

React o cualquier otro elemento de la interfaz puede ocultar la opción para usuarios que no tengan permiso, pero la comprobación definitiva se realiza en el backend.

---

## 9. Editar proyectos

La edición de un proyecto requiere permisos suficientes sobre dicho proyecto.

Django comprueba:

- Usuario autenticado.
- Proyecto existente.
- Relación del usuario con el proyecto.
- Rol y permisos correspondientes.

Si las condiciones no se cumplen, la operación es rechazada.

---

## 10. Eliminar proyectos

La eliminación de proyectos está restringida a los usuarios autorizados.

La operación no depende únicamente de que aparezca un botón de eliminación en la interfaz.

El backend realiza la comprobación antes de ejecutar la modificación.

---

## 11. Archivar proyectos

El archivado y desarchivado de proyectos requiere los permisos correspondientes.

El estado de archivado se modifica mediante Django.

Las interfaces React o Django pueden reflejar visualmente el estado, pero la autorización se realiza en el backend.

---

## 12. Seguir proyectos

El seguimiento de proyectos tiene reglas específicas.

Los usuarios con capacidad de gestión pueden seguir proyectos cuando cumplen las condiciones establecidas por la aplicación.

En particular, la lógica actual permite el seguimiento por parte de un usuario de gestión cuando no está asignado al proyecto.

La operación se valida en Django.

El estado de seguimiento se almacena en la base de datos.

---

## 13. Tareas y permisos

Las tareas heredan parte de su contexto de permisos del proyecto al que pertenecen.

Las operaciones disponibles pueden depender de:

- Rol del usuario.
- Relación con el proyecto.
- Asignación a la tarea.
- Estado actual de la tarea.
- Operación que se intenta realizar.

Por ello, no todas las tareas tienen necesariamente las mismas posibilidades de modificación para todos los usuarios.

---

## 14. Cambio de estado en Kanban

El cambio de estado de una tarea está sujeto a dos condiciones:

1. El usuario debe tener permisos para modificar la tarea.
2. La transición entre los estados debe ser válida.

Por ejemplo:

Usuario
   ↓
¿Puede modificar la tarea?
   ↓
Sí
   ↓
¿La transición es válida?
   ↓
Sí
   ↓
Cambiar estado

Si cualquiera de las comprobaciones falla, el cambio no se realiza.

---

## 15. Transiciones de estado

El Kanban no permite realizar cualquier transición arbitraria.

Las transiciones se validan en el backend.

Una operación inválida no debe modificar la tarea aunque el usuario consiga enviar manualmente una petición.

La interfaz puede impedir o indicar visualmente determinadas acciones, pero Django mantiene la validación definitiva.

---

## 16. Copiar tareas

La copia de una tarea a otro proyecto requiere permisos suficientes.

El usuario debe tener autorización para realizar la operación y para utilizar el proyecto de destino correspondiente.

El flujo es:

Seleccionar tarea
      ↓
Seleccionar destino
      ↓
Petición a Django
      ↓
Comprobación de permisos
      ↓
¿Permitido?
   ┌──┴──┐
  Sí     No
  ↓       ↓
Copiar   Rechazar

La tarea original no se modifica como consecuencia de una copia válida.

---

## 17. APIs y permisos

Las APIs utilizadas por React están sujetas a las mismas reglas de autorización que las funcionalidades tradicionales de Django.

Por ejemplo:

/api/workflow/
/kanban/move/
/kanban/copy/
/projects/follow/api/
/projects/archive/api/

Una petición realizada directamente contra una API no evita las comprobaciones de permisos.

Esto es especialmente importante porque React es únicamente el cliente que realiza la petición.

La seguridad permanece en Django.

---

## 18. React y autorización

React puede utilizar la información proporcionada por Django para adaptar la interfaz.

Por ejemplo:

Usuario sin permiso
        ↓
React oculta acción

Usuario con permiso
        ↓
React muestra acción

Sin embargo, este comportamiento es únicamente de presentación.

La validación real es:

React
   ↓
Petición
   ↓
Django
   ↓
Comprobación de permisos
   ↓
Operación

Por este motivo, nunca debe implementarse una regla de seguridad únicamente en React.

---

## 19. Autenticación

Las funcionalidades protegidas requieren que el usuario esté autenticado.

Django gestiona la autenticación mediante su sistema de usuarios y sesiones.

Si un usuario no autenticado intenta acceder a una funcionalidad protegida, el sistema no debe permitir la operación.

La autenticación y la autorización son conceptos diferentes:

Autenticación
→ ¿Quién es el usuario?

Autorización
→ ¿Qué puede hacer ese usuario?

---

## 20. Workflow y permisos

El progreso del workflow está asociado al usuario mediante el modelo WorkflowProgress.

Cada usuario mantiene su propio progreso.

El acceso a este progreso requiere una sesión autenticada.

El usuario puede consultar y modificar su propio progreso mediante:

GET /api/workflow/
POST /api/workflow/

El progreso de un usuario no debe utilizarse como mecanismo para acceder al progreso de otro usuario.

---

## 21. Sesiones y cierre de sesión

Cuando un usuario cierra sesión, pierde el acceso a las funcionalidades protegidas.

Sin embargo, los datos persistentes asociados al usuario no se eliminan automáticamente.

Por ejemplo, el progreso del workflow almacenado en WorkflowProgress permanece en la base de datos.

Cuando el usuario vuelve a iniciar sesión, Django vuelve a identificarlo y puede recuperar sus datos persistentes.

---

## 22. Superusuario

El sistema distingue el usuario administrador/superusuario de los roles funcionales utilizados dentro de los proyectos.

Un superusuario dispone de capacidades administrativas adicionales proporcionadas por Django.

Las comprobaciones de permisos específicas del proyecto deben seguir respetándose en las funcionalidades donde corresponda.

No debe confundirse:

Superusuario Django
        ≠
OWNER de un proyecto

Son conceptos relacionados con niveles de autorización diferentes.

---

## 23. Principio de mínimo privilegio

ProjectFlow sigue el principio de conceder a cada usuario únicamente las capacidades necesarias para su función.

De forma conceptual:

OWNER
  ↓
Mayor capacidad de gestión

MANAGER
  ↓
Capacidad de gestión dentro de sus proyectos

MEMBER
  ↓
Capacidad de participación y trabajo

Las capacidades exactas dependen de la relación del usuario con cada proyecto.

---

## 24. Resumen de permisos

Operación	                              OWNER             MANAGER             MEMBER
Consultar proyecto accesible	            ✓                  ✓                  ✓
Consultar tareas accesibles	              ✓                  ✓                  ✓
Gestionar proyecto	                      ✓           Según permisos            —
Gestionar tareas	                        ✓           Según permisos     Según permisos
Utilizar Kanban	                          ✓                  ✓                  ✓
Cambiar estados permitidos	              ✓                  ✓                  ✓
Copiar tareas	                     Según permisos     Según permisos     Según permisos
Seguir proyecto	                    Según reglas	     Según reglas       Según reglas
Archivar proyecto                  Según permisos     Según permisos            —
Administrar usuarios/proyectos	   Según permisos     Según permisos            —

La tabla representa el modelo funcional general. La autorización definitiva siempre corresponde a las reglas implementadas en Django.

---

## 25. Principio de seguridad

El principio fundamental de ProjectFlow es:

NO CONFIAR EN EL FRONTEND

Que una acción:

- aparezca,
- desaparezca,
- esté deshabilitada,
- sea posible mediante JavaScript,
- o no esté disponible visualmente,

no determina por sí solo si el usuario está autorizado.

La decisión definitiva se toma en el backend.

        USUARIO
            ↓
      React / Web
            ↓
        Django
            ↓
  Autenticación
            ↓
      Autorización
            ↓
  Lógica de negocio
            ↓
  Base de datos

Esta separación permite mantener las reglas de seguridad independientemente del cliente utilizado para acceder a la aplicación.

---

## 26. Conclusión

El sistema de permisos de ProjectFlow se basa en los roles y relaciones del usuario con los proyectos y tareas.

Django mantiene la responsabilidad sobre:

- Autenticación.
- Autorización.
- Roles.
- Acceso a proyectos.
- Acceso a tareas.
- Operaciones de modificación.
- Validación de transiciones.
- Seguridad de las APIs.

React adapta la interfaz a las capacidades conocidas del usuario, pero no sustituye las comprobaciones realizadas por el backend.

De esta manera, la incorporación de React no modifica el principio fundamental de seguridad de ProjectFlow: los permisos se hacen cumplir en el servidor.
