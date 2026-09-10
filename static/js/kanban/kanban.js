// static\js\kanban\kanban.js ...
// ... se utiliza en:
// templates\kanban\kanban.html en la gestión de arrastrar, mover y copiar tareas


// =========================================
// GESTIÓN DE TAREAS DEL TABLERO KANBAN
// Gestiona el arrastre de las tareas entre columnas,
// determina si pueden moverse o copiarse y guarda
// los cambios realizados en el servidor.
// =========================================

document.addEventListener("DOMContentLoaded", function () {
  // Tarea arrastrada
  let draggedTask = null;
  // Determinar si una tarea puede moverse, copiarse, o soltarse en la columna seleccionada.
  function getDropAction(
    oldProject,
    oldStatus,
    newProject,
    newStatus
  ) {
    // Copiar tarea al cambiarla de proyecto 
    if (oldProject !== newProject) {
      return "copy";
    }
    // Mover tarea pendiente 
    if (oldStatus === "TODO") {
      if (
        newStatus === "IN_PROGRESS" ||
        newStatus === "CANCELLED"
      ) {
        return "move";
      }
    }
    // Mover tarea en progreso
    if (oldStatus === "IN_PROGRESS") {
      if (
        newStatus === "DONE" ||
        newStatus === "CANCELLED"
      ) {
        return "move";
      }
      if (
        newStatus === "TODO" &&
        draggedTask.dataset.planned !== "true"
      ) {
        return "move";
      }
    }
    // Mover tarea terminada
    if (oldStatus === "DONE") {
      if (newStatus === "IN_PROGRESS") {
        return "move";
      }
    }
    // Mover tarea cancelada
    if (oldStatus === "CANCELLED") {
      if (
        newStatus === "TODO" ||
        newStatus === "IN_PROGRESS"
      ) {
        return "move";
      }
    }
    // Cambio de columna no permitido
    return "none";
  }
  // Tarjetas del tablero arrastables por el usuario
  document.querySelectorAll(".kanban-card").forEach(card => {
    attachDrag(card);
  });
  // Eventos de arrastre de una tarjeta
  function attachDrag(card) {
    const canMove = card.dataset.canMove === "true";
    card.draggable = canMove;
    if (!canMove) {return}
    // Guardar tarea arrastrada y registro de proyecto y estado de origen
    card.addEventListener("dragstart", function (e) {
      draggedTask = card;
      const originCell = card.closest(".kanban-cell");
      draggedTask.dataset.previousStatus = originCell.dataset.status;
      draggedTask.dataset.previousProject = originCell.dataset.project;
      e.dataTransfer.effectAllowed = "copyMove";
    });
    // Eliminar tarea arrastrada una vez finalizado el proceso de arrastre
    card.addEventListener("dragend", function () {
      draggedTask = null;
    });
  }
  // Configurar columnas donde se soltar las tareas arrastradas
  document.querySelectorAll(".kanban-cell").forEach(cell => {
    // Comprobar arrastre tarea sobre columna
    cell.addEventListener("dragover", function (e) {
      if (!draggedTask) {return}
      const dropAction = getDropAction(
        draggedTask.dataset.previousProject,
        draggedTask.dataset.previousStatus,
        this.dataset.project,
        this.dataset.status
      );
      if (dropAction === "move") {
        e.preventDefault();
        e.dataTransfer.dropEffect = "move";
      }
      else if (dropAction === "copy") {
        e.preventDefault();
        e.dataTransfer.dropEffect = "copy";
      }
      else {
        e.dataTransfer.dropEffect = "none";
      }
    });
    // Acción tras soltar tarea sobre columna
    cell.addEventListener("drop", function (e) {
      if (!draggedTask) return;
      const oldStatus = draggedTask.dataset.previousStatus;
      const newStatus = this.dataset.status;
      const oldProject = draggedTask.dataset.previousProject;
      const newProject = this.dataset.project;
      const dropAction = getDropAction(
        oldProject,
        oldStatus,
        newProject,
        newStatus
      );
      if (dropAction === "none") return;
      e.preventDefault();
      // Copia de tarea tras soltarla a otro proyecto
      if (dropAction === "copy") {
        fetch("/kanban/copy/", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
          },
          body:
            `task_id=${draggedTask.dataset.taskId}` +
            `&project_id=${this.dataset.project}`
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            window.location.reload();
          }
        });
        return;
      }
      // Mover visualmente tarea a la nueva columna y adaptar su formato según estado.
      this.appendChild(draggedTask);
      if (this.dataset.status === "DONE" ||
        this.dataset.status === "CANCELLED") {
        draggedTask.classList.add("compact");
      } else {
        draggedTask.classList.remove("compact");
      }
      // Enviar nuevo estado de la tarea al servidor después de moverla.  
      fetch("/kanban/move/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": getCookie("csrftoken")
        },
        body:
          `task_id=${draggedTask.dataset.taskId}` +
          `&status=${this.dataset.status}`
      })
      .then(response => response.json())
      .then(data => {
        // Mostrar error y restaurar tablero si el movimiento es rechazado por el servidor.
        if (!data.success) {
          alert(data.error);
          window.location.reload();
          return;
        }
        // Actualizar tablero con los datos definitivos.
        window.location.reload();
      });
    });
  });
});
