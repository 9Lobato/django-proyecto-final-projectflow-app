// frontend/src/App.jsx sirve para:
// definir la aplicación principal de React,
// cargar los datos del Kanban y mostrar los componentes React según la ruta.

// Dependencias del frontend
import { useEffect, useState } from "react";
// Imports internos del frontend
import Kanban from "./components/Kanban";
import Navbar from "./components/Navbar";
import Workflow from "./components/Workflow";
import Start from "./components/Start";
// Estilos del frontend
import "./styles/kanban.css";


function App() {
  const [projects, setProjects] = useState([]);
  const [error, setError] = useState(null);

  const currentPath = window.location.pathname;

  useEffect(() => {
    /*
     * El Kanban se carga desde React únicamente en su propia ruta.
     * El resto de rutas continúan siendo gestionadas por Django.
     */
    if (currentPath !== "/kanban/") {
      return;
    }

    const search = new URLSearchParams(
      window.location.search
    ).get("search");

    const apiUrl = search
      ? `/kanban/api/?search=${encodeURIComponent(search)}`
      : "/kanban/api/";

    fetch(apiUrl, {
      credentials: "include",
    })
      .then(async (response) => {
        const contentType =
          response.headers.get("content-type") || "";

        if (response.status === 401) {
          window.location.href = "/login/";
          return;
        }

        if (!response.ok) {
          const text = await response.text();

          throw new Error(
            `Error ${response.status}: ${text.substring(0, 200)}`
          );
        }

        if (!contentType.includes("application/json")) {
          const text = await response.text();

          throw new Error(
            `Django no devolvió JSON: ${text.substring(0, 200)}`
          );
        }

        return response.json();
      })
      .then((data) => {
        if (data) {
          setProjects(data.projects);
        }
      })
      .catch((error) => {
        console.error(error);
        setError(error.message);
      });
  }, [currentPath]);

  /*
   * La guía rápida /start/ utiliza React, pero el resto de la aplicación
   * mantiene sus vistas Django sin necesidad de convertirlas a React.
   */
  if (currentPath === "/start/") {
    return (
      <>
        <Navbar />
        <Start />
      </>
    );
  }

  return (
    <>
      <Navbar />
      <Workflow />

      <div className="container mt-4">
        <h1 className="mb-4">Mi Kanban</h1>

        {error && <p>{error}</p>}

        {!error && <Kanban projects={projects} />}
      </div>
    </>
  );
}

export default App;
