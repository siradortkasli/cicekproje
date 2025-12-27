from django.urls import path
from . import views
from .api_service import getCities

print("STORE URLS LOADED")

urlpatterns = [
    # 🏠 Ana sayfa
    path('', views.index, name='index'),
    # 🛍️ Ürün sayfaları
    path('urun/<int:product_id>/', views.product_detail, name='product_detail'),
    # 📦 API – Kategoriler & Ürünler
    path('api/categories/', views.category_list_api),
    path('api/products/', views.product_list_api),
    path('api/product/<int:id>/', views.product_detail_api),
    # ⭐ Ürün yorumları
    path('api/product/<int:id>/reviews/', views.product_reviews_api),
    path('api/product/<int:id>/reviews/create/', views.product_review_create_api), 
    # 🌍 Şehirler (Fake API)
    path("api/cities/", getCities),
    # 🛒 Sepet işlemleri       
    path("api/cart/add/", views.add_to_cart),       
    path("sepet/", views.cart_view, name="cart"),
    path("api/cart/remove/", views.remove_from_cart),
    path("api/cart/update/", views.update_quantity),
     # 💳 Checkout & Sipariş
    path("api/order/single/", views.order_single, name="order_single"),
    path("api/order/checkout/", views.checkout, name="checkout"),
    path("checkout/", views.checkout_page, name="checkout_page"),
    # ✅ Sipariş sonucu
    path("order/success/<int:order_id>/", views.order_success, name="order_success"),
    # 🚚 Sipariş takibi
    path("api/order/track/", views.order_track_api),
    path("siparis-takibi/", views.order_tracking, name="order_tracking"),
    # 🏢 COMPANY PANEL
    path("company/register/", views.company_register, name="company_register"),
    path("company/login/", views.company_login, name="company_login"),
    path("company/dashboard/", views.company_dashboard, name="company_dashboard"),
    path("company/products/", views.company_products, name="company_products"),
    path("company/products/add/", views.company_product_add, name="company_product_add"),
    path("company/products/<int:product_id>/edit/", views.company_product_edit, name="company_product_edit"),
    path("company/orders/", views.company_orders, name="company_orders"),
    path("company/orders/<int:order_id>/edit/", views.company_order_edit, name="company_order_edit"),
    path("company/orders/<int:order_id>/cancel/", views.company_cancel_order, name="company_cancel_order"),
    path("company/orders/<int:order_item_id>/upload-image/", views.company_upload_preparation_image, name="company_upload_preparation_image"),
    path("company/orders/<int:order_id>/update-status/", views.company_update_order_status, name="company_update_order_status"),
    path("company/logout/", views.company_logout, name="company_logout"),
    
    # 👤 USER APPROVAL
    path("order/<int:order_id>/approval/", views.user_order_approval_page, name="user_order_approval"),
    path("api/order-item/<int:order_item_id>/approve/", views.user_approve_order_item, name="user_approve_order_item"),
    
    # 📦 Kullanıcı Siparişleri
    path("siparislerim/", views.my_orders, name="my_orders"),

]   
