# 📥 تثبيت Git على Windows

## الطريقة الأولى: التحميل المباشر (الأسهل)

### 1. تحميل Git:
- اذهب إلى: **https://git-scm.com/download/win**
- سيبدأ التحميل تلقائياً
- أو اضغط: **Click here to download manually**

### 2. التثبيت:
1. شغّل الملف المحمّل: `Git-2.xx.x-64-bit.exe`
2. اضغط **Next** في كل خطوة (الإعدادات الافتراضية جيدة)
3. **مهم**: عند "Adjusting your PATH environment":
   - اختر: ✅ **Git from the command line and also from 3rd-party software**
4. أكمل التثبيت
5. أعد تشغيل PowerShell

### 3. التحقق من التثبيت:
افتح PowerShell جديد وشغّل:
```powershell
git --version
```

إذا ظهر:
```
git version 2.43.0
```
✅ تم التثبيت بنجاح!

---

## الطريقة الثانية: باستخدام winget (Windows 10/11)

افتح PowerShell كـ **Administrator** وشغّل:

```powershell
winget install --id Git.Git -e --source winget
```

ثم أعد تشغيل PowerShell.

---

## ✅ بعد التثبيت

### 1. إعداد Git (مرة واحدة فقط):

```powershell
git config --global user.name "اسمك"
git config --global user.email "your@email.com"
```

### 2. تشغيل السكريبت الجاهز:

```powershell
cd "C:\Users\lenovo\Desktop\بوت"
.\START_DEPLOY.bat
```

السكريبت سيقوم بكل شيء تلقائياً! 🚀

---

## 🎁 البديل: GitHub Desktop (بدون أوامر)

إذا كنت لا تريد استخدام الأوامر:

### 1. تحميل GitHub Desktop:
- https://desktop.github.com
- حمّل وثبّت البرنامج
- سجل دخول بحساب GitHub

### 2. رفع المشروع:
1. اضغط: **File** → **Add Local Repository**
2. اختر: `C:\Users\lenovo\Desktop\بوت`
3. إذا قال "not a Git repository":
   - اضغط: **create a repository**
4. اكتب Summary: "Trading Bot - Complete System"
5. اضغط: **Commit to main**
6. اضغط: **Publish repository**
7. اختر: **Public**
8. اضغط: **Publish repository**

انتهى! ✅ الكود الآن على GitHub

---

## 📱 الخطوة التالية

بعد رفع الكود على GitHub:

1. اذهب إلى: https://render.com
2. سجل دخول بحساب GitHub
3. اضغط: **New +** → **Web Service**
4. اختر: `بوت` (أو `trading-bot`)
5. اضغط: **Connect**
6. املأ الإعدادات:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web_app:app --bind 0.0.0.0:$PORT`
7. اضغط: **Create Web Service**

انتظر 3-5 دقائق... وسيكون التطبيق جاهزاً! 🎉

---

## ❓ أيهما أفضل؟

| الخيار | السهولة | المرونة | موصى به لـ |
|--------|---------|---------|------------|
| **Git CMD** | متوسطة | عالية | المبرمجين |
| **GitHub Desktop** | سهلة جداً | متوسطة | المبتدئين ⭐ |

**نصيحتي**: ابدأ بـ **GitHub Desktop** إذا كنت مبتدئ!
