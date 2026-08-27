// static\js\projects\project_list.js ...
// ... se utiliza en:
// templates\projects\project_list.html en la gestión de los desplegables
// por año y la conservación de la posición del scroll


// =========================================
// LISTA DE PROYECTOS
// Gestiona los desplegables de la lista de proyectos,
// conserva los años abiertos y restaura la posición
// del scroll al volver a la página.
// =========================================

document.addEventListener("DOMContentLoaded", function () {
  // Obtener años abiertos anteriormente del almacenamiento local
  const storageKey = "open_years";
  let openYears = JSON.parse(localStorage.getItem(storageKey) || "[]");
  // Obtener botones desplegables de proyectos por año
  const buttons = document.querySelectorAll("[data-bs-toggle='collapse']");
  let scrollRestored = false;
  // Restaurar scroll
  function tryRestoreScroll() {
    if (scrollRestored) return;
    // Comprobar que no haya ningún desplegable en proceso de apertura o cierre.
    const allDone = [...buttons].every(btn => {
      const target = document.querySelector(btn.dataset.bsTarget);
      return !target.classList.contains("collapsing");
    });
    if (!allDone) return;
    // Recuperar la posición del scroll del usuario.
    const userId = "{{ request.user.id }}";
    const savedScroll = sessionStorage.getItem(`project_list_scroll_${userId}`);
    if (savedScroll !== null) {
      window.scrollTo(0, parseInt(savedScroll, 10));
      scrollRestored = true;}
  }
  // Desplegables por año
  buttons.forEach(btn => {
    const targetSelector = btn.getAttribute("data-bs-target");
    const target = document.querySelector(targetSelector);
    const icon = btn.querySelector("i");
    const year = btn.dataset.year;
    const section = btn.dataset.section;
    const key = `${section}:${year}`;
    const rememberState = section !== "disponible-a-seguir";
    // Restaurar estado de secciones abiertas anteriormente
    if (rememberState && openYears.includes(key)) {
      new bootstrap.Collapse(target, { toggle: true });
    }
    // Guardar sección como abierta y actualizar icono
    target.addEventListener("show.bs.collapse", () => {
      if (rememberState && !openYears.includes(key)) {
        openYears.push(key);
        localStorage.setItem(storageKey, JSON.stringify(openYears));
      }
      icon?.classList.replace("bi-chevron-right", "bi-chevron-down");
    });
    // Eliminar sección de la lista de años abiertos
    target.addEventListener("hide.bs.collapse", () => {
      if (rememberState) {
        openYears = openYears.filter(y => y !== key);
        localStorage.setItem(storageKey, JSON.stringify(openYears));
      }
      icon?.classList.replace("bi-chevron-down", "bi-chevron-right");
    });
    // Restaurar scroll tras cambiar estado abierto / cerrado
    target.addEventListener("shown.bs.collapse", tryRestoreScroll);
    target.addEventListener("hidden.bs.collapse", tryRestoreScroll);
  });
  setTimeout(tryRestoreScroll, 300);
});
window.addEventListener("beforeunload", function () {
  const userId = "{{ request.user.id }}";
  sessionStorage.setItem(
    `project_list_scroll_${userId}`,
    window.scrollY
  );
});
