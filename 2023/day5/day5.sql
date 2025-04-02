-- IMPORT DATA

DECLARE @input NVARCHAR(MAX);

SELECT @input = BulkColumn
FROM OPENROWSET(BULK '<INPUT>', SINGLE_NCLOB) AS filedata;

DROP TABLE IF EXISTS #almanac;

WITH input_lines AS(
    SELECT ROW_NUMBER() OVER (ORDER BY ordinal) AS ordinal
        ,value AS row
    FROM STRING_SPLIT(SUBSTRING(@input, CHARINDEX(CHAR(13), @input) + 4, LEN(@input)), CHAR(13), 1)
    WHERE value <> CHAR(10)
),
cte_add_category AS (
    SELECT *
        ,row AS category
    FROM input_lines
    WHERE ordinal = 1
    UNION ALL
    SELECT i.ordinal
        ,i.row
        ,CASE WHEN i.row LIKE '%:%'
            THEN i.row
            ELSE c.category
        END AS category
    FROM cte_add_category AS c
    INNER JOIN input_lines AS i ON c.ordinal + 1 = i.ordinal
)
SELECT ROW_NUMBER() OVER (ORDER BY c.ordinal) AS ordinal
    ,cat.i_category AS category
    ,CAST(SUBSTRING(row, 2, CHARINDEX(' ', row) - 2) AS BIGINT) AS destination_start
    ,CAST(SUBSTRING(row, CHARINDEX(' ', row) + 1, LEN(row) - CHARINDEX(' ', row) - CHARINDEX(' ', REVERSE(row))) AS BIGINT) AS source_start
    ,CAST(SUBSTRING(row, LEN(row) - CHARINDEX(' ', REVERSE(row)) + 2, LEN(row)) AS BIGINT) AS range_length
INTO #almanac
FROM cte_add_category AS c
INNER JOIN (
    SELECT category
        ,ROW_NUMBER() OVER (ORDER BY MIN(ordinal)) AS i_category
    FROM cte_add_category AS c
    GROUP BY category
) AS cat ON c.category = cat.category
WHERE row NOT LIKE '%:'
OPTION (MAXRECURSION 0);

CREATE CLUSTERED INDEX ix_almanac ON #almanac(category);

-- PART ONE

DECLARE @input_first_row NVARCHAR(MAX) = SUBSTRING(@input, 1, CHARINDEX(CHAR(13), @input));

WITH seeds AS (
    SELECT CAST(s.value AS BIGINT) AS seed
    FROM STRING_SPLIT(SUBSTRING(@input_first_row, CHARINDEX(':', @input_first_row) + 2, LEN(@input_first_row) - CHARINDEX(':', @input_first_row) - 2), ' ', 1) AS s
),
cte AS (
    SELECT seed AS original_seed
        ,seed as num
        ,1 AS category
    FROM seeds
    UNION ALL
    SELECT c.original_seed
        ,ISNULL(c.num + (o.destination_start - o.source_start), c.num)
        ,c.category + 1
    FROM cte AS c
    OUTER APPLY (
        SELECT *
        FROM #almanac AS s
        WHERE (c.num >= s.source_start AND c.num < s.source_start + s.range_length)
        AND s.category = c.category
    ) AS o
    WHERE c.category < 8
)
SELECT MIN(num)
FROM cte
WHERE category = 8;

-- PART TWO

DROP TABLE IF EXISTS #seeds_joined;

WITH seeds AS (
    SELECT ordinal
        ,CAST(s.value AS BIGINT) AS seed
    FROM STRING_SPLIT(SUBSTRING(@input_first_row, CHARINDEX(':', @input_first_row) + 2, LEN(@input_first_row) - CHARINDEX(':', @input_first_row) - 2), ' ', 1) AS s
)
SELECT s1.seed AS seed_from
    ,s2.seed AS seed_to
INTO #seeds_joined
FROM (
    SELECT *
    FROM seeds
    WHERE ordinal % 2 = 1
) AS s1
INNER JOIN (
    SELECT *
    FROM seeds
    WHERE ordinal % 2 = 0
) AS s2 ON s1.ordinal + 1 = s2.ordinal;

DECLARE @starting_point INT;

WITH cte AS (
    SELECT CAST(1 AS BIGINT) AS last_num
        ,CAST(1 AS BIGINT) AS num
        ,7 AS category
    UNION ALL
    SELECT CASE WHEN c.category > 0 THEN c.last_num ELSE last_num + 1000 END
        ,CASE WHEN c.category > 0 THEN ISNULL(c.num - (o.destination_start - o.source_start), c.num) ELSE last_num + 1000 END AS num
        ,CASE WHEN c.category > 0 THEN c.category - 1 ELSE 7 END AS category
    FROM cte AS c
    OUTER APPLY (
        SELECT *
        FROM #almanac AS s
        WHERE 
            (c.num >= s.destination_start AND c.num < s.destination_start + s.range_length)
            AND s.category = c.category
    ) AS o
    OUTER APPLY (
        SELECT *
        FROM #seeds_joined AS sj
        WHERE c.category = 0
        AND c.num >= sj.seed_from
        AND c.num < seed_from + sj.seed_to
    ) AS sjo
    WHERE sjo.seed_from IS NULL
)
SELECT @starting_point = MAX(last_num)
FROM cte
OPTION (MAXRECURSION 0);

WITH cte AS (
    SELECT CAST(@starting_point - 1000 AS BIGINT) AS last_num
        ,CAST(@starting_point - 1000 AS BIGINT) AS num
        ,7 AS category
    UNION ALL
    SELECT CASE WHEN c.category > 0 THEN c.last_num ELSE last_num + 1 END
        ,CASE WHEN c.category > 0 THEN ISNULL(c.num - (o.destination_start - o.source_start), c.num) ELSE last_num + 1 END AS num
        ,CASE WHEN c.category > 0 THEN c.category - 1 ELSE 7 END AS category
    FROM cte AS c
    OUTER APPLY (
        SELECT *
        FROM #almanac AS s
        WHERE 
            (c.num >= s.destination_start AND c.num < s.destination_start + s.range_length)
            AND s.category = c.category
    ) AS o
    OUTER APPLY (
        SELECT *
        FROM #seeds_joined AS sj
        WHERE c.category = 0
        AND c.num >= sj.seed_from
        AND c.num < seed_from + sj.seed_to
    ) AS sjo
    WHERE sjo.seed_from IS NULL
)
SELECT MAX(last_num)
FROM cte
OPTION (MAXRECURSION 0);