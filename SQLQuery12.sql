USE CicekProje
GO
ALTER FUNCTION fn_IsProductActive (@ProductID INT)
RETURNS BIT
AS
BEGIN
    DECLARE @IsActive BIT

    SELECT @IsActive = is_active
    FROM store_product
    WHERE id = @ProductID

    RETURN ISNULL(@IsActive, 0)
END
/*sadece satýlabilir ürünleri görmek*/