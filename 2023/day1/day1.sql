DROP TABLE IF EXISTS #t

CREATE TABLE #t (
    input VARCHAR(MAX)
)

BULK INSERT #t
FROM '<PATH>'

-- PART ONE

ALTER TABLE #t
ADD pos_first_num INT
    ,pos_last_num INT
    ,merged_num INT;

UPDATE #t
SET pos_first_num = PATINDEX('%[0-9]%', input)
    ,pos_last_num = LEN(input) - PATINDEX('%[0-9]%', REVERSE(input)) + 1

UPDATE #t
SET merged_num = SUBSTRING(input, pos_first_num, 1) * 10 + SUBSTRING(input, pos_last_num, 1)

SELECT SUM(merged_num)
FROM #t

-- PART TWO

ALTER TABLE #t
ADD input_p2 VARCHAR(MAX)
    ,input_p2_reverse VARCHAR(MAX)
    ,pos_first_num_p2 INT
    ,pos_first_num_p2_reverse INT
    ,pos_last_num_p2 INT
    ,pos_last_num_p2_reverse INT
    ,first_num INT
    ,last_num INT
    ,merged_num_p2 INT;

UPDATE #t
SET input_p2 = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
        input, 'one', '1')
        , 'two', '2')
        , 'three', '3')
        , 'four', '4')
        , 'five', '5')
        , 'six', '6')
        , 'seven', '7')
        , 'eight', '8')
        , 'nine', '9')

UPDATE #t
SET input_p2_reverse = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
        input, 'nine', '9')
        , 'eight', '8')
        , 'seven', '7')
        , 'six', '6')
        , 'five', '5')
        , 'four', '4')
        , 'three', '3')
        , 'two', '2')
        , 'one', '1')

UPDATE #t
SET pos_first_num_p2 = PATINDEX('%[0-9]%', input_p2)
    , pos_first_num_p2_reverse = PATINDEX('%[0-9]%', input_p2_reverse)
    , pos_last_num_p2 = LEN(input_p2) - PATINDEX('%[0-9]%', REVERSE(input_p2)) + 1
    , pos_last_num_p2_reverse = LEN(input_p2_reverse) - PATINDEX('%[0-9]%', REVERSE(input_p2_reverse)) + 1

UPDATE #t
SET first_num = 
    CASE
        WHEN pos_first_num_p2 < pos_first_num_p2_reverse
            THEN SUBSTRING(input_p2, pos_first_num_p2, 1)
        ELSE
            SUBSTRING(input_p2_reverse, pos_first_num_p2_reverse, 1)
        END
    , last_num = 
    CASE
        WHEN pos_last_num_p2 > pos_last_num_p2_reverse
            THEN SUBSTRING(input_p2, pos_last_num_p2, 1)
        ELSE
            SUBSTRING(input_p2_reverse, pos_last_num_p2_reverse, 1)
        END

UPDATE #t
SET merged_num_p2 = first_num * 10 + last_num

SELECT SUM(merged_num_p2)
FROM #t