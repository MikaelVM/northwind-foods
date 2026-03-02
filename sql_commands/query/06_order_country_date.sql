SELECT *
FROM orders
WHERE shipcountry = 'Germany'
  AND extract(YEAR FROM orderdate) = '1996'
  AND employeeid = 1
  AND freight > 100;