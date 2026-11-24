# Dashboard reproducible

Esta carpeta contiene los componentes asociados a la generación y reproducción del dashboard descrito en el artículo científico.

## Tecnologías

El dashboard utiliza:

- HTML
- CSS
- JavaScript
- Chart.js

## Flujo de generación

El flujo utilizado es:

```text
Google BigQuery
      ↓
Pandas DataFrame
      ↓
Serialización JSON
      ↓
Plantilla HTML
      ↓
JavaScript + Chart.js
      ↓
Dashboard interactivo
