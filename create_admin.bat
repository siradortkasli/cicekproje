@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo Admin kullanici olusturuluyor...
echo.
python create_admin.py
pause


