CREATE PROCEDURE sp_CalculateCartTotal
    @CartID INT
AS
BEGIN
    DECLARE @TotalPrice DECIMAL(10,2)

    SELECT @TotalPrice = SUM(p.price * ci.qty)
    FROM store_cartitem ci
    JOIN store_product p ON ci.product_id = p.id
    WHERE ci.cart_id = @CartID

    SELECT ISNULL(@TotalPrice, 0) AS TotalPrice
END
GO
