CREATE TABLE IF NOT EXISTS rpt_sales (
    sale_id SERIAL PRIMARY KEY,
    total_orders INTEGER,
    total_revenue INTEGER,
    total_discount INTEGER,
    sales_date DATE,
    sales_month SMALLINT,
    sales_year SMALLINT
);
