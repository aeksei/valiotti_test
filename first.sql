--PostgreSQL 9.6
--'\\' is a delimiter

-- Вспомогательная часть
-- генерация данных для проверки работы скрипта
CREATE TABLE "city_population" (
  id SERIAL PRIMARY KEY,
  City varchar(255),
  population integer NULL
);

INSERT INTO "city_population" (city,population) VALUES ('Mackay',77690);
INSERT INTO "city_population" (city,population) VALUES ('Yuryuzan',32256);
INSERT INTO "city_population" (city,population) VALUES ('Rekem',67957);
INSERT INTO "city_population" (city,population) VALUES ('Goes',58056);
INSERT INTO "city_population" (city,population) VALUES ('Mitú',78999);
INSERT INTO "city_population" (city,population) VALUES ('Budaun',96922);
INSERT INTO "city_population" (city,population) VALUES ('West Ham',24816);
INSERT INTO "city_population" (city,population) VALUES ('Canmore',84126);
INSERT INTO "city_population" (city,population) VALUES ('Seevetal',89964);
INSERT INTO "city_population" (city,population) VALUES ('Gilgit',22274);
INSERT INTO "city_population" (city,population) VALUES ('Tucapel',16069);
-- окончание вспомогательной части

SELECT City
FROM city_population
WHERE population = (SELECT MIN(population) FROM city_population);
