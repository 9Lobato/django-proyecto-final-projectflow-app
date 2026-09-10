// frontend/src/components/Kanban.jsx sirve para:
// mostrar y gestionar el tablero Kanban mediante React,
// incluyendo tareas, estados, drag and drop y acciones sobre proyectos y tareas.

// Dependencias del frontend
import { useEffect, useRef, useState } from "react";


const columns = [
  { key: "TODO", label: "To do" },
  { key: "IN_PROGRESS", label: "In progress" },
  { key: "DONE", label: "Done" },
  { key: "CANCELLED", label: "Cancelled" },
];

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);

  if (parts.length === 2) {
    return parts.pop().split(";").shift();
  }

  return null;
}

// Devuelve:
// move -> cambiar estado
// copy -> copiar a otro proyecto
// none -> operación no permitida

function getDropAction(task, newProject, newStatus) {
  const oldProject = String(task.projectId);
  const targetProject = String(newProject);
  const oldStatus = String(task.status)
    .trim()
    .toUpperCase();

  // Otro proyecto = COPY.
  // Se permite independientemente del estado.
  if (oldProject !== targetProject) {
    return "copy";
  }

  // Mismo proyecto + mismo estado = nada que hacer.
  if (oldStatus === newStatus) {
    return "none";
  }

  // Transiciones permitidas dentro del mismo proyecto:
  // TODO -> IN_PROGRESS / CANCELLED
  // IN_PROGRESS -> TODO (solo si la tarea no está planificada) / DONE / CANCELLED
  // DONE -> IN_PROGRESS
  // CANCELLED -> TODO / IN_PROGRESS

  if (oldStatus === "TODO") {
    if (
      newStatus === "IN_PROGRESS" ||
      newStatus === "CANCELLED"
    ) {
      return "move";
    }
  }

  if (oldStatus === "IN_PROGRESS") {
    if (
      newStatus === "DONE" ||
      newStatus === "CANCELLED"
    ) {
      return "move";
    }

    if (
      newStatus === "TODO" &&
      !task.is_planned
    ) {
      return "move";
    }
  }

  if (oldStatus === "DONE") {
    if (newStatus === "IN_PROGRESS") {
      return "move";
    }
  }

  if (oldStatus === "CANCELLED") {
    if (
      newStatus === "TODO" ||
      newStatus === "IN_PROGRESS"
    ) {
      return "move";
    }
  }

  return "none";
}

function Kanban({ projects }) {

  /*
   * El estado del drag debe estar en useRef porque dragover
   * ocurre muchas veces y no debemos depender de que React
   * haya terminado un setState.
   */

  const draggedTaskRef = useRef(null);
  const [dragOver, setDragOver] = useState(null);

  // Altura mínima de cada fila para mantener una presentación uniforme.
  const KANBAN_MIN_HEIGHT = 246.36;

  useEffect(() => {
    function adjustKanbanHeights() {
      document.querySelectorAll(".kanban-row").forEach((row) => {
        row
          .querySelectorAll(".kanban-project, .kanban-cell")
          .forEach((element) => {
            element.style.height = "";
            element.style.maxHeight = "";
          });
        
        const todo = row.querySelector('[data-status="TODO"]');
        const progress = row.querySelector(
          '[data-status="IN_PROGRESS"]'
        );

        const histories = row.querySelectorAll(".kanban-history");

        const todoHeight = todo ? todo.scrollHeight : 0;
        const progressHeight = progress
          ? progress.scrollHeight
          : 0;

        const rowHeight = Math.max(
          KANBAN_MIN_HEIGHT,
          todoHeight,
          progressHeight
        );

        const project = row.querySelector(".kanban-project");

        if (project) {
          project.style.height = `${rowHeight}px`;
        }

        row
          .querySelectorAll(
            ".kanban-cell:not(.kanban-history)"
          )
          .forEach((cell) => {
            cell.style.height = `${rowHeight}px`;
            cell.style.maxHeight = `${rowHeight}px`;
          });

        histories.forEach((cell) => {
          cell.style.height = `${rowHeight}px`;
          cell.style.maxHeight = `${rowHeight}px`;
          cell.style.overflowY = "auto";
        });
      });
    }

    // Esperar a que React haya terminado de pintar las tarjetas.
    const frame = requestAnimationFrame(() => {
      adjustKanbanHeights();
    });

    window.addEventListener("resize", adjustKanbanHeights);

    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener(
        "resize",
        adjustKanbanHeights
      );
    };
  }, [projects]);

  function handleDragStart(event, task, projectId) {
    const taskWithProject = {
      ...task,
      projectId,
      status: String(task.status)
        .trim()
        .toUpperCase(),
    };

    draggedTaskRef.current = taskWithProject;

    event.dataTransfer.effectAllowed = "copyMove";

    /*
     * Es conveniente establecer algún dato en dataTransfer
     * para que el drag nativo funcione correctamente.
     */

    event.dataTransfer.setData(
      "text/plain",
      String(task.id)
    );
  }

  function handleDragOver(event, projectId, status) {
    const draggedTask = draggedTaskRef.current;

    if (!draggedTask) {
      return;
    }

    const action = getDropAction(
      draggedTask,
      projectId,
      status
    );

    if (action === "none") {
      event.dataTransfer.dropEffect = "none";
      return;
    }

    // MUY IMPORTANTE:
    // preventDefault() permite que el elemento reciba el drop.

    event.preventDefault();
    event.stopPropagation();

    event.dataTransfer.dropEffect =
      action === "copy" ? "copy" : "move";

    setDragOver(`${projectId}-${status}`);
  }

  async function handleDrop(event, projectId, status) {

    event.preventDefault();
    event.stopPropagation();

    const draggedTask = draggedTaskRef.current;

    if (!draggedTask) {
      return;
    }

    const action = getDropAction(
      draggedTask,
      projectId,
      status
    );

    setDragOver(null);

    if (action === "none") {
      draggedTaskRef.current = null;
      return;
    }

    try {
      const csrfToken = getCookie("csrftoken");

      if (!csrfToken) {
        throw new Error(
          "No se encontró el token CSRF."
        );
      }

      const url =
        action === "copy"
          ? "/kanban/copy/"
          : "/kanban/move/";

      const body =
        action === "copy"
          ? `task_id=${encodeURIComponent(
              draggedTask.id
            )}&project_id=${encodeURIComponent(
              projectId
            )}`
          : `task_id=${encodeURIComponent(
              draggedTask.id
            )}&status=${encodeURIComponent(
              status
            )}`;

      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type":
            "application/x-www-form-urlencoded",
          "X-CSRFToken": csrfToken,
        },
        credentials: "include",
        body,
      });

      const contentType =
        response.headers.get("content-type") || "";

      const responseText = await response.text();

      if (!contentType.includes("application/json")) {
        throw new Error(
          `El servidor respondió con ${response.status} en lugar de JSON`
        );
      }

      const data = JSON.parse(responseText);

      if (!response.ok || !data.success) {
        throw new Error(
          data.error ||
            "No se pudo realizar la operación."
        );
      }

      // Recargar solamente después de una operación confirmada por Django.

      window.location.reload();
    } catch (error) {
      console.error("KANBAN ERROR:", error);
      alert(error.message);
    } finally {
      draggedTaskRef.current = null;
      setDragOver(null);
    }
  }


async function handleFollowToggle(event, projectId) {
  event.preventDefault();
  event.stopPropagation();

  try {
    const csrfToken = getCookie("csrftoken");
    if (!csrfToken) throw new Error("No se encontró el token CSRF.");

    const response = await fetch(`/projects/${projectId}/follow/api/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      credentials: "include",
    });

    const contentType = response.headers.get("content-type") || "";
    const responseText = await response.text();

    if (!contentType.includes("application/json")) {
      throw new Error(
        `El servidor respondió con ${response.status} en lugar de JSON`
      );
    }

    const data = JSON.parse(responseText);

    if (!response.ok || !data.success) {
      throw new Error(
        data.error || "No se pudo cambiar el seguimiento del proyecto."
      );
    }

    window.location.reload();
  } catch (error) {
    console.error("FOLLOW ERROR:", error);
    alert(error.message);
  }
}


async function handleArchiveToggle(event, projectId) {
  event.preventDefault();
  event.stopPropagation();

  try {
    const csrfToken = getCookie("csrftoken");

    if (!csrfToken) {
      throw new Error(
        "No se encontró el token CSRF."
      );
    }

    const response = await fetch(
      `/projects/${projectId}/archive/api/`,
      {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
        credentials: "include",
      }
    );

    const contentType =
      response.headers.get("content-type") || "";

    const responseText = await response.text();

    if (!contentType.includes("application/json")) {
      throw new Error(
        `El servidor respondió con ${response.status} en lugar de JSON`
      );
    }

    const data = JSON.parse(responseText);

    if (!response.ok || !data.success) {
      throw new Error(
        data.error ||
          "No se pudo cambiar el estado de archivo del proyecto."
      );
    }

    window.location.reload();

  } catch (error) {
    console.error("ARCHIVE ERROR:", error);
    alert(error.message);
  }
}


  function handleDragEnd() {
    draggedTaskRef.current = null;
    setDragOver(null);
  }

  return (
    <div className="kanban-board mb-4">
      <div className="kanban-header">
        <div className="kanban-project-col"></div>

        {columns.map((column) => (
          <div
            key={column.key}
            className="kanban-col text-center"
          >
            <a
              href={`/tasks/?status=${column.key}`}
              className="text-decoration-none text-reset"
            >
              {column.label}
            </a>
          </div>
        ))}
      </div>

      {projects.map((project) => (
        <div className="kanban-row" data-project={project.id} key={project.id}>
          <div className="kanban-project">
            <div className="d-flex justify-content-between align-items-center">
              {/* Código */}
              <span className="kanban-project-code">
                {project.code}
              </span>

              {/* Iconos */}
              <div className="kanban-project-icons">
                <div className="d-flex align-items-center gap-1">

                  {/* Seguir */}
                  {project.can_follow && (
                    <button
                      type="button"
                      className="btn btn-link p-0 border-0 shadow-none"
                      onClick={(event) => handleFollowToggle(event, project.id)}
                      title={
                        project.is_followed
                          ? "Dejar de seguir proyecto"
                          : "Seguir proyecto"
                      }
                    >
                      {project.is_followed ? (
                        <i className="bi bi-bookmark text-info"></i>
                      ) : (
                        <i className="bi bi-bookmark text-secondary opacity-25"></i>
                      )}
                    </button>
                  )}

                  {/* Archivar */}
                  {project.user_role === "OWNER" ? (
                    <button
                      type="button"
                      className="btn btn-link p-0 border-0 shadow-none"
                      onClick={(event) =>
                        handleArchiveToggle(event, project.id)
                      }
                      title={
                        project.is_archived
                          ? "Desarchivar proyecto"
                          : "Archivar proyecto"
                      }
                    >
                      {project.is_archived ? (
                        <i className="bi bi-archive text-info"></i>
                      ) : (
                        <i className="bi bi-archive text-secondary opacity-25"></i>
                      )}
                    </button>
                  ) : (
                    project.is_archived && (
                      <i className="bi bi-archive text-info"></i>
                    )
                  )}

                </div>
              </div>
            </div>

            {/* Nombre */}
            <div className="kanban-project-name">
              <a
                href={`/projects/${project.id}/edit/?next=/kanban/`}
                className="text-decoration-none text-reset"
              >
                {project.name}
              </a>
            </div>
          </div>

          {columns.map((column) => {
            const tasks = project.tasks.filter(
              (task) =>
                String(task.status)
                  .trim()
                  .toUpperCase() === column.key
            );

            const compact =
              column.key === "DONE" ||
              column.key === "CANCELLED";

            const cellKey =
              `${project.id}-${column.key}`;

            return (
              <div
                key={column.key}
                className={`kanban-cell ${
                  compact ? "kanban-history" : ""
                } ${
                  dragOver === cellKey
                    ? "drag-over"
                    : ""
                }`}
                data-project={project.id}
                data-status={column.key}
                onDragOver={(event) =>
                  handleDragOver(
                    event,
                    project.id,
                    column.key
                  )
                }
                onDragLeave={() =>
                  setDragOver(null)
                }
                onDrop={(event) =>
                  handleDrop(
                    event,
                    project.id,
                    column.key
                  )
                }
              >
                {tasks.map((task) => (
                  <div
                    key={task.id}
                    className={`kanban-card ${compact ? "compact" : ""}`}
                    data-task-id={task.id}
                    data-title={task.title}
                    data-assigned={task.assigned_to || "Sin asignar"}
                    data-time_remaining={task.time_remaining}
                    data-time_estimated={task.time_estimated ?? "-"}
                    data-planned={task.is_planned ? "true" : "false"}
                    data-can-move={task.can_move ? "true" : "false"}
                    data-priority={task.priority}
                    draggable={Boolean(task.can_move)}
                    onDragStart={(event) =>
                      handleDragStart(event, task, project.id)
                    }
                    onDragEnd={handleDragEnd}
                  >
                    {/* Prioridad y título */}
                    <div className="d-flex align-items-center gap-2 kanban-title-row">

                      {/* Prioridad */}
                      <span className="kanban-priority">
                        {task.priority === "HIGH" && (
                          <i className="bi bi-circle-fill text-danger fs-8 opacity-50"></i>
                        )}

                        {task.priority === "MEDIUM" && (
                          <i className="bi bi-circle-fill text-warning fs-8 opacity-50"></i>
                        )}

                        {task.priority === "LOW" && (
                          <i className="bi bi-circle-fill text-primary fs-8 opacity-50"></i>
                        )}
                      </span>

                      {/* Título */}
                      <a
                        href={`/tasks/${task.id}/edit/?next=/kanban/`}
                        className="kanban-title text-decoration-none text-dark fw-semibold"
                      >
                        {task.title}
                      </a>
                    </div>

                    {/* Detalles */}
                    <div className="kanban-details mt-1">

                      {/* Asignado a */}
                      <div className="d-flex justify-content-between">
                        <small>
                          👤 {task.assigned_to || "Sin asignar"}
                        </small>
                      </div>

                      {/* Fecha y estimado */}
                      <div className="d-flex justify-content-between">

                        {/* Fecha */}
                        <small>
                          📅{" "}
                          {task.due_at
                            ? new Date(task.due_at).toLocaleDateString("es-ES", {
                                day: "2-digit",
                                month: "2-digit",
                                year: "numeric",
                              })
                            : "Sin fecha"}
                        </small>

                        {/* Estimado */}
                        <small>
                          {task.is_planned ? (
                            <>
                              {task.time_estimated ?? "-"} |{" "}
                              {task.time_remaining == null
                                ? "- días"
                                : task.time_remaining < 0
                                  ? "Vencida"
                                  : `${Number(task.time_remaining).toFixed(2)} días`}
                            </>
                          ) : (
                            "Sin planificar"
                          )}
                        </small>
                      </div>

                      {/* Línea temporal */}
                      <div className="d-flex align-items-center gap-1">
                        <small>⏳</small>

                        <div className="kanban-timeline flex-grow-1">

                          {/* Tramo estimado */}
                          <div
                            className="timeline-estimated"
                            style={{
                              left: `${task.timeline_estimated_start_percent}%`,
                              width: `${task.timeline_estimated_percent}%`,
                            }}
                          />

                          {/* Marca del día actual */}
                          <div
                            className="timeline-today"
                            style={{
                              left: `${task.timeline_today_percent}%`,
                            }}
                          />

                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}

export default Kanban;
