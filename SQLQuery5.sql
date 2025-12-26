USE CicekProje
GO
CREATE OR ALTER PROCEDURE sp_CheckStock
    @ProductID INT,
    @Qty INT
AS
BEGIN
    DECLARE @Stock INT

    SELECT @Stock = stock
    FROM store_product
    WHERE id = @ProductID

    IF @Stock < @Qty
        SELECT 0 AS IsAvailable
    ELSE
        SELECT 1 AS IsAvailable
END
GO

/*sipariþ öncesi stok yeterli mi?*/