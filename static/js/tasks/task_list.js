// static\js\tasks\task_list.js ...
// ... se utiliza en:
// templates\tasks\task_list.html en la gestión de filtros, proyectos desplegados y posición del scroll


// =========================================
// LISTADO DE TAREAS
// Gestiona los filtros de estado, entrega y prioridad,
// el estado de los proyectos desplegados y la posición
// del scroll del listado.
// =========================================

document.addEventListener("dragover", function (event) {
  event.preventDefault();

  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = "move";
  }
});

document.addEventListener("DOMContentLoaded", function () {
  // Estados -->
  const allStatus = document.getElementById("status_all");
  const statusCheckboxes = document.querySelectorAll(".status-checkbox");
  if (!allStatus) return;
  statusCheckboxes.forEach(cb => {
    cb.addEventListener("change", function () {
      const checkedStatuses = [...statusCheckboxes].filter(x => x.checked);
      // Si no se selecciona ningún estado → activar Todas
      if (checkedStatuses.length === 0) {
        allStatus.checked = true;}
      // Si se seleccionan todos los estados uno a uno → activar Todas y desactivar los estados
      else if (checkedStatuses.length === statusCheckboxes.length) {
        allStatus.checked = true; statusCheckboxes.forEach(x => x.checked = false);}
      // Si se ha seleccionado algún estado → desactivar Todas
      else {allStatus.checked = false;}
    });
  });
  // Si seleccionamos Todas → desactivar cada uno de los estados
  allStatus.addEventListener("change", function () {
    if (allStatus.checked) {
      statusCheckboxes.forEach(cb => cb.checked = false);}
  });
  // Entrega -->
  const allDelivery = document.getElementById("delivery_all");
  const deliveryCheckboxes = document.querySelectorAll(".delivery-checkbox");
  if (!allDelivery) return;
  deliveryCheckboxes.forEach(cb => {
    cb.addEventListener("change", function () {
      const checkedDelivery = [...deliveryCheckboxes].filter(x => x.checked);
      // Si no se selecciona ningún progreso → activar Todas
      if (checkedDelivery.length === 0) {
        allDelivery.checked = true;}
      // Si se seleccionan todos los progresos uno a uno → activar Todas y desactivar los progresos
      else if (checkedDelivery.length === deliveryCheckboxes.length) {
        allDelivery.checked = true; deliveryCheckboxes.forEach(x => x.checked = false);}
      // Si se ha seleccionado algún progresos → desactivar Todas
      else {allDelivery.checked = false;}
    });
  });
  // Si seleccionamos Todas → desactivar cada uno de los estados
  allDelivery.addEventListener("change", function () {
    if (allDelivery.checked) {
      deliveryCheckboxes.forEach(cb => cb.checked = false);}
  });
  // Prioridades -->
  const allPriority = document.getElementById("priority_all");
  const priorityCheckboxes = document.querySelectorAll(".priority-checkbox");
  if (!allPriority) return;
  priorityCheckboxes.forEach(cb => {
    cb.addEventListener("change", function () {
      const checkedPriority = [...priorityCheckboxes].filter(x => x.checked);
      // Si no se selecciona ninguna prioridad → activar Todas
      if (checkedPriority.length === 0) {
        allPriority.checked = true;}
      // Si se seleccionan todas las prioridades una a una → activar Todas y desactivar las prioridades
      else if (checkedPriority.length === priorityCheckboxes.length) {
        allPriority.checked = true; priorityCheckboxes.forEach(x => x.checked = false);}
      // Si se ha seleccionado alguna prioridad → desactivar Todas
      else {allPriority.checked = false;}
    });
  });
  // Si seleccionamos Todas → desactivar cada una de las prioridades
  allPriority.addEventListener("change", function () {
    if (allPriority.checked) {
      priorityCheckboxes.forEach(cb => cb.checked = false);}
  });
});
// Recordar proyectos abiertos/cerrados
document.querySelectorAll(".project-toggle").forEach(btn => {
  const projectId = btn.dataset.project;
  const target = document.querySelector(btn.dataset.bsTarget);
  const params = new URLSearchParams(window.location.search);
  const requestedProject = params.get("project");
  const mustOpen =
    requestedProject === projectId ||
    localStorage.getItem("task_project_" + projectId) === "open";
  // Restaurar estado
  if (mustOpen) {
    target.classList.add("show");
    btn.setAttribute("aria-expanded", "true");
    const icon = btn.querySelector("i");
    if (icon) {
      icon.classList.remove("bi-chevron-right");
      icon.classList.add("bi-chevron-down");
    }
  }
  // Guardar cuando se abre
  target.addEventListener("shown.bs.collapse", function () {
    localStorage.setItem("task_project_" + projectId, "open");
    const icon = btn.querySelector("i");
    if (icon) {
      icon.classList.remove("bi-chevron-right");
      icon.classList.add("bi-chevron-down");
    }
  });
  // Guardar cuando se cierra
  target.addEventListener("hidden.bs.collapse", function () {
    localStorage.setItem("task_project_" + projectId, "closed");
    const icon = btn.querySelector("i");
    if (icon) {
      icon.classList.remove("bi-chevron-down");
      icon.classList.add("bi-chevron-right");
    }
  });
});
// Restaurar scroll SIEMPRE
function restoreScroll() {
  const userId = "{{ request.user.id }}";
  const savedScroll = sessionStorage.getItem(`task_list_scroll_${userId}`);
  if (savedScroll !== null) {
    window.scrollTo(0, parseInt(savedScroll, 10));
  }
}
// Guardar scroll
function saveScroll() {
  const userId = "{{ request.user.id }}";
  sessionStorage.setItem(
    `task_list_scroll_${userId}`,
    window.scrollY
  );
}
document.addEventListener("DOMContentLoaded", function () {
  restoreScroll();
});
// MUY IMPORTANTE: back/forward cache fix
window.addEventListener("pageshow", function () {
  restoreScroll();
});
// Guardar antes de salir
window.addEventListener("beforeunload", function () {
  saveScroll();
});


// =========================================
// PRUEBA ARRASTRAR TAREAS
// =========================================

function getCookie(name) {

  const cookies = document.cookie.split(";");

  for (const cookie of cookies) {

    const [key, value] = cookie.trim().split("=");

    if (key === name) {
      return decodeURIComponent(value);
    }

  }

  return null;
}

document.addEventListener("DOMContentLoaded", function () {

  const draggableTasks =
    document.querySelectorAll(".task-drag-item");

  draggableTasks.forEach(task => {

    task.addEventListener("dragstart", function (event) {

      event.dataTransfer.setData(
        "text/plain",
        this.dataset.taskId
      );

      event.dataTransfer.effectAllowed = "move";

      this.classList.add("task-dragging");

    });

    task.addEventListener("dragend", function () {

      this.classList.remove("task-dragging");

    });

  });


  const taskColumns =
    document.querySelectorAll(
      ".col-sm-6.col-md-4.col-xl-3"
    );

  taskColumns.forEach(column => {

    column.addEventListener("dragover", function (event) {

      event.preventDefault();

      if (event.dataTransfer) {
        event.dataTransfer.dropEffect = "move";
      }

    });

    column.addEventListener("drop", function (event) {

      event.preventDefault();

      const draggedTaskId =
        event.dataTransfer.getData("text/plain");

      const draggedTask =
        document.querySelector(
          `.task-drag-item[data-task-id="${draggedTaskId}"]`
        );

      const draggedColumn =
        draggedTask.closest(".col-sm-6.col-md-4.col-xl-3");

      const targetTask =
        this.querySelector(".task-drag-item");

      if (!draggedTask || !draggedColumn || !targetTask) {
        return;
      }

      if (draggedColumn === this) {
        return;
      }

      this.parentNode.insertBefore(
        draggedColumn,
        this
      );

      const taskColumnsInProject =
        this.parentNode.querySelectorAll(
          ".col-sm-6.col-md-4.col-xl-3"
        );

      taskColumnsInProject.forEach((column, index) => {

        const task =
          column.querySelector(".task-drag-item");

        if (!task) {
          return;
        }

        const newSequence = index + 1;

        task.dataset.sequence = newSequence;

        const title =
          task.querySelector("a");

        if (title) {

          const currentText =
            title.textContent.trim();

          title.textContent =
            currentText.replace(
              /^#\d+/,
              `#${newSequence}`
            );

        }

      });

      const reorderUrl =
        this.parentNode.dataset.reorderUrl;

      const formData = new FormData();

      taskColumnsInProject.forEach(column => {

        const task =
          column.querySelector(".task-drag-item");

        if (!task) {
          return;
        }

        formData.append(
          "task_ids",
          task.dataset.taskId
        );

      });

      fetch(reorderUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: formData,
      })
      .then(response => response.json())
      .catch(error => {

        console.error(
          "ERROR AL GUARDAR EL ORDEN:",
          error
        );

      });

    });

  });

});
