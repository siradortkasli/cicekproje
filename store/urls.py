from django.urls import path
from . import views
from .api_service import getCities

print("STORE URLS LOADED")

urlpatterns = [
    path('', views.index, name='index'),
    path('urun/<int:product_id>/', views.product_detail, name='product_detail'),
    path('api/categories/', views.category_list_api),
    path('api/products/', views.product_list_api),
    path('api/product/<int:id>/', views.product_detail_api),
    path('api/product/<int:id>/reviews/', views.product_reviews_api),
    path('api/product/<int:id>/reviews/create/', views.product_review_create_api),
    # path("api/cities/", views.get_cities),   
    path("api/cities/", getCities),       
    path("api/cart/add/", views.add_to_cart),       
    path("order/complete/<int:cart_id>/", views.complete_order),
    path("sepet/", views.cart_view, name="cart"),
    path("api/order/single/", views.order_single, name="order_single"),
    path("order/success/<int:order_id>/", views.order_success, name="order_success"),
    path("api/cart/remove/", views.remove_from_cart),
    path("api/cart/update/", views.update_quantity),
    path("api/order/checkout/", views.checkout, name="checkout"),
    path("checkout/", views.checkout_page, name="checkout"),
    path("siparis-takibi/", views.order_tracking, name="order_tracking"),
    path("order/success/", views.order_success, name="order_success"),
]   
