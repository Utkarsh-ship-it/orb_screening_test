
'''
CREATE TABLE companies (
company_id INT,
name TEXT,
city TEXT,
country TEXT,
revenue INT
);

CREATE TABLE offices (
location_id INT,
company_id INT REFERENCES companies (company_id),
name TEXT,
city TEXT,
country TEXT
);

Write a SQL query that returns name, revenue and number of offices for all companies that have less than 5
offices. Order the result by companies’ number of offices.
'''
SELECT 
	c.name,
	c.revenue,
    COUNT(f.location_id) no_of_offices
FROM companies c
INNER JOIN offices f
	ON c.company_id = f.company_id
GROUP BY c.name, c.revenue
HAVING no_of_offices < 5
ORDER BY no_of_offices DESC