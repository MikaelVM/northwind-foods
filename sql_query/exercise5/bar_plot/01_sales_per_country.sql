SELECT country, count(*) as total_sales
FROM orders JOIN customers USING (customerid)
GROUP BY country
ORDER BY total_sales ASC;
