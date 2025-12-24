from django.shortcuts import render , get_object_or_404
from .models import Product,Category, ProductImage, Review, Cart, Order, OrderItem, CartItem, City
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
import json
from django.db import connection
from django.views.decorators.http import require_POST

def index(request):
    """Ana sayfa view'ı"""
    return render(request, 'store/index.html')

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
    reviews = p.reviews.order_by('-created_at').values('username','rating','comment','created_at')
    return JsonResponse(list(reviews), safe=False)

def get_cities(request):
    cities = City.objects.all().order_by("name")
    return JsonResponse({
        "cities": list(cities.values_list("name", flat=True))
    })

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
    Review.objects.create(product=p, username=name, rating=rating, comment=comment)
    return JsonResponse({"ok": True})
@csrf_exempt
def add_to_cart(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)

    product_id = data.get("product_id")
    if not product_id:
        return JsonResponse({"error": "Product ID missing"}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    quantity = int(data.get("quantity", 1))
    city = data.get("city")
    delivery_date = data.get("delivery_date")
    time_range = data.get("time_range")
   
# 🔥 EN ÜSTE KOY
    image_url = product.image_url

# Eğer ProductImage varsa onu tercih et
    image = product.images.first()
    if image and image.image_url:
     image_url = image.image_url

    else:
      image_url = "https://via.placeholder.com/120"




    cart = request.session.get("cart", [])

    
    
    for item in cart:
        if item["product_id"] == product.id:
            item["quantity"] += quantity
            request.session["cart"] = cart
            return JsonResponse({"success": True, "message": "Adet artırıldı"})

    cart.append({
        "product_id": product.id,
        "name": product.name,
        "price": float(product.price),
        "quantity": quantity,
        "city": city,
        "image_url": image_url,
        "delivery_date": delivery_date,
        "time_range": time_range
    })

    request.session["cart"] = cart

    return JsonResponse({"success": True, "message": "Sepete eklendi"})

def get_cart(request):
    items = Cart.objects.all()
    data = []

    for i in items:
        data.append({
            "id": i.id,
            "product": i.product.name,
            "quantity": i.quantity,
            "city": i.city,
            "delivery_date": i.delivery_date,
            "total_price": i.total_price,
            "image": i.product.image_url
        })

    return JsonResponse({"cart": data})

@csrf_exempt
def order_checkout(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Normalde DB’ye order kaydedilir
        return JsonResponse({
            "payment_url": f"/payment/?cart={data['cart_id']}"
        })

@require_POST
def complete_order(request, cart_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC sp_CreateOrder %s", [cart_id])

        return JsonResponse({
            "status": "success",
            "message": "Sipariş başarıyla oluşturuldu"
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)
    
@csrf_exempt
def checkout(request):
    if request.method == "POST":
        cart = request.session.get("cart", [])

        if not cart:
            return JsonResponse({"error": "Sepet boş"})

        total = sum(item["price"] * item["quantity"] for item in cart)

        order = Order.objects.create(
            total_price=total
        )

        for item in cart:
            OrderItem.objects.create(
    order=order,
    product_id=item["product_id"],
    quantity=item["quantity"],
    price=item["price"],
    city=item.get("city"),
    delivery_date=item.get("delivery_date"),
    time_range=item.get("time_range")
)

        request.session["cart"] = []

        return JsonResponse({
            "success": True,
           "redirect_url": f"/order/success/{order.id}/"
        })
@csrf_exempt
def order_single(request):
    if request.method == "POST":
        data = json.loads(request.body)

        product_id = data.get("product_id")
        quantity = int(data.get("quantity", 1))

        if not product_id:
            return JsonResponse({"error": "Ürün yok"}, status=400)

        product = Product.objects.get(id=product_id)

        total = product.price * quantity

        order = Order.objects.create(total_price=total)

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        return JsonResponse({
            "success": True,
            "payment_url": f"/order/success/{order.id}/"
        })
def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, "store/order_success.html", {"order": order})

def cart_view(request):
    cart = request.session.get("cart", [])

    total = sum(item["price"] * item["quantity"] for item in cart)

    return render(request, "store/cart.html", {
        "cart": cart,
        "total": total
    })
@csrf_exempt
def remove_from_cart(request):
    if request.method != "POST":
        return JsonResponse({"success": False}, status=400)

    data = json.loads(request.body)
    product_id = int(data.get("product_id"))

    cart = request.session.get("cart", [])

    # 🔥 list comprehension ile ürünü çıkar
    new_cart = [item for item in cart if item["product_id"] != product_id]

    request.session["cart"] = new_cart
    request.session.modified = True

    return JsonResponse({"success": True})
@csrf_exempt
def update_quantity(request):
    if request.method == "POST":
        data = json.loads(request.body)

        product_id = int(data["product_id"])
        quantity = int(data["quantity"])

        cart = request.session.get("cart", [])

        for item in cart:
            if item["product_id"] == product_id:
                item["quantity"] = quantity

        request.session["cart"] = cart
        return JsonResponse({"success": True})

def checkout_page(request):
    cart = request.session.get("cart", [])
    total = sum(item["price"] * item["quantity"] for item in cart)

    return render(request, "store/checkout.html", {
        "total": total
    })

def order_success(request):
    request.session["cart"] = []  # sepeti temizle
    return render(request, "store/order_success.html")
def order_tracking(request):
    return render(request, "store/order_tracking.html")
