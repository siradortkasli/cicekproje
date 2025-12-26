USE CicekProje
GO
CREATE OR ALTER TRIGGER trg_PreventNegativeStock
ON store_product
AFTER UPDATE
AS
BEGIN
    IF EXISTS (SELECT 1 FROM inserted WHERE stock < 0)
    BEGIN
        ROLLBACK
        RAISERROR ('Stok 0 altýna düþemez!', 16, 1)
    END
END
GO
/*stok 0 altýna düþmez*/