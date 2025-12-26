USE CicekProje
GO
CREATE OR ALTER TRIGGER trg_DeactivateProductIfOutOfStock
ON store_product
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE p
    SET p.is_active = 0
    FROM store_product p
    INNER JOIN inserted i ON p.id = i.id
    WHERE i.stock <= 0;
END
GO

/*stok biterse ürün pasif yap*/