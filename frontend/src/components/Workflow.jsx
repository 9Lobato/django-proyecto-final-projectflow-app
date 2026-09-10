// frontend/src/components/Workflow.jsx sirve para:
// mostrar y gestionar el flujo de trabajo de la aplicación,
// manteniendo el progreso y las comprobaciones del usuario.

// Dependencias del frontend
import { useEffect, useState } from "react";


function Workflow() {
  const [workflowData, setWorkflowData] = useState(null);

  /*
  * Se conserva el paso actual en el navegador para que el workflow
  * mantenga su posición al cambiar de página o recargar.
  */

  const [currentStep, setCurrentStep] = useState(() => {
    const saved = localStorage.getItem("projectflow_workflow_current");
    return saved ? parseInt(saved, 10) : 0;
  });

  const [checkedItems, setCheckedItems] = useState({});

  /*
  * El estado abierto/cerrado también se conserva entre páginas.
  */

  const [isOpen, setIsOpen] = useState(() => {
    return localStorage.getItem("projectflow_workflow_open") === "true";
  });

  useEffect(() => {
    async function loadWorkflow() {
      try {
        const response = await fetch("/api/workflow/", {
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("No se pudo cargar el workflow.");
        }

        const data = await response.json();

        setWorkflowData(data);
        setCheckedItems(data.workflow_checks || {});
      } catch (error) {
        console.error("WORKFLOW ERROR:", error);
      }
    }

    loadWorkflow();
  }, []);
  if (!workflowData) {
    return null;
  }

  const steps = workflowData.workflow_steps || [];

  if (steps.length === 0) {
    return null;
  }

  const validCurrentStep = Math.min(
    Math.max(currentStep, 0),
    steps.length - 1
  );

  const step = steps[validCurrentStep];

  async function toggleItem(itemIndex) {
    const key = `${currentStep}-${itemIndex}`;

    const updated = {
      ...checkedItems,
      [key]: !checkedItems[key],
    };

    setCheckedItems(updated);

    try {
      const csrfToken = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        ?.split("=")[1];

      const response = await fetch("/api/workflow/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        credentials: "include",
        body: JSON.stringify({
          checks: updated,
        }),
      });

      if (!response.ok) {
        throw new Error("No se pudieron guardar los checks.");
      }
    } catch (error) {
      console.error("WORKFLOW CHECKS ERROR:", error);
    }
  }

  function previousStep() {
    setCurrentStep((previous) => {
      const next = previous === 0 ? steps.length - 1 : previous - 1;
      localStorage.setItem("projectflow_workflow_current", next);
      return next;
    });
  }

  function nextStep() {
    setCurrentStep((previous) => {
      const next = previous === steps.length - 1 ? 0 : previous + 1;
      localStorage.setItem("projectflow_workflow_current", next);
      return next;
    });
  }

  return (
    <div id="workflow-widget">
      <div id="workflow-panel" className={isOpen ? "open" : ""}>
        <button
          id="workflow-prev"
          type="button"
          className="workflow-arrow"
          onClick={previousStep}
        >
          <i className="bi bi-chevron-left"></i>
        </button>

        <div id="workflow-content">
          <div id="workflow-title">
            <a href={step.url}>{step.title}</a>
          </div>

          <div id="workflow-text">
            {step.items.map((item, index) => {
              const key = `${currentStep}-${index}`;

              return (
                <label
                  className="workflow-check"
                  key={key}
                >
                  <input
                    type="checkbox"
                    checked={Boolean(checkedItems[key])}
                    onChange={() => toggleItem(index)}
                  />

                  <span>{item}</span>
                </label>
              );
            })}
          </div>
        </div>

        <button
          id="workflow-next"
          type="button"
          className="workflow-arrow"
          onClick={nextStep}
        >
          <i className="bi bi-chevron-right"></i>
        </button>
      </div>

      <button
        id="workflow-toggle"
        type="button"
        className="btn btn-info shadow"
        aria-expanded={isOpen}
        onClick={() => {
          setIsOpen((previous) => {
            const next = !previous;
            localStorage.setItem(
              "projectflow_workflow_open",
              next ? "true" : "false"
            );
            return next;
          });
        }}
      >
        <span>
          Workflow for a {workflowData.workflow_role?.toLowerCase()}
        </span>

        <span id="workflow-counter">
          {currentStep + 1} / {steps.length}
        </span>
      </button>
    </div>
  );
}

export default Workflow;
