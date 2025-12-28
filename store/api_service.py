import requests
from .models import Product, Category
from rest_framework.decorators import api_view
from rest_framework.response import Response

print("🔥 YENİ FAKE API SERVICE KULLANILIYOR!")

# Türkiye şehirlerini döndüren API endpoint'i
@api_view(['GET'])
def getCities(request):
    cities = [
        "Adana","Adıyaman","Afyonkarahisar","Ağrı","Amasya","Ankara","Antalya","Artvin",
        "Aydın","Balıkesir","Bilecik","Bingöl","Bitlis","Bolu","Burdur","Bursa",
        "Çanakkale","Çankırı","Çorum","Denizli","Diyarbakır","Edirne","Elazığ","Erzincan",
        "Erzurum","Eskişehir","Gaziantep","Giresun","Gümüşhane","Hakkâri","Hatay","Isparta",
        "Mersin","İstanbul","İzmir","Kars","Kastamonu","Kayseri","Kırıkkale","Kırklareli",
        "Kırşehir","Kocaeli","Konya","Kütahya","Malatya","Manisa","Kahramanmaraş","Mardin",
        "Muğla","Muş","Nevşehir","Niğde","Ordu","Rize","Sakarya","Samsun","Siirt",
        "Sinop","Sivas","Tekirdağ","Tokat","Trabzon","Tunceli","Şanlıurfa","Uşak",
        "Van","Yozgat","Zonguldak","Aksaray","Bayburt","Karaman","Kırıkkale","Batman",
        "Şırnak","Bartın","Ardahan","Iğdır","Yalova","Karabük","Kilis","Osmaniye","Düzce"
    ]
    return Response({
        "cities": cities
    })
# FakeStore API'den ürünleri çekip veritabanına kaydeden fonksiyon
# Admin panelinden çağrılabilir
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

    
    
