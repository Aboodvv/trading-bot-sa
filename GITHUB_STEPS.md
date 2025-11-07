# 📤 رفع المشروع على GitHub - خطوات بسيطة

## 🎯 الخطوة 1: إنشاء مستودع على GitHub

### أولاً: اذهب إلى GitHub
1. افتح المتصفح
2. اذهب إلى: **https://github.com/new**
3. سجل دخول إذا لم تكن مسجلاً

### ثانياً: املأ معلومات المستودع

```
Repository name: trading-bot-sa
Description (اختياري): نظام تداول ذكي للأسهم السعودية والأمريكية
```

**مهم جداً:**
- ✅ اختر **Public** (عام)
- ❌ لا تضع علامة على "Add a README file"
- ❌ لا تضف .gitignore
- ❌ لا تضف license

### ثالثاً: اضغط زر "Create repository" الأخضر 🟢

---

## 🎯 الخطوة 2: نسخ رابط المستودع

بعد إنشاء المستودع، ستظهر صفحة فيها تعليمات.

### انسخ الرابط من هنا:
```
https://github.com/اسم_المستخدم_الخاص_بك/trading-bot-sa.git
```

**مثال:**
- إذا كان اسم المستخدم: `ahmed123`
- الرابط: `https://github.com/ahmed123/trading-bot-sa.git`

---

## 🎯 الخطوة 3: ربط المشروع بـ GitHub

### افتح PowerShell في مجلد المشروع

```powershell
cd "C:\Users\lenovo\Desktop\بوت"
```

### الآن شغّل هذه الأوامر **واحد تلو الآخر**:

#### 1. إعداد معلوماتك (مرة واحدة فقط):
```powershell
git config --global user.name "اسمك"
git config --global user.email "your@email.com"
```

**مثال حقيقي:**
```powershell
git config --global user.name "Ahmed"
git config --global user.email "ahmed@gmail.com"
```

#### 2. تهيئة Git في المجلد:
```powershell
git init
```

#### 3. إضافة جميع الملفات:
```powershell
git add .
```

#### 4. حفظ النسخة الأولى:
```powershell
git commit -m "Trading Bot - Complete System"
```

#### 5. تسمية الفرع الرئيسي:
```powershell
git branch -M main
```

#### 6. ربط المشروع بمستودع GitHub:
**⚠️ مهم: غيّر الرابط بالرابط الخاص بك!**

```powershell
git remote add origin https://github.com/اسم_المستخدم_الخاص_بك/trading-bot-sa.git
```

**مثال:**
```powershell
git remote add origin https://github.com/ahmed123/trading-bot-sa.git
```

#### 7. رفع الملفات إلى GitHub:
```powershell
git push -u origin main
```

---

## 🔐 ماذا لو طلب اسم مستخدم وكلمة مرور؟

GitHub لا يقبل كلمة المرور العادية الآن. تحتاج **Personal Access Token**.

### إنشاء Token:

#### 1. اذهب إلى:
```
https://github.com/settings/tokens
```

#### 2. اضغط "Generate new token" → "Generate new token (classic)"

#### 3. املأ المعلومات:
```
Note: Trading Bot Deploy
Expiration: 90 days (أو No expiration)
```

#### 4. اختر الصلاحيات:
✅ ضع علامة على **repo** فقط (كل الخيارات تحتها)

#### 5. اضغط "Generate token" الأخضر

#### 6. انسخ الـ Token:
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**⚠️ مهم جداً:** احفظه في مكان آمن! لن تراه مرة أخرى!

### استخدام الـ Token:

عند تشغيل `git push`، سيطلب منك:

```
Username: اسم_المستخدم_الخاص_بك
Password: الصق_الـ_Token_هنا (ghp_xxxxx...)
```

**لن تظهر الأحرف أثناء اللصق - هذا طبيعي!**

---

## ✅ التحقق من النجاح

### في PowerShell، إذا رأيت:
```
Enumerating objects: 50, done.
Counting objects: 100% (50/50), done.
Writing objects: 100% (50/50), 15.2 MiB | 2.1 MiB/s, done.
To https://github.com/username/trading-bot-sa.git
 * [new branch]      main -> main
```

🎉 **تم الرفع بنجاح!**

### تحقق على GitHub:
1. اذهب إلى: `https://github.com/اسم_المستخدم/trading-bot-sa`
2. ستجد جميع الملفات موجودة!

---

## 🚀 الخطوة التالية: النشر على Render

الآن بعد رفع الكود على GitHub:

### 1. اذهب إلى Render:
```
https://render.com
```

### 2. سجل دخول بحساب GitHub
- اضغط "Get Started"
- اختر "Sign in with GitHub"

### 3. أنشئ Web Service:
- اضغط "New +" → "Web Service"
- اختر `trading-bot-sa` من القائمة
- اضغط "Connect"

### 4. املأ الإعدادات:

| الحقل | القيمة |
|------|--------|
| Name | `trading-bot-sa` |
| Region | `Singapore` |
| Branch | `main` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn web_app:app --bind 0.0.0.0:$PORT` |
| Instance Type | `Free` |

### 5. اضغط "Create Web Service"

### 6. انتظر 3-5 دقائق... 

سترى Logs تظهر:
```
==> Downloading code from GitHub...
==> Installing dependencies...
==> Starting application...
==> Your service is live! 🎉
```

### 7. افتح الرابط:
```
https://trading-bot-sa.onrender.com
```

**تطبيقك الآن على الإنترنت ويعمل على أي جهاز!** 🌍

---

## 📝 الأوامر كاملة (للنسخ السريع)

```powershell
# 1. الانتقال للمجلد
cd "C:\Users\lenovo\Desktop\بوت"

# 2. إعداد Git (مرة واحدة)
git config --global user.name "اسمك"
git config --global user.email "your@email.com"

# 3. تهيئة المشروع
git init
git add .
git commit -m "Trading Bot - Complete System"
git branch -M main

# 4. ربط مع GitHub (غيّر الرابط!)
git remote add origin https://github.com/USERNAME/trading-bot-sa.git

# 5. رفع الكود
git push -u origin main
```

---

## ❓ المشاكل الشائعة

### ❌ "fatal: remote origin already exists"
**الحل:**
```powershell
git remote remove origin
git remote add origin https://github.com/USERNAME/trading-bot-sa.git
```

### ❌ "error: failed to push some refs"
**الحل:**
```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### ❌ "Permission denied"
**الحل:** استخدم Personal Access Token بدلاً من كلمة المرور

---

## 🎁 نصيحة: احفظ الـ Token

لتجنب كتابة الـ Token كل مرة:

```powershell
git config --global credential.helper wincred
```

الآن Windows سيحفظ الـ Token تلقائياً! ✅

---

**جاهز؟ ابدأ الآن! 🚀**

1. أنشئ المستودع على GitHub
2. انسخ الرابط
3. شغّل الأوامر في PowerShell
4. انتظر النجاح!
