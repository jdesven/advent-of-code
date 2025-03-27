CREATE FUNCTION dbo.GCD (@a BIGINT, @b BIGINT)
RETURNS BIGINT
AS
BEGIN
    IF @b = 0
        RETURN @a
    IF @b = 0
        RETURN @b
    RETURN dbo.GCD(@b, @a % @b)
END;