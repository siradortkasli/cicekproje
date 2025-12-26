USE CicekProje
GO
CREATE OR ALTER PROCEDURE sp_AddToCart
    @CartID INT,
    @ProductID INT,
    @Qty INT,
    @Package NVARCHAR(50),
    @DeliveryDate NVARCHAR(20)
AS
BEGIN
    INSERT INTO store_cartitem (cart_id, product_id, qty, package, delivery_date)
    VALUES (@CartID, @ProductID, @Qty, @Package, @DeliveryDate)
END
GO

/* sepete �r�n ekleme*/