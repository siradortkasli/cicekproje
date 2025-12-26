USE CicekProje
GO
CREATE OR ALTER TRIGGER trg_DeactivateProductIfOutOfStock
ON store_product
AFTER UPDATE
AS
BEGIN
    UPDATE store_product
    SET is_active = 0
    WHERE stock <= 0
END
GO
/*stok biterse ürün pasif yap*/