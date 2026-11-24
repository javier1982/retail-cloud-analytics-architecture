"""
Validación funcional de 20 escenarios y 5 KPI.

Este script compara:
- Ruta A: Google BigQuery + SQL
- Ruta B: Pandas

Total esperado:
20 escenarios × 5 KPI = 100 comprobaciones.
"""

from __future__ import annotations

import math
from typing import Any

import pandas as pd
from google.cloud import bigquery

from src.kpi_calculation import calculate_kpis_with_filters
from src.query_service import execute_kpi_query


SCENARIOS = [
    {
        "name": "Sin filtros",
        "year": None,
        "region": None,
        "category": None,
        "segment": None,
    },
    {
        "name": "Año 2014",
        "year": 2014,
        "region": None,
        "category": None,
        "segment": None,
    },
    {
        "name": "Año 2015",
        "year": 2015,
        "region": None,
        "category": None,
        "segment": None,
    },
    {
        "name": "Año 2016",
        "year": 2016,
        "region": None,
        "category": None,
        "segment": None,
    },
    {
        "name": "Año 2017",
        "year": 2017,
        "region": None,
        "category": None,
        "segment": None,
    },
    {
        "name": "Región Central",
        "year": None,
        "region": "Central",
        "category": None,
        "segment": None,
    },
    {
        "name": "Región East",
        "year": None,
        "region": "East",
        "category": None,
        "segment": None,
    },
    {
        "name": "Región South",
        "year": None,
        "region": "South",
        "category": None,
        "segment": None,
    },
    {
        "name": "Región West",
        "year": None,
        "region": "West",
        "category": None,
        "segment": None,
    },
    {
        "name": "Categoría Furniture",
        "year": None,
        "region": None,
        "category": "Furniture",
        "segment": None,
    },
    {
        "name": "Categoría Office Supplies",
        "year": None,
        "region": None,
        "category": "Office Supplies",
        "segment": None,
    },
    {
        "name": "Categoría Technology",
        "year": None,
        "region": None,
        "category": "Technology",
        "segment": None,
    },
    {
        "name": "Segmento Consumer",
        "year": None,
        "region": None,
        "category": None,
        "segment": "Consumer",
    },
    {
        "name": "Segmento Corporate",
        "year": None,
        "region": None,
        "category": None,
        "segment": "Corporate",
    },
    {
        "name": "Segmento Home Office",
        "year": None,
        "region": None,
        "category": None,
        "segment": "Home Office",
    },
    {
        "name": "2017 / West / Technology / Consumer",
        "year": 2017,
        "region": "West",
        "category": "Technology",
        "segment": "Consumer",
    },
    {
        "name": "2016 / East / Furniture / Corporate",
        "year": 2016,
        "region": "East",
        "category": "Furniture",
        "segment": "Corporate",
    },
    {
        "name": "2015 / Central / Office Supplies / Home Office",
        "year": 2015,
        "region": "Central",
        "category": "Office Supplies",
        "segment": "Home Office",
    },
    {
        "name": "2014 / South / Technology / Consumer",
        "year": 2014,
        "region": "South",
        "category": "Technology",
        "segment": "Consumer",
    },
    {
        "name": "2017 / East / Office Supplies / Corporate",
        "year": 2017,
        "region": "East",
        "category": "Office Supplies",
        "segment": "Corporate",
    },
]


NUMERIC_KPIS = [
    "sales",
    "profit",
    "margin",
]

INTEGER_KPIS = [
    "orders",
    "customers",
]


def numeric_equal(
    value_a: float,
    value_b: float,
) -> bool:
    """
    Compara valores numéricos con tolerancia.
    """

    return math.isclose(
        float(value_a),
        float(value_b),
        rel_tol=1e-9,
        abs_tol=1e-6,
    )


def compare_kpis(
    bigquery_result: dict[str, Any],
    pandas_result: dict[str, Any],
) -> dict[str, bool]:
    """
    Compara los cinco KPI.
    """

    checks: dict[str, bool] = {}

    for kpi in NUMERIC_KPIS:
        checks[kpi] = numeric_equal(
            bigquery_result[kpi],
            pandas_result[kpi],
        )

    for kpi in INTEGER_KPIS:
        checks[kpi] = (
            int(bigquery_result[kpi])
            ==
            int(pandas_result[kpi])
        )

    return checks


def validate_scenario(
    client: bigquery.Client,
    dataframe: pd.DataFrame,
    full_table: str,
    scenario: dict[str, Any],
    maximum_bytes_billed: int | None = None,
) -> dict[str, Any]:
    """
    Ejecuta un escenario en ambas rutas y compara resultados.
    """

    filters = {
        "year": scenario["year"],
        "region": scenario["region"],
        "category": scenario["category"],
        "segment": scenario["segment"],
    }

    bigquery_result = execute_kpi_query(
        client=client,
        full_table=full_table,
        maximum_bytes_billed=maximum_bytes_billed,
        **filters,
    )

    pandas_result = calculate_kpis_with_filters(
        dataframe=dataframe,
        **filters,
    )

    checks = compare_kpis(
        bigquery_result=bigquery_result,
        pandas_result=pandas_result,
    )

    return {
        "scenario": scenario["name"],
        "filters": filters,
        "bigquery": bigquery_result,
        "pandas": pandas_result,
        "checks": checks,
        "passed": all(checks.values()),
    }


def run_validation(
    client: bigquery.Client,
    dataframe: pd.DataFrame,
    full_table: str,
    maximum_bytes_billed: int | None = None,
) -> dict[str, Any]:
    """
    Ejecuta los 20 escenarios de validación.
    """

    results = []

    total_checks = 0
    passed_checks = 0

    for scenario in SCENARIOS:
        result = validate_scenario(
            client=client,
            dataframe=dataframe,
            full_table=full_table,
            scenario=scenario,
            maximum_bytes_billed=maximum_bytes_billed,
        )

        results.append(result)

        for passed in result["checks"].values():
            total_checks += 1

            if passed:
                passed_checks += 1

    return {
        "scenario_count": len(SCENARIOS),
        "kpis_per_scenario": 5,
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "failed_checks": (
            total_checks - passed_checks
        ),
        "all_passed": (
            total_checks == passed_checks
        ),
        "results": results,
    }


def print_validation_summary(
    report: dict[str, Any],
) -> None:
    """
    Imprime un resumen legible de la validación.
    """

    print("\nVALIDACIÓN FUNCIONAL")
    print("-" * 50)

    print(
        f"Escenarios: "
        f"{report['scenario_count']}"
    )

    print(
        f"KPI por escenario: "
        f"{report['kpis_per_scenario']}"
    )

    print(
        f"Comprobaciones totales: "
        f"{report['total_checks']}"
    )

    print(
        f"Comprobaciones coincidentes: "
        f"{report['passed_checks']}"
    )

    print(
        f"Comprobaciones fallidas: "
        f"{report['failed_checks']}"
    )

    if report["all_passed"]:
        print(
            "\nResultado: coincidencia funcional "
            "del 100 % en los escenarios evaluados."
        )
    else:
        print(
            "\nResultado: existen diferencias "
            "que deben revisarse."
        )

    print("\nDETALLE POR ESCENARIO")
    print("-" * 50)

    for result in report["results"]:
        status = (
            "OK"
            if result["passed"]
            else "REVISAR"
        )

        print(
            f"{status} - {result['scenario']}"
        )

        for kpi, passed in result["checks"].items():
            mark = "OK" if passed else "ERROR"

            print(
                f"  {kpi}: {mark}"
            )


if __name__ == "__main__":
    print(
        "Este módulo contiene la validación "
        "de 20 escenarios y 100 comprobaciones."
    )

    print(
        "Debe ejecutarse proporcionando:"
    )

    print(
        "- cliente BigQuery"
    )

    print(
        "- DataFrame preparado"
    )

    print(
        "- nombre completo de la tabla"
    )
