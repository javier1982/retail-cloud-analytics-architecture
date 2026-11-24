-- Análisis agregado por categoría.
--
-- Sustituir TU_PROJECT_ID por el proyecto de Google Cloud
-- utilizado durante la reproducción.

SELECT
    category,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,

    SAFE_DIVIDE(
        SUM(profit),
        SUM(sales)
    ) AS profit_margin,

    COUNT(
        DISTINCT order_id
    ) AS total_orders,

    COUNT(
        DISTINCT customer_id
    ) AS total_customers

FROM
    `TU_PROJECT_ID.retail_analytics.superstore_sales`

GROUP BY
    category

ORDER BY
    total_sales DESC;
