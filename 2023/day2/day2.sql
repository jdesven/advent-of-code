DROP TABLE IF EXISTS #raw_input

CREATE TABLE #raw_input (
    input VARCHAR(MAX)
)

BULK INSERT #raw_input
FROM '<PATH>'

-- PART ONE

DROP TABLE IF EXISTS #games

SELECT CAST(SUBSTRING(input, 6, CHARINDEX(':', input) - 6) AS INT) as game
    , CAST(ca_1.ordinal AS INT) as hand
    , CAST(SUBSTRING(ca_2.value, 2, CHARINDEX(' ', ca_2.value, 2) - 2) AS INT) as amount
    , SUBSTRING(ca_2.value, CHARINDEX(' ', ca_2.value, 2) + 1, LEN(ca_2.value)) as color
INTO #games
FROM #raw_input
CROSS APPLY STRING_SPLIT(SUBSTRING(input, CHARINDEX(':', input) + 1, LEN(input)), ';', enable_ordinal = 1) AS ca_1
CROSS APPLY STRING_SPLIT(ca_1.value, ',') AS ca_2;

WITH invalid_games AS (
    SELECT DISTINCT game
    FROM #games
    WHERE (amount > 12 AND color = 'red')
        OR (amount > 13 AND color = 'green')
        OR (amount > 14 AND color = 'blue')
)
SELECT SUM(game)
FROM (
    SELECT DISTINCT g.game
    FROM #games AS g
    LEFT JOIN invalid_games AS i
        ON g.game = i.game
    WHERE i.game IS NULL
) t

-- PART TWO

SELECT SUM(red * green * blue)
FROM (
    SELECT game, red, green, blue
    FROM (
        select game
            ,amount
            ,color
        from #games
    ) t
    PIVOT (
        MAX(amount)
        for color in ([red], [green], [blue])
    ) piv
) t