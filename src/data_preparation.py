"""
Preparación y transformación del dataset Sample Superstore.

Este archivo forma parte del código de reproducción de la arquitectura
analítica descrita en el artículo científico.

No representa necesariamente una copia literal del notebook histórico;
consolida y documenta el procedimiento utilizado para reproducir
las transformaciones reportadas.
"""

from pathlib import Path

import pandas as pd


DERIVED_COLUMNS = [
    "year",
    "month_number",
    "month_name",
    "year_month",
    "month_start",
    "profit_margin",
    "shipping_days",
]


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los nombres de columnas al formato snake_case.
    """

    result = df.copy()

    result.columns = (
        result.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    return result


def convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte las columnas de fecha utilizadas por la arquitectura.
    """

    result = df.copy()

    required_columns = [
        "order_date",
        "ship_date",
    ]

    for column in required_columns:
        if column not in result.columns:
            raise ValueError(
                f"No se encontró la columna requerida: {column}"
            )

        result[column] = pd.to_datetime(
            result[column],
            errors="raise",
        )

    return result


def convert_numeric_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convierte las variables analíticas principales a formato numérico.
    """

    result = df.copy()

    numeric_columns = [
        "sales",
        "profit",
    ]

    for column in numeric_columns:
        if column not in result.columns:
            raise ValueError(
                f"No se encontró la columna requerida: {column}"
            )

        result[column] = pd.to_numeric(
            result[column],
            errors="coerce",
        )

    return result


def create_derived_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Crea las siete variables derivadas documentadas en el estudio.
    """

    result = df.copy()

    result["year"] = (
        result["order_date"].dt.year
    )

    result["month_number"] = (
        result["order_date"].dt.month
    )

    result["month_name"] = (
        result["order_date"].dt.month_name()
    )

    result["year_month"] = (
        result["order_date"]
        .dt.to_period("M")
        .astype(str)
    )

    result["month_start"] = (
        result["order_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    result["profit_margin"] = (
        result["profit"]
        .div(result["sales"])
        .where(result["sales"] != 0)
    )

    result["shipping_days"] = (
        result["ship_date"]
        - result["order_date"]
    ).dt.days

    return result


def validate_dataset(
    df: pd.DataFrame,
) -> dict:
    """
    Genera métricas básicas de calidad y estructura del dataset.
    """

    required_columns = [
        "order_id",
        "customer_id",
        "sales",
        "profit",
        "order_date",
        "ship_date",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Faltan columnas requeridas: "
            + ", ".join(missing_columns)
        )

    validation = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "duplicate_rows": int(
            df.duplicated().sum()
        ),
        "missing_values": int(
            df.isna().sum().sum()
        ),
        "unique_orders": int(
            df["order_id"].nunique()
        ),
        "unique_customers": int(
            df["customer_id"].nunique()
        ),
    }

    return validation


def prepare_dataset(
    file_path: str | Path,
    encoding: str = "latin1",
) -> tuple[pd.DataFrame, dict]:
    """
    Ejecuta el flujo completo de preparación.

    Parameters
    ----------
    file_path:
        Ruta del archivo CSV Sample Superstore.

    encoding:
        Codificación utilizada para leer el archivo.

    Returns
    -------
    tuple[pd.DataFrame, dict]
        Dataset preparado y métricas de validación.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {file_path}"
        )

    df = pd.read_csv(
        file_path,
        encoding=encoding,
    )

    original_shape = df.shape

    df = normalize_column_names(df)
    df = convert_dates(df)
    df = convert_numeric_columns(df)
    df = create_derived_columns(df)

    validation = validate_dataset(df)

    validation["original_rows"] = int(
        original_shape[0]
    )

    validation["original_columns"] = int(
        original_shape[1]
    )

    validation["derived_columns"] = len(
        DERIVED_COLUMNS
    )

    return df, validation


if __name__ == "__main__":
    dataset_path = Path(
        "data/Sample-Superstore.csv"
    )

    prepared_df, report = prepare_dataset(
        dataset_path
    )

    print(
        "\nDataset preparado correctamente."
    )

    print(
        f"Filas: {report['rows']}"
    )

    print(
        f"Columnas originales: "
        f"{report['original_columns']}"
    )

    print(
        f"Columnas finales: "
        f"{report['columns']}"
    )

    print(
        f"Variables derivadas: "
        f"{report['derived_columns']}"
    )

    print(
        f"Duplicados: "
        f"{report['duplicate_rows']}"
    )

    print(
        f"Valores faltantes: "
        f"{report['missing_values']}"
    )

    print(
        f"Pedidos únicos: "
        f"{report['unique_orders']}"
    )

    print(
        f"Clientes únicos: "
        f"{report['unique_customers']}"
    )
