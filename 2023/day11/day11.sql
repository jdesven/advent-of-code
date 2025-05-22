-- IMPORT MAP

DECLARE @input NVARCHAR(MAX);

SELECT @input = BulkColumn
FROM OPENROWSET(BULK '<PATH>', SINGLE_NCLOB) AS filedata;

DROP TABLE IF EXISTS #galaxies

SELECT ROW_NUMBER() OVER (ORDER BY i.ordinal, c.value) AS id
    ,CAST(c.value AS INT) AS x
    ,CAST(i.ordinal AS INT) AS y
    ,CAST(SUBSTRING(i.value, c.value, 1) AS NVARCHAR(1)) AS val
INTO #galaxies
FROM STRING_SPLIT(REPLACE(@input, CHAR(10), ''), CHAR(13), 1) AS i
CROSS APPLY GENERATE_SERIES(CAST(1 AS INT), CAST(LEN(i.value) AS INT), CAST(1 AS INT)) AS c;

CREATE UNIQUE CLUSTERED INDEX i_map ON #galaxies(x, y);

-- PART ONE

DROP TABLE IF EXISTS #combinations;

WITH empty_lines AS (
    SELECT DISTINCT 'x' AS axis
        ,x AS val
    FROM #galaxies AS t0
    WHERE NOT EXISTS (
        SELECT *
        FROM #galaxies
        WHERE x = t0.x
        AND val = '#'
    )
    UNION ALL
    SELECT DISTINCT 'y' AS axis
        ,y AS val
    FROM #galaxies AS t0
    WHERE NOT EXISTS (
        SELECT *
        FROM #galaxies
        WHERE y = t0.y
        AND val = '#'
    )
)
SELECT x1
    ,y1
    ,x2
    ,y2
    ,dist
    ,CASE WHEN MIN(axis) IS NULL THEN 0 ELSE COUNT(dist) END AS crossings
INTO #combinations
FROM (
    SELECT g1.x AS x1
        ,g1.y AS y1
        ,g2.x AS x2
        ,g2.y AS y2
        ,ABS(g2.x - g1.x) + ABS(g2.y - g1.y) AS dist
        ,e1.axis
    FROM #galaxies AS g1
    INNER JOIN #galaxies AS g2
    ON g1.x > g2.x OR (g1.x = g2.x AND g1.y > g2.y)
    LEFT JOIN empty_lines AS e1
        ON (e1.axis = 'x' AND (e1.val BETWEEN g1.x AND g2.x OR e1.val BETWEEN g2.x AND g1.x))
        OR (e1.axis = 'y' AND (e1.val BETWEEN g1.y AND g2.y OR e1.val BETWEEN g2.y AND g1.y))
    WHERE g1.val = '#' AND g2.val = '#'
) AS t
GROUP BY x1, y1, x2, y2, dist;

SELECT SUM(dist + crossings)
FROM #combinations

-- PART TWO

SELECT SUM(dist + (1e6 - 1) * crossings)
FROM #combinations