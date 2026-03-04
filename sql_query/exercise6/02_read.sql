SELECT
    sum(total_revenue) as sum_revenue,
    sum(total_discount) as sum_discount,
    sales_month,
    sales_year
FROM rpt_sales
GROUP BY sales_year, sales_month
ORDER BY sales_year, sales_month;
