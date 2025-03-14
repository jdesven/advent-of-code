DROP TABLE IF EXISTS #raw_input

CREATE TABLE #raw_input (
    input VARCHAR(MAX)
)

BULK INSERT #raw_input
FROM '<PATH>'

-- PART ONE

DROP TABLE IF EXISTS #winning_numbers;

WITH winning_numbers_list AS (
    SELECT CAST(SUBSTRING(input, CHARINDEX(' ', input), 4) AS INT) AS card
        , SUBSTRING(input, CHARINDEX(':', input) + 1, CHARINDEX('|', input) - CHARINDEX(':', input) - 1) as numbers
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
        , SUBSTRING(input, CHARINDEX('|', input) + 1, LEN(input)) as numbers
    FROM #raw_input
)
SELECT card
    ,CAST(value AS INT) AS number
INTO #owned_numbers
FROM owned_numbers_list
CROSS APPLY STRING_SPLIT(numbers, ' ')
WHERE value <> ''

DROP TABLE IF EXISTS #winnings_per_card

SELECT w.card
    , 1 as card_amount
    , COUNT(w.number) as winnings
INTO #winnings_per_card
FROM #winning_number w
INNER JOIN #owned_numbers o
    ON w.card = o.card AND w.number = o.number
GROUP BY w.card

SELECT SUM(points)
FROM (
    SELECT card
        ,POWER(2, winnings - 1) as points
    FROM #winnings_per_card
) t