from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from store.models import Company, Product


# ============================================
# FİRMA GİRİŞ İŞLEMİ
# Firma kullanıcıları için özel giriş sayfası
# Kontroller: Kullanıcı var mı, şifre doğru mu, aktif mi, firma profili var mı, firma onaylı mı
# ============================================
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
        
        # Firma profili var mı ve onaylı mı kontrol et
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
    from store.models import OrderItem
    
    company = request.user.company_profile
    
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
