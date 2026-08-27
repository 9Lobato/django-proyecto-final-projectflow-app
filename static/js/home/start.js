// static\js\home\start.js ...
// ... se utiliza en:
// templates\home\start.html en la página inicial de selección de área


// =========================================
// CONFIGURACIÓN DE ÁREAS
// Define las áreas que se seleccionan automáticamente
// para cada rol de usuario y las áreas que pueden aparecer
// en la página inicial.
// =========================================

const AREAS = ["project", "task", "kanban", "report", "management"];
const CONFIG = {
  OWNER: { selected: ["project", "management"] },
  MANAGER: { selected: ["task", "kanban", "report"] },
  MEMBER: { selected: ["task", "kanban"] }
};


// =========================================
// ACTUALIZAR ÁREAS
// Marca visualmente las áreas correspondientes
// al rol del usuario actual.
// =========================================

function updateAreas(role) {
  // Quitar la selección actual de todas las áreas
  AREAS.forEach(area => {
    document
      .getElementById(`card-${area}`)
      ?.classList.remove("border-primary", "bg-light");
  });
  // Marcar las áreas correspondientes al rol
  CONFIG[role]?.selected.forEach(area => {
    document
      .getElementById(`card-${area}`)
      ?.classList.add("border-primary", "bg-light");
  });
}
document.addEventListener("DOMContentLoaded", function () {
  /* Áreas según el rol */
  updateAreas(window.selectedRole || "MEMBER");
  /* Flujo de trabajo */
  const workflowGroups = document.querySelectorAll(".workflow-step-group");
  workflowGroups.forEach((group) => {
    const button = group.querySelector(".workflow-step-number");
    if (!button) {return}
    // Detectar cuándo el usuario pulsa el número de un paso del workflow.
    button.addEventListener("click", function () {
      // Quitar el estado activo de todos
      workflowGroups.forEach((item) => {
        item.classList.remove("active");
        const itemButton = item.querySelector(".workflow-step-number");
        if (itemButton) {
          itemButton.setAttribute("aria-expanded", "false");
        }
      });
      // Activar el seleccionado
      group.classList.add("active");
      button.setAttribute("aria-expanded", "true");
    });
  });
});
