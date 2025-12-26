USE CicekProje
GO
ALTER VIEW vw_OrderDetails
AS
SELECT
    o.id AS order_id,
    o.created_at,
    p.name AS product_name,
    oi.quantity,
    p.price,
    (oi.quantity * p.price) AS total_price
FROM store_order o
JOIN store_orderitem oi ON o.id = oi.order_id
JOIN store_product p ON oi.product_id = p.id
/*Sipariþ + ürün + adet + fiyat + toplam tek yerden gelsin*/