from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from store.models import Company


def company_login(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            error = "Kullanıcı adı veya şifre hatalı"
        else:
            try:
                company = user.company_profile
            except Company.DoesNotExist:
                error = "Bu kullanıcı bir firmaya ait değil"
            else:
                if not company.is_approved:
                    error = "Firma henüz admin tarafından onaylanmadı"
                else:
                    login(request, user)
                    return redirect("company_dashboard")

    return render(request, "company/clogin.html", {"error": error})


@login_required
def company_dashboard(request):
    from store.models import Product, OrderItem
    
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
