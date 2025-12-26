USE CicekProje
GO
CREATE OR ALTER PROCEDURE sp_CalculateCartTotal
    @CartID INT
AS
BEGIN
    SELECT ISNULL(SUM(p.price * ci.qty), 0) AS TotalPrice
    FROM store_cartitem ci
    JOIN store_product p ON ci.product_id = p.id
    WHERE ci.cart_id = @CartID
END
GO

/*sepet toplamý hesaplamak*/