-- Top 10 productos por ventas.
--
-- Sustituir TU_PROJECT_ID por el proyecto de Google Cloud
-- utilizado durante la reproducción.

SELECT
    product_name,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,

    SAFE_DIVIDE(
        SUM(profit),
        SUM(sales)
    ) AS profit_margin,

    COUNT(
        DISTINCT order_id
    ) AS total_orders

FROM
    `TU_PROJECT_ID.retail_analytics.superstore_sales`

GROUP BY
    product_name

ORDER BY
    total_sales DESC

LIMIT 10;
