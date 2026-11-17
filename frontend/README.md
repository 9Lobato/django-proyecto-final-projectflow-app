# ProjectFlow — Frontend

Esta carpeta contiene el frontend de **ProjectFlow**, desarrollado con **React** y **Vite**.

React se utiliza actualmente para los componentes y funcionalidades que se han migrado desde Django, manteniendo **Django como backend y como responsable de las vistas que todavía no se han migrado a React**.


## Estructura

frontend/
├── public/          # Recursos públicos utilizados por React
├── src/             # Código fuente de la aplicación React
│   ├── components/  # Componentes reutilizables
│   ├── App.jsx      # Componente principal
│   ├── index.css    # Estilos globales
│   └── main.jsx     # Punto de entrada de React
├── index.html       # Documento HTML principal de Vite
├── package.json     # Dependencias y scripts del frontend
└── vite.config.js   # Configuración de Vite


## Desarrollo

Desde esta carpeta:

npm install
npm run dev

Vite inicia el servidor de desarrollo y proporciona recarga automática mediante HMR.

El frontend se comunica con el backend Django mediante las rutas y proxies configurados en `vite.config.js`.


## Producción

Para generar una compilación de producción:

npm run build

Los archivos generados se almacenan en:

../static/react/

Esta carpeta contiene los recursos compilados que Django utiliza para servir la aplicación React.

Cuando se quiera probar la compilación desde Django en local, hay que volver a la raíz del proyecto y ejecutar:

python manage.py collectstatic --noinput

Este comando recopila los archivos estáticos en STATIC_ROOT y únicamente es necesario cuando se quiere probar la compilación mediante Django. No es necesario para utilizar el servidor de desarrollo de Vite.

La carpeta `node_modules/` contiene las dependencias del proyecto. Los archivos generados en `../static/react/` son compilados automáticamente por Vite y no deben editarse manualmente.


## Tecnologías principales

* React
* Vite
* JavaScript
* ESLint
* Bootstrap / Bootstrap Icons
* Django como backend
