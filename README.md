# Arquitectura analítica cloud de bajo costo de entrada para PYMEs retail

Repositorio asociado al artículo científico:

**“Arquitectura analítica cloud de bajo costo de entrada para PYMEs del sector retail”**

Este repositorio contiene la documentación técnica, consultas SQL, scripts, configuraciones y procedimientos necesarios para reproducir la arquitectura analítica descrita en el estudio.

## Objetivo

Proporcionar una implementación reproducible de una arquitectura analítica cloud orientada a pequeñas y medianas empresas del sector retail, utilizando servicios de consumo controlado y herramientas de bajo costo de entrada.

La arquitectura permite ejecutar el flujo completo desde la preparación de los datos hasta la generación de un dashboard interactivo y la validación funcional de los indicadores calculados.

## Arquitectura general

El flujo implementado es:

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
BigQuery → DataFrame
      ↓
Cálculo y validación de KPI
      ↓
Generación del dashboard
      ↓
HTML + CSS + JavaScript + Chart.js
```

## Tecnologías utilizadas

- Google Colab
- Python
- Pandas
- Google BigQuery
- SQL
- HTML
- CSS
- JavaScript
- Chart.js

Gemini fue utilizado únicamente como apoyo de programación durante la construcción de la interfaz del dashboard. No intervino en la preparación del conjunto de datos, almacenamiento, cálculo de indicadores, consultas SQL ni validación de resultados.

## Conjunto de datos

El estudio utiliza **Sample Superstore** como conjunto de datos de prueba para evaluar técnicamente la arquitectura.

Características utilizadas en el experimento:

- 9.994 registros.
- 21 variables originales.
- 7 variables derivadas.
- 28 variables después del proceso de preparación.
- 5.009 pedidos únicos.
- 793 clientes.
- 3 categorías.
- 17 subcategorías.
- 4 regiones.
- Periodo analizado: 2014–2017.

Las variables derivadas son:

- `year`
- `month_number`
- `month_name`
- `year_month`
- `month_start`
- `profit_margin`
- `shipping_days`

## Indicadores principales

La arquitectura calcula cinco KPI principales:

1. Ventas totales.
2. Beneficio total.
3. Margen de beneficio.
4. Número de pedidos únicos.
5. Número de clientes únicos.

Las definiciones utilizadas son:

```text
Ventas = SUM(sales)

Beneficio = SUM(profit)

Margen = SUM(profit) / SUM(sales)

Pedidos = COUNT(DISTINCT order_id)

Clientes = COUNT(DISTINCT customer_id)
```

## Validación funcional

La validación del artefacto se realizó mediante:

**20 escenarios × 5 KPI = 100 comprobaciones**

Los resultados obtenidos mediante BigQuery fueron contrastados con una ruta independiente de reproducción utilizando Pandas.

El experimento obtuvo una:

**coincidencia funcional del 100 % en los escenarios evaluados.**

Este resultado se limita exclusivamente a los escenarios y reglas analíticas evaluadas y no representa una afirmación de exactitud universal del sistema.

## Control de consumo

La arquitectura utiliza mecanismos de estimación previa del volumen procesado mediante **BigQuery Dry Run**.

Esto permite estimar los bytes que procesaría una consulta antes de ejecutarla y facilita el control del consumo dentro de un escenario de bajo costo de entrada.

Las reducciones de datos procesados documentadas en el estudio corresponden únicamente al conjunto de datos, esquema y consultas evaluadas.

## Dashboard

El dashboard generado utiliza:

- HTML
- CSS
- JavaScript
- Chart.js

Los datos son recuperados desde BigQuery y posteriormente serializados dentro del artefacto generado.

El dashboard representa una **instantánea de los datos obtenidos durante su generación** y no mantiene una conexión en tiempo real con BigQuery.

Para incorporar nuevos datos debe volver a ejecutarse el proceso de generación.

## Reproducibilidad

Este repositorio tiene como objetivo permitir que otro investigador o desarrollador pueda reconstruir la arquitectura utilizando una cuenta independiente de Google Cloud.

La documentación incluirá instrucciones para:

1. Crear o seleccionar un proyecto de Google Cloud.
2. Habilitar BigQuery.
3. Crear el dataset.
4. Preparar el conjunto de datos.
5. Ejecutar las transformaciones.
6. Crear la tabla analítica.
7. Cargar los datos en BigQuery.
8. Ejecutar las consultas SQL.
9. Realizar pruebas Dry Run.
10. Recuperar los resultados mediante Python.
11. Calcular los KPI.
12. Ejecutar los escenarios de validación.
13. Generar el dashboard HTML.

No se incluyen credenciales, claves privadas, tokens ni archivos de cuentas de servicio.

## Trazabilidad del código

El repositorio distingue entre:

### Evidencia histórica

Componentes conservados durante el desarrollo original del proyecto, como consultas, fragmentos funcionales y el dashboard generado.

### Código de reproducción

Código consolidado y documentado posteriormente para permitir reconstruir de manera reproducible el procedimiento descrito en el artículo.

Esta distinción evita presentar código reconstruido como si fuera una copia literal de archivos históricos no conservados.

## Estructura prevista del repositorio

```text
retail-cloud-analytics-architecture/
│
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
│
├── docs/
│   ├── MANUAL_REPLICACION.md
│   ├── ARQUITECTURA.md
│   ├── VALIDACION.md
│   └── COSTOS_Y_SUPUESTOS.md
│
├── notebooks/
│   └── retail_analytics_replication.ipynb
│
├── src/
├── sql/
├── dashboard/
├── tests/
├── config/
└── evidence/
```

## Seguridad

El repositorio no debe contener:

- claves privadas;
- tokens;
- credenciales de Google Cloud;
- archivos de cuentas de servicio;
- archivos `.env`;
- información sensible.

Los valores específicos de cada implementación deben configurarse localmente.

## Licencia

El código y la documentación se distribuyen bajo la **MIT License**.

## Autores

- Diego Javier Portilla Martínez
- Mónica Elizabeth Páez Padilla
- Alejandro Israel Portilla Páez

## Artículo relacionado

**Arquitectura analítica cloud de bajo costo de entrada para PYMEs del sector retail**

El repositorio constituye el artefacto técnico de reproducibilidad asociado al manuscrito científico.
