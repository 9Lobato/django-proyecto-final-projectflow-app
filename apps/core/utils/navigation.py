# apps\core\utils\navigation.py sirve para:
# proporcionar funciones auxiliares reutilizables para la navegación
# entre elementos y para comprobar si un usuario puede eliminarse

# Librerías estándar de Python
# Librerías externas (Django, requests, openpyxl, reportlab, etc.)
# Imports internos de proyecto/apps


# devuelve el elemento anterior y el siguiente de una colección
def get_previous_next(items, current):

  items = list(items)

  if not items:
    return None, None

  if len(items) == 1:
    return current, current

  try:
    index = next(i for i, item in enumerate(items) if item.id == current.id)
  except StopIteration:
    return None, None

  previous_item = items[index - 1] if index > 0 else items[-1]
  next_item = items[index + 1] if index < len(items) - 1 else items[0]

  return previous_item, next_item


# comprueba si un usuario puede ser eliminado
def user_can_be_deleted(user, request):
  return not (
    user == request.user
    or user.is_superuser
    or user.project_assignments.exists()
  )
