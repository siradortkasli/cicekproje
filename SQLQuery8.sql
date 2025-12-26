USE CicekProje
GO
CREATE OR ALTER PROCEDURE sp_ListOrders
AS
BEGIN
    SELECT
        id,
        created_at,
        total_price,
        city,
        delivery_date,
        time_range
    FROM store_order
    ORDER BY created_at DESC
END
GO
/*sipariþ listele*/