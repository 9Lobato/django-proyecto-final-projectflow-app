// static\js\common\utils.js ...
// ... se utiliza en:
// templates\base.html en la carga global de utilidades JavaScript


// =========================================
// COOKIES
// Obtiene el valor de una cookie a partir de su nombre
// para que otros scripts puedan utilizarla.
// =========================================

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
