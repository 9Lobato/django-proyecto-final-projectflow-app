// static\js\common\template_selector.js ...
// ... se utiliza en:
// templates\manage\user_form.html en el selector de plantilla de usuario
// templates\projects\project_form.html en el selector de plantilla de proyecto


document.addEventListener("DOMContentLoaded", function () {


  // =========================================
  // ELEMENTOS
  // Obtiene los campos del formulario que se utilizan
  // para seleccionar una plantilla y mostrar sus datos.
  // =========================================
  
  const templateSelect = document.getElementById("id_template");
  const nameInput = document.getElementById("id_name");
  const descriptionInput = document.getElementById("id_description");


  // =========================================
  // SELECTOR DE PLANTILLA
  // Detecta cuándo el usuario selecciona una plantilla
  // y obtiene los datos asociados a esa opción.
  // =========================================

  if (!templateSelect) return;
  templateSelect.addEventListener("change", function () {
    const option = templateSelect.options[templateSelect.selectedIndex];
    if (!templateSelect.value) return;
    const templateName = option.getAttribute("data-name");
    const templateDescription = option.getAttribute("data-description");
    // Rellena los campos de nombre y descripción con los datos de la plantilla seleccionada.
    if (nameInput) {nameInput.value = templateName || ""}
    if (descriptionInput) {descriptionInput.value = templateDescription || ""}
  });
});
