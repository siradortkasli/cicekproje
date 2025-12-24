USE CicekProje
GO

CREATE PROCEDURE sp_CreateOrder
    @CartID INT
AS
BEGIN
    INSERT INTO store_order (cart_id, status, created_at)
    VALUES (@CartID, 'Completed', GETDATE())
END
GO
