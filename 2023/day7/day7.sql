DECLARE @input NVARCHAR(MAX);

SELECT @input = BulkColumn
FROM OPENROWSET(BULK '<PATH>', SINGLE_NCLOB) AS filedata;

-- PART ONE

DROP TABLE IF EXISTS #hands;

WITH split AS (
    SELECT t.ordinal AS i_hand
        ,ROW_NUMBER() OVER (PARTITION BY t.ordinal ORDER BY n.ordinal) AS val_type 
        ,n.value AS val
    FROM STRING_SPLIT(REPLACE(@Input, CHAR(10), ''), CHAR(13), 1) AS t
    CROSS APPLY STRING_SPLIT(t.value, ' ', 1) AS n
)
SELECT s1.i_hand
    ,s1.val AS hand
    ,CAST(s2.val AS INT) AS bid
INTO #hands
FROM split s1
INNER JOIN split s2
    ON s1.i_hand = s2.i_hand
WHERE s1.val_type = 1
    AND s2.val_type = 2;

WITH hands_split AS (
    SELECT h.i_hand
        ,c.value AS i_card
        ,CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(SUBSTRING(h.hand, c.value, 1), 'A', 14), 'K', 13), 'Q', 12), 'J', 11), 'T', 10) AS INT) AS card
    FROM #hands AS h
    CROSS APPLY GENERATE_SERIES(1, 5, 1) AS c
),
type_priority AS (
    SELECT i_hand
        ,CASE
            WHEN MAX(count_card) = 5
                THEN 1
            WHEN MAX(count_card) = 4
                THEN 2
            WHEN MAX(count_card) = 3 AND MIN(count_card) = 2
                THEN 3
            WHEN MAX(count_card) = 3
                THEN 4
            WHEN MAX(count_card) = 2 AND COUNT(DISTINCT card) = 3
                THEN 5
            WHEN MAX(count_card) = 2 AND COUNT(DISTINCT card) = 4
                THEN 6
            ELSE 7
            END AS type_priority
    FROM (
        SELECT i_hand
            ,card
            ,COUNT(*) AS count_card
        FROM hands_split
        GROUP BY i_hand, card
    ) t
    GROUP BY i_hand
),
card_priority AS (
    SELECT i_hand
        ,SUM(card * POWER(10, 2 * (6 - i_card - 1))) AS card_priority
    FROM hands_split
    GROUP BY i_hand
)
SELECT SUM(winnings) AS sum_winnings
FROM (
    SELECT bid * ROW_NUMBER() OVER (ORDER BY type_priority DESC, card_priority ASC) AS winnings
    FROM #hands AS h
    INNER JOIN type_priority AS tp
        ON h.i_hand = tp.i_hand
    INNER JOIN card_priority AS cp
        ON h.i_hand = cp.i_hand
) t;

-- PART TWO

WITH hands_split AS (
    SELECT h.i_hand
        ,c.value AS i_card
        ,CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(SUBSTRING(h.hand, c.value, 1), 'A', 14), 'K', 13), 'Q', 12), 'J', 1), 'T', 10) AS INT) AS card
    FROM #hands AS h
    CROSS APPLY GENERATE_SERIES(1, 5, 1) AS c
),
jokers_per_hand AS (
    SELECT hs.i_hand
        ,ISNULL(c.count_jokers, 0) AS count_jokers
    FROM #hands AS hs
    LEFT JOIN (
        SELECT i_hand
            ,COUNT(*) AS count_jokers
        FROM hands_split
        WHERE card = 1
        GROUP BY i_hand
    ) AS c
        ON hs.i_hand = c.i_hand
),
type_priority AS (
    SELECT h.i_hand
        ,CASE
            WHEN ISNULL(MAX(count_card), 0) + MAX(count_jokers) = 5
                THEN 1
            WHEN MAX(count_card) + MAX(count_jokers) = 4
                THEN 2
            WHEN (MAX(count_card) = 3 AND MIN(count_card) = 2 AND MAX(count_jokers) = 0)
                OR (MAX(count_card) = 2 AND MIN(count_card) = 2 AND MAX(count_jokers) = 1)
                THEN 3
            WHEN MAX(count_card) + MAX(count_jokers) = 3
                THEN 4
            WHEN (MAX(count_card) = 2 AND COUNT(DISTINCT card) = 3 AND MAX(count_jokers) = 0)
                THEN 5
            WHEN (MAX(count_card) = 2 AND COUNT(DISTINCT card) = 4)
                OR (COUNT(DISTINCT card) = 4 AND MAX(count_jokers) = 1)
                THEN 6
            ELSE 7
            END AS type_priority
    FROM #hands AS h
    LEFT JOIN (
        SELECT hs.i_hand
            ,hs.card
            ,COUNT(*) AS count_card
        FROM hands_split AS hs
        WHERE hs.card <> 1
        GROUP BY hs.i_hand, hs.card
    ) AS t
        ON h.i_hand = t.i_hand
    LEFT JOIN jokers_per_hand AS j
        ON h.i_hand = j.i_hand
    GROUP BY h.i_hand
),
card_priority AS (
    SELECT i_hand
        ,SUM(card * POWER(10, 2 * (6 - i_card - 1))) AS card_priority
    FROM hands_split
    GROUP BY i_hand
)
SELECT SUM(winnings) AS sum_winnings
FROM (
    SELECT bid * ROW_NUMBER() OVER (ORDER BY type_priority DESC, card_priority ASC) AS winnings
    FROM #hands AS h
    INNER JOIN type_priority AS tp
        ON h.i_hand = tp.i_hand
    INNER JOIN card_priority AS cp
        ON h.i_hand = cp.i_hand
) t