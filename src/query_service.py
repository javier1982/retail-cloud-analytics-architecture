"""
Servicio de consultas analíticas para Google BigQuery.

Este módulo construye y ejecuta consultas SQL reproducibles
para los KPI y escenarios de validación descritos en el estudio.
"""

from typing import Any

from google.cloud import bigquery


def build_where_clause(
    year: int | None = None,
    region: str | None = None,
    category: str | None = None,
    segment: str | None = None,
) -> tuple[str, list[bigquery.ScalarQueryParameter]]:
    """
    Construye una cláusula WHERE parametrizada.

    El uso de parámetros evita concatenar directamente
    valores suministrados por el usuario dentro del SQL.
    """

    conditions: list[str] = []
    parameters: list[bigquery.ScalarQueryParameter] = []

    if year is not None:
        conditions.append("year = @year")
        parameters.append(
            bigquery.ScalarQueryParameter(
                "year",
                "INT64",
                year,
            )
        )

    if region is not None:
        conditions.append("region = @region")
        parameters.append(
            bigquery.ScalarQueryParameter(
                "region",
                "STRING",
                region,
            )
        )

    if category is not None:
        conditions.append("category = @category")
        parameters.append(
            bigquery.ScalarQueryParameter(
                "category",
                "STRING",
                category,
            )
        )

    if segment is not None:
        conditions.append("segment = @segment")
        parameters.append(
            bigquery.ScalarQueryParameter(
                "segment",
                "STRING",
                segment,
            )
        )

    if not conditions:
        return "", parameters

    where_clause = (
        "WHERE "
        + " AND ".join(conditions)
    )

    return where_clause, parameters


def build_kpi_query(
    full_table: str,
    year: int | None = None,
    region: str | None = None,
    category: str | None = None,
    segment: str | None = None,
) -> tuple[
    str,
    list[bigquery.ScalarQueryParameter],
]:
    """
    Construye la consulta SQL de los cinco KPI principales.
    """

    where_clause, parameters = (
        build_where_clause(
            year=year,
            region=region,
            category=category,
            segment=segment,
        )
    )

    query = f"""
    SELECT
        SUM(sales) AS sales,
        SUM(profit) AS profit,

        SAFE_DIVIDE(
            SUM(profit),
            SUM(sales)
        ) AS margin,

        COUNT(
            DISTINCT order_id
        ) AS orders,

        COUNT(
            DISTINCT customer_id
        ) AS customers

    FROM
        `{full_table}`

    {where_clause}
    """

    return query, parameters


def execute_kpi_query(
    client: bigquery.Client,
    full_table: str,
    year: int | None = None,
    region: str | None = None,
    category: str | None = None,
    segment: str | None = None,
    maximum_bytes_billed: int | None = None,
) -> dict[str, Any]:
    """
    Ejecuta la consulta de KPI y devuelve
    los resultados normalizados.
    """

    query, parameters = build_kpi_query(
        full_table=full_table,
        year=year,
        region=region,
        category=category,
        segment=segment,
    )

    job_config = bigquery.QueryJobConfig(
        query_parameters=parameters
    )

    if maximum_bytes_billed is not None:
        job_config.maximum_bytes_billed = (
            maximum_bytes_billed
        )

    query_job = client.query(
        query,
        job_config=job_config,
    )

    rows = list(
        query_job.result()
    )

    if not rows:
        return {
            "sales": 0.0,
            "profit": 0.0,
            "margin": 0.0,
            "orders": 0,
            "customers": 0,
        }

    row = rows[0]

    return {
        "sales": float(
            row.sales or 0
        ),
        "profit": float(
            row.profit or 0
        ),
        "margin": float(
            row.margin or 0
        ),
        "orders": int(
            row.orders or 0
        ),
        "customers": int(
            row.customers or 0
        ),
    }


def dry_run_query(
    client: bigquery.Client,
    query: str,
    parameters: list[
        bigquery.ScalarQueryParameter
    ] | None = None,
) -> dict[str, Any]:
    """
    Ejecuta un Dry Run sin procesar realmente la consulta.
    """

    job_config = bigquery.QueryJobConfig(
        dry_run=True,
        use_query_cache=False,
        query_parameters=(
            parameters or []
        ),
    )

    query_job = client.query(
        query,
        job_config=job_config,
    )

    processed_bytes = int(
        query_job.total_bytes_processed
        or 0
    )

    return {
        "bytes_processed": processed_bytes,
        "mib_processed": (
            processed_bytes
            / (1024 ** 2)
        ),
        "gib_processed": (
            processed_bytes
            / (1024 ** 3)
        ),
    }


def dry_run_kpi_query(
    client: bigquery.Client,
    full_table: str,
    year: int | None = None,
    region: str | None = None,
    category: str | None = None,
    segment: str | None = None,
) -> dict[str, Any]:
    """
    Estima el volumen procesado por la consulta
    de los cinco KPI.
    """

    query, parameters = build_kpi_query(
        full_table=full_table,
        year=year,
        region=region,
        category=category,
        segment=segment,
    )

    return dry_run_query(
        client=client,
        query=query,
        parameters=parameters,
    )


if __name__ == "__main__":
    print(
        "Servicio de consultas BigQuery."
    )

    print(
        "Este módulo permite ejecutar "
        "KPI y Dry Run con filtros parametrizados."
    )
