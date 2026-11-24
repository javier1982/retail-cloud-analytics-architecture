-- Consultas utilizadas para evaluar volumen de datos procesados
-- mediante BigQuery Dry Run.
--
-- Sustituir TU_PROJECT_ID por el proyecto de Google Cloud
-- utilizado durante la reproducción.

-- ============================================================
-- 1. Consulta de referencia: todas las columnas
-- ============================================================

SELECT *
FROM
    `TU_PROJECT_ID.retail_analytics.superstore_sales`;


-- ============================================================
-- 2. Solo ventas y beneficio
-- ============================================================

SELECT
    sales,
    profit
FROM
    `TU_PROJECT_ID.retail_analytics.superstore_sales`;


-- ============================================================
-- 3. Agregación por categoría
-- ============================================================

SELECT
    category,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit
FROM
    `TU_PROJECT_ID.retail_analytics.superstore_sales`
GROUP BY
    category;


-- ============================================================
-- 4. Top 10 productos por ventas
-- ============================================================

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
