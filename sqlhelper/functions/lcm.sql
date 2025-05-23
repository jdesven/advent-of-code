CREATE FUNCTION dbo.LCM (@a BIGINT, @b BIGINT)
RETURNS BIGINT
AS
BEGIN
    RETURN (@a * @b) / dbo.GCD(@a, @b)
END;