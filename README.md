📌 Proyecto final — App ProjectFlow Gestor de proyectos

ProjectFlow es una aplicación web desarrollada con Django para la gestión y seguimiento de proyectos, equipos y tareas.
Django proporciona el backend, la lógica de negocio, la persistencia y la API utilizada por las vistas React.
La aplicación permite organizar proyectos mediante tareas y tableros Kanban, gestionar equipos y roles, controlar permisos de acceso, utilizar plantillas reutilizables y consultar información sobre el progreso mediante informes y métricas.
El objetivo del proyecto es consolidar el desarrollo de una aplicación web completa con Django, aplicando una arquitectura modular, gestión de usuarios y permisos, persistencia de datos mediante ORM, formularios, plantillas, servicios y funcionalidades de seguimiento y análisis.

✨ Características

- Gestión de proyectos
- Gestión de tareas
- Tablero Kanban
- Gestión de equipos y miembros
- Roles y permisos
- Asignación de tareas a usuarios
- Seguimiento del estado de las tareas
- Fechas de inicio, finalización y cancelación
- Estimación y control del tiempo de las tareas
- Comentarios y seguimiento de actividad
- Seguimiento de proyectos
- Archivado de proyectos
- Seguimiento de proyectos mediante favoritos
- Plantillas de proyectos y tareas
- Generación de proyectos a partir de plantillas
- Dashboard de proyectos y tareas
- Informes y métricas
- Exportación de información
- Generación de informes en PDF
- Internacionalización mediante traducciones
- Datos de demostración para facilitar la presentación del proyecto


🧩 Funcionalidades principales

1. Gestión de proyectos

Permite crear y administrar proyectos, incluyendo información básica, equipo de trabajo, estado y seguimiento.

Los proyectos pueden:
- Crear y editar información.
- Asignar miembros y roles.
- Contener múltiples tareas.
- Marcarse como archivados.
- Consultarse mediante diferentes vistas.
- Seguirse para facilitar su acceso.

2. Gestión de tareas

Las tareas permiten organizar el trabajo dentro de cada proyecto.

Incluyen funcionalidades como:
- Título y descripción.
- Estado y fase de trabajo.
- Usuario asignado.
- Proyecto asociado.
- Fecha de creación.
- Fecha prevista.
- Inicio y finalización.
- Cancelación.
- Estimación de tiempo.
- Seguimiento del tiempo restante.
- Número de secuencia.
- Comentarios.
- Seguimiento por usuarios.

3. Tablero Kanban

ProjectFlow incorpora un tablero Kanban para visualizar las tareas según su estado y facilitar la organización del trabajo.
Permite trabajar de forma visual con el flujo de tareas dentro de cada proyecto.

4. Equipos, roles y permisos

La aplicación dispone de un sistema de gestión de equipos y permisos.

Permite:
- Añadir usuarios a proyectos.
- Asignar diferentes roles.
- Controlar las acciones disponibles según los permisos.
- Gestionar miembros del equipo.
- Restringir determinadas operaciones según el contexto del proyecto.

5. Plantillas

ProjectFlow permite crear plantillas reutilizables para acelerar la creación de nuevos proyectos.

Las plantillas pueden contener:
- Información del proyecto.
- Tareas predefinidas.
- Configuración reutilizable.
- Información descriptiva sobre el tipo de proyecto.

A partir de una plantilla se puede generar un nuevo proyecto con su estructura inicial.

6. Seguimiento y actividad

La aplicación incorpora diferentes mecanismos para realizar el seguimiento de proyectos y tareas.

Entre ellos:
- Estados de las tareas.
- Fechas de inicio y finalización.
- Tiempo estimado.
- Tiempo restante.
- Comentarios.
- Seguimiento de proyectos.
- Archivado de proyectos.

7. Dashboard e informes

ProjectFlow incluye vistas de información y análisis para consultar el estado de los proyectos.

Los informes permiten consultar métricas relacionadas con:
- Proyectos.
- Tareas.
- Usuarios.
- Progreso.
- Distribución del trabajo.
- Actividad.
- También se incluyen funcionalidades de exportación y generación de informes en PDF.

8. Datos de demostración

El proyecto incluye un sistema de datos de demostración mediante un comando de gestión de Django.
Esto permite preparar rápidamente un entorno con proyectos, usuarios, tareas, comentarios, roles y otros datos necesarios para presentar las funcionalidades de la aplicación.


🛠 Tecnologías utilizadas

1. Backend
  - Python
  - Django
  - Django ORM
  - Django Templates
  - Django Forms
  - Django Migrations
  - SQLite
2. Frontend
  - React
  - JavaScript
  - HTML5
  - CSS3
  - Vite
  - Django Template Language
3. Otras tecnologías y herramientas
  - Git
  - GitHub
  - gettext / traducciones de Django
  - ReportLab para generación de PDF
  - openpyxl para exportación de datos


🛠 Integración React

ProjectFlow incorpora React en determinadas vistas de la aplicación para demostrar la integración entre el frontend y el backend Django.

Las vistas React consumen datos reales proporcionados por Django mediante endpoints del backend y actualizan dinámicamente la interfaz sin necesidad de recargar completamente la página.


🏗 Arquitectura

El proyecto está organizado siguiendo una estructura modular basada en aplicaciones Django.

ProjectFlow/
│
├── apps/
│   ├── accounts/
│   ├── core/
│   ├── home/
│   ├── kanban/
│   ├── manage/
│   ├── projects/
│   ├── reports/
│   └── tasks/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── docs/
├── locale/
├── static/
├── templates/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── .gitattributes

La separación por aplicaciones permite mantener las diferentes áreas funcionales del proyecto independientes y facilita su mantenimiento y evolución.


🚀 Instalación

1. Clonar el repositorio
  git clone https://github.com/TU_USUARIO/django-proyecto-final-projectflow-app.git
  cd django-proyecto-final-projectflow-app
2. Crear el entorno virtual
  python -m venv env
  env\Scripts\activate (en Windows)
  source env/bin/activate (en Linux/macOS)
3. Instalar dependencias
  pip install -r requirements.txt
4. Configurar las variables de entorno
  Crear un archivo .env a partir de .env.example y establecer una SECRET_KEY propia.
  Por ejemplo:
  SECRET_KEY=tu-clave-secreta
  La clave real no debe subirse al repositorio.
5. Ejecutar las migraciones
  (python manage.py makemigrations)
  python manage.py migrate
6. Crear un superusuario
  python manage.py createsuperuser
7. Cargar los datos de demostración
  python manage.py seed_demo
8. Ejecutar el servidor
  python manage.py runserver


📚 Documentación

Se incluye documentación específica sobre diferentes aspectos de la aplicación:

- docs/01 Manual_funcional.md — Manual funcional.
- docs/02 Permisos.md — Sistema de permisos.
- docs/03 Arquitectura.md — Arquitectura del proyecto.
- docs/04 Convenciones.md — Convenciones y criterios utilizados durante el desarrollo.


🎯 Objetivo de aprendizaje

Consolidar conocimientos relacionados con:

- Desarrollo web con Django.
- Arquitectura modular mediante Django Apps.
- Modelado de datos mediante Django ORM.
- Relaciones entre modelos.
- Migraciones.
- Formularios y validaciones.
- Sistema de autenticación.
- Gestión de permisos y roles.
- Django Templates.
- Context processors.
- Servicios para separar lógica de negocio.
- Consultas y optimización de datos.
- JavaScript integrado con Django.
- Internacionalización.
- Generación de documentos PDF.
- Exportación de datos.
- Organización y documentación de un proyecto completo.
- Control de versiones con Git y GitHub.


👨‍💻 Autor

Sergio Lobato Gallego


📅 Fecha

? de septiembre de 2026
