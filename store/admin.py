from django.contrib import admin
from .models import Product, Category, ProductImage, Review, Cart, CartItem, Order, City, Company, OrderItem
from .api_service import save_products_to_db

#ürün görselleri
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
#sipariş kalemleri
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price", "preparation_image", "is_user_approved")

# COMPANY (FİRMA) ADMIN
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "is_approved", "created_at")
    list_filter = ("is_approved",)
    search_fields = ("name", "user__username")
    actions = ["approve_companies", "reject_companies"]

    def approve_companies(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Seçilen firmalar onaylandı.")

    def reject_companies(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Seçilen firmalar reddedildi.")

    approve_companies.short_description = "Firmaları Onayla"
    reject_companies.short_description = "Firmaları Reddet"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","company", "price", "category","is_approved", "is_active","created_at")
    list_filter = ("is_approved", "is_active", "category", "company")
    search_fields = ("name", "company__name")
    inlines = [ProductImageInline]
    actions = ["approve_products", "reject_products", "fetch_api_products"]

    def approve_products(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Ürünler onaylandı.")

    def reject_products(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Ürünler reddedildi.")

    def fetch_api_products(self, request, queryset):
        save_products_to_db()
        self.message_user(request, "API'den ürünler başarıyla çekildi!")
    
    approve_products.short_description = "Ürünleri Onayla"
    reject_products.short_description = "Ürünleri Reddet"
    fetch_api_products.short_description = "API'den Ürün Çek"

# ORDER (SİPARİŞ) ADMIN
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "total_price", "created_at")
    list_filter = ("status",)
    inlines = [OrderItemInline]

#Diğer modeller
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "rating", "product", "created_at")
    
admin.site.register(Category)
admin.site.register(City)
