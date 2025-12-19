from django.contrib import admin
from .models import Product, Category, ProductImage, Review, Cart, CartItem, Order, City
from .api_service import save_products_to_db

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "is_active")
    actions = ["fetch_api_products"]
    inlines = [ProductImageInline]

    def fetch_api_products(self, request, queryset):
        save_products_to_db()
        self.message_user(request, "API'den ürünler başarıyla çekildi!")
    
    fetch_api_products.short_description = "API'den Ürün Çek"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "rating", "product", "created_at")
    
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(City)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
