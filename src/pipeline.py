"""
Pipeline reproducible de la arquitectura analítica cloud.

Este módulo integra:

1. Preparación del dataset.
2. Carga hacia Google BigQuery.
3. Recuperación de datos.
4. Cálculo de KPI.
5. Validación funcional.
6. Generación del dashboard.

Debe ejecutarse desde la raíz del repositorio.

Ejemplo:

    python -m src.pipeline
"""

from pathlib import Path

from google.cloud import bigquery

from src.data_preparation import prepare_dataset
from src.bigquery_loader import upload_dataset
from src.kpi_calculation import calculate_kpis
from src.dashboard_generator import generate_dashboard
from tests.validation_20_scenarios import (
    run_validation,
    print_validation_summary,
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

PROJECT_ID = "TU_PROJECT_ID"

DATASET_ID = "retail_analytics"

TABLE_ID = "superstore_sales"

DATASET_PATH = Path(
    "data/Sample-Superstore.csv"
)

DASHBOARD_TEMPLATE = Path(
    "dashboard/dashboard_template.html"
)

DASHBOARD_OUTPUT = Path(
    "dashboard/dashboard_retail.html"
)

MAXIMUM_BYTES_BILLED = 100_000_000


def build_full_table() -> str:
    """
    Construye el identificador completo
    de la tabla BigQuery.
    """

    return (
        f"{PROJECT_ID}."
        f"{DATASET_ID}."
        f"{TABLE_ID}"
    )


def retrieve_bigquery_data(
    client: bigquery.Client,
    full_table: str,
):
    """
    Recupera la tabla analítica desde BigQuery
    hacia un Pandas DataFrame.
    """

    query = f"""
    SELECT *
    FROM `{full_table}`
    """

    job_config = bigquery.QueryJobConfig(
        maximum_bytes_billed=(
            MAXIMUM_BYTES_BILLED
        )
    )

    query_job = client.query(
        query,
        job_config=job_config,
    )

    dataframe = (
        query_job
        .result()
        .to_dataframe()
    )

    return dataframe


def print_kpi_summary(
    kpis: dict,
) -> None:
    """
    Muestra los KPI globales.
    """

    print("\nKPI GLOBALES")
    print("-" * 50)

    print(
        f"Ventas: "
        f"{kpis['sales']:.2f}"
    )

    print(
        f"Beneficio: "
        f"{kpis['profit']:.2f}"
    )

    print(
        f"Margen: "
        f"{kpis['margin'] * 100:.2f}%"
    )

    print(
        f"Pedidos: "
        f"{kpis['orders']}"
    )

    print(
        f"Clientes: "
        f"{kpis['customers']}"
    )


def run_pipeline() -> None:
    """
    Ejecuta la arquitectura completa.
    """

    print(
        "\nRETAIL CLOUD ANALYTICS"
    )

    print(
        "=" * 50
    )

    # --------------------------------------------------------
    # 1. PREPARACIÓN
    # --------------------------------------------------------

    print(
        "\n1. Preparando dataset..."
    )

    prepared_df, preparation_report = (
        prepare_dataset(
            DATASET_PATH
        )
    )

    print(
        "Dataset preparado."
    )

    print(
        f"Filas: "
        f"{preparation_report['rows']}"
    )

    print(
        f"Columnas: "
        f"{preparation_report['columns']}"
    )

    print(
        f"Variables derivadas: "
        f"{preparation_report['derived_columns']}"
    )

    # --------------------------------------------------------
    # 2. CARGA A BIGQUERY
    # --------------------------------------------------------

    print(
        "\n2. Cargando datos a BigQuery..."
    )

    upload_report = upload_dataset(
        dataframe=prepared_df,
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        table_id=TABLE_ID,
    )

    print(
        "Carga completada."
    )

    print(
        f"Tabla: "
        f"{upload_report['full_table']}"
    )

    print(
        f"Filas BigQuery: "
        f"{upload_report['rows']}"
    )

    print(
        f"Tamaño MiB: "
        f"{upload_report['size_mib']:.4f}"
    )

    # --------------------------------------------------------
    # 3. CLIENTE BIGQUERY
    # --------------------------------------------------------

    client = bigquery.Client(
        project=PROJECT_ID
    )

    full_table = build_full_table()

    # --------------------------------------------------------
    # 4. RECUPERACIÓN
    # --------------------------------------------------------

    print(
        "\n3. Recuperando datos desde BigQuery..."
    )

    bigquery_df = retrieve_bigquery_data(
        client=client,
        full_table=full_table,
    )

    print(
        f"Registros recuperados: "
        f"{len(bigquery_df)}"
    )

    # --------------------------------------------------------
    # 5. KPI
    # --------------------------------------------------------

    print(
        "\n4. Calculando KPI..."
    )

    kpis = calculate_kpis(
        bigquery_df
    )

    print_kpi_summary(
        kpis
    )

    # --------------------------------------------------------
    # 6. VALIDACIÓN
    # --------------------------------------------------------

    print(
        "\n5. Ejecutando validación funcional..."
    )

    validation_report = run_validation(
        client=client,
        dataframe=bigquery_df,
        full_table=full_table,
        maximum_bytes_billed=(
            MAXIMUM_BYTES_BILLED
        ),
    )

    print_validation_summary(
        validation_report
    )

    # --------------------------------------------------------
    # 7. DASHBOARD
    # --------------------------------------------------------

    print(
        "\n6. Generando dashboard..."
    )

    dashboard_path = generate_dashboard(
        dataframe=bigquery_df,
        template_path=DASHBOARD_TEMPLATE,
        output_path=DASHBOARD_OUTPUT,
    )

    print(
        f"Dashboard generado en: "
        f"{dashboard_path}"
    )

    # --------------------------------------------------------
    # RESULTADO FINAL
    # --------------------------------------------------------

    print(
        "\n" + "=" * 50
    )

    if validation_report[
        "all_passed"
    ]:

        print(
            "PIPELINE COMPLETADO CORRECTAMENTE"
        )

        print(
            "Coincidencia funcional del 100 % "
            "en los escenarios evaluados."
        )

    else:

        print(
            "PIPELINE COMPLETADO "
            "CON DIFERENCIAS DE VALIDACIÓN."
        )

    print(
        "=" * 50
    )


if __name__ == "__main__":
    run_pipeline()
