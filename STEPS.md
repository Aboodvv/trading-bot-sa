# 🚀 خطوات النشر السريع (3 خطوات فقط!)

## الخطوة 1: رفع على GitHub ⬆️

افتح PowerShell في مجلد المشروع:

```powershell
cd "C:\Users\lenovo\Desktop\بوت"

git init
git add .
git commit -m "Trading Bot Complete"
git branch -M main

# غير YOUR_USERNAME باسمك على GitHub
git remote add origin https://github.com/YOUR_USERNAME/trading-bot.git
git push -u origin main
```

---

## الخطوة 2: النشر على Render 🌐

1. اذهب إلى: **https://render.com**
2. سجل دخول بـ **GitHub**
3. اضغط **New +** → **Web Service**
4. اختر **trading-bot**
5. املأ:
   - Name: `trading-bot-sa`
   - Start Command: `gunicorn web_app:app --bind 0.0.0.0:$PORT`
6. اضغط **Create Web Service**

---

## الخطوة 3: جاهز! ✅

بعد 3-5 دقائق، التطبيق يعمل على:

```
https://trading-bot-sa.onrender.com
```

شاركه مع أي شخص! يعمل على الجوال والكمبيوتر 📱💻

---

## 🔄 للتحديث لاحقاً:

```powershell
git add .
git commit -m "تحديثات جديدة"
git push
```

Render سيحدث تلقائياً! 🎉

---

**انتهى! التطبيق الآن على الإنترنت! 🌍**
