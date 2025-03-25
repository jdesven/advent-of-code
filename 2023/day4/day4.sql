-- IMPORT DATA

DROP TABLE IF EXISTS #raw_input;

CREATE TABLE #raw_input (
    input VARCHAR(MAX)
)

BULK INSERT #raw_input
FROM '<PATH>'

DROP TABLE IF EXISTS #winning_numbers;

WITH winning_numbers_list AS (
    SELECT CAST(SUBSTRING(input, CHARINDEX(' ', input), 4) AS INT) AS card
        , SUBSTRING(input, CHARINDEX(':', input) + 1, CHARINDEX('|', input) - CHARINDEX(':', input) - 1) AS numbers
    FROM #raw_input
)
SELECT card
    ,CAST(value AS INT) AS number
INTO #winning_numbers
FROM winning_numbers_list
CROSS APPLY STRING_SPLIT(numbers, ' ')
WHERE value <> ''

DROP TABLE IF EXISTS #owned_numbers;

WITH owned_numbers_list AS (
    SELECT CAST(SUBSTRING(input, CHARINDEX(' ', input), 4) AS INT) AS card
        , SUBSTRING(input, CHARINDEX('|', input) + 1, LEN(input)) AS numbers
    FROM #raw_input
)
SELECT card
    ,CAST(value AS INT) AS number
INTO #owned_numbers
FROM owned_numbers_list
CROSS APPLY STRING_SPLIT(numbers, ' ')
WHERE value <> '';

-- PART ONE

DROP TABLE IF EXISTS #winnings_per_card;

SELECT w.card
    ,ISNULL(j.winnings, 0) AS winnings
INTO #winnings_per_card
FROM (
    SELECT DISTINCT card
    FROM #winning_numbers
) AS w
LEFT JOIN (
    SELECT w.card
        , COUNT(w.number) AS winnings
    FROM #winning_numbers w
    INNER JOIN #owned_numbers o
        ON w.card = o.card AND w.number = o.number
    GROUP BY w.card
) AS j ON w.card = j.card

SELECT SUM(points) AS total_points
FROM (
    SELECT card
        ,POWER(2, winnings - 1) AS points
    FROM #winnings_per_card
) t;

-- PART TWO

WITH rec AS (
    SELECT *
    FROM #winnings_per_card
    UNION ALL
    SELECT w.*
    FROM rec as r
    INNER JOIN #winnings_per_card AS w
        ON w.card BETWEEN r.card + 1 AND r.card + r.winnings
)
SELECT COUNT(*) AS total_cards
FROM rec