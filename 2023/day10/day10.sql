-- DECLARE SYMBOL HIDDEN BY 'S'
DECLARE @start_symbol NVARCHAR(1) = '-';

-- DECLARE ONE COORDINATE CONNECTED TO S, RELATIVE TO S
-- THIS COORDINATE IS IGNORED IN THE FIRST STEP, I.E. ONLY THE OTHER DIRECTION IS EXPLORED
DECLARE @ignore_start_x INT = 1
DECLARE @ignore_start_y INT = 0

-- IMPORT MAP

DECLARE @input NVARCHAR(MAX);

SELECT @input = BulkColumn
FROM OPENROWSET(BULK '<PATH>', SINGLE_NCLOB) AS filedata;

DROP TABLE IF EXISTS #map

SELECT ROW_NUMBER() OVER (ORDER BY i.ordinal, c.value) AS id
    ,CAST(c.value AS INT) AS x
    ,CAST(i.ordinal AS INT) AS y
    ,CAST(SUBSTRING(i.value, c.value, 1) AS NVARCHAR(1)) AS val
INTO #map
FROM STRING_SPLIT(REPLACE(@input, CHAR(10), ''), CHAR(13), 1) AS i
CROSS APPLY GENERATE_SERIES(CAST(1 AS INT), CAST(LEN(i.value) AS INT), CAST(1 AS INT)) AS c;

CREATE UNIQUE CLUSTERED INDEX i_map ON #map(x, y);

-- PART ONE

DROP TABLE IF EXISTS #path_loop;

WITH rec AS (
    SELECT 1 AS ordinal
        ,x
        ,y
        ,x + @ignore_start_x AS x_prev 
        ,y + @ignore_start_y AS y_prev
        ,@start_symbol AS val
    FROM #map
    WHERE val = 'S'
    UNION ALL
    SELECT ordinal + 1 AS ordinal
        ,m.x AS x
        ,m.y AS y
        ,r.x AS x_prev
        ,r.y AS y_prev
        ,m.val
    FROM rec AS r
    INNER JOIN #map AS m
        ON (ABS(m.x - r.x) <= 1) AND (ABS(m.y - r.y) <= 1)
        AND (
            (r.val = '|' AND ((m.x = r.x AND m.y = r.y + 1) OR (m.x = r.x AND m.y = r.y - 1)))
            OR (r.val = '-' AND ((m.x = r.x - 1 AND m.y = r.y) OR (m.x = r.x + 1 AND m.y = r.y)))
            OR (r.val = 'L' AND ((m.x = r.x AND m.y = r.y - 1) OR (m.x = r.x + 1 AND m.y = r.y)))
            OR (r.val = 'J' AND ((m.x = r.x AND m.y = r.y - 1) OR (m.x = r.x - 1 AND m.y = r.y)))
            OR (r.val = '7' AND ((m.x = r.x - 1 AND m.y = r.y) OR (m.x = r.x AND m.y = r.y + 1)))
            OR (r.val = 'F' AND ((m.x = r.x AND m.y = r.y + 1) OR (m.x = r.x + 1 AND m.y = r.y)))
        )
        AND NOT (m.x = r.x_prev AND m.y = r.y_prev)
        AND NOT m.val = 'S'
)
SELECT ordinal
    ,x
    ,y
    ,val
INTO #path_loop
FROM rec
OPTION (MAXRECURSION 0);

SELECT MAX(ordinal) / 2 AS steps
FROM #path_loop;

-- PART TWO

WITH map_relevant AS (
    SELECT m.x
        ,m.y
        ,ISNULL(p.val, '.') AS val
    FROM #map AS m
    LEFT JOIN #path_loop AS p
        ON m.x = p.x AND m.y = p.y
),
rec AS (
    SELECT x
        ,y
        ,val
        ,CASE WHEN val IN ('|', 'L', 'J') THEN 1
            ELSE 0
        END AS parity
    FROM map_relevant
    WHERE x = 1
    UNION ALL
    SELECT m.x
        ,m.y
        ,m.val
        ,CASE WHEN m.val IN ('|', 'L', 'J') THEN
            CASE WHEN r.parity = 0 THEN 1 ELSE 0 END
        ELSE r.parity
        END AS parity
    FROM rec AS r
    INNER JOIN map_relevant AS m
        ON m.x = r.x + 1 AND m.y = r.y
)
SELECT COUNT(*) AS enclosed
FROM rec
WHERE val = '.' AND parity = 1
OPTION (MAXRECURSION 0);