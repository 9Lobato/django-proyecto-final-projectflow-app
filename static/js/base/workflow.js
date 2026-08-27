// static\js\base\workflow.js ...
// ... se utiliza en:
// templates\base.html en el panel de flujo de trabajo


document.addEventListener("DOMContentLoaded", function () {

  
  // =========================================
  // ELEMENTOS
  // Obtiene los elementos del panel de ayuda
  // que serán utilizados por el script.
  // =========================================

  const workflowData = document.getElementById("workflow-data");
  const panel = document.getElementById("workflow-panel");
  const toggle = document.getElementById("workflow-toggle");
  const title = document.getElementById("workflow-title");
  const text = document.getElementById("workflow-text");
  const counter = document.getElementById("workflow-counter");
  const prev = document.getElementById("workflow-prev");
  const next = document.getElementById("workflow-next");
  // Comprueba que existen los elementos principales necesarios para ejecutar el workflow.
  if (!workflowData || !panel || !toggle) {
    console.error("Workflow: faltan elementos necesarios en el HTML.");
    return;
  }


  // =========================================
  // DATOS DEL WORKFLOW
  // Lee los pasos del flujo de trabajo definidos
  // en el HTML y comprueba que tengan un formato válido.
  // =========================================

  let steps;
  try {
    steps = JSON.parse(workflowData.textContent);
  } catch (error) {
    console.error("Workflow: no se pudieron leer workflow_steps.", error);
    return;
  }
  if (!Array.isArray(steps) || steps.length === 0) {
    toggle.style.display = "none";
    return;
  }


  // =========================================
  // STORAGE
  // Define las claves utilizadas para conservar
  // el estado del workflow entre páginas y sesiones.
  // =========================================

  const CHECKS_STORAGE_KEY = "projectflow_workflow_checks";
  const PANEL_STORAGE_KEY = "projectflow_workflow_open";
  const CURRENT_STORAGE_KEY = "projectflow_workflow_current";


  // =========================================
  // URL Y PÁGINA ACTUAL
  // Comprueba la página actual y los parámetros de URL
  // utilizados para abrir y posicionar el workflow.
  // =========================================

  const url = new URL(window.location.href);
  const isStartPage = window.location.pathname === "/start/" || window.location.pathname === "/start";
  const workflowOpen = url.searchParams.get("workflow") === "open";


  // =========================================
  // ESTADO INICIAL
  // Determina el paso que debe mostrarse inicialmente,
  // recuperando el último paso guardado cuando corresponde.
  // =========================================

  let current;
  if (isStartPage) {
    current = 0;
    localStorage.setItem(CURRENT_STORAGE_KEY, "0");
    localStorage.removeItem(PANEL_STORAGE_KEY);
  } else {
    const savedCurrent = parseInt(localStorage.getItem(CURRENT_STORAGE_KEY) || "0", 10);
    current = Math.min(Math.max(savedCurrent, 0), steps.length - 1);
  }


  // =========================================
  // ABRIR / CERRAR PANEL
  // Controla la visibilidad del panel y guarda
  // su estado para recuperarlo al cambiar de página.
  // =========================================

  function setWorkflowOpen(open, save = true) {
    panel.classList.toggle("open", open);
    toggle.setAttribute(
      "aria-expanded",
      open ? "true" : "false"
    );
    if (save) {
      localStorage.setItem(
        PANEL_STORAGE_KEY,
        open ? "true" : "false"
      );
    }
  }


  // =========================================
  // CHECKS
  // Lee y guarda en localStorage los puntos completados
  // por el usuario en cada paso del workflow.
  // =========================================

  function getChecks() {
    try {
      return JSON.parse(
        localStorage.getItem(CHECKS_STORAGE_KEY) || "{}"
      );
    } catch (error) {
      console.error("Workflow: error leyendo checks.", error);
      return {};
    }
  }
  function saveChecks(checks) {
    localStorage.setItem(
      CHECKS_STORAGE_KEY,
      JSON.stringify(checks)
    );
  }


  // =========================================
  // RENDER
  // Actualiza el contenido visible del workflow según
  // el paso actual y restaura los checks guardados.
  // =========================================

  function render() {
    const step = steps[current];
    if (!step) {
      console.error("Workflow: paso no encontrado:", current);
      return;
    }
    counter.textContent = `${current + 1} / ${steps.length}`;
    title.innerHTML = `<a href="${step.href || "#"}">${step.title || ""}</a>`;
    text.innerHTML = (step.items || [])
      .map((item, index) => `
        <label class="workflow-check">
          <input
            type="checkbox"
            data-step="${current}"
            data-item="${index}"
          >
          <span>${item}</span>
        </label>
      `)
      .join("");
    // Recupera el estado guardado de cada check y registra los cambios realizados por el usuario.
    const checks = getChecks();
    text
      .querySelectorAll("input[type='checkbox']")
      .forEach(checkbox => {
        const key = `${current}-${checkbox.dataset.item}`;
        checkbox.checked = checks[key] === true;
        checkbox.addEventListener(
          "change",
          function () {
            const checks = getChecks();
            checks[key] = checkbox.checked;
            saveChecks(checks);
          }
        );
      });
    // Activa o desactiva la navegación según la posición del paso actual.
    prev.disabled = current === 0;
    next.disabled = false;
  }
  // Muestra el contenido correspondiente al paso seleccionado al cargar la página.
  render();


  // =========================================
  // RESTAURAR ESTADO DEL PANEL
  // Recupera si el panel estaba abierto o cerrado
  // en la navegación anterior.
  // =========================================

  if (isStartPage) {
    setWorkflowOpen(false, false);
  } else {
    const savedOpen = localStorage.getItem(PANEL_STORAGE_KEY) === "true";
    setWorkflowOpen(savedOpen, false);
  }


  // =========================================
  // BOTÓN FLUJO DE TRABAJO
  // Permite abrir y cerrar manualmente el panel
  // de ayuda mediante el botón principal.
  // =========================================

  toggle.addEventListener(
    "click",
    function () {
      const isOpen = panel.classList.contains("open");
      setWorkflowOpen(!isOpen);
    }
  );


  // =========================================
  // SIGUIENTE
  // Avanza al siguiente paso del workflow y vuelve
  // al primero cuando se alcanza el último paso.
  // =========================================

  next.addEventListener(
    "click",
    function () {
      if (current < steps.length - 1) {
        current++;
      } else {
        current = 0;
      }
      localStorage.setItem(CURRENT_STORAGE_KEY, current);
      render();
    }
  );


  // =========================================
  // ANTERIOR
  // Retrocede al paso anterior cuando existe
  // un paso previo al actual.
  // =========================================

  prev.addEventListener(
    "click",
    function () {
      if (current > 0) {
        current--;
        localStorage.setItem(CURRENT_STORAGE_KEY, current);
        render();
      }
    }
  );


  // =========================================
  // "GUÍAME"
  // Procesa los parámetros de navegación de la URL
  // para abrir el workflow directamente en el paso indicado.
  // =========================================

  if (!isStartPage && workflowOpen) {
    const workflowStep = url.searchParams.get("workflow_step");
    if (workflowStep !== null) {
      current = Math.min(Math.max(parseInt(workflowStep, 10) || 0, 0), steps.length - 1);
    } else {
      current = 0;
    }
    // Guarda y muestra el paso indicado y elimina los parámetros temporales de la URL.
    localStorage.setItem(CURRENT_STORAGE_KEY, current);
    render();
    setWorkflowOpen(true);
    url.searchParams.delete("workflow");
    url.searchParams.delete("workflow_step");
    window.history.replaceState({}, "", url);
  }
});
