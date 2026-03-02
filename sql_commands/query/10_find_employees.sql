SELECT * FROM employees
WHERE extract(year FROM birthdate) >= '1960'
AND region IS NULL;