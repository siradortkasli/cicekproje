from django.db import connection

def create_order(cart_id):
    with connection.cursor() as cursor:
        cursor.execute("EXEC sp_CreateOrder %s", [cart_id])

def add_to_cart(cart_id, product_id, qty, package, delivery_date):
    with connection.cursor() as cursor:
        cursor.execute(
            "EXEC sp_AddToCart %s,%s,%s,%s,%s",
            [cart_id, product_id, qty, package, delivery_date]
        )

def calculate_cart_total(cart_id):
    with connection.cursor() as cursor:
        cursor.execute("EXEC sp_CalculateCartTotal %s", [cart_id])
        return cursor.fetchone()[0]
