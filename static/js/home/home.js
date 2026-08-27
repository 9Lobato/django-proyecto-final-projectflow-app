// static\js\home\home.js ...
// ... se utiliza en:
// templates\home\home.html en el dashboard principal de inicio


// =========================================
// USUARIO ACTUAL
// Obtiene el identificador del usuario actual
// para guardar preferencias y estados individuales.
// =========================================

const userId = window.ProjectFlow.userId;
// Resolver / Reabrir solicitudes desde las notificaciones mostradas en el dashboard.
document.querySelectorAll(".toggle-status").forEach(button => {
  button.addEventListener("click", function () {
    fetch(`/tasks/comments/${this.dataset.id}/status/`, {
      method: "POST",
      headers: {"X-CSRFToken": getCookie("csrftoken")}
    })
    .then(response => response.json())
    .then(data => {
      if (!data.success) return;
      // Cambia el contenido del botón según el nuevo estado de la solicitud.
      this.dataset.status = data.status;
      if (data.status === "RESOLVED") {
        if (data.can_reopen) {
          this.textContent = "Reabrir";
        } else {
          const span = document.createElement("span");
          span.className = "badge card text-secondary";
          span.textContent = "Resuelta";
          this.replaceWith(span);
        }
      }
      // Actualiza el estado y la fecha de resolución de la fila correspondiente.
      const row = this.closest("tr");
      row.dataset.status = data.status;
      row.cells[6].textContent = data.resolved_at || "—";
      // Vuelve a aplicar los filtros del proyecto después de modificar el estado.
      const projectId = this.closest(".collapse").id.replace("project", "");
      applyFilters(projectId);
    });
  });
});


// =========================================
// CAMBIAR TIPO DE SOLICITUD
// Guarda el tipo de solicitud seleccionado
// y actualiza el filtro correspondiente.
// =========================================

document.querySelectorAll(".request-kind").forEach(select => {
  const row = select.closest("tr");
  // Sincroniza el tipo de solicitud con los datos almacenados en la fila al cargar la página.
  row.dataset.requestKind = select.value;
  // Envía al servidor el nuevo tipo de solicitud cuando el usuario modifica el selector.
  select.addEventListener("change", function () {
    row.dataset.requestKind = this.value;
    fetch(`/tasks/comments/${this.dataset.id}/request-kind/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: "value=" + this.value
    });
    // Actualiza inmediatamente la lista después de cambiar el tipo de solicitud.
    const projectId = this.closest(".collapse").id.replace("project", "");
    applyFilters(projectId);
  });
});


// =========================================
// GUARDAR CAMBIO EN ESTADO
// Actualiza el estado de una solicitud y sincroniza
// la información mostrada en la fila.
// =========================================

document.querySelectorAll(".toggle-status").forEach(button => {
  const row = button.closest("tr");
  row.dataset.status = button.dataset.status;
  button.addEventListener("click", function () {
    fetch(`/tasks/comments/${this.dataset.id}/status/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      }
    })
    .then(r => r.json())
    .then(data => {
      if (!data.success) return;
      this.dataset.status = data.status;
      row.dataset.status = data.status;
      this.textContent =
        data.status === "RESOLVED"
          ? "Reabrir"
          : "Resolver";
      row.cells[6].textContent = data.resolved_at || "—";
      // Actualiza la visibilidad de la fila según el nuevo estado de la solicitud.
      const projectId = this.closest(".collapse").id.replace("project", "");
      applyFilters(projectId);
    });
  });
});


// =========================================
// ETIQUETAS DE FILTROS
// Define los textos mostrados para los distintos
// valores utilizados por los filtros del dashboard.
// =========================================

const labels = {
  ALL: "Todos",
  REQUEST: "Solicitud",
  COMMENT: "Comentario",
  IMMEDIATE: "Inmediata",
  MITIGATION: "Revisión",
  SCHEDULED: "Programada",
  ROUTINE: "Rutinaria",
  IMPROVEMENT: "Mejora",
  OPTIONAL: "Opcional",
  DELEGATED: "Delegada",
  OPEN: "Abiertas",
  RESOLVED: "Resueltas",
  NONE: "—"
};


// =========================================
// OBTENER VALORES EXISTENTES
// Obtiene los valores disponibles para un filtro
// a partir de las filas existentes en un proyecto.
// =========================================

function getExistingValues(projectId, dataset) {
  const rows = document.querySelectorAll(
    `#project${projectId} tbody tr`
  );
  const values = new Set();
  rows.forEach(row => {
    let value = row.dataset[dataset];
    if (!value)
      return;
    if (dataset === "mentions") {
      if (value === "NONE") {
        values.add("NONE");
      } else {
        value.split(",").forEach(v => values.add(v));
      }
    } else {
      values.add(value);
    }
  });
  // Ordena los valores de los filtros y coloca las opciones generales en las primeras posiciones.
  if (dataset === "requestKind") {
    const ordered = ["ALL", "NONE"];
    Array.from(values)
      .sort()
      .forEach(v => {
        if (v !== "NONE") {
          ordered.push(v);
        }
      });
    return ordered;
  }
  if (dataset === "status") {
    const ordered = ["ALL", "NONE"];
    Array.from(values)
      .sort()
      .forEach(v => {
        if (v !== "NONE") {
          ordered.push(v);
        }
      });
    return ordered;
  }
  if (dataset === "task") {
    return [
      "ALL",
      ...Array.from(values)
        .sort((a, b) => Number(a) - Number(b))
    ];
  }
  return [
    "ALL",
    ...Array.from(values).sort()
  ];
}


// =========================================
// SIGUIENTE VALOR DEL FILTRO
// Avanza al siguiente valor disponible de un filtro
// y actualiza su icono, título y resultados.
// =========================================

function nextDynamicValue(button, key, dataset) {
  const values = getExistingValues(button.dataset.project, dataset);
  let current = button.dataset[key];
  let index = values.indexOf(current);
  if (index === -1)
    index = 0;
  index++;
  if (index >= values.length)
    index = 0;
  button.dataset[key] = values[index];
  // Cambia el icono del botón para indicar si existe un filtro activo.
  const icon = button.querySelector("i");
  if (values[index] === "ALL") {
    icon.classList.remove("bi-funnel-fill");
    icon.classList.add("bi-funnel");
  } else {
    icon.classList.remove("bi-funnel");
    icon.classList.add("bi-funnel-fill");
  }
  // Muestra en el botón el nombre correspondiente al valor seleccionado del filtro.
  button.title = labels[values[index]] || values[index];
  applyFilters(button.dataset.project);
}


// =========================================
// APLICAR FILTROS
// Determina qué filas de un proyecto deben permanecer
// visibles según los filtros seleccionados.
// =========================================

function applyFilters(projectId) {
  const project = document.querySelector("#project" + projectId);
  if (!project)
    return;
  const rows = project.querySelectorAll("tbody tr");
  const taskFilter = project.querySelector(".filter-task").dataset.task;
  const authorFilter = project.querySelector(".filter-author").dataset.author;
  const mentionFilter = project.querySelector(".filter-mention").dataset.mention;
  const typeFilter = project.querySelector(".filter-type").dataset.type;
  const kindFilter = project.querySelector(".filter-kind").dataset.requestKind;
  const statusFilter = project.querySelector(".filter-status").dataset.status;
  // Comprueba cada fila frente a los filtros activos y determina si debe mostrarse u ocultarse.
  rows.forEach(row => {
    const task = row.dataset.task;
    const author = row.dataset.author || "NONE";
    const isRequest = row.dataset.type === "REQUEST";
    const type = row.dataset.type;
    const kind = isRequest ? row.dataset.requestKind : "";
    const status = isRequest ? row.dataset.status : "";
    const mentions = row.dataset.mentions || "NONE";
    let visible = true;
    // Comprueba si la tarea de la fila coincide con la tarea seleccionada.
    if (taskFilter !== "ALL" && task !== taskFilter)
      visible = false;
    // Comprueba si el autor de la fila coincide con el autor seleccionado.
    if (authorFilter !== "ALL" && author !== authorFilter)
      visible = false;
    // Comprueba si la fila corresponde al tipo de comentario seleccionado.
    if (typeFilter !== "ALL" && type !== typeFilter)
      visible = false;
    // Oculta las filas que no coinciden con el tipo de solicitud seleccionado.
    if (kindFilter === "NONE") {
      if (isRequest)
        visible = false;
    } else if (kindFilter !== "ALL") {
      if (!isRequest || kind !== kindFilter)
        visible = false;
    }
    // Oculta las filas que no coinciden con el estado de solicitud seleccionado.
    if (statusFilter === "NONE") {
      if (isRequest)
        visible = false;
    } else if (statusFilter !== "ALL") {
      if (!isRequest || status !== statusFilter)
        visible = false;
    }
    // Comprueba si la fila contiene la mención seleccionada o si no contiene ninguna.
    if (mentionFilter !== "ALL") {
      if (mentionFilter === "NONE") {
        if (mentions !== "NONE")
          visible = false;
      } else {
        const mentionList =
          mentions === "NONE"
            ? []
            : mentions.split(",");
        if (!mentionList.includes(mentionFilter))
          visible = false;
      }
    }
    row.style.display = visible ? "" : "none";
  });
}


// =========================================
// FILTROS PRINCIPALES
// Configura los botones de tarea, autor, tipo
// y estado para avanzar entre sus valores disponibles.
// =========================================

[
  ["task", "task"],
  ["author", "author"],
  ["type", "type"],
  ["status", "status"]
].forEach(([name, dataset]) => {
  document.querySelectorAll(`.filter-${name}`).forEach(btn => {
    btn.addEventListener("click", function () {
      nextDynamicValue(this, name, dataset);
    });
  });
});


// =========================================
// FILTRO DE TIPO DE SOLICITUD
// Configura el botón para avanzar entre los
// distintos tipos de solicitud disponibles.
// =========================================

document.querySelectorAll(".filter-kind").forEach(btn => {
  btn.addEventListener("click", function () {
    nextDynamicValue(this, "requestKind", "requestKind");
  });
});


// =========================================
// FILTRO DE MENCIONES
// Configura el botón para avanzar entre las
// menciones disponibles en cada proyecto.
// =========================================

document.querySelectorAll(".filter-mention").forEach(btn => {
  btn.addEventListener("click", function () {
    const values = getExistingValues(this.dataset.project, "mentions");
    let current = this.dataset.mention;
    let index = values.indexOf(current);
    index = (index + 1) % values.length;
    this.dataset.mention = values[index];
    // Indica visualmente si el filtro de menciones está activo o muestra todos los valores.
    const icon = this.querySelector("i");
    if (values[index] === "ALL") {
      icon.classList.remove("bi-funnel-fill");
      icon.classList.add("bi-funnel");
    } else {
      icon.classList.remove("bi-funnel");
      icon.classList.add("bi-funnel-fill");
    }
    // Muestra el nombre correspondiente al valor seleccionado del filtro.
    this.title = labels[values[index]] || values[index];
    applyFilters(this.dataset.project);
  });
});


// =========================================
// ACORDEONES DE PROYECTOS
// Recupera y guarda qué proyectos están abiertos
// o cerrados para cada usuario.
// =========================================

document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".project-toggle");
  buttons.forEach(btn => {
    const projectId = btn.dataset.project;
    const target = document.querySelector(btn.dataset.bsTarget);
    const icon = btn.querySelector("i");
    const storageKey = `home_project_${userId}_${projectId}`;
    const isOpen = localStorage.getItem(storageKey) === "open";
    // Abre automáticamente los proyectos que estaban abiertos durante la visita anterior.
    if (isOpen) {
      target.classList.add("show");
      btn.setAttribute("aria-expanded", "true");
      if (icon) {
        icon.classList.remove("bi-chevron-right");
        icon.classList.add("bi-chevron-down");
      }
    }
    // Guarda el estado cuando el usuario abre un proyecto.
    target.addEventListener("shown.bs.collapse", function () {
      localStorage.setItem(storageKey, "open");
      if (icon) {
        icon.classList.remove("bi-chevron-right");
        icon.classList.add("bi-chevron-down");
      }
    });
    // Guarda el estado cuando el usuario cierra un proyecto.
    target.addEventListener("hidden.bs.collapse", function () {
      localStorage.setItem(storageKey, "closed");
      if (icon) {
        icon.classList.remove("bi-chevron-down");
        icon.classList.add("bi-chevron-right");
      }
    });
  });
});


// =========================================
// SCROLL DEL DASHBOARD
// Guarda y restaura la posición de desplazamiento
// del dashboard para cada usuario.
// =========================================

function restoreScroll() {
  const savedScroll = sessionStorage.getItem(
    `home_scroll_${userId}`
  );
  if (savedScroll !== null) {
    window.scrollTo(
      0,
      parseInt(savedScroll, 10)
    );
  }
}
function saveScroll() {
  sessionStorage.setItem(
    `home_scroll_${userId}`,
    window.scrollY
  );
}


// =========================================
// RESTAURAR SCROLL
// Restaura la posición guardada al cargar la página
// y al volver a ella mediante el historial del navegador.
// =========================================

document.addEventListener("DOMContentLoaded", function () {requestAnimationFrame(restoreScroll)});
window.addEventListener("pageshow", function () {requestAnimationFrame(restoreScroll)});
window.addEventListener("beforeunload", saveScroll);
// Controla los iconos de notificación de cada comentario y el icono general de cada proyecto.
document.addEventListener("DOMContentLoaded", function () {
  // Muestra el icono general del proyecto cuando existe al menos una notificación sin leer.
  function updateProjectBell(projectId) {
    const projectBell = document.querySelector(
      `.project-bell[data-project="${projectId}"]`
    );
    if (!projectBell) return;
    const notifications = document.querySelectorAll(
      `.notification-bell[data-project="${projectId}"]`
    );
    const hasUnread = Array.from(notifications).some(
      bell => bell.style.display !== "none"
    );
    projectBell.style.display = hasUnread ? "" : "none";
  }
  // Recupera las notificaciones ya vistas y permite marcarlas como vistas al hacer clic.
  document.querySelectorAll(".notification-bell").forEach(bell => {
    const key = `notification_seen_${userId}_${bell.dataset.id}`;
    if (localStorage.getItem(key) === "true") {
      bell.style.display = "none";
    }
    // Guarda la notificación como vista y actualiza el icono general del proyecto.
    bell.addEventListener("click", function () {
      localStorage.setItem(key, "true");
      this.style.display = "none";
      updateProjectBell(this.dataset.project);
    });
  });
  // Actualiza el estado inicial de los iconos generales de cada proyecto.
  document.querySelectorAll(".project-bell").forEach(projectBell => {
    updateProjectBell(projectBell.dataset.project);
  });
});
