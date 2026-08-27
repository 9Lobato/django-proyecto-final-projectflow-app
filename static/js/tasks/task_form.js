// static\js\tasks\task_form.js ...
// ... se utiliza en:
// templates\tasks\task_form.html en la gestión del formulario de tareas,
// comentarios y cálculo de tiempo estimado y fecha límite


// =========================================
// FORMULARIO DE TAREAS
// Gestiona los comentarios de la tarea, los cambios
// del formulario y la relación entre tiempo estimado
// y fecha límite.
// =========================================


document.addEventListener("DOMContentLoaded", function () {
  const discardBtn = document.getElementById("discardCommentBtn");
  const textarea = document.getElementById("commentText");
  if (discardBtn && textarea) {
    function updateDiscardButton() {
      discardBtn.style.display =
        textarea.value.trim() ? "inline-block" : "none";
    }
    updateDiscardButton();
    textarea.addEventListener("input", updateDiscardButton);
    discardBtn.addEventListener("click", function () {
      textarea.value = "";
      updateDiscardButton();
      textarea.focus();
    });
  }
  const applyBtn = document.getElementById("applyBtn");
  if (applyBtn) {
    applyBtn.style.display = "none";
    const fields = document.querySelectorAll(
      "input, select, textarea:not(#commentText)");
    fields.forEach(field => {
      field.addEventListener("input", function () {
        applyBtn.style.display = "inline-block";});
      field.addEventListener("change", function () {
        applyBtn.style.display = "inline-block";});
    });
  }
  let selectedComment = null;
  const deleteBtn = document.getElementById("deleteCommentBtn");
  document.querySelectorAll(".comment-item").forEach(item => {
    item.addEventListener("click", function () {
      document.querySelectorAll(".comment-item").forEach(c => {
        c.classList.remove("comment-selected");
      });
      selectedComment = this;
      this.classList.add("comment-selected");
      if (this.dataset.canDelete === "true") {
        deleteBtn.style.display = "inline-block";
      } else {
        deleteBtn.style.display = "none";
      }
    });
  });
  document.getElementById("deleteCommentBtn")
    .addEventListener("click", function() {
      if (!selectedComment) return;
        const commentId = selectedComment.dataset.commentId;
        const csrftoken = getCookie('csrftoken');
        fetch("{% url 'delete_comment' 0 %}".replace("0", commentId), {
          method: "POST",
          credentials: "same-origin",
          headers: {"X-CSRFToken": csrftoken}
        })
        .then(res => res.json())
        .then(data => {
          if (data.ok) {
            selectedComment.remove();
            selectedComment = null;
            deleteBtn.style.display = "none";
            const container = document.getElementById("commentsContainer");
            const remaining = container.querySelectorAll(".comment-item");
            let emptyMsg = document.getElementById("noCommentsMsg");
            if (remaining.length === 0) {
              if (!emptyMsg) {
                emptyMsg = document.createElement("p");
                emptyMsg.id = "noCommentsMsg";
                emptyMsg.className = "text-muted mb-0";
                emptyMsg.textContent = "Sin comentarios";
                container.appendChild(emptyMsg);
              } else {
                emptyMsg.style.display = "block";
              }
            }
          }
        })
        .catch(err => console.error(err));
    });
  const typeField = document.getElementById("id_type");
  const requestContainer = document.getElementById("requestKindContainer");
  function updateRequestVisibility() {
    if (!typeField || !requestContainer)
      return;
    if (typeField.value === "REQUEST") {
      requestContainer.style.display = "block";
    } else {
      requestContainer.style.display = "none";
    }
  }
  if (typeField) {
    updateRequestVisibility();
    typeField.addEventListener(
      "change",
      updateRequestVisibility
    );
  }
  const estimatedField = document.getElementById("id_time_estimated");
  const dueDateField = document.getElementById("id_due_at");
  function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  }
  function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }
  function today() {
    const date = new Date();
    date.setHours(0, 0, 0, 0);
    return date;
  }
  function daysUntil(dateString) {
    const [year, month, day] = dateString.split("-");
    const due = new Date(year, month - 1, day);
    due.setHours(0, 0, 0, 0);
    return Math.max(Math.ceil((due - today()) / (1000 * 60 * 60 * 24)),0);
  }
  if (estimatedField && dueDateField) {
    // Tiempo estimado → Fecha límite
    estimatedField.addEventListener("input", function () {
      const estimated = parseInt(this.value);
      // Si se elimina el tiempo estimado, eliminar la fecha límite
      if (isNaN(estimated)) {
        dueDateField.value = "";
        return;
      }
      const minimumDue = addDays(today(), estimated);
      // Crear fecha mínima si no existe
      if (!dueDateField.value) {
        dueDateField.value = formatDate(minimumDue);
        return;
      }
      const currentDue = new Date(dueDateField.value);
      currentDue.setHours(0, 0, 0, 0);
      // Nunca permitir una fecha menor que el tiempo estimado
      if (currentDue < minimumDue) {
        dueDateField.value = formatDate(minimumDue);
      }
    });
    // Fecha límite → Tiempo estimado
    dueDateField.addEventListener("change", function () {
      // Si se elimina la fecha límite, eliminar tiempo estimado
      if (!this.value) {
        estimatedField.value = "";
        return;
      }
      const availableDays = daysUntil(this.value);
      const estimated = parseInt(estimatedField.value);
      // Si estaba vacío, crear el tiempo estimado
      if (isNaN(estimated)) {
        estimatedField.value = availableDays;
        return;
      }
      // Sólo reducir el tiempo estimado si es necesario
      if (estimated > availableDays) {
        estimatedField.value = availableDays;
      }
    });
  }
});
