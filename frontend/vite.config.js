// frontend/vite.config.js sirve para:
// configurar Vite, React y el proxy de desarrollo que conecta el frontend
// con el servidor Django.

// Dependencias del frontend
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'


/*
 * Mantiene la página principal de Django disponible desde el servidor
 * de desarrollo de Vite. Solo la ruta / se reenvía directamente a Django;
 * las demás rutas se gestionan mediante el proxy definido más abajo.
 */

function djangoRootProxy() {
  return {
    name: "django-root-proxy",

    configureServer(server) {
      server.middlewares.use(async (req, res, next) => {
        if (req.url !== "/") {
          return next();
        }

        try {
          const response = await fetch("http://localhost:8000/", {
            headers: {
              cookie: req.headers.cookie || "",
            },
          });

          res.statusCode = response.status;

          const contentType = response.headers.get("content-type");
          if (contentType) {
            res.setHeader("content-type", contentType);
          }

          const body = await response.text();
          res.end(body);
        } catch (error) {
          console.error("DJANGO ROOT PROXY ERROR:", error);
          next();
        }
      });
    },
  };
}

export default defineConfig({
  plugins: [react(), djangoRootProxy()],

  base: "/static/react/",

  build: {
    outDir: "../static/react",
    emptyOutDir: true,
  },

  server: {

    /*
     * Las peticiones de React a Django se mantienen bajo el mismo host
     * durante el desarrollo para conservar la sesión y las cookies.
     */

    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/static': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/projects': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/tasks': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/kanban': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/report': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/manage/': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/logout': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/login': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/i18n': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
