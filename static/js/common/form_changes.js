// static\js\common\form_changes.js ...
// ... se utiliza en:
// templates\manage\user_form.html en el formulario de usuarios
// templates\projects\project_form.html en el formulario de proyectos


document.addEventListener("DOMContentLoaded", function () {

  
  // =========================================
  // BOTÓN APLICAR
  // Obtiene el botón Aplicar y lo oculta
  // hasta que el usuario modifique algún campo.
  // =========================================

  const applyBtn = document.getElementById("applyBtn");
  if (applyBtn) {applyBtn.style.display = "none";
    // Detecta los cambios realizados en los campos para mostrar el botón Aplicar.
    const fields = document.querySelectorAll("input, textarea, select");
    fields.forEach(field => {
      // Cambio de valor
      field.addEventListener("input", function () {
        applyBtn.style.display = "inline-block";});
      // Cambio confirmado del campo
      field.addEventListener("change", function () {
        applyBtn.style.display = "inline-block";});
    });
  }
});
