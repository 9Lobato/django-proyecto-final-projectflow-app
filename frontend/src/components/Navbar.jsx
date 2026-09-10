// frontend/src/components/Navbar.jsx sirve para:
// mostrar la barra de navegación de la aplicación,
// incluyendo navegación, búsqueda, idioma y opciones según el usuario.

// Dependencias del frontend
import { useEffect, useState } from "react";


function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(";").shift();
  }
  return null;
}


function Navbar() {
  const [navbarData, setNavbarData] = useState(null);
  const currentPath = window.location.pathname;

  /*
  * El buscador reutiliza las vistas Django de cada sección.
  * Solo se habilita en proyectos, tareas y Kanban.
  */

  const searchAction =
    currentPath.startsWith("/projects/")
      ? "/projects/"
      : currentPath.startsWith("/tasks/")
        ? "/tasks/"
        : currentPath.startsWith("/kanban/")
          ? "/kanban/"
          : null;

  async function handleLogout(event) {
    event.preventDefault();

    try {
      const csrfToken = getCookie("csrftoken");

      if (!csrfToken) {
        throw new Error("No se encontró el token CSRF.");
      }

      const response = await fetch("/logout/", {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("No se pudo cerrar la sesión.");
      }

      window.location.href = "/login/";
    } catch (error) {
      console.error("LOGOUT ERROR:", error);
      alert(error.message);
    }
  }

  async function handleLanguageChange(event) {
    const language = event.target.value;
    const csrfToken = getCookie("csrftoken");

    if (!csrfToken) {
      console.error("No se encontró el token CSRF.");
      return;
    }

    const formData = new URLSearchParams();
    formData.append("language", language);
    formData.append("next", window.location.pathname);

    try {
      const response = await fetch("/i18n/setlang/", {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        credentials: "include",
        body: formData.toString(),
      });

      if (!response.ok) {
        throw new Error(
          `No se pudo cambiar el idioma (${response.status}).`
        );
      }

      window.location.reload();
    } catch (error) {
      console.error("LANGUAGE ERROR:", error);
    }
  }

  useEffect(() => {
    async function loadNavbar() {
      try {
        const response = await fetch("/api/navbar/", {
          credentials: "include",
        });

        if (response.status === 401) {
          window.location.href = "/login/";
          return;
        }

        if (!response.ok) {
          throw new Error("No se pudieron cargar los datos del navbar.");
        }

        const data = await response.json();
        setNavbarData(data);
      } catch (error) {
        console.error("NAVBAR ERROR:", error);
      }
    }

    loadNavbar();
  }, []);

  if (!navbarData) {
    return null;
  }

  function handleSearch(event) {

    event.preventDefault();

    const search = event.currentTarget.search.value.trim();
    const currentPath = window.location.pathname;

    let target = null;

    if (currentPath.startsWith("/projects/")) {
      target = "/projects/";
    } else if (currentPath.startsWith("/tasks/")) {
      target = "/tasks/";
    } else if (currentPath.startsWith("/kanban/")) {
      target = "/kanban/";
    }

    if (!target) {
      return;
    }

    const params = new URLSearchParams();

    if (search) {
      params.set("search", search);
    }

    window.location.href = `${target}?${params.toString()}`;
  }

  return (
    <nav className="navbar navbar-dark bg-dark"
      style={{ minHeight: "80px", display: "block" }}>
      <div
        className="d-flex align-items-center w-100"
        style={{maxWidth: "1296px", height: "80px", margin: "0 auto"}}
      >
        <a className="navbar-brand m-0 fs-1" href="/">
          ProjectFlow
        </a>

        <div className="flex-grow-1 d-flex flex-column justify-content-between h-100">

          {/* Primera fila: navegación */}
          <div className="d-flex align-items-center justify-content-end h-50 pt-2">
            <ul
              className="navbar-nav d-flex flex-row gap-3 align-items-center"
              style={{ width: "480px" }}
            >

              <li className="nav-item">
                <a className="nav-link py-0" href="/projects/">{navbarData.translations.projects}</a>
              </li>

              <li className="nav-item">
                <a className="nav-link py-0" href="/tasks/">{navbarData.translations.tasks}</a>
              </li>

              <li className="nav-item">
                <a className="nav-link py-0" href="/kanban/">{navbarData.translations.kanban}</a>
              </li>

              {navbarData.is_manager || navbarData.is_owner ? (
                <li className="nav-item">
                  <a className="nav-link py-0" href="/report/">{navbarData.translations.report}</a>
                </li>
              ) : null}

              {navbarData.is_owner ? (
                <li className="nav-item">
                  <a className="nav-link py-0" href="/manage/">{navbarData.translations.manage}</a>
                </li>
              ) : null}

              <li className="nav-item d-flex align-items-center">
                <button type="button"
                  className="btn btn-link nav-link py-0 p-0 border-0"
                  onClick={handleLogout}>{navbarData.translations.logout}:
                </button>
                <span className="text-light ms-1">{navbarData.username}</span>
              </li>

            </ul>
          </div>

          {/* Segunda fila: buscador + idioma */}
          <div className="d-flex justify-content-end align-items-center h-50 pb-2">

            <form
              className="d-flex"
              onSubmit={handleSearch}
            >
              <button
                type="submit"
                className="btn btn-outline-light btn-sm me-2"
                disabled={!searchAction}
              >
                {navbarData.translations.search}
              </button>
              <input
                className="form-control form-control-sm me-2"
                type="search"
                name="search"
                placeholder={navbarData.translations.search_placeholder}
                style={{ width: "410px" }}
                disabled={!searchAction}
              />
            </form>

            <select
              className="form-select form-select-sm"
              style={{ width: "62px" }}
              value={navbarData.language}
              onChange={handleLanguageChange}
            >
              {navbarData.languages.map((language) => (
                <option
                  key={language.code}
                  value={language.code}
                >
                  {language.name}
                </option>
              ))}
            </select>

          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
