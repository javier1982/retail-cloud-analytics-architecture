"""
Generador reproducible del dashboard HTML.

Este módulo recibe un DataFrame de Pandas, serializa sus registros
a JSON y reemplaza el marcador __DATA_JSON__ contenido en la
plantilla dashboard/dashboard_template.html.

El resultado es un archivo HTML portable que no requiere una
conexión activa con BigQuery durante su visualización.
"""

from pathlib import Path
import json

import pandas as pd


DEFAULT_TEMPLATE = Path(
    "dashboard/dashboard_template.html"
)

DEFAULT_OUTPUT = Path(
    "dashboard/dashboard_retail.html"
)


def dataframe_to_records(
    dataframe: pd.DataFrame,
) -> list[dict]:
    """
    Convierte un DataFrame en registros compatibles con JSON.
    """

    if dataframe.empty:
        raise ValueError(
            "El DataFrame está vacío."
        )

    prepared = dataframe.copy()

    # Convierte fechas y timestamps a texto ISO.
    for column in prepared.columns:
        if pd.api.types.is_datetime64_any_dtype(
            prepared[column]
        ):
            prepared[column] = (
                prepared[column]
                .dt.strftime("%Y-%m-%d")
            )

    prepared = prepared.where(
        pd.notnull(prepared),
        None,
    )

    return prepared.to_dict(
        orient="records"
    )


def serialize_dataframe(
    dataframe: pd.DataFrame,
) -> str:
    """
    Serializa el DataFrame a JSON.
    """

    records = dataframe_to_records(
        dataframe
    )

    return json.dumps(
        records,
        ensure_ascii=False,
        default=str,
    )


def load_template(
    template_path: str | Path,
) -> str:
    """
    Lee la plantilla HTML.
    """

    template_path = Path(
        template_path
    )

    if not template_path.exists():
        raise FileNotFoundError(
            f"No existe la plantilla: "
            f"{template_path}"
        )

    return template_path.read_text(
        encoding="utf-8"
    )


def generate_dashboard(
    dataframe: pd.DataFrame,
    template_path: str | Path = DEFAULT_TEMPLATE,
    output_path: str | Path = DEFAULT_OUTPUT,
) -> Path:
    """
    Genera el dashboard HTML completo.

    Parameters
    ----------
    dataframe:
        DataFrame recuperado desde BigQuery.

    template_path:
        Plantilla HTML que contiene __DATA_JSON__.

    output_path:
        Ruta del HTML generado.

    Returns
    -------
    pathlib.Path
        Ruta del dashboard generado.
    """

    template = load_template(
        template_path
    )

    marker = "__DATA_JSON__"

    if marker not in template:
        raise ValueError(
            "La plantilla no contiene "
            "el marcador __DATA_JSON__."
        )

    data_json = serialize_dataframe(
        dataframe
    )

    final_html = template.replace(
        marker,
        data_json,
        1,
    )

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        final_html,
        encoding="utf-8",
    )

    return output_path


def validate_generated_dashboard(
    output_path: str | Path,
) -> dict:
    """
    Realiza comprobaciones básicas sobre el HTML generado.
    """

    output_path = Path(
        output_path
    )

    if not output_path.exists():
        raise FileNotFoundError(
            f"No existe el dashboard: "
            f"{output_path}"
        )

    html = output_path.read_text(
        encoding="utf-8"
    )

    return {
        "exists": True,
        "size_bytes": (
            output_path.stat().st_size
        ),
        "contains_placeholder": (
            "__DATA_JSON__" in html
        ),
        "contains_chartjs": (
            "Chart" in html
        ),
        "contains_source_data": (
            "const sourceData" in html
        ),
    }


if __name__ == "__main__":
    print(
        "Generador reproducible del dashboard."
    )

    print(
        "Uso esperado:"
    )

    print(
        "1. Recuperar datos desde BigQuery."
    )

    print(
        "2. Obtener un Pandas DataFrame."
    )

    print(
        "3. Ejecutar generate_dashboard(df)."
    )

    print(
        "4. Abrir dashboard/dashboard_retail.html."
    )
