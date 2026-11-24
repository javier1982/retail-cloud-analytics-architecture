-- Consulta principal de KPI
-- Arquitectura analítica cloud para PYMEs retail
--
-- Sustituir TU_PROJECT_ID por el proyecto de Google Cloud
-- utilizado durante la reproducción.

SELECT
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
    `TU_PROJECT_ID.retail_analytics.superstore_sales`;
