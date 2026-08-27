// static\js\tasks\task_list.js ...
// ... se utiliza en:
// templates\tasks\task_list.html en la gestión de filtros, proyectos desplegados y posición del scroll


// =========================================
// LISTADO DE TAREAS
// Gestiona los filtros de estado, entrega y prioridad,
// el estado de los proyectos desplegados y la posición
// del scroll del listado.
// =========================================

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
  sessionStorage.setItem(`task_list_scroll_${userId}`, window.scrollY);
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
