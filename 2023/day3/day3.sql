-- IMPORT MAP

DECLARE @input NVARCHAR(MAX);

SELECT @input = BulkColumn
FROM OPENROWSET(BULK '<PATH>', SINGLE_NCLOB) AS filedata;

DROP TABLE IF EXISTS #map

SELECT ROW_NUMBER() OVER (ORDER BY i.ordinal, c.value) AS id
    ,c.value AS x
    ,i.ordinal AS y
    ,SUBSTRING(i.value, c.value, 1) AS val
INTO #map
FROM STRING_SPLIT(REPLACE(@input, CHAR(10), ''), CHAR(13), 1) AS i
CROSS APPLY GENERATE_SERIES(CAST(1 AS INT), CAST(LEN(i.value) AS INT), CAST(1 AS INT)) AS c;

CREATE UNIQUE CLUSTERED INDEX i_#map ON #map(x, y);

-- PART ONE

DROP TABLE IF EXISTS #rec;

WITH map_integers AS (
    SELECT *
    FROM #map
    WHERE val LIKE '[0-9]'
),
rec AS (
    SELECT m1.id AS start_id
        ,m1.*
    FROM map_integers AS m1
    LEFT JOIN map_integers AS m2
        ON m1.y = m2.y AND m1.x = m2.x + 1
    WHERE m2.val IS NULL
    UNION ALL
    SELECT r.start_id
        ,m.*
    FROM rec AS r
    INNER JOIN map_integers AS m
        ON m.y = r.y AND m.x = r.x + 1
)
SELECT *
INTO #rec
FROM rec;

DROP TABLE IF EXISTS #valid_numbers;

WITH valid_start_ids AS (
    SELECT DISTINCT r.start_id
    FROM #rec AS r
    INNER JOIN (
        SELECT *
        FROM #map
        WHERE val LIKE '[^.0-9]'
    ) AS m
        ON ABS(r.x - m.x) <= 1 AND ABS(r.y - m.y) <= 1
)
SELECT r.start_id
    ,CAST(STRING_AGG(val, '') WITHIN GROUP (ORDER BY id ASC) AS INT) AS num
INTO #valid_numbers
FROM #rec AS r
INNER JOIN valid_start_ids AS v
    ON r.start_id = v.start_id
GROUP BY r.start_id;

SELECT SUM(num)
FROM #valid_numbers;

-- PART TWO

WITH touching_gears AS (
    SELECT DISTINCT m.id
        ,v.num
    FROM #map AS m
    LEFT JOIN #rec AS r
        ON ABS(m.x - r.x) <= 1 AND ABS(m.y - r.y) <= 1
    LEFT JOIN #valid_numbers AS v
        ON r.start_id = v.start_id
    WHERE m.val = '*'
)
SELECT SUM(gear_ratio)
FROM (
    SELECT id
        ,CAST(ROUND(EXP(SUM(LOG(num))), 0) AS INT) AS gear_ratio
    FROM touching_gears
    GROUP BY id
    HAVING COUNT(id) = 2
) t