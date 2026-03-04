SELECT * FROM orders
WHERE employeeid in (2,5,8)
  AND shipregion IS NOT NULL
  AND shipvia in (1,3)
ORDER BY employeeid, shipvia;
