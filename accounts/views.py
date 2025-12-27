from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Bu e-posta ile kullanıcı bulunamadı.")
            return redirect("login")

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user is None:
            messages.error(request, "Şifre yanlış!")
            return redirect("login")

        # Normal kullanıcılar için aktiflik kontrolü yok (kayıt olduklarında direkt aktif)
        # Sadece firma kullanıcıları için kontrol yapılır (company_login'de)
        # Firma kullanıcıları company_login kullanmalı, burada kontrol etmiyoruz
        login(request, user)
        # Giriş yaptıktan sonra anasayfaya yönlendir (index view kontrol edecek)
        return redirect("/")

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email:
            messages.error(request, "Email alanı boş olamaz.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Bu e-posta zaten kayıtlı!")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Normal kullanıcılar için admin onayı gerekmez, direkt aktif
        user.is_active = True
        user.is_approved = True
        user.save()

        messages.success(
            request,
            "Kayıt başarılı! Giriş yapabilirsiniz."
        )
        return redirect("login")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")