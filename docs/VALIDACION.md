# Validación funcional de la arquitectura analítica

## 1. Propósito

Este documento describe el procedimiento utilizado para validar funcionalmente la arquitectura presentada en el artículo:

**“Arquitectura analítica cloud de bajo costo de entrada para PYMEs del sector retail”.**

La validación busca comprobar que los indicadores calculados mediante Google BigQuery puedan reproducirse mediante una segunda ruta de cálculo implementada con Pandas.

---

## 2. Estrategia de validación

La validación utiliza dos rutas de cálculo.

### Ruta A: BigQuery

```text
Datos preparados
      ↓
Google BigQuery
      ↓
Consulta SQL
      ↓
KPI de referencia
```

### Ruta B: Pandas

```text
Datos preparados
      ↓
Pandas DataFrame
      ↓
Filtros equivalentes
      ↓
KPI reproducidos
```

BigQuery se utiliza como referencia de cálculo.

Pandas se utiliza como una ruta independiente de reproducción de las reglas analíticas.

Ambas rutas operan sobre los mismos datos y aplican las mismas definiciones de indicadores.

Por esta razón, la comparación evalúa consistencia funcional entre implementaciones y no constituye una validación de la calidad externa del conjunto de datos.

---

# 3. Indicadores evaluados

Se validan cinco KPI.

## 3.1 Ventas totales

BigQuery:

```sql
SUM(sales)
```

Pandas:

```python
total_sales = df["sales"].sum()
```

---

## 3.2 Beneficio total

BigQuery:

```sql
SUM(profit)
```

Pandas:

```python
total_profit = df["profit"].sum()
```

---

## 3.3 Margen de beneficio

La definición utilizada es:

```text
Margen =
SUM(profit) / SUM(sales)
```

BigQuery:

```sql
SAFE_DIVIDE(
    SUM(profit),
    SUM(sales)
)
```

Pandas:

```python
profit_margin = (
    df["profit"].sum()
    /
    df["sales"].sum()
)
```

El margen global no se obtiene mediante el promedio simple de los márgenes individuales.

---

## 3.4 Pedidos únicos

BigQuery:

```sql
COUNT(DISTINCT order_id)
```

Pandas:

```python
orders = df["order_id"].nunique()
```

---

## 3.5 Clientes únicos

BigQuery:

```sql
COUNT(DISTINCT customer_id)
```

Pandas:

```python
customers = (
    df["customer_id"].nunique()
)
```

---

# 4. Número total de comprobaciones

La validación utiliza:

```text
20 escenarios
×
5 KPI
=
100 comprobaciones
```

Cada escenario produce cinco resultados:

```text
Ventas
Beneficio
Margen
Pedidos
Clientes
```

---

# 5. Escenarios de validación

| Escenario | Filtro |
|---|---|
| 1 | Sin filtros |
| 2 | Año 2014 |
| 3 | Año 2015 |
| 4 | Año 2016 |
| 5 | Año 2017 |
| 6 | Región Central |
| 7 | Región East |
| 8 | Región South |
| 9 | Región West |
| 10 | Categoría Furniture |
| 11 | Categoría Office Supplies |
| 12 | Categoría Technology |
| 13 | Segmento Consumer |
| 14 | Segmento Corporate |
| 15 | Segmento Home Office |
| 16 | 2017 / West / Technology / Consumer |
| 17 | 2016 / East / Furniture / Corporate |
| 18 | 2015 / Central / Office Supplies / Home Office |
| 19 | 2014 / South / Technology / Consumer |
| 20 | 2017 / East / Office Supplies / Corporate |

---

# 6. Escenario 1: análisis global

No se aplican filtros.

Consulta conceptual:

```sql
SELECT
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    SAFE_DIVIDE(
        SUM(profit),
        SUM(sales)
    ) AS profit_margin,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_id) AS customers
FROM
    `PROJECT_ID.retail_analytics.superstore_sales`;
```

Valores de referencia documentados:

| KPI | Valor aproximado |
|---|---:|
| Ventas | 2.297.200,86 |
| Beneficio | 286.397,02 |
| Margen | 12,47 % |
| Pedidos | 5.009 |
| Clientes | 793 |

---

# 7. Escenarios por año

Se evalúan:

```text
2014
2015
2016
2017
```

Ejemplo SQL:

```sql
SELECT
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    SAFE_DIVIDE(
        SUM(profit),
        SUM(sales)
    ) AS profit_margin,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_id) AS customers
FROM
    `PROJECT_ID.retail_analytics.superstore_sales`
WHERE
    year = 2017;
```

Equivalente Pandas:

```python
filtered = df[
    df["year"] == 2017
]
```

---

# 8. Escenarios por región

Se evalúan las regiones:

```text
Central
East
South
West
```

Ejemplo:

```sql
WHERE region = 'West'
```

Pandas:

```python
filtered = df[
    df["region"] == "West"
]
```

---

# 9. Escenarios por categoría

Las categorías evaluadas son:

```text
Furniture
Office Supplies
Technology
```

Ejemplo:

```sql
WHERE category = 'Technology'
```

---

# 10. Escenarios por segmento

Los segmentos evaluados son:

```text
Consumer
Corporate
Home Office
```

Ejemplo:

```sql
WHERE segment = 'Consumer'
```

---

# 11. Escenarios combinados

Los cinco escenarios finales utilizan múltiples filtros simultáneos.

## Escenario 16

```text
Año:
2017

Región:
West

Categoría:
Technology

Segmento:
Consumer
```

## Escenario 17

```text
Año:
2016

Región:
East

Categoría:
Furniture

Segmento:
Corporate
```

## Escenario 18

```text
Año:
2015

Región:
Central

Categoría:
Office Supplies

Segmento:
Home Office
```

## Escenario 19

```text
Año:
2014

Región:
South

Categoría:
Technology

Segmento:
Consumer
```

## Escenario 20

```text
Año:
2017

Región:
East

Categoría:
Office Supplies

Segmento:
Corporate
```

---

# 12. Construcción dinámica de filtros en BigQuery

Una implementación reproducible puede construir la consulta de acuerdo con los filtros del escenario.

Ejemplo conceptual:

```python
conditions = []

if year is not None:
    conditions.append(
        f"year = {year}"
    )

if region is not None:
    conditions.append(
        f"region = '{region}'"
    )

if category is not None:
    conditions.append(
        f"category = '{category}'"
    )

if segment is not None:
    conditions.append(
        f"segment = '{segment}'"
    )
```

Posteriormente:

```python
where_clause = ""

if conditions:
    where_clause = (
        "WHERE "
        + " AND ".join(conditions)
    )
```

---

# 13. Aplicación equivalente en Pandas

Ejemplo:

```python
filtered = df.copy()

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
```

---

# 14. Cálculo de KPI en Pandas

```python
def calculate_kpis(df):
    total_sales = df["sales"].sum()

    total_profit = df["profit"].sum()

    if total_sales != 0:
        profit_margin = (
            total_profit / total_sales
        )
    else:
        profit_margin = 0

    orders = (
        df["order_id"].nunique()
    )

    customers = (
        df["customer_id"].nunique()
    )

    return {
        "sales": total_sales,
        "profit": total_profit,
        "margin": profit_margin,
        "orders": orders,
        "customers": customers,
    }
```

---

# 15. Criterio de comparación

Los KPI monetarios y el margen pueden presentar diferencias mínimas relacionadas con representación de punto flotante.

Se recomienda utilizar:

```python
import math

def numeric_equal(a, b):
    return math.isclose(
        float(a),
        float(b),
        rel_tol=1e-9,
        abs_tol=1e-6
    )
```

Para:

```text
Ventas
Beneficio
Margen
```

se utiliza tolerancia numérica.

Para:

```text
Pedidos
Clientes
```

se utiliza igualdad exacta.

---

# 16. Función de comparación

Ejemplo:

```python
def compare_results(
    bigquery_result,
    pandas_result
):
    checks = {
        "sales": numeric_equal(
            bigquery_result["sales"],
            pandas_result["sales"]
        ),

        "profit": numeric_equal(
            bigquery_result["profit"],
            pandas_result["profit"]
        ),

        "margin": numeric_equal(
            bigquery_result["margin"],
            pandas_result["margin"]
        ),

        "orders": (
            bigquery_result["orders"]
            ==
            pandas_result["orders"]
        ),

        "customers": (
            bigquery_result["customers"]
            ==
            pandas_result["customers"]
        )
    }

    return checks
```

---

# 17. Registro de resultados

Cada comprobación puede almacenarse con la siguiente estructura:

```text
Escenario
KPI
Valor BigQuery
Valor Pandas
Diferencia
Resultado
```

Ejemplo:

```text
Escenario:
2017

KPI:
Ventas

BigQuery:
733215.2552

Pandas:
733215.2552

Resultado:
Coincidente
```

---

# 18. Resultado de referencia para 2017

Los valores documentados para el año 201
