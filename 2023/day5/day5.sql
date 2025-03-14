-- IMPORTING

DROP TABLE IF EXISTS #import

CREATE TABLE #import (
    import_chars VARCHAR(MAX)
);

DROP TABLE IF EXISTS #mapping

CREATE TABLE #mapping (
    source VARCHAR(100)
    ,destination VARCHAR(100)
    ,destination_number BIGINT
    ,source_number BIGINT
    ,conversion_range BIGINT
);

TRUNCATE TABLE #import

BULK INSERT #import
FROM '<PATH>\day5_input_seeds_soil.txt'

INSERT INTO #mapping
SELECT 'seed'
    ,'soil'
    ,SUBSTRING(import_chars, 1, CHARINDEX(' ', import_chars))
    ,SUBSTRING(import_chars, CHARINDEX(' ', import_chars) + 1, LEN(import_chars) - CHARINDEX(' ', import_chars) - CHARINDEX(' ', REVERSE(import_chars)))
    ,SUBSTRING(import_chars, LEN(import_chars) - CHARINDEX(' ', REVERSE(import_chars)) + 2, LEN(import_chars))
FROM #import
WHERE import_chars <> 'seed-to-soil map:'

TRUNCATE TABLE #import

BULK INSERT #import
FROM '<PATH>\day5_input_soil_fertilizer.txt'

INSERT INTO #mapping
SELECT 'soil'
    ,'fertilizer'
    ,SUBSTRING(import_chars, 1, CHARINDEX(' ', import_chars))
    ,SUBSTRING(import_chars, CHARINDEX(' ', import_chars) + 1, LEN(import_chars) - CHARINDEX(' ', import_chars) - CHARINDEX(' ', REVERSE(import_chars)))
    ,SUBSTRING(import_chars, LEN(import_chars) - CHARINDEX(' ', REVERSE(import_chars)) + 2, LEN(import_chars))
FROM #import
WHERE import_chars <> 'soil-to-fertilizer map:'

TRUNCATE TABLE #import

BULK INSERT #import
FROM '<PATH>\day5_input_fertilizer_water.txt'

INSERT INTO #mapping
SELECT 'fertilizer'
    ,'water'
    ,SUBSTRING(import_chars, 1, CHARINDEX(' ', import_chars))
    ,SUBSTRING(import_chars, CHARINDEX(' ', import_chars) + 1, LEN(import_chars) - CHARINDEX(' ', import_chars) - CHARINDEX(' ', REVERSE(import_chars)))
    ,SUBSTRING(import_chars, LEN(import_chars) - CHARINDEX(' ', REVERSE(import_chars)) + 2, LEN(import_chars))
FROM #import
WHERE import_chars <> 'fertilizer-to-water map:'

TRUNCATE TABLE #import

BULK INSERT #import
FROM '<PATH>\day5_input_water_light.txt'

INSERT INTO #mapping
SELECT 'water'
    ,'light'
    ,SUBSTRING(import_chars, 1, CHARINDEX(' ', import_chars))
    ,SUBSTRING(import_chars, CHARINDEX(' ', import_chars) + 1, LEN(import_chars) - CHARINDEX(' ', import_chars) - CHARINDEX(' ', REVERSE(import_chars)))
    ,SUBSTRING(import_chars, LEN(import_chars) - CHARINDEX(' ', REVERSE(import_chars)) + 2, LEN(import_chars))
FROM #import
WHERE import_chars <> 'water-to-light map:'

TRUNCATE TABLE #import

BULK INSERT #import
FROM '<PATH>\day5_input_light_temperature.txt'

INSERT INTO #mapping
SELECT 'light'
    ,'temperature'
    ,SUBSTRING(import_chars, 1, CHARINDEX(' ', import_chars))
    ,SUBSTRING(import_chars, CHARINDEX(' ', import_chars) + 1, LEN(import_chars) - CHARINDEX(' ', import_chars) - CHARINDEX(' ', REVERSE(import_chars)))
    ,SUBSTRING(import_chars, LEN(import_chars) - CHARINDEX(' ', REVERSE(import_chars)) + 2, LEN(import_chars))
FROM #import
WHERE import_chars <> 'light-to-temperature map:'

TRUNCATE TABLE #import

BULK INSERT #import
FROM '<PATH>\day5_input_temperature_humidity.txt'

INSERT INTO #mapping
SELECT 'temperature'
    ,'humidity'
    ,SUBSTRING(import_chars, 1, CHARINDEX(' ', import_chars))
    ,SUBSTRING(import_chars, CHARINDEX(' ', import_chars) + 1, LEN(import_chars) - CHARINDEX(' ', import_chars) - CHARINDEX(' ', REVERSE(import_chars)))
    ,SUBSTRING(import_chars, LEN(import_chars) - CHARINDEX(' ', REVERSE(import_chars)) + 2, LEN(import_chars))
FROM #import
WHERE import_chars <> 'temperature-to-humidity map:'

TRUNCATE TABLE #import

BULK INSERT #import
FROM '<PATH>\day5_input_humidity_location.txt'

INSERT INTO #mapping
SELECT 'humidity'
    ,'location'
    ,SUBSTRING(import_chars, 1, CHARINDEX(' ', import_chars))
    ,SUBSTRING(import_chars, CHARINDEX(' ', import_chars) + 1, LEN(import_chars) - CHARINDEX(' ', import_chars) - CHARINDEX(' ', REVERSE(import_chars)))
    ,SUBSTRING(import_chars, LEN(import_chars) - CHARINDEX(' ', REVERSE(import_chars)) + 2, LEN(import_chars))
FROM #import
WHERE import_chars <> 'humidity-to-location map:'

-- PART ONE

BULK INSERT #import
FROM '<PATH>\day5_input_seeds.txt'

DROP TABLE IF EXISTS #conversions

SELECT value AS seed 
INTO #conversions
FROM (
    SELECT SUBSTRING(import_chars, CHARINDEX(':', import_chars) + 2, LEN(import_chars)) AS seeds
    FROM #import
) t
CROSS APPLY STRING_SPLIT(seeds, ' ')

ALTER TABLE #conversions
ADD soil BIGINT
    ,fertilizer BIGINT
    ,water BIGINT
    ,light BIGINT
    ,temperature BIGINT
    ,humidity BIGINT
    ,location BIGINT

UPDATE c
SET c.soil = ISNULL(c.seed - m.source_number + m.destination_number, 123)
FROM #conversions c
LEFT JOIN #mapping m ON c.seed >= m.source_number AND c.seed <= m.source_number + m.conversion_range
WHERE m.source = 'seed' AND m.destination = 'soil'

UPDATE #conversions
SET soil = seed
WHERE soil IS NULL

UPDATE c
SET c.fertilizer = ISNULL(c.soil - m.source_number + m.destination_number, 123)
FROM #conversions c
LEFT JOIN #mapping m ON c.soil >= m.source_number AND c.soil <= m.source_number + m.conversion_range
WHERE m.source = 'soil' AND m.destination = 'fertilizer'

UPDATE #conversions
SET fertilizer = seed
WHERE fertilizer IS NULL

UPDATE c
SET c.water = ISNULL(c.fertilizer - m.source_number + m.destination_number, 123)
FROM #conversions c
LEFT JOIN #mapping m ON c.fertilizer >= m.source_number AND c.fertilizer <= m.source_number + m.conversion_range
WHERE m.source = 'fertilizer' AND m.destination = 'water'

UPDATE #conversions
SET water = seed
WHERE water IS NULL

UPDATE c
SET c.light = ISNULL(c.water - m.source_number + m.destination_number, 123)
FROM #conversions c
LEFT JOIN #mapping m ON c.water >= m.source_number AND c.water <= m.source_number + m.conversion_range
WHERE m.source = 'water' AND m.destination = 'light'

UPDATE #conversions
SET light = seed
WHERE light IS NULL

UPDATE c
SET c.temperature = ISNULL(c.light - m.source_number + m.destination_number, 123)
FROM #conversions c
LEFT JOIN #mapping m ON c.light >= m.source_number AND c.light <= m.source_number + m.conversion_range
WHERE m.source = 'light' AND m.destination = 'temperature'

UPDATE #conversions
SET temperature = seed
WHERE temperature IS NULL

UPDATE c
SET c.humidity = ISNULL(c.temperature - m.source_number + m.destination_number, 123)
FROM #conversions c
LEFT JOIN #mapping m ON c.temperature >= m.source_number AND c.temperature <= m.source_number + m.conversion_range
WHERE m.source = 'temperature' AND m.destination = 'humidity'

UPDATE #conversions
SET humidity = seed
WHERE humidity IS NULL

UPDATE c
SET c.location = ISNULL(c.humidity - m.source_number + m.destination_number, 123)
FROM #conversions c
LEFT JOIN #mapping m ON c.humidity >= m.source_number AND c.humidity <= m.source_number + m.conversion_range
WHERE m.source = 'humidity' AND m.destination = 'location'

UPDATE #conversions
SET location = seed
WHERE location IS NULL

SELECT MIN(location) FROM #conversions