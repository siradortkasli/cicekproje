import requests
from .models import Product, Category

print("🔥 YENİ FAKE API SERVICE KULLANILIYOR!")

def save_products_to_db():
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)

    if response.status_code != 200:
        print("❌ API'den veri çekilemedi!")
        return

    products = response.json()
    print("✅ API'den veri geldi:", len(products))

    for item in products:
        category_name = item["category"].title()
        category, _ = Category.objects.get_or_create(name=category_name)

        Product.objects.update_or_create(
    name=item["title"],
    defaults={
        "description": item.get("description", ""),
        "price": item["price"],
        "stock": 10,
        "image_url": item["image"],
        "category": category,
        "is_active": True
    }
)


    print("✅ TÜM ÜRÜNLER VERİTABANINA KAYDEDİLDİ!")
