CREATE PROCEDURE sp_UpdateOrderStatus
    @OrderID INT,
    @Status NVARCHAR(30)
AS
BEGIN
    UPDATE store_order
    SET status = @Status
    WHERE id = @OrderID
END
GO
