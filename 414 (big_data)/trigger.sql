#If the population of a particular city needs to be decreased by any value larger than 8% from its
#current population size, then decrease the population of every country on that same continent by 
#4%.


DELIMITER $$
USE world;
DROP TRIGGER /*!50032 IF EXISTS */ decreasing_population $$


CREATE TRIGGER decreasing_population

BEFORE UPDATE ON city
FOR EACH ROW
BEGIN
    DECLARE original_population INT;
    DECLARE new_population INT;
    DECLARE population_diff INT;
    DECLARE continent_name VARCHAR(50);

    SET original_population = OLD.Population;
    SET new_population = NEW.Population;
    SET population_diff = original_population - new_population;

    IF (population_diff > 0.08 * original_population) THEN
        SELECT Continent INTO continent_name
        FROM country
        WHERE Code = OLD.CountryCode;

        UPDATE country
        SET Population = Population - FLOOR(0.04 * Population)
        WHERE Continent = continent_name;
    END IF;
END;


$$
DELIMITER ;
