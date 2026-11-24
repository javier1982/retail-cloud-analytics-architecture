"""
Cálculo reproducible de los indicadores principales del estudio.

Este módulo implementa las mismas definiciones de KPI utilizadas
en BigQuery y en la ruta de validación con Pandas.
"""

from typing import Any

import pandas as pd


def calculate_kpis(
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    """
    Calcula los cinco KPI principales.

    KPI:
    - Ventas totales.
    - Beneficio total.
    - Margen de beneficio.
    - Pedidos únicos.
    - Clientes únicos.
    """

    required_columns = [
        "sales",
        "profit",
        "order_id",
        "customer_id",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Faltan columnas requeridas: "
            + ", ".join(missing_columns)
        )

    total_sales = float(
        dataframe["sales"].sum()
    )

    total_profit = float(
        dataframe["profit"].sum()
    )

    if total_sales != 0:
        profit_margin = (
            total_profit / total_sales
        )
    else:
        profit_margin = 0.0

    orders = int(
        dataframe["order_id"].nunique()
    )

    customers = int(
        dataframe["customer_id"].nunique()
    )

    return {
        "sales": total_sales,
        "profit": total_profit,
        "margin": profit_margin,
        "orders": orders,
        "customers": customers,
    }


def calculate_kpis_with_filters(
    dataframe: pd.DataFrame,
    year: int | None = None,
    region: str | None = None,
    category: str | None = None,
    segment: str | None = None,
) -> dict[str, Any]:
    """
    Aplica filtros opcionales y calcula los KPI.

    Los filtros corresponden a los utilizados
    durante la validación del estudio.
    """

    filtered = dataframe.copy()

    if year is not None:
        filtered = filtered[
            filtered["year"] == year
        ]

    if region is not None:
        filtered = filtered[
            filtered["region"] == region
        ]

    if category is not None:
        filtered = filtered[
            filtered["category"] == category
        ]

    if segment is not None:
        filtered = filtered[
            filtered["segment"] == segment
        ]

    return calculate_kpis(
        filtered
    )


def format_kpis(
    kpis: dict[str, Any],
) -> dict[str, Any]:
    """
    Devuelve una versión formateada para visualización.
    """

    return {
        "sales": round(
            kpis["sales"],
            2,
        ),
        "profit": round(
            kpis["profit"],
            2,
        ),
        "margin_percent": round(
            kpis["margin"] * 100,
            2,
        ),
        "orders": kpis["orders"],
        "customers": kpis["customers"],
    }


if __name__ == "__main__":
    print(
        "Módulo de cálculo de KPI."
    )

    print(
        "Definiciones:"
    )

    print(
        "Ventas = SUM(sales)"
    )

    print(
        "Beneficio = SUM(profit)"
    )

    print(
        "Margen = SUM(profit) / SUM(sales)"
    )

    print(
        "Pedidos = COUNT(DISTINCT order_id)"
    )

    print(
        "Clientes = COUNT(DISTINCT customer_id)"
    )
