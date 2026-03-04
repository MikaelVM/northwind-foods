INSERT INTO rpt_sales (total_orders, total_revenue, total_discount, sales_date, sales_month, sales_year)
SELECT
    count(*) as total_orders,
    sum(unitprice*quantity*(1-discount)) AS total_revenue,
    sum(unitprice*quantity*(discount)) AS total_discount,
    orderdate AS sales_date,
    extract(MONTH FROM orderdate) AS sales_month,
    extract(YEAR FROM orderdate) as sales_year
FROM orders JOIN orderdetails USING (orderid) GROUP BY orderdate
ORDER BY sales_date
RETURNING sale_id;
