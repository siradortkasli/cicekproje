CREATE TRIGGER trg_PreventNegativeStock
ON store_product
AFTER UPDATE
AS
BEGIN
    IF EXISTS (
        SELECT 1 FROM store_product WHERE stock < 0
    )
    BEGIN
        ROLLBACK TRANSACTION
        RAISERROR ('Stok miktarý 0 altýna düþemez!', 16, 1)
    END
END
GO
