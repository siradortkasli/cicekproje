USE CicekProje
GO

CREATE TRIGGER trg_CalculateOrderTotal
ON store_orderitem
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE o
    SET o.total_price = (
        SELECT SUM(oi.quantity * p.price)
        FROM store_orderitem oi
        JOIN store_product p ON oi.product_id = p.id
        WHERE oi.order_id = o.id
    )
    FROM store_order o
    WHERE o.id IN (
        SELECT order_id FROM inserted
        UNION
        SELECT order_id FROM deleted
    )
END
GO
/* sipariþ toplamý otomatik hesaplama*/