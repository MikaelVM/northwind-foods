SELECT * FROM orders
WHERE orderdate BETWEEN '1997-01-01' AND '1997-04-30'
  AND shipcountry = 'Canada';