USE CicekProje
GO
CREATE OR ALTER PROCEDURE sp_CreateOrder
    @TotalPrice DECIMAL(10,2),
    @City NVARCHAR(50),
    @DeliverDate DATE,
    @TimeRange NVARCHAR(50)
AS
BEGIN
    INSERT INTO store_order
        (created_at, total_price, city, delivery_date, time_range)
    VALUES
        (GETDATE(), @TotalPrice, @City, @DeliverDate, @TimeRange)
END
GO
/*sipariþ oluþtur*/