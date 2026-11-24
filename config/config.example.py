"""
Configuración de ejemplo para reproducir la arquitectura.

No incluir credenciales, tokens ni claves privadas.
Cada usuario debe adaptar PROJECT_ID a su propia cuenta
de Google Cloud.
"""

PROJECT_ID = "TU_PROJECT_ID"

DATASET_ID = "retail_analytics"

TABLE_ID = "superstore_sales"

FULL_TABLE = (
    f"{PROJECT_ID}."
    f"{DATASET_ID}."
    f"{TABLE_ID}"
)

# Límite opcional de bytes facturables por consulta.
# Puede modificarse según el escenario de reproducción.
MAXIMUM_BYTES_BILLED = 100_000_000
