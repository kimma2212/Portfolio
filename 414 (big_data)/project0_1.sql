-- create new view as continentlcnc
CREATE VIEW continentlcnc AS 

-- # will have the attributes (continent, largestCity, numOfCountries)
SELECT 
    country.Continent,
    (SELECT ci.Name
     FROM city AS ci
     JOIN country AS co ON ci.CountryCode = co.Code
     WHERE co.Continent = country.Continent
     ORDER BY ci.Population DESC
     LIMIT 1) AS largestCity,
    COUNT(DISTINCT country.Code) AS numOfCountries
FROM
    country
GROUP BY
    country.Continent;


SHOW FULL TABLES IN world WHERE TABLE_TYPE LIKE 'VIEW';
