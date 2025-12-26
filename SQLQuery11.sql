USE CicekProje
GO
CREATE OR ALTER TRIGGER trg_DecreaseStockAfterOrderItem
ON store_orderitem
AFTER INSERT
AS
BEGIN
    UPDATE p
    SET p.stock = p.stock - i.quantity
    FROM store_product p
    INNER JOIN inserted i ON p.id = i.product_id
END
GO
/*sipariþ kalemi eklenince stok azalt*/