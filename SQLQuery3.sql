USE CicekProje
GO
ALTER FUNCTION fn_IsStockAvailable
(
    @ProductID INT,
    @Qty INT
)
RETURNS BIT
AS
BEGIN
    DECLARE @Result BIT

    IF EXISTS (
        SELECT 1
        FROM store_product
        WHERE id = @ProductID AND stock >= @Qty
    )
        SET @Result = 1
    ELSE
        SET @Result = 0

    RETURN @Result
END
/*ürün sepete eklenmeden önce kontrol*/