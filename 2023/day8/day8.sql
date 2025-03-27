-- IMPORT DATA

DECLARE @input NVARCHAR(MAX);

SELECT @input = BulkColumn
FROM OPENROWSET(BULK '<PATH', SINGLE_NCLOB) AS filedata;

DROP TABLE IF EXISTS #directions

SELECT s.value AS ordinal
    ,SUBSTRING(@input, s.value, 1) AS direction
INTO #directions
FROM GENERATE_SERIES(1, CAST(CHARINDEX(CHAR(13), @input) AS INT) - 1, 1) AS s

DROP TABLE IF EXISTS #nodes

SELECT s.ordinal AS ordinal
    ,SUBSTRING(s.value, 1, CHARINDEX('=', s.value) - 2) AS node
    ,SUBSTRING(s.value, CHARINDEX('(', s.value) + 1, CHARINDEX(',', s.value) - CHARINDEX('(', s.value) - 1) AS direction_left
    ,SUBSTRING(s.value, CHARINDEX(',', s.value) + 2, CHARINDEX(')', s.value) - CHARINDEX(',', s.value) - 2) AS direction_right
INTO #nodes
FROM STRING_SPLIT(@input, CHAR(10), 1) AS s
WHERE s.ordinal > 2;

-- PART ONE

DECLARE @length_directions INT = (SELECT COUNT(*) FROM #directions);

WITH cte AS(
    SELECT 1 AS path_order
        ,n.node
        ,n.direction_left
        ,n.direction_right
        ,d.direction
    FROM #nodes AS n
    INNER JOIN #directions AS d
        ON d.ordinal = 1
    WHERE node = 'AAA'
    UNION ALL
    SELECT c.path_order + 1 AS path_order
        ,n.node
        ,n.direction_left
        ,n.direction_right
        ,d.direction
    FROM cte AS c
    INNER JOIN #nodes AS n
        ON n.node <> 'ZZZ' AND ( 
            (c.direction = 'L' AND n.node = c.direction_left)
            OR
            (c.direction = 'R' AND n.node = c.direction_right)
        )
    INNER JOIN #directions AS d
        ON (c.path_order) % @length_directions = (d.ordinal - 1)
)
SELECT COUNT(*) AS steps
FROM cte
OPTION (MAXRECURSION 0);

-- PART TWO

WITH cte AS(
    SELECT ROW_NUMBER() OVER (ORDER BY n.ordinal) AS starting_ordinal
        ,1 AS path_order
        ,n.node
        ,n.direction_left
        ,n.direction_right
        ,d.direction
    FROM #nodes AS n
    INNER JOIN #directions AS d
        ON d.ordinal = 1
    WHERE node LIKE '%A'
    UNION ALL
    SELECT c.starting_ordinal
        ,c.path_order + 1 AS path_order
        ,n.node
        ,n.direction_left
        ,n.direction_right
        ,d.direction
    FROM cte AS c
    INNER JOIN #nodes AS n
        ON n.node NOT LIKE '%Z' AND ( 
            (c.direction = 'L' AND n.node = c.direction_left)
            OR
            (c.direction = 'R' AND n.node = c.direction_right)
        )
    INNER JOIN #directions AS d
        ON (c.path_order) % @length_directions = (d.ordinal - 1)
),
steps_per_starting_ordinal AS (
    SELECT starting_ordinal
        ,COUNT(*) AS amount_steps
    FROM cte
    GROUP BY starting_ordinal
),
lcms AS (
    SELECT starting_ordinal
        ,CAST(amount_steps AS BIGINT) AS lcm
    FROM steps_per_starting_ordinal
    WHERE starting_ordinal = 1
    UNION ALL
    SELECT s.starting_ordinal
        ,dbo.LCM(l.lcm, s.amount_steps) AS lcm
    FROM lcms AS l
    INNER JOIN steps_per_starting_ordinal AS s
        ON l.starting_ordinal + 1 = s.starting_ordinal
)
SELECT MAX(lcm) FROM lcms AS steps
OPTION (MAXRECURSION 0);