-- IMPORT MAP

DECLARE @input NVARCHAR(MAX);

SELECT @input = BulkColumn
FROM OPENROWSET(BULK '<PATH>', SINGLE_NCLOB) AS filedata;

DROP TABLE IF EXISTS #input

SELECT CAST(i.ordinal AS INT) AS step
    ,CAST(c.value AS INT) AS i_char
    ,CAST(SUBSTRING(i.value, c.value, 1) AS NVARCHAR(1)) AS char
INTO #input
FROM STRING_SPLIT(@input, ',', 1) AS i
CROSS APPLY GENERATE_SERIES(CAST(1 AS INT), CAST(LEN(i.value) AS INT), CAST(1 AS INT)) AS c;

-- PART ONE

WITH rec AS (
    SELECT *
        ,ASCII(char) * 17 % 256 as val
    FROM #input
    WHERE i_char = 1
    UNION ALL
    SELECT i.step
        ,i.i_char
        ,i.char
        ,(r.val + ASCII(i.char)) * 17 % 256
    FROM rec AS r
    INNER JOIN #input AS i
        ON r.step = i.step AND r.i_char + 1 = i.i_char
)
SELECT SUM(r.val) AS total
FROM rec AS r
INNER JOIN (
    SELECT step
        ,MAX(i_char) AS i_char_max
    FROM rec
    GROUP BY step
) AS m ON r.step = m.step AND r.i_char = m.i_char_max