from django.urls import path
from . import views
from .api_service import getCities, addToCart

urlpatterns = [
    path('', views.index, name='index'),
    path('kategori/<int:category_id>/', views.category_products, name='category_products'),
    path('urun/<int:product_id>/', views.product_detail, name='product_detail'),
    path('api/categories/', views.category_list_api),
    path('api/products/', views.product_list_api, name='product_list_api'),
    path('api/product/<int:id>/', views.product_detail_api),
    path('api/product/<int:id>/reviews/', views.product_reviews_api),
    path('api/product/<int:id>/reviews/create/', views.product_review_create_api),
    path("cities/", getCities),
    path("cart/add/", addToCart),

]


