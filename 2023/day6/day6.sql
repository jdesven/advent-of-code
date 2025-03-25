-- IMPORT DATA

DECLARE @input NVARCHAR(MAX);

SELECT @input = BulkColumn
FROM OPENROWSET(BULK '<PATH>', SINGLE_NCLOB) AS filedata;

DROP TABLE IF EXISTS #input;

WITH split AS (
    SELECT t.ordinal AS val_type
        ,ROW_NUMBER() OVER (PARTITION BY t.ordinal ORDER BY n.ordinal) AS race 
        ,CAST(n.value AS INT) AS val
    FROM STRING_SPLIT(REPLACE(@Input, CHAR(10), ''), CHAR(13), 1) AS t
    CROSS APPLY STRING_SPLIT(t.value, ' ', 1) AS n
    WHERE n.value LIKE '%[0-9]%'
)
SELECT CAST(s1.race AS INT) AS race
    ,CAST(s1.val AS INT) AS t_race
    ,CAST(s2.val AS INT) AS dist_record
INTO #input
FROM split AS s1
INNER JOIN split AS s2
    ON s1.race = s2.race
WHERE s1.val_type = 1
    AND s2.val_type = 2;

-- PART ONE

WITH possibilities AS (
    SELECT i.*
        ,c.value AS t_charge
        ,c.value * (t_race - c.value) AS dist
    FROM #input AS i
    CROSS APPLY GENERATE_SERIES(1, t_race, 1) AS c
)
SELECT CAST(ROUND(EXP(SUM(LOG(number_ways))), 0) AS INT) AS multiplication
FROM (
    SELECT race
        ,COUNT(*) AS number_ways
    FROM possibilities
    WHERE dist > dist_record
    GROUP BY race
) t

-- PART TWO

DECLARE @t_race BIGINT = (
    SELECT CAST(STRING_AGG(CAST(t_race AS NVARCHAR), '') AS BIGINT)
    FROM #input
);

DECLARE @record BIGINT = (
    SELECT CAST(STRING_AGG(CAST(dist_record AS NVARCHAR), '') AS BIGINT)
    FROM #input
);

SELECT COUNT(*) AS ways 
FROM GENERATE_SERIES(CAST(1 AS BIGINT), @t_race, CAST(1 AS BIGINT)) AS c
WHERE c.value * (@t_race - c.value) > @record