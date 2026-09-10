// frontend/src/components/Start.jsx sirve para:
// mostrar la guía rápida de la aplicación,
// adaptando las secciones disponibles al rol del usuario.

// Dependencias del frontend
import { useEffect, useState } from "react";
// Estilos del frontend
import "../styles/start.css";


// Secciones disponibles en la guía rápida.
// CONFIG determina qué secciones se resaltan para cada rol.

const CONFIG = {
  OWNER: {
    selected: ["project", "management"],
  },
  MANAGER: {
    selected: ["task", "kanban", "report"],
  },
  MEMBER: {
    selected: ["task", "kanban"],
  },
};

function Start() {
  const [workflowData, setWorkflowData] = useState(null);
  const [activeStep, setActiveStep] = useState(0);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadWorkflow() {
      try {
        const response = await fetch("/api/workflow/", {
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error(
            "No se pudo cargar la información de la guía rápida."
          );
        }

        const data = await response.json();

        setWorkflowData(data);
      } catch (error) {
        console.error("START WORKFLOW ERROR:", error);
        setError(error.message);
      }
    }

    loadWorkflow();
  }, []);

  if (!workflowData) {
    return null;
  }

  // El backend determina el rol y el flujo de trabajo.
  // Si no llega un rol válido, se utiliza MEMBER como valor seguro.

  const role = workflowData.workflow_role || "MEMBER";
  const steps = workflowData.workflow_steps || [];
  const selectedAreas = CONFIG[role]?.selected || [];

  function isSelected(area) {
    return selectedAreas.includes(area);
  }

  function handleStepClick(index) {
    setActiveStep(index);
  }

  function handleGuide() {
    if (steps.length === 0) {
      return;
    }

    const firstStep = steps[0];

    window.location.href =
      `${firstStep.url}?workflow=open&workflow_step=0`;
  }

  return (
    <div className="container mt-4">
      <h1 className="mb-5">Guia rápida</h1>

      {error && <p>{error}</p>}

      <div className="mb-4">

        <div className="mb-5">
          <h3 className="mb-3">¿Qué és ProjectFlow?</h3>

          <p className="mb-0">
            ProjectFlow es una aplicación para gestionar proyectos,
            organizar tareas y facilitar la colaboración entre los miembros
            de un equipo.
            <br />
            Su objetivo es ofrecer una visión clara del trabajo pendiente,
            mejorar la comunicación y permitir un seguimiento sencillo del
            progreso de cada proyecto.
          </p>
        </div>

        <div className="mb-5">
          <h3 className="mb-3">¿Qué puedes hacer en ProjectFlow?</h3>

          <p className="mb-0">
            ✓ Crear y gestionar proyectos.
            <br />
            ✓ Incorporar miembros de proyecto.
            <br />
            ✓ Definir equipos de trabajo de proyecto.
            <br />
            ✓ Crear tareas y asignarlas a los miembros del equipo de trabajo.
            <br />
            ✓ Controlar el estado, prioridad y fecha límite de cada tarea.
            <br />
            ✓ Mantener conversaciones mediante comentarios.
            <br />
            ✓ Realizar solicitudes entre los miembros del equipo y gestionar
            su resolución.
            <br />
            ✓ Visualizar el progreso del proyecto desde el Kanban.
            <br />
            ✓ Obtener informes de proyecto.
            <br />
          </p>
        </div>

        <div className="mb-5">
          <h3 className="mb-3">¿Qué rol ocupas?</h3>

          <div className="row text-center">

            <div className="col-md-4 mb-3">
              <div
                className={`card h-100 shadow-sm ${
                  role === "OWNER"
                    ? "border-primary bg-light"
                    : ""
                }`}
              >
                <div className="card-body">
                  <div className="d-flex justify-content-center align-items-center gap-2 mb-2">
                    <h5 className="mb-0">Owner</h5>
                    <i className="bi bi-emoji-sunglasses"></i>
                  </div>

                  <p className="mb-0">
                    Administra completamente la aplicación y todos los
                    proyectos. Gestiona equipos y solicitudes.
                  </p>
                </div>
              </div>
            </div>

            <div className="col-md-4 mb-3">
              <div
                className={`card h-100 shadow-sm ${
                  role === "MANAGER"
                    ? "border-primary bg-light"
                    : ""
                }`}
              >
                <div className="card-body">
                  <div className="d-flex justify-content-center align-items-center gap-2 mb-2">
                    <h5 className="mb-0">Manager</h5>
                    <i className="bi bi-emoji-smile"></i>
                  </div>

                  <p className="mb-0">
                    Gestiona proyectos, solicitudes y comentarios, organiza
                    tareas y coordina el trabajo del equipo.
                  </p>
                </div>
              </div>
            </div>

            <div className="col-md-4 mb-3">
              <div
                className={`card h-100 shadow-sm ${
                  role === "MEMBER"
                    ? "border-primary bg-light"
                    : ""
                }`}
              >
                <div className="card-body">
                  <div className="d-flex justify-content-center align-items-center gap-2 mb-2">
                    <h5 className="mb-0">Member</h5>
                    <i className="bi bi-emoji-smile-upside-down"></i>
                  </div>

                  <p className="mb-0">
                    Ejecuta las tareas asignadas y colabora con su equipo de
                    trabajo mediante comentarios.
                  </p>
                </div>
              </div>
            </div>

          </div>
        </div>

        <div className="mb-5">
          <h3 className="mb-3">
            ¿En que secciones intervienes?
          </h3>

          <div className="row text-center">

            <div className="col-md-3 mb-3">

              <div
                id="card-project"
                className={`card shadow-sm mb-3 ${
                  isSelected("project")
                    ? "border-primary bg-light"
                    : ""
                }`}
              >
                <div className="card-body">
                  <div className="d-flex justify-content-center align-items-center gap-2 mb-1">
                    <h5 className="mb-1">Proyectos</h5>
                    <i className="bi bi-folder2-open"></i>
                  </div>

                  <p className="small mb-0">
                    Agrupa toda la información relacionada con un trabajo o
                    iniciativa.
                  </p>
                </div>
              </div>

              <div
                id="card-task"
                className={`card shadow-sm ${
                  isSelected("task")
                    ? "border-primary bg-light"
                    : ""
                }`}
              >
                <div className="card-body">
                  <div className="d-flex justify-content-center align-items-center gap-2 mb-1">
                    <h5 className="mb-1">Tareas</h5>
                    <i className="bi bi-folder2-open"></i>
                  </div>

                  <p className="small mb-0">
                    Dividen el proyecto en actividades concretas.
                  </p>
                </div>
              </div>

            </div>

            <div className="col-md-3 mb-3">

              <div
                id="card-kanban"
                className={`card h-100 shadow-sm ${
                  isSelected("kanban")
                    ? "border-primary bg-light"
                    : ""
                }`}
              >
                <div className="card-body">
                  <div className="d-flex justify-content-center align-items-center gap-2 mb-1">
                    <h5 className="mb-1">Kanban</h5>
                    <i className="bi bi-folder2-open"></i>
                  </div>

                  <p className="mb-0">
                    Permite visualizar todas las tareas del proyecto
                    organizadas por estado, facilitando el seguimiento del
                    trabajo y la planificación del equipo.
                  </p>
                </div>
              </div>

            </div>

            <div className="col-md-3 mb-3">

              <div
                id="card-report"
                className={`card h-100 shadow-sm ${
                  isSelected("report")
                    ? "border-primary bg-light"
                    : ""
                }`}
              >
                <div className="card-body">
                  <div className="d-flex justify-content-center align-items-center gap-2 mb-1">
                    <h5 className="mb-1">Informe</h5>
                    <i className="bi bi-folder2-open"></i>
                  </div>

                  <p className="small mb-0">
                    Muestra indicadores del proyecto, evolución de las
                    tareas y estadísticas que ayudan a controlar el progreso
                    y detectar incidencias.
                  </p>
                </div>
              </div>

            </div>

            <div className="col-md-3 mb-3">

              <div
                id="card-management"
                className={`card h-100 shadow-sm ${
                  isSelected("management")
                    ? "border-primary bg-light"
                    : ""
                }`}
              >
                <div className="card-body">
                  <div className="d-flex justify-content-center align-items-center gap-2 mb-1">
                    <h5 className="mb-1">Gestión</h5>
                    <i className="bi bi-folder2-open"></i>
                  </div>

                  <p className="small mb-0">
                    Permite administrar usuarios, proyectos, equipos de
                    trabajo, clientes y la configuración general de la
                    aplicación, según el rol asignado.
                  </p>
                </div>
              </div>

            </div>

          </div>
        </div>

        <div className="mb-5">
          <h3 className="mb-3">
            Flujo de trabajo recomendado
          </h3>

          {steps.length > 0 ? (
            <div className="workflow-steps">

              {steps.map((step, index) => (
                <div
                  className={`workflow-step-group ${
                    index === activeStep ? "active" : ""
                  }`}
                  key={step.title}
                >
                  <div className="workflow-step">

                    <div className="card h-100 shadow-sm">
                      <div className="card-body">

                        <div className="workflow-step-header">

                          <div className="workflow-step-title">
                            <a
                              href={step.url}
                              className="text-decoration-none text-dark"
                            >
                              <span>{step.title}</span>
                            </a>
                          </div>

                          <button
                            type="button"
                            className="workflow-step-number"
                            aria-expanded={
                              index === activeStep
                            }
                            aria-label={`Mostrar ${step.title}`}
                            onClick={() =>
                              handleStepClick(index)
                            }
                          >
                            <strong>{index + 1}</strong>
                          </button>

                        </div>

                      </div>
                    </div>

                  </div>

                  <div className="workflow-step-items">
                    <ul>
                      {step.items.map((item) => (
                        <li key={item}>{item}</li>
                      ))}
                    </ul>
                  </div>

                </div>
              ))}

            </div>
          ) : (
            <p className="text-muted mb-0">
              Selecciona un rol para ver el flujo de trabajo recomendado.
            </p>
          )}
        </div>

        <div className="d-flex gap-2 mt-4">

          {steps.length > 0 && (
            <button
              type="button"
              className="btn btn-info"
              style={{ width: "100px" }}
              onClick={handleGuide}
            >
              Guíame
            </button>
          )}

          <a
            href="/"
            className="btn btn-secondary"
            style={{ width: "100px" }}
          >
            Volver
          </a>

        </div>

      </div>
    </div>
  );
}

export default Start;
