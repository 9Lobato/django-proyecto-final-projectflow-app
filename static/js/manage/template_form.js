// static\js\manage\template_form.js ...
// ... se utiliza en:
// templates\manage\template_form.html en la gestión del formulario de plantillas, sus tareas asociadas y el guardado automático de cambios


// =========================================
// GESTIÓN DEL FORMULARIO DE PLANTILLA
// Gestiona la creación, eliminación y guardado
// de las tareas asociadas a una plantilla.
// =========================================

document.addEventListener("DOMContentLoaded", function () {
  // Obtner los elementos del formulario
  const addBtn = document.getElementById("add-task");
  const container = document.getElementById("task-container");
  const template = document.getElementById("empty-form");
  const totalForms = document.querySelector("input[name$='-TOTAL_FORMS']");
  // Comprueba que existan los elementos necesarios para el formset
  if (!addBtn || !container || !template || !totalForms) {
    console.error("Formset no inicializado");
    return;}
  // Añadir tarea al formulario utilizando formset
  addBtn.addEventListener("click", function () {
    const noTasksMessage = document.getElementById("no-tasks-message");
    if (noTasksMessage) {noTasksMessage.remove();}
    // Comprobar nueva tarea
    const existingNew = document.querySelector("#task-container .new-task");
    if (existingNew) return;
    // Crear formulario de tarea
    const index = parseInt(totalForms.value);
    const html = template.innerHTML.replace(/__prefix__/g, index);
    container.insertAdjacentHTML("afterbegin", html);
    // Actualizar el número total de formularios
    totalForms.value = index + 1;
  });
});
// Mostrar mensaje para formularios sin tareas
function showNoTasksMessageIfNeeded() {
  const container = document.getElementById("task-container");
  const remainingTasks = container.querySelectorAll(".task-card").length;
  let message = document.getElementById("no-tasks-message");
  if (remainingTasks === 0 && !message) {
    message = document.createElement("div");
    message.id = "no-tasks-message";
    message.className = "alert border mb-4";
    message.innerHTML =
      "No existen tareas. Pulsa <strong>Nueva tarea</strong> para añadir una.";
    container.insertAdjacentElement("beforebegin", message);
  }
}
// Marca la tarea seleccionada para su eliminación
function markDelete(btn) {
  const card = btn.closest(".task-card");
  const deleteInput =
    card.querySelector("input[name$='-DELETE']");
  if (!deleteInput) return;
  deleteInput.checked = true;
  autoSaveFormset()
    .then(() => {
      card.remove();
      showNoTasksMessageIfNeeded();
    })
    .catch(error => {
      console.error(error);
    });
}
// Envía el formulario de plantilla al servidor
function autoSaveFormset() {
  const form = document.getElementById("template-form");
  const formData = new FormData(form);
  return fetch(window.location.href, {
    method: "POST",
    body: formData,
    headers: {"X-Requested-With": "XMLHttpRequest"}
  });
}
// Oculta inicialmente el botón Aplicar y lo muestra tras algún cambio
document.addEventListener("DOMContentLoaded", function () {
  const applyBtn = document.getElementById("applyBtn");
  if (!applyBtn) return;
  applyBtn.style.display = "none";
  const fields = document.querySelectorAll(
      "#template-form input, #template-form textarea, #template-form select");
  fields.forEach(field => {
    field.addEventListener("input", function () {applyBtn.style.display = "inline-block";});
    field.addEventListener("change", function () {applyBtn.style.display = "inline-block";});
  });
});
