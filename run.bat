@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo ========================================
echo Django Sunucusu Baslatiliyor...
echo ========================================
echo.
python manage.py runserver
if errorlevel 1 (
    echo.
    echo HATA: Sunucu baslatilamadi!
    echo Lutfen hata mesajini kontrol edin.
    echo.
    pause
)

