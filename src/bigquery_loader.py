"""
Creación del dataset y carga de datos hacia Google BigQuery.

Este módulo forma parte del código de reproducción de la arquitectura
analítica descrita en el artículo científico.

Permite crear o verificar el dataset de destino y cargar el DataFrame
preparado en una tabla BigQuery.

No contiene credenciales ni depende de una cuenta específica.
"""

from typing import Any

import pandas as pd
from google.cloud import bigquery


DEFAULT_LOCATION = "US"


def create_client(
    project_id: str,
) -> bigquery.Client:
    """
    Crea un cliente autenticado de BigQuery.

    La autenticación debe haberse realizado previamente mediante
    Google Colab o Application Default Credentials.
    """

    if not project_id:
        raise ValueError(
            "PROJECT_ID no puede estar vacío."
        )

    return bigquery.Client(
        project=project_id
    )


def ensure_dataset(
    client: bigquery.Client,
    project_id: str,
    dataset_id: str,
    location: str = DEFAULT_LOCATION,
) -> bigquery.Dataset:
    """
    Crea el dataset si todavía no existe.

    Si ya existe, BigQuery mantiene el dataset existente.
    """

    dataset_reference = (
        f"{project_id}.{dataset_id}"
    )

    dataset = bigquery.Dataset(
        dataset_reference
    )

    dataset.location = location

    created_dataset = (
        client.create_dataset(
            dataset,
            exists_ok=True,
        )
    )

    return created_dataset


def build_full_table_name(
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> str:
    """
    Construye el identificador completo de una tabla BigQuery.
    """

    return (
        f"{project_id}."
        f"{dataset_id}."
        f"{table_id}"
    )


def load_dataframe_to_bigquery(
    client: bigquery.Client,
    dataframe: pd.DataFrame,
    full_table: str,
) -> bigquery.Table:
    """
    Carga un DataFrame preparado hacia BigQuery.

    WRITE_TRUNCATE garantiza una reproducción determinista:
    si la tabla ya existe, su contenido se reemplaza con los
    datos utilizados en la nueva ejecución.
    """

    if dataframe.empty:
        raise ValueError(
            "El DataFrame está vacío."
        )

    job_config = bigquery.LoadJobConfig(
        write_disposition=(
            bigquery.WriteDisposition.WRITE_TRUNCATE
        ),
        create_disposition=(
            bigquery.CreateDisposition.CREATE_IF_NEEDED
        ),
    )

    load_job = (
        client.load_table_from_dataframe(
            dataframe,
            full_table,
            job_config=job_config,
        )
    )

    load_job.result()

    table = client.get_table(
        full_table
    )

    return table


def get_table_metrics(
    table: bigquery.Table,
) -> dict[str, Any]:
    """
    Devuelve métricas básicas de la tabla cargada.
    """

    return {
        "project": table.project,
        "dataset_id": table.dataset_id,
        "table_id": table.table_id,
        "rows": int(
            table.num_rows or 0
        ),
        "bytes": int(
            table.num_bytes or 0
        ),
        "schema_fields": len(
            table.schema
        ),
    }


def bytes_to_mib(
    value: int,
) -> float:
    """
    Convierte bytes a MiB.
    """

    return value / (1024 ** 2)


def upload_dataset(
    dataframe: pd.DataFrame,
    project_id: str,
    dataset_id: str = "retail_analytics",
    table_id: str = "superstore_sales",
    location: str = DEFAULT_LOCATION,
) -> dict[str, Any]:
    """
    Ejecuta el proceso completo de carga hacia BigQuery.

    1. Crea el cliente.
    2. Crea o verifica el dataset.
    3. Construye el nombre completo de la tabla.
    4. Carga el DataFrame.
    5. Recupera métricas de control.
    """

    client = create_client(
        project_id
    )

    ensure_dataset(
        client=client,
        project_id=project_id,
        dataset_id=dataset_id,
        location=location,
    )

    full_table = build_full_table_name(
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )

    table = load_dataframe_to_bigquery(
        client=client,
        dataframe=dataframe,
        full_table=full_table,
    )

    metrics = get_table_metrics(
        table
    )

    metrics["size_mib"] = bytes_to_mib(
        metrics["bytes"]
    )

    metrics["full_table"] = full_table

    return metrics


if __name__ == "__main__":
    print(
        "Este módulo debe ejecutarse después "
        "de preparar el dataset."
    )

    print(
        "Ejemplo de tabla de destino:"
    )

    print(
        "TU_PROJECT_ID."
        "retail_analytics."
        "superstore_sales"
    )
