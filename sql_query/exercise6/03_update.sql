UPDATE rpt_sales
SET total_revenue = total_revenue * 1.1
WHERE sales_year = 1997
RETURNING sale_id;
