USE CicekProje
GO
ALTER FUNCTION fn_GetCartTotal (@CartID INT)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @Total DECIMAL(10,2)

    SELECT @Total = SUM(p.price * ci.qty)
    FROM store_cartitem ci
    JOIN store_product p ON ci.product_id = p.id
    WHERE ci.cart_id = @CartID

    RETURN ISNULL(@Total, 0)
END
/*Sepet Toplamýný Hesapla*/