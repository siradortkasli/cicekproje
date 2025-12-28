from django.db import models
from django.conf import settings


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    """Firma modeli: Her firma bir kullanıcıya bağlıdır"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_profile"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)  # Admin onayı: Firma onaylanmadan ürün ekleyemez
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    """Ürün modeli: Firma tarafından eklenen ürünler"""
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="products"
        # null=True ve blank=True kaldırıldı - Tüm ürünler bir firmaya bağlı olmalı
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image_url = models.CharField(max_length=500)

    has_video = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    is_approved = models.BooleanField(default=False)  # Admin onayı: Onaylanmadan sitede görünmez
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField()
    order = models.IntegerField(default=0)
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    username = models.CharField(max_length=50, default="Misafir Kullanıcı")
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)


class Cart(models.Model):
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    package = models.CharField(max_length=50)
    delivery_date = models.CharField(max_length=20)

class Order(models.Model):
    """Sipariş modeli: Kullanıcı siparişleri ve durum takibi"""
    
    # Sipariş durum seçenekleri
    STATUS_CHOICES = [
        ("PREPARING", "Hazırlanıyor"),
        ("WAITING_APPROVAL", "Kullanıcı Onayı Bekleniyor"),  # Hazırlık fotoğrafı yüklendi, kullanıcı onayı bekleniyor
        ("SHIPPED", "Yola Çıktı"),
        ("DELIVERED", "Teslim Edildi"),
        ("CANCELLED", "İptal Edildi"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PREPARING"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    city = models.CharField(max_length=100, null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    time_range = models.CharField(max_length=50, blank=True, null=True)
    
    is_cancelled = models.BooleanField(default=False)
    cancellation_reason = models.TextField(blank=True, null=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )
    address = models.TextField(blank=True, null=True, verbose_name="Adres")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon Numarası")
    customer_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Müşteri Adı")

    def __str__(self):
        return f"Order #{self.id}"



class OrderItem(models.Model):
    """Sipariş kalemi: Her siparişteki ürün bilgileri"""
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    # Firma tarafından yüklenen hazırlık fotoğrafı
    preparation_image = models.ImageField(
       upload_to="order_preparations/",
       null=True,
       blank=True
    )
    # Kullanıcı fotoğrafı onayladı mı? (True ise sipariş "Yola Çıktı" durumuna geçer)
    is_user_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} x {self.quantity}"


class MessageCard(models.Model):
    """Mesaj kartı modeli: Sipariş başarı sayfasında kullanıcı tarafından eklenen mesaj kartları"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="message_cards"
    )
    sender_name = models.CharField(max_length=150, verbose_name="Gönderici İsim Soyisim")
    recipient_name = models.CharField(max_length=150, verbose_name="Alıcı İsim Soyisim")
    recipient_phone = models.CharField(max_length=20, verbose_name="Alıcı Telefon Numarası")
    message_title = models.CharField(max_length=200, verbose_name="Mesaj Başlığı")
    message_content = models.TextField(verbose_name="Mesaj İçeriği")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mesaj Kartı - Sipariş #{self.order.id} - {self.sender_name}"
    
