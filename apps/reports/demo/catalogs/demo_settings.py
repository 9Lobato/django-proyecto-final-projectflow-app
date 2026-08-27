# apps\reports\demo\catalogs\demo_settings.py sirve para:
# definir los valores y parámetros generales utilizados en la generación de datos de demostración,
# como la duración de la jornada, la antigüedad de los proyectos y los valores iniciales de las instantáneas

# duración de una jornada laboral en minutos
WORKDAY_MINUTES = 8 * 60

# valores de antigüedad utilizados para clasificar los proyectos de demostración
VERY_OLD_PROJECT = 700
OLD_PROJECT = 350
RECENT_PROJECT = 150

# valores predeterminados de progreso para las instantáneas de demostración
DEFAULT_SNAPSHOT_VALUES = [
  {
    "month": "2026-01-01",
    "completion_percentage": 10,
  },
  {
    "month": "2026-02-01",
    "completion_percentage": 40,
  },
  {
    "month": "2026-03-01",
    "completion_percentage": 70,
  },
]
