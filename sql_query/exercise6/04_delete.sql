DELETE FROM rpt_sales
WHERE sales_year = 1997
RETURNING sale_id;
