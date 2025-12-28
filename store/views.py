from django.shortcuts import render , get_object_or_404, redirect
from .models import Product,Category, ProductImage, Review, Order, OrderItem, CartItem, City, Company
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
import json
from django.db import connection
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# ============================================
# FİRMA KAYIT İŞLEMİ
# Mevcut kullanıcılar için firma özelliği ekleme veya yeni firma kaydı
# ============================================
def company_register(request):
    from accounts.models import User
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        company_name = request.POST.get("company_name")
        description = request.POST.get("description", "")
        
        if not all([username, email, password, company_name]):
            return render(request, "company/cregister.html", {
                "error": "Tüm alanlar zorunludur."
            })
        
        # Kullanıcı zaten var mı kontrol et
        user = None
        user_exists = User.objects.filter(username=username).first()
        
        if user_exists:
            # Kullanıcı var, önce firma profili var mı kontrol et
            try:
                existing_company = Company.objects.get(user=user_exists)
                # Firma profili var, şifre kontrolü yap
                if not user_exists.check_password(password):
                    return render(request, "company/cregister.html", {
                        "error": "Bu kullanıcı zaten bir firmaya kayıtlı. Şifreniz yanlış. Lütfen firma giriş sayfasından giriş yapmayı deneyin."
                    })
                # Şifre doğru ama zaten firma profili var
                return render(request, "company/cregister.html", {
                    "error": "Bu kullanıcı zaten bir firmaya kayıtlı. Lütfen firma giriş sayfasından giriş yapın."
                })
            except Company.DoesNotExist:
                # Firma profili yok, şifre kontrolü yap
                if not user_exists.check_password(password):
                    return render(request, "company/cregister.html", {
                        "error": "Şifre yanlış. Lütfen doğru şifrenizi girin."
                    })
                # Şifre doğru, kullanıcıyı al
                user = user_exists
            
            # Mevcut kullanıcıya firma özelliği ekle
            # Mevcut kullanıcılar için is_active değerini değiştirmiyoruz
            # Çünkü kullanıcı zaten aktif ve normal giriş yapabiliyor
            # Sadece firma özelliği ekliyoruz
            user.is_company = True
            user.is_approved = False  # Firma onayı bekliyor (Company.is_approved kontrol edilecek)
            user.save()
        else:
            # Email kontrolü (yeni kullanıcı için)
            if User.objects.filter(email=email).exists():
                return render(request, "company/cregister.html", {
                    "error": "Bu e-posta zaten kayıtlı."
                })
            
            # Yeni kullanıcı oluştur
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_company=True,
                is_active=False,
                is_approved=False
            )
        
        # Firma oluştur (eğer daha önce oluşturulmamışsa)
        try:
            company = Company.objects.get(user=user)
            # Zaten varsa güncelle
            company.name = company_name
            company.description = description
            company.is_approved = False
            company.save()
        except Company.DoesNotExist:
            # Yeni firma oluştur
            try:
                company = Company.objects.create(
                    user=user,
                    name=company_name,
                    description=description,
                    is_approved=False
                )
            except Exception as e:
                return render(request, "company/cregister.html", {
                    "error": f"Firma oluşturulurken bir hata oluştu: {str(e)}"
                })
        
        return render(request, "company/cregister.html", {
            "success": "Kayıt başarılı! Admin onayından sonra giriş yapabilirsiniz."
        })
    
    return render(request, "company/cregister.html")

# 🔐 Firma Logout
@login_required
def company_logout(request):
    """Firma panelinden çıkış yapar"""
    logout(request)
    return redirect("login")

# 🔐 Firma Login
def company_login(request):
    from accounts.models import User
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Önce kullanıcıyı bul
        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "company/clogin.html", {
                "error": "Kullanıcı adı veya şifre hatalı"
            })
        
        # Şifre kontrolü
        if not user_obj.check_password(password):
            return render(request, "company/clogin.html", {
                "error": "Kullanıcı adı veya şifre hatalı"
            })
        
        # Kullanıcı aktif mi kontrol et
        if not user_obj.is_active:
            return render(request, "company/clogin.html", {
                "error": "Hesabınız aktif değil. Lütfen admin ile iletişime geçin."
            })
        
        # Firma profili var mı kontrol et
        try:
            company = user_obj.company_profile
            if not company.is_approved:
                return render(request, "company/clogin.html", {
                    "error": "Firma henüz admin tarafından onaylanmadı. Lütfen admin onayını bekleyin."
                })
        except Company.DoesNotExist:
            return render(request, "company/clogin.html", {
                "error": "Bu kullanıcı bir firmaya ait değil. Firma kaydı yapmak için kayıt sayfasına gidin."
            })
        
        # Her şey tamam, giriş yap
        login(request, user_obj)
        return redirect("company_dashboard")

    return render(request, "company/clogin.html")


@login_required
def company_dashboard(request):
    try:
        company = request.user.company_profile
    except Company.DoesNotExist:
        return redirect("company_login")
    
    # İstatistikler
    total_products = Product.objects.filter(company=company).count()
    approved_products = Product.objects.filter(company=company, is_approved=True).count()
    pending_products = Product.objects.filter(company=company, is_approved=False).count()
    total_orders = OrderItem.objects.filter(product__company=company).count()
    
    return render(request, "company/dashboard.html", {
        "company": company,
        "total_products": total_products,
        "approved_products": approved_products,
        "pending_products": pending_products,
        "total_orders": total_orders
    })


@login_required
def company_products(request):
    try:
        company = request.user.company_profile
    except Company.DoesNotExist:
        return redirect("company_login")
    
    products = Product.objects.filter(company=company).order_by('-created_at')
    return render(request, "company/products.html", {
        "company": company,
        "products": products
    })


@login_required
def company_product_add(request):
    try:
        company = request.user.company_profile
    except Company.DoesNotExist:
        return redirect("company_login")
    
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        price = request.POST.get("price")
        stock = request.POST.get("stock", 0)
        image_url = request.POST.get("image_url", "")
        category_id = request.POST.get("category")
        has_video = request.POST.get("has_video") == "on"
        is_premium = request.POST.get("is_premium") == "on"
        
        if not name or not price:
            return render(request, "company/products_add.html", {
                "company": company,
                "error": "Ürün adı ve fiyat zorunludur.",
                "categories": Category.objects.all()
            })
        
        try:
            category = Category.objects.get(id=category_id) if category_id else None
        except Category.DoesNotExist:
            category = None
        
        product = Product.objects.create(
            company=company,
            name=name,
            description=description,
            price=price,
            stock=stock,
            image_url=image_url,
            category=category,
            has_video=has_video,
            is_premium=is_premium,
            is_approved=False  # Admin onayı bekliyor
        )
        
        return redirect("company_products")
    
    return render(request, "company/products_add.html", {
        "company": company,
        "categories": Category.objects.all()
    })


@login_required
def company_product_edit(request, product_id):
    """Firma ürününü düzenler"""
    try:
        company = request.user.company_profile
    except Company.DoesNotExist:
        return redirect("company_login")
    
    try:
        product = Product.objects.get(id=product_id, company=company)
    except Product.DoesNotExist:
        return redirect("company_products")
    
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        price = request.POST.get("price")
        stock = request.POST.get("stock", 0)
        image_url = request.POST.get("image_url", "")
        category_id = request.POST.get("category")
        has_video = request.POST.get("has_video") == "on"
        is_premium = request.POST.get("is_premium") == "on"
        
        if not name or not price:
            return render(request, "company/product_edit.html", {
                "company": company,
                "product": product,
                "error": "Ürün adı ve fiyat zorunludur.",
                "categories": Category.objects.all()
            })
        
        try:
            category = Category.objects.get(id=category_id) if category_id else None
        except Category.DoesNotExist:
            category = None
        
        # Ürün bilgilerini güncelle
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        product.image_url = image_url
        product.category = category
        product.has_video = has_video
        product.is_premium = is_premium
        # Düzenleme yapıldığında onay durumunu sıfırla (admin tekrar onaylamalı)
        product.is_approved = False
        product.save()
        
        return redirect("company_products")
    
    return render(request, "company/product_edit.html", {
        "company": company,
        "product": product,
        "categories": Category.objects.all()
    })


@login_required
def company_orders(request):
    try:
        company = request.user.company_profile
    except Company.DoesNotExist:
        return redirect("company_login")
    
    # Firma ürünlerine ait sipariş kalemleri
    order_items = OrderItem.objects.filter(
        product__company=company
    ).select_related('order', 'product').order_by('-order__created_at')
    
    return render(request, "company/orders.html", {
        "company": company,
        "order_items": order_items
    })


@login_required
def company_order_edit(request, order_id):
    """Firma sipariş bilgilerini düzenler"""
    try:
        company = request.user.company_profile
    except Company.DoesNotExist:
        return redirect("company_login")
    
    try:
        order = Order.objects.get(id=order_id)
        # Siparişteki ürünlerden en az biri bu firmaya ait olmalı
        if not OrderItem.objects.filter(order=order, product__company=company).exists():
            return render(request, "company/order_edit.html", {
                "error": "Bu sipariş size ait değil"
            })
    except Order.DoesNotExist:
        return render(request, "company/order_edit.html", {
            "error": "Sipariş bulunamadı"
        })
    
    if request.method == "POST":
        # Sipariş bilgilerini güncelle
        order.city = request.POST.get("city", order.city)
        if request.POST.get("delivery_date"):
            from datetime import datetime
            try:
                order.delivery_date = datetime.strptime(request.POST.get("delivery_date"), "%Y-%m-%d").date()
            except:
                pass
        order.time_range = request.POST.get("time_range", order.time_range)
        order.save()
        
        return redirect("company_orders")
    
    order_items = order.items.filter(product__company=company)
    return render(request, "company/order_edit.html", {
        "company": company,
        "order": order,
        "order_items": order_items
    })


@login_required
@csrf_exempt
def company_cancel_order(request, order_id):
    """Firma siparişi iptal eder"""
    try:
        company = request.user.company_profile
    except Company.DoesNotExist:
        return JsonResponse({"success": False, "error": "Yetkisiz erişim"}, status=403)
    
    try:
        order = Order.objects.get(id=order_id)
        # Siparişteki ürünlerden en az biri bu firmaya ait olmalı
        if not OrderItem.objects.filter(order=order, product__company=company).exists():
            return JsonResponse({"success": False, "error": "Bu sipariş size ait değil"}, status=403)
    except Order.DoesNotExist:
        return JsonResponse({"success": False, "error": "Sipariş bulunamadı"}, status=404)
    
    if request.method == "POST":
        data = json.loads(request.body)
        cancellation_reason = data.get("cancellation_reason", "")
        
        if not cancellation_reason:
            return JsonResponse({"success": False, "error": "İptal nedeni zorunludur"}, status=400)
        
        order.is_cancelled = True
        order.cancellation_reason = cancellation_reason
        order.status = "CANCELLED"
        order.save()
        
        return JsonResponse({
            "success": True,
            "message": "Sipariş iptal edildi"
        })
    
    return JsonResponse({"success": False, "error": "Geçersiz istek"}, status=400)


@login_required
@csrf_exempt
def company_upload_preparation_image(request, order_item_id):
    """Firma hazırlanan ürünün fotoğrafını yükler"""
    try:
        company = request.user.company_profile
    except Company.DoesNotExist:
        return JsonResponse({"success": False, "error": "Yetkisiz erişim"}, status=403)
    
    try:
        order_item = OrderItem.objects.get(
            id=order_item_id,
            product__company=company
        )
    except OrderItem.DoesNotExist:
        return JsonResponse({"success": False, "error": "Sipariş bulunamadı"}, status=404)
    
    if request.method == "POST":
        if 'preparation_image' in request.FILES:
            order_item.preparation_image = request.FILES['preparation_image']
            order_item.save()
            
            # Sipariş durumunu "Kullanıcı Onayı Bekleniyor" yap
            order_item.order.status = "WAITING_APPROVAL"
            order_item.order.save()
            
            return JsonResponse({
                "success": True,
                "message": "Fotoğraf yüklendi. Kullanıcı onayı bekleniyor."
            })
    
    return JsonResponse({"success": False, "error": "Geçersiz istek"}, status=400)


@login_required
@csrf_exempt
def company_update_order_status(request, order_id):
    """Firma sipariş durumunu günceller"""
    try:
        company = request.user.company_profile
    except Company.DoesNotExist:
        return JsonResponse({"success": False, "error": "Yetkisiz erişim"}, status=403)
    
    try:
        order = Order.objects.get(id=order_id)
        # Siparişteki ürünlerden en az biri bu firmaya ait olmalı
        if not OrderItem.objects.filter(order=order, product__company=company).exists():
            return JsonResponse({"success": False, "error": "Bu sipariş size ait değil"}, status=403)
    except Order.DoesNotExist:
        return JsonResponse({"success": False, "error": "Sipariş bulunamadı"}, status=404)
    
    if request.method == "POST":
        data = json.loads(request.body)
        new_status = data.get("status")
        
        valid_statuses = ["PREPARING", "WAITING_APPROVAL", "SHIPPED", "DELIVERED"]
        if new_status not in valid_statuses:
            return JsonResponse({"success": False, "error": "Geçersiz durum"}, status=400)
        
        order.status = new_status
        order.save()
        
        return JsonResponse({
            "success": True,
            "message": f"Sipariş durumu '{order.get_status_display()}' olarak güncellendi"
        })
    
    return JsonResponse({"success": False, "error": "Geçersiz istek"}, status=400)


# Kullanıcı onayı için view
@csrf_exempt
def user_approve_order_item(request, order_item_id):
    """Kullanıcı hazırlanan ürünü onaylar"""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Geçersiz istek"}, status=400)
    
    # Kullanıcı giriş yapmış olmalı
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Giriş yapmanız gerekiyor"}, status=403)
    
    try:
        order_item = OrderItem.objects.get(id=order_item_id)
    except OrderItem.DoesNotExist:
        return JsonResponse({"success": False, "error": "Sipariş kalemi bulunamadı"}, status=404)
    
    # Kullanıcı sadece kendi siparişlerini onaylayabilir
    if order_item.order.user != request.user:
        return JsonResponse({"success": False, "error": "Bu sipariş size ait değil"}, status=403)
    
    if not order_item.preparation_image:
        return JsonResponse({"success": False, "error": "Henüz hazırlık fotoğrafı yüklenmemiş"}, status=400)
    
    # Kullanıcı onayını ver
    order_item.is_user_approved = True
    order_item.save()
    
    # Sipariş durumunu "Yola Çıktı" yap
    order_item.order.status = "SHIPPED"
    order_item.order.save()
    
    return JsonResponse({
        "success": True,
        "message": "Ürün onaylandı. Sipariş yola çıktı."
    })


# ============================================
# KULLANICI FOTOĞRAF REDDETME İŞLEMİ
# Kullanıcı firma tarafından yüklenen hazırlık fotoğrafını reddeder
# Fotoğraf silinir, onay durumu sıfırlanır, sipariş "Hazırlanıyor" durumuna döner
# ============================================
@csrf_exempt
def user_reject_order_item(request, order_item_id):
    """Kullanıcı hazırlanan ürünün fotoğrafını reddeder"""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Geçersiz istek"}, status=400)
    
    # Kullanıcı giriş yapmış olmalı
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Giriş yapmanız gerekiyor"}, status=403)
    
    try:
        order_item = OrderItem.objects.get(id=order_item_id)
    except OrderItem.DoesNotExist:
        return JsonResponse({"success": False, "error": "Sipariş kalemi bulunamadı"}, status=404)
    
    # Kullanıcı sadece kendi siparişlerini reddedebilir
    if order_item.order.user != request.user:
        return JsonResponse({"success": False, "error": "Bu sipariş size ait değil"}, status=403)
    
    if not order_item.preparation_image:
        return JsonResponse({"success": False, "error": "Henüz hazırlık fotoğrafı yüklenmemiş"}, status=400)
    
    # Fotoğrafı sil ve onay durumunu sıfırla
    if order_item.preparation_image:
        order_item.preparation_image.delete()
    order_item.preparation_image = None
    order_item.is_user_approved = False
    order_item.save()
    
    # Sipariş durumunu "Hazırlanıyor" yap (firma yeniden fotoğraf yüklemeli)
    order_item.order.status = "PREPARING"
    order_item.order.save()
    
    return JsonResponse({
        "success": True,
        "message": "Fotoğraf reddedildi. Firma yeniden fotoğraf yüklemelidir."
    })


def user_order_approval_page(request, order_id):
    """Kullanıcının sipariş onay sayfası"""
    # Kullanıcı giriş yapmış olmalı
    if not request.user.is_authenticated:
        return redirect("login")
    
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return render(request, "store/error.html", {"error": "Sipariş bulunamadı"})
    
    # Kullanıcı sadece kendi siparişlerini görebilir
    if order.user != request.user:
        return render(request, "store/error.html", {"error": "Bu sipariş size ait değil"})
    
    # Onay bekleyen ürünler
    pending_items = order.items.filter(
        preparation_image__isnull=False,
        is_user_approved=False
    )
    
    return render(request, "store/order_approval.html", {
        "order": order,
        "pending_items": pending_items
    })


def index(request):
    """Ana sayfa view'ı - Giriş yapmamışsa giriş sayfasına yönlendir"""
    if not request.user.is_authenticated:
        return redirect("login")
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

    products = Product.objects.filter(
    is_active=True,
    is_approved=True,
    company__is_approved=True
)


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
            "company_name": product.company.name,  # Artık company her zaman dolu (null=False)
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
        "company_name": p.company.name if p.company else "",
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
    image_url = product.image_url or "https://via.placeholder.com/120"
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
    cart = request.session.get("cart", [])
    return JsonResponse({"cart": cart})
    
# ============================================
# SİPARİŞ OLUŞTURMA (CHECKOUT)
# Sepetteki ürünlerden sipariş oluşturur ve sepeti temizler
# ============================================
@csrf_exempt
def checkout(request):
    if request.method != "POST":
        return JsonResponse({"success": False})

    cart = request.session.get("cart", [])

    if not cart:
        return JsonResponse({
            "success": False,
            "error": "Sepet boş"
        })

    data = json.loads(request.body)
    
    # Toplam fiyat hesaplama
    total = sum(item["price"] * item["quantity"] for item in cart)

    # Sipariş oluştur
    order = Order.objects.create(
        total_price=total,
        user=request.user if request.user.is_authenticated else None,
        customer_name=data.get("customer_name", ""),
        phone_number=data.get("phone_number", ""),
        address=data.get("address", ""),
        city=data.get("city", "")
    )

    # Sepetteki her ürün için sipariş kalemi oluştur
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product_id=item["product_id"],
            quantity=item["quantity"],
            price=item["price"],
            image_url=item.get("image_url")
        )

    # Sepeti temizle
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
        total = float(product.price) * quantity
        order = Order.objects.create(total_price=total)

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price,
            image_url=product.image_url
        )

        return JsonResponse({
            "success": True,
            "payment_url": f"/order/success/{order.id}/"
        })
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
    print("🛒 CHECKOUT CART:", cart) 
    return render(request, "store/checkout.html", {
        "total": total,
        "cart" : cart
    })

def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    items = order.items.all()  # related_name="items"

    return render(request, "store/order_success.html", {
        "order": order,
        "items": items
    })

@login_required
def order_tracking(request):
    return render(request, "store/order_tracking.html")

@login_required
def my_orders(request):
    """Kullanıcının siparişlerini gösterir"""
    # Kullanıcının siparişlerini en yeni → en eski sırala
    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related('items__product').order_by('-created_at')
    
    return render(request, "store/my_orders.html", {
        "orders": orders
    })
@csrf_exempt
def payment_complete(request):
    if request.method != "POST":
        return JsonResponse({"success": False})

    cart = request.session.get("cart", [])
    if not cart:
        return JsonResponse({"success": False, "error": "Sepet boş"})

    data = json.loads(request.body)
    total = sum(item["price"] * item["quantity"] for item in cart)

    # ✅ ÖDEME BAŞARILI KABUL EDİYORUZ (simülasyon)
    order = Order.objects.create(
        total_price=total,
        user=request.user if request.user.is_authenticated else None,
        customer_name=data.get("customer_name", ""),
        phone_number=data.get("phone_number", ""),
        address=data.get("address", ""),
        city=data.get("city", "")
    )

    for item in cart:
        OrderItem.objects.create(
            order=order,
            product_id=item["product_id"],
            quantity=item["quantity"],
            price=item["price"],
            city=item.get("city"),
            delivery_date=item.get("delivery_date"),
            time_range=item.get("time_range"),
            image_url=item.get("image_url") 
        )

    # 🧹 sepeti temizle
    request.session["cart"] = []
    request.session.modified = True

    return JsonResponse({
        "success": True,
        "order_id": order.id
    })
# ============================================
# SİPARİŞ TAKİP API
# Kullanıcı sipariş numarası ile sipariş durumunu sorgular
# Güvenlik: Kullanıcı sadece kendi siparişlerini görebilir
# ============================================
@csrf_exempt
def order_track_api(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Geçersiz istek"
        })

    # Kullanıcı giriş yapmış olmalı
    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "error": "Sipariş takibi için giriş yapmanız gerekiyor"
        })

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "error": "Geçersiz veri"
        })

    order_id = data.get("order_id")

    if not order_id:
        return JsonResponse({
            "success": False,
            "error": "Sipariş numarası girilmedi"
        })

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Sipariş bulunamadı"
        })

    # Güvenlik kontrolü: Kullanıcı sadece kendi siparişlerini görebilir
    if order.user != request.user:
        return JsonResponse({
            "success": False,
            "error": "Bu sipariş size ait değil"
        })

    items_data = []
    for item in order.items.all():
        # Fotoğraf URL'i
        prep_image_url = ""
        if item.preparation_image:
            prep_image_url = item.preparation_image.url
        
        items_data.append({
            "id": item.id,
            "product": item.product.name,
            "quantity": item.quantity,
            "price": float(item.price),
            "city": getattr(item, "city", ""),
            "delivery_date": (
                order.created_at.strftime("%d.%m.%Y")
                + " tarihinden itibaren 3–7 iş günü"
            ),
            "time_range": getattr(item, "time_range", ""),
            "image": item.image_url if item.image_url else "",
            "preparation_image": prep_image_url,
            "is_user_approved": item.is_user_approved,
            "company_name": item.product.company.name if item.product.company else ""
        })

    # Sipariş durumu adımları
    status_steps = [
        {
            "status": "PREPARING",
            "label": "Hazırlanıyor",
            "icon": "⏳",
            "active": order.status == "PREPARING",
            "completed": False
        },
        {
            "status": "WAITING_APPROVAL",
            "label": "Kullanıcı Onayı Bekleniyor",
            "icon": "📸",
            "active": order.status == "WAITING_APPROVAL",
            "completed": order.status in ["SHIPPED", "DELIVERED"]
        },
        {
            "status": "SHIPPED",
            "label": "Yola Çıktı",
            "icon": "🚚",
            "active": order.status == "SHIPPED",
            "completed": order.status == "DELIVERED"
        },
        {
            "status": "DELIVERED",
            "label": "Teslim Edildi",
            "icon": "✅",
            "active": order.status == "DELIVERED",
            "completed": order.status == "DELIVERED"
        }
    ]

    return JsonResponse({
        "success": True,
        "order": {
            "id": order.id,
            "total": float(order.total_price),
            "created_at": order.created_at.strftime("%d.%m.%Y %H:%M"),
            "status": order.status,
            "status_display": order.get_status_display(),
            "is_cancelled": order.is_cancelled,
            "cancellation_reason": order.cancellation_reason or "",
            "customer_name": order.customer_name or "",
            "phone_number": order.phone_number or "",
            "address": order.address or "",
            "city": order.city or ""
        },
        "items": items_data,
        "status_steps": status_steps
    })