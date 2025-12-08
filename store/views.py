from django.shortcuts import render , get_object_or_404
from .models import Product,Category, ProductImage, Review
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
import json

def index(request):
    """Ana sayfa view'ı"""
    return render(request, 'store/index.html')

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_active=True)

    return render(request, 'store/category_products.html', {
        'category': category,
        'products': products
    })
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    return render(request, 'store/product_detail.html', {
        'product': product
    })

def category_list_api(request):
    categories = Category.objects.all().values("id", "name")
    return JsonResponse(list(categories), safe=False)


def product_list_api(request):
    q = request.GET.get("q", "")
    category_id = request.GET.get("category", "")

    products = Product.objects.all()

    if q:
        products = products.filter(name__icontains=q)

    if category_id:
        products = products.filter(category_id=category_id)

    data = []
    for product in products:
        data.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "image_url": product.image_url,
        })

    return JsonResponse(data, safe=False)

def product_detail_api(request, id):
    p = get_object_or_404(Product, id=id, is_active=True)
    images = list(p.images.order_by('order').values_list('image_url', flat=True))
    reviews_qs = p.reviews.order_by('-created_at')
    avg = reviews_qs.aggregate(avg=Avg('rating'))['avg'] or 0
    data = {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": float(p.price),
        "stock": p.stock,
        "image_url": p.image_url,
        "images": images,
        "is_premium": p.is_premium,
        "has_video": p.has_video,
        "avg_rating": round(avg, 1),
        "review_count": reviews_qs.count(),
    }
    return JsonResponse(data)

def product_reviews_api(request, id):
    p = get_object_or_404(Product, id=id)
    reviews = p.reviews.order_by('-created_at').values('name','rating','comment','created_at')
    return JsonResponse(list(reviews), safe=False)

@csrf_exempt
def product_review_create_api(request, id):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    try:
        payload = json.loads(request.body)
        name = payload.get("name","Anonim")
        rating = int(payload.get("rating",0))
        comment = payload.get("comment","")
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")
    if not (1 <= rating <= 5):
        return HttpResponseBadRequest("Rating 1-5 olmalı")
    p = get_object_or_404(Product, id=id)
    Review.objects.create(product=p, name=name, rating=rating, comment=comment)
    return JsonResponse({"ok": True})