#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Admin kullanıcısı oluşturma scripti
Kullanım: python create_admin.py
"""
import os
import sys
import django

# Proje dizinine geç
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User

def create_admin():
    """Admin kullanıcısı oluşturur"""
    print("\n" + "="*50)
    print("Admin Kullanıcısı Oluşturma")
    print("="*50 + "\n")
    
    username = input("Kullanıcı adı girin (varsayılan: admin): ").strip() or "admin"
    email = input("E-posta adresi girin (varsayılan: admin@example.com): ").strip() or "admin@example.com"
    
    # Kullanıcı zaten var mı kontrol et
    if User.objects.filter(username=username).exists():
        print(f"\nHATA: '{username}' kullanıcı adı zaten kullanılıyor!")
        update = input("Mevcut kullanıcının şifresini güncellemek ister misiniz? (e/h): ").strip().lower()
        if update != 'e':
            print("İşlem iptal edildi.")
            return
        user = User.objects.get(username=username)
    else:
        user = User.objects.create_user(username=username, email=email)
    
    # Şifre al
    while True:
        password = input("Şifre girin: ").strip()
        if len(password) < 8:
            print("Şifre en az 8 karakter olmalıdır!")
            continue
        password_confirm = input("Şifreyi tekrar girin: ").strip()
        if password != password_confirm:
            print("Şifreler eşleşmiyor! Tekrar deneyin.")
            continue
        break
    
    # Admin yetkilerini ver
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.is_approved = True
    user.save()
    
    print("\n" + "="*50)
    print("✓ Admin kullanıcısı başarıyla oluşturuldu!")
    print("="*50)
    print(f"Kullanıcı Adı: {username}")
    print(f"E-posta: {email}")
    print(f"\nAdmin paneline giriş yapabilirsiniz: http://127.0.0.1:8000/admin/")
    print("="*50 + "\n")

if __name__ == '__main__':
    try:
        create_admin()
    except KeyboardInterrupt:
        print("\n\nİşlem iptal edildi.")
    except Exception as e:
        print(f"\nHATA: {e}")
        import traceback
        traceback.print_exc()
        input("\nÇıkmak için Enter'a basın...")


