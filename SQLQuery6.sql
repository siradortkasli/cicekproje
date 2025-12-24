USE CicekProje
GO

CREATE TRIGGER trg_DecreaseStockAfterOrder
ON store_order
AFTER INSERT
AS
BEGIN
    UPDATE p
    SET p.stock = p.stock - ci.qty
    FROM store_product p
    INNER JOIN store_cartitem ci ON p.id = ci.product_id
    INNER JOIN inserted i ON ci.cart_id = i.cart_id
END
GO
