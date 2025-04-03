-- IMPORT DATA

DECLARE @input NVARCHAR(MAX);

SELECT @input = BulkColumn
FROM OPENROWSET(BULK '<PATH>', SINGLE_NCLOB) AS filedata;

-- CALCULATE

DROP TABLE IF EXISTS #calculated;

WITH numbers AS (
    SELECT *
        ,CAST(SUBSTRING(nums, 2, CHARINDEX(',', nums) - 2) AS INT) AS first_num
        ,CAST(REVERSE(SUBSTRING(REVERSE(nums), 2, CHARINDEX(',', REVERSE(nums)) - 2)) AS INT) AS last_num
    FROM (
        SELECT ordinal
            ,CAST('[' + REPLACE(REPLACE(value, CHAR(13), ''), ' ', ',') + ']' AS VARCHAR(MAX)) AS nums
        FROM STRING_SPLIT(@input, CHAR(10), 1)
    ) AS t
),
rec AS (
    SELECT 1 AS depth
        ,*
    FROM numbers
    UNION ALL
    SELECT r.depth + 1
        ,r.ordinal
        ,c.nums
        ,CAST(SUBSTRING(c.nums, 2, CHARINDEX(',', c.nums) - 2) AS INT)
        ,CAST(REVERSE(SUBSTRING(REVERSE(c.nums), 2, CHARINDEX(',', REVERSE(c.nums)) - 2)) AS INT)
    FROM rec AS r
    CROSS APPLY (
        SELECT CAST(REPLACE(REPLACE(
            (SELECT CAST(i2.value AS INT) - CAST(i1.value AS INT) AS v
            FROM OPENJSON(r.nums) AS i1
            INNER JOIN OPENJSON(r.nums) AS i2
                ON CAST(i2.[key] AS INT) = CAST(i1.[key] AS INT) + 1
            ORDER BY CAST(i1.[key] AS INT)
            FOR JSON PATH
        ), '{"v":', ''), '}', '') AS VARCHAR(MAX)) AS nums
    ) AS c
    WHERE EXISTS (
        SELECT *
        FROM OPENJSON(r.nums) AS j
        WHERE j.value != '0'
    )
)
SELECT *
INTO #calculated
from rec;

-- PART ONE

SELECT SUM(last_num) AS sum
FROM #calculated

-- PART TWO

SELECT SUM(top_left_num) AS sum
FROM (
    SELECT SUM(first_num * CASE WHEN depth % 2 = 0 THEN -1 ELSE 1 END) AS top_left_num
    FROM #calculated
    GROUP BY ordinal
) AS t