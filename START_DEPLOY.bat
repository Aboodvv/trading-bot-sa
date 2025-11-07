@echo off
chcp 65001 >nul
echo.
echo ============================================
echo 🚀 تحضير المشروع للنشر على الإنترنت
echo ============================================
echo.

echo 📝 الخطوة 1: التحقق من Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git غير مثبت!
    echo.
    echo 📥 حمل Git من: https://git-scm.com/download/win
    echo.
    pause
    exit /b
)
echo ✅ Git مثبت

echo.
echo 📝 الخطوة 2: اسم المستخدم على GitHub
set /p GITHUB_USER="أدخل اسم المستخدم على GitHub: "

echo.
echo 📝 الخطوة 3: اسم المشروع (افتراضي: trading-bot)
set /p REPO_NAME="أدخل اسم المشروع (Enter للافتراضي): "
if "%REPO_NAME%"=="" set REPO_NAME=trading-bot

echo.
echo ============================================
echo 🔧 تهيئة Git Repository
echo ============================================

git init
git add .
git commit -m "Trading Bot - Complete System with Subscriptions"
git branch -M main
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git

echo.
echo ============================================
echo ⬆️ رفع الكود على GitHub
echo ============================================
echo.
echo 📌 ملاحظة: سيطلب منك:
echo    - Username: %GITHUB_USER%
echo    - Password: استخدم Personal Access Token
echo.
echo 🔑 للحصول على Token:
echo    https://github.com/settings/tokens
echo.

git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ فشل الرفع!
    echo.
    echo تأكد من:
    echo 1. إنشاء repository على GitHub: https://github.com/new
    echo 2. استخدام Personal Access Token كـ password
    echo.
    pause
    exit /b
)

echo.
echo ============================================
echo ✅ تم رفع الكود بنجاح!
echo ============================================
echo.
echo 📱 الخطوة التالية:
echo.
echo 1. اذهب إلى: https://render.com
echo 2. سجل دخول بحساب GitHub
echo 3. اضغط "New +" → "Web Service"
echo 4. اختر: %REPO_NAME%
echo 5. Start Command: gunicorn web_app:app --bind 0.0.0.0:$PORT
echo 6. اضغط "Create Web Service"
echo.
echo بعد 3-5 دقائق سيكون التطبيق جاهز! 🎉
echo.
echo رابط Render: https://render.com
echo.
pause
