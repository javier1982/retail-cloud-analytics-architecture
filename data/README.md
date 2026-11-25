# Dataset utilizado

## Sample Superstore

La arquitectura analítica utiliza **Sample Superstore** como conjunto de datos de prueba.

Sample Superstore es un conjunto de datos ficticio distribuido como recurso de ejemplo por Tableau y contiene información relacionada con pedidos, productos, clientes, ventas, beneficios y localización geográfica.

El dataset se utiliza exclusivamente como banco de pruebas técnico para reproducir la arquitectura descrita en el artículo científico.

No representa datos obtenidos directamente de una PYME participante.

## Fuente

Fuente oficial:

**Tableau Public – Sample Data / Superstore Sales**

Para reproducir el experimento debe descargarse la versión de Sample Superstore compatible con la estructura descrita en este repositorio.

## Características esperadas

La versión utilizada durante el estudio contiene:

- 9.994 registros.
- 21 columnas originales.
- 5.009 pedidos únicos.
- 793 clientes únicos.
- 3 categorías.
- 17 subcategorías.
- 4 regiones.
- Periodo comprendido entre 2014 y 2017.

Después de la etapa de preparación se generan siete variables adicionales:

- `year`
- `month_number`
- `month_name`
- `year_month`
- `month_start`
- `profit_margin`
- `shipping_days`

Por tanto:

```text
21 columnas originales
+
7 variables derivadas
=
28 columnas finales
```

## Nombre esperado del archivo

El pipeline incluido en este repositorio utiliza por defecto:

```text
data/Sample-Superstore.csv
```

Por tanto, después de descargar el dataset, el archivo utilizado para la reproducción debe colocarse en esta carpeta con el nombre:

```text
Sample-Superstore.csv
```

## Validación antes de ejecutar

Antes de continuar con la reproducción debe comprobarse que el archivo utilizado corresponde a la estructura esperada.

El código disponible en:

```text
src/data_preparation.py
```

realiza verificaciones sobre:

- columnas requeridas;
- número de registros;
- duplicados;
- valores faltantes;
- pedidos únicos;
- clientes únicos.

## Columnas fundamentales

La arquitectura requiere, entre otras, las siguientes variables:

```text
Order ID
Order Date
Ship Date
Customer ID
Segment
Region
Category
Sub-Category
Product Name
Sales
Profit
```

Después de la normalización estas columnas se utilizan como:

```text
order_id
order_date
ship_date
customer_id
segment
region
category
sub_category
product_name
sales
profit
```

## Distribución del dataset

El archivo de datos no se incluye directamente dentro de este repositorio.

Esta decisión permite:

1. mantener claramente separada la fuente de datos del código de reproducción;
2. conservar la atribución hacia la fuente oficial;
3. evitar distribuir copias no controladas del dataset;
4. permitir que cada investigador obtenga el archivo desde su fuente correspondiente.

## Procedimiento de reproducción

1. Obtener Sample Superstore desde la fuente oficial de Tableau.
2. Identificar la tabla o archivo correspondiente a pedidos.
3. Exportarlo o guardarlo como CSV cuando sea necesario.
4. Verificar que la versión utilizada sea compatible con el periodo y estructura documentados.
5. Guardar el archivo como:

```text
data/Sample-Superstore.csv
```

6. Ejecutar:

```bash
python -m src.pipeline
```

## Importante

Las distintas versiones de Sample Superstore distribuidas a lo largo del tiempo pueden presentar diferencias de estructura, periodo o formato.

Por esta razón, una reproducción debe documentar la versión concreta del dataset utilizada y verificar sus características antes de comparar los resultados con los valores publicados en el estudio.
