# Manual de replicación de la arquitectura analítica cloud

## 1. Propósito

Este manual describe el procedimiento necesario para reconstruir la arquitectura analítica presentada en el artículo:

**“Arquitectura analítica cloud de bajo costo de entrada para PYMEs del sector retail”.**

El objetivo es que un investigador, docente, estudiante o desarrollador pueda reproducir el flujo utilizando una cuenta independiente de Google Cloud, sin depender de la infraestructura utilizada durante el desarrollo original.

La arquitectura implementa el siguiente proceso:

```text
Dataset retail
      ↓
Google Colab
Python + Pandas
      ↓
Preparación y transformación
      ↓
Google BigQuery
      ↓
Consultas SQL y control de consumo
      ↓
BigQuery → Pandas DataFrame
      ↓
Validación funcional
      ↓
Generación del dashboard
      ↓
HTML + CSS + JavaScript + Chart.js
```

---

## 2. Alcance

La reproducción cubre:

- preparación del conjunto de datos;
- transformación de variables;
- creación de variables derivadas;
- carga hacia Google BigQuery;
- ejecución de consultas SQL;
- cálculo de indicadores;
- uso de Dry Run;
- recuperación de resultados;
- validación BigQuery–Pandas;
- generación del dashboard;
- reproducción de los escenarios utilizados en el estudio.

No incluye:

- despliegue productivo;
- autenticación empresarial;
- conexión en tiempo real del dashboard;
- pruebas de concurrencia;
- pruebas de carga;
- pruebas de escalabilidad;
- gobierno de datos empresarial.

---

# 3. Requisitos previos

## 3.1 Cuenta Google

Se requiere una cuenta de Google con acceso a:

- Google Cloud;
- Google BigQuery;
- Google Colab.

## 3.2 Conocimientos mínimos

Se recomienda conocimiento básico de:

- Python;
- Pandas;
- SQL;
- Google Cloud;
- análisis de datos.

## 3.3 Dependencias

Las dependencias necesarias se encuentran definidas en:

```text
requirements.txt
```

Para una instalación local pueden instalarse mediante:

```bash
pip install -r requirements.txt
```

En Google Colab varias dependencias pueden estar disponibles previamente.

---

# 4. Creación del proyecto en Google Cloud

## Paso 1. Acceder a Google Cloud

Ingresar a:

```text
https://console.cloud.google.com/
```

## Paso 2. Crear un proyecto

Crear un proyecto nuevo.

Ejemplo:

```text
retail-analytics-replication
```

El nombre puede cambiar.

El identificador utilizado originalmente en el estudio fue:

```text
retailanalytics2026
```

No es obligatorio utilizar el mismo identificador.

---

# 5. Habilitación de BigQuery

Desde Google Cloud Console:

1. Abrir el menú de servicios.
2. Seleccionar BigQuery.
3. Confirmar que la API se encuentre habilitada.
4. Abrir BigQuery Studio.

---

# 6. Creación del dataset

Crear un dataset denominado:

```text
retail_analytics
```

La configuración utilizada como referencia es:

```python
PROJECT_ID = "retailanalytics2026"
DATASET_ID = "retail_analytics"
TABLE_ID = "superstore_sales"

FULL_TABLE = (
    f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
)
```

En una reproducción externa debe modificarse únicamente `PROJECT_ID` por el identificador correspondiente.

---

# 7. Creación del entorno en Google Colab

Crear un notebook nuevo en Google Colab.

## 7.1 Autenticación

Ejecutar:

```python
from google.colab import auth

auth.authenticate_user()
```

Posteriormente:

```python
from google.cloud import bigquery

PROJECT_ID = "TU_PROJECT_ID"

client = bigquery.Client(
    project=PROJECT_ID
)
```

Sustituir:

```text
TU_PROJECT_ID
```

por el proyecto creado anteriormente.

---

# 8. Carga del conjunto de datos

El experimento utiliza el conjunto **Sample Superstore**.

El conjunto utilizado contiene:

- 9.994 registros;
- 21 variables originales;
- periodo 2014–2017.

Ejemplo de carga:

```python
import pandas as pd

df = pd.read_csv(
    "Sample-Superstore.csv",
    encoding="latin1"
)

print(df.shape)
df.head()
```

El resultado esperado antes de transformaciones es aproximadamente:

```text
(9994, 21)
```

---

# 9. Normalización de nombres de columnas

Para facilitar el procesamiento se normalizan los nombres:

```python
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
      .str.replace("-", "_")
)
```

Ejemplos:

```text
Order ID → order_id
Order Date → order_date
Customer ID → customer_id
Sales → sales
Profit → profit
```

---

# 10. Conversión de fechas

Las variables de fecha deben convertirse a formato `datetime`.

```python
df["order_date"] = pd.to_datetime(
    df["order_date"]
)

df["ship_date"] = pd.to_datetime(
    df["ship_date"]
)
```

---

# 11. Variables derivadas

El proceso genera siete variables adicionales.

## 11.1 Año

```python
df["year"] = df["order_date"].dt.year
```

## 11.2 Número de mes

```python
df["month_number"] = (
    df["order_date"].dt.month
)
```

## 11.3 Nombre de mes

```python
df["month_name"] = (
    df["order_date"].dt.month_name()
)
```

## 11.4 Año y mes

```python
df["year_month"] = (
    df["order_date"]
      .dt.to_period("M")
      .astype(str)
)
```

## 11.5 Inicio del mes

```python
df["month_start"] = (
    df["order_date"]
      .dt.to_period("M")
      .dt.to_timestamp()
)
```

## 11.6 Margen de beneficio por registro

```python
df["profit_margin"] = (
    df["profit"] / df["sales"]
)
```

## 11.7 Días de envío

```python
df["shipping_days"] = (
    df["ship_date"] -
    df["order_date"]
).dt.days
```

Después de estas transformaciones se esperan:

```text
28 variables
```

---

# 12. Validación inicial de calidad

Comprobar valores nulos:

```python
print(df.isnull().sum())
```

Comprobar duplicados:

```python
print(
    "Duplicados:",
    df.duplicated().sum()
)
```

En el conjunto utilizado durante el estudio no se identificaron registros duplicados ni valores faltantes en la validación inicial reportada.

---

# 13. Conversión de variables numéricas

Asegurar que las variables analíticas principales sean numéricas:

```python
numeric_columns = [
    "sales",
    "profit",
    "profit_margin"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )
```

---

# 14. Creación de la tabla en BigQuery

Configurar:

```python
PROJECT_ID = "TU_PROJECT_ID"
DATASET_ID = "retail_analytics"
TABLE_ID = "superstore_sales"

FULL_TABLE = (
    f"{PROJECT_ID}."
    f"{DATASET_ID}."
    f"{TABLE_ID}"
)
```

Carga:

```python
job = client.load_table_from_dataframe(
    df,
    FULL_TABLE
)

job.result()

print(
    f"Datos cargados en {FULL_TABLE}"
)
```

---

# 15. Verificación de la tabla

Ejecutar:

```python
table = client.get_table(
    FULL_TABLE
)

print(
    "Filas:",
    table.num_rows
)

print(
    "Bytes:",
    table.num_bytes
)
```

Para el artefacto evaluado se obtuvieron aproximadamente:

```text
9.994 filas
3,01 MiB
```

Estos valores pueden presentar pequeñas variaciones según representación, versión de librerías o esquema.

---

# 16. Consulta de indicadores principales

La consulta de referencia para los cinco KPI es:

```sql
SELECT
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,

    SAFE_DIVIDE(
        SUM(profit),
        SUM(sales)
    ) AS profit_margin,

    COUNT(
        DISTINCT order_id
    ) AS orders,

    COUNT(
        DISTINCT customer_id
    ) AS customers

FROM
    `TU_PROJECT_ID.retail_analytics.superstore_sales`;
```

Los indicadores son:

```text
Ventas = SUM(sales)

Beneficio = SUM(profit)

Margen =
SUM(profit) / SUM(sales)

Pedidos =
COUNT(DISTINCT order_id)

Clientes =
COUNT(DISTINCT customer_id)
```

---

# 17. Resultado global de referencia

Para el conjunto utilizado en el estudio se obtuvieron aproximadamente:

```text
Ventas:
2.297.200,86

Beneficio:
286.397,02

Margen:
12,47 %

Pedidos:
5.009

Clientes:
793
```

Estos valores funcionan como referencia para comprobar una reproducción correcta del procedimiento.

---

# 18. Uso de BigQuery Dry Run

Dry Run permite conocer cuántos bytes procesaría una consulta sin ejecutarla.

Ejemplo en Python:

```python
from google.cloud import bigquery

job_config = bigquery.QueryJobConfig(
    dry_run=True,
    use_query_cache=False
)

query = f"""
SELECT
    sales,
    profit
FROM
    `{FULL_TABLE}`
"""

query_job = client.query(
    query,
    job_config=job_config
)

print(
    "Bytes estimados:",
    query_job.total_bytes_processed
)
```

---

# 19. Consultas utilizadas para evaluar reducción de datos

## Consulta completa

```sql
SELECT *
FROM
    `TU_PROJECT_ID.retail_analytics.superstore_sales`;
```

## Ventas y beneficio

```sql
SELECT
    sales,
    profit
FROM
    `TU_PROJECT_ID.retail_analytics.superstore_sales`;
```

## Agrupación por categoría

```sql
SELECT
    category,
    SUM(sales) AS sales,
    SUM(profit) AS profit
FROM
    `TU_PROJECT_ID.retail_analytics.superstore_sales`
GROUP BY
    category;
```

## Productos principales

```sql
SELECT
    product_name,
    SUM(sales) AS total_sales
FROM
    `TU_PROJECT_ID.retail_analytics.superstore_sales`
GROUP BY
    product_name
ORDER BY
    total_sales DESC
LIMIT 10;
```

---

# 20. Recuperación desde BigQuery hacia Pandas

Ejemplo:

```python
query = f"""
SELECT *
FROM `{FULL_TABLE}`
"""

df_bq = (
    client.query(query)
          .to_dataframe()
)

print(df_bq.shape)
```

Este DataFrame permite realizar la ruta independiente de reproducción y construir posteriormente el dashboard.

---

# 21. Cálculo independiente de KPI con Pandas

```python
total_sales = (
    df_bq["sales"].sum()
)

total_profit = (
    df_bq["profit"].sum()
)

profit_margin = (
    total_profit / total_sales
)

orders = (
    df_bq["order_id"].nunique()
)

customers = (
    df_bq["customer_id"].nunique()
)
```

---

# 22. Validación funcional

La validación compara los resultados calculados por:

```text
Ruta A:
Google BigQuery + SQL

Ruta B:
Pandas sobre los datos recuperados
```

Ambas rutas aplican las mismas reglas analíticas.

BigQuery funciona como referencia de cálculo y Pandas como ruta independiente de reproducción.

---

# 23. Escenarios de validación

Se utilizaron veinte escenarios.

1. Sin filtros.
2. Año 2014.
3. Año 2015.
4. Año 2016.
5. Año 2017.
6. Región Central.
7. Región East.
8. Región South.
9. Región West.
10. Furniture.
11. Office Supplies.
12. Technology.
13. Consumer.
14. Corporate.
15. Home Office.
16. 2017 / West / Technology / Consumer.
17. 2016 / East / Furniture / Corporate.
18. 2015 / Central / Office Supplies / Home Office.
19. 2014 / South / Technology / Consumer.
20. 2017 / East / Office Supplies / Corporate.

Cada escenario valida:

```text
Ventas
Beneficio
Margen
Pedidos
Clientes
```

Por tanto:

```text
20 escenarios × 5 KPI
=
100 comprobaciones
```

---

# 24. Criterio de comparación

Para valores monetarios puede utilizarse una tolerancia numérica:

```python
import math

def close_enough(a, b):
    return math.isclose(
        float(a),
        float(b),
        rel_tol=1e-9,
        abs_tol=1e-6
    )
```

Para pedidos y clientes:

```python
bigquery_orders == pandas_orders
```

y:

```python
bigquery_customers == pandas_customers
```

---

# 25. Resultado de validación de referencia

La ejecución documentada del estudio obtuvo:

```text
100 comprobaciones correctas
de
100 comprobaciones realizadas.
```

La interpretación correcta es:

**coincidencia funcional del 100 % en los escenarios evaluados.**

Este resultado no demuestra exactitud universal, ausencia total de errores, calidad de los datos originales, escalabilidad o comportamiento bajo cualquier escenario posible.

---

# 26. Preparación de datos para el dashboard

Los datos recuperados desde BigQuery pueden convertirse a JSON:

```python
import json

records = (
    df_bq
    .fillna("")
    .to_dict(
        orient="records"
    )
)

data_json = json.dumps(
    records,
    default=str
)
```

El JSON puede insertarse posteriormente en una plantilla HTML.

---

# 27. Generación del dashboard

La implementación utiliza:

```text
HTML
CSS
JavaScript
Chart.js
```

El dashboard permite aplicar filtros sobre:

- año;
- región;
- categoría;
- segmento.

Los KPI se recalculan sobre los registros filtrados.

---

# 28. Naturaleza del dashboard

El dashboard generado no mantiene conexión permanente con BigQuery.

El flujo es:

```text
BigQuery
   ↓
DataFrame
   ↓
JSON
   ↓
HTML
```

Por ello representa una:

**instantánea de los datos disponibles en el momento de generación.**

Si los datos cambian, debe ejecutarse nuevamente el proceso de generación.

---

# 29. Consideraciones de seguridad

Nunca deben publicarse:

```text
service-account.json
credentials.json
.env
tokens
contraseñas
API keys
claves privadas
```

El archivo `.gitignore` del repositorio se encuentra configurado para reducir este riesgo.

---

# 30. Replicación en otra instancia

Para reproducir completamente la arquitectura en otra cuenta:

1. Crear un nuevo proyecto Google Cloud.
2. Habilitar BigQuery.
3. Crear `retail_analytics`.
4. Obtener Sample Superstore.
5. Abrir Google Colab.
6. Instalar las dependencias.
7. Autenticarse.
8. Configurar `PROJECT_ID`.
9. Cargar el CSV.
10. Normalizar columnas.
11. Procesar fechas.
12. Crear siete variables derivadas.
13. Validar calidad.
14. Cargar los datos a BigQuery.
15. Ejecutar las consultas SQL.
16. Ejecutar Dry Run.
17. Recuperar los datos.
18. Calcular KPI con Pandas.
19. Ejecutar los veinte escenarios.
20. Comparar las cien comprobaciones.
21. Generar el dashboard.
22. Verificar los resultados.

---

# 31. Trazabilidad

El código disponible en este repositorio se clasifica en dos categorías:

## Evidencia histórica

Código, consultas, dashboard y componentes recuperados del proceso original cuando estos se encuentran disponibles.

## Código de reproducción

Código reconstruido y documentado a partir de:

- arquitectura implementada;
- evidencia histórica recuperada;
- resultados registrados;
- consultas utilizadas;
- reglas analíticas;
- procedimiento descrito en el artículo.

El código de reproducción no debe interpretarse como una copia literal de notebooks históricos que no fueron conservados íntegramente.

---

# 32. Limitaciones de la replicación

La reproducción permite verificar el flujo analítico y los resultados descritos en el estudio.

No permite concluir automáticamente:

- desempeño productivo;
- escalabilidad;
- experiencia de usuario;
- adopción empresarial;
- calidad externa del dataset;
- rendimiento con cargas masivas;
- comportamiento bajo concurrencia;
- costo total de propiedad.

Estos aspectos requieren evaluaciones adicionales.

---

# 33. Resultado esperado

Una reproducción correcta debería permitir obtener valores equivalentes a los KPI documentados y reproducir los escenarios de validación dentro de las tolerancias definidas.

Las pequeñas diferencias relacionadas con representación numérica, versiones de librerías o configuración de ejecución deben documentarse.

---

# 34. Licencia

El código y la documentación se distribuyen bajo la licencia MIT incluida en el repositorio.

---

# 35. Autores

- Diego Javier Portilla Martínez
- Mónica Elizabeth Páez Padilla
- Alejandro Israel Portilla Páez

---

# 36. Repositorio asociado

```text
https://github.com/javier1982/retail-cloud-analytics-architecture
```

Este repositorio constituye el artefacto técnico de reproducibilidad asociado al artículo científico.
