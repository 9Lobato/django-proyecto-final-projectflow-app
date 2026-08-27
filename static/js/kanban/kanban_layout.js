// static\js\kanban\kanban_layout.js ...
// ... se utiliza en:
// templates\kanban\kanban.html en la gestión del scroll y la altura de las filas del tablero


// =========================================
// SCROLL KANBAN
// Guarda y restaura la posición del scroll del tablero
// para mantener la posición del usuario al navegar.
// =========================================

// Restaurar scroll Kanban
function restoreKanbanScroll() {
  const savedScroll = sessionStorage.getItem("kanban_scroll");
  if (savedScroll !== null) {
    window.scrollTo(0, parseInt(savedScroll, 10));
  }
}
// Guardar scroll Kanban
function saveKanbanScroll() {
  sessionStorage.setItem("kanban_scroll", window.scrollY);
}
// Restaurar el scroll al cargar la página
document.addEventListener(
  "DOMContentLoaded",
  function () {
    restoreKanbanScroll();
  }
);
// Restaurar el scroll al recuperar la página
window.addEventListener(
  "pageshow",
  function () {
    restoreKanbanScroll();
  }
);
// Guardar la posición del scroll antes de salir
window.addEventListener(
  "beforeunload",
  function () {
    saveKanbanScroll();
  }
);


// =========================================
// AJUSTAR ALTURA DE LAS FILAS
// Calcula la altura necesaria para cada fila
// según el contenido de las columnas activas.
// =========================================

const KANBAN_MIN_HEIGHT = 246.36;
// Cálculo de la altura necesaria para cada fila según el contenido de las columnas activas.
function adjustKanbanHeights() {
  document.querySelectorAll(".kanban-row").forEach(row => {
    const todo = row.querySelector('[data-status="TODO"]');
    const progress = row.querySelector('[data-status="IN_PROGRESS"]');
    const histories = row.querySelectorAll(".kanban-history");
    const todoHeight = todo ? todo.scrollHeight : 0;
    const progressHeight = progress ? progress.scrollHeight : 0;
    const rowHeight = Math.max(KANBAN_MIN_HEIGHT, todoHeight, progressHeight);
    // Altura de fila base
    row.querySelector(".kanban-project").style.height = rowHeight + "px";
    row.querySelectorAll('.kanban-cell:not(.kanban-history)'
    ).forEach(cell => {
      cell.style.height = rowHeight + "px";
      cell.style.maxHeight = rowHeight + "px";
    });
    // Mantener las columnas históricas con la misma altura.
    histories.forEach(cell => {
      cell.style.height = rowHeight + "px";
      cell.style.maxHeight = rowHeight + "px";
      cell.style.overflowY = "auto";
    });
  });
};
// Ajuste altura elementos y contenidos al terminar de cargar.
window.addEventListener(
  "load",
  function () {
    adjustKanbanHeights();
  }
);
// Ajuste altura elementos al cambiar el tamaño de la ventana del navegador.
window.addEventListener(
  "resize",
  adjustKanbanHeights
);
