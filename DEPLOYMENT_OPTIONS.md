# 🚀 خيارات نشر بوت التداول
# Deployment Options for Trading Bot

## 📋 المحتويات
1. [Render.com (مجاني + سهل)](#1-rendercom---)
2. [Railway.app (مجاني)](#2-railwayapp---)
3. [Heroku (سهل جداً)](#3-heroku---)
4. [PythonAnywhere (للمبتدئين)](#4-pythonanywhere---)
5. [VPS/DigitalOcean (احترافي)](#5-vpsdigitalocean---)

---

## 1. Render.com (⭐ الأفضل - مجاني)

### المميزات:
- ✅ مجاني تماماً
- ✅ سهل جداً
- ✅ SSL مجاني (HTTPS)
- ✅ دومين مجاني
- ✅ Auto-deploy من GitHub
- ❌ ينام بعد 15 دقيقة بدون استخدام (النسخة المجانية)

### الخطوات:

#### أ) تحضير الملفات:
```bash
# 1. إنشاء ملف requirements.txt (موجود مسبقاً)
# 2. إنشاء runtime.txt
echo "python-3.14.0" > runtime.txt

# 3. تعديل Procfile (موجود مسبقاً)
```

#### ب) رفع الكود على GitHub:
```bash
# في مجلد المشروع
git init
git add .
git commit -m "Initial commit - Trading Bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/trading-bot.git
git push -u origin main
```

#### ج) النشر على Render:
1. اذهب إلى https://render.com
2. سجل دخول بحساب GitHub
3. اضغط "New +" → "Web Service"
4. اختر المشروع من GitHub
5. إعدادات:
   - **Name**: `trading-bot-sa`
   - **Region**: `Singapore` (أقرب للسعودية)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web_app:app`
6. اضغط "Create Web Service"

#### د) رابط التطبيق:
بعد النشر سيكون متاح على:
```
https://trading-bot-sa.onrender.com
```

---

## 2. Railway.app (مجاني)

### المميزات:
- ✅ مجاني ($5 شهرياً مجاناً)
- ✅ سهل جداً
- ✅ لا ينام
- ✅ Deploy من GitHub مباشرة

### الخطوات:

1. اذهب إلى https://railway.app
2. سجل دخول بحساب GitHub
3. اضغط "New Project" → "Deploy from GitHub repo"
4. اختر المشروع
5. Railway سيكتشف Python تلقائياً
6. أضف متغير البيئة:
   ```
   PORT=5000
   ```
7. انتظر حتى ينتهي البناء

#### الرابط:
```
https://trading-bot-production.up.railway.app
```

---

## 3. Heroku (سهل جداً)

### المميزات:
- ✅ موثوق جداً
- ✅ Documentation ممتازة
- ❌ أصبح مدفوع ($5-$7/شهر)

### الخطوات:

#### أ) تثبيت Heroku CLI:
```bash
# تحميل من: https://devcenter.heroku.com/articles/heroku-cli
```

#### ب) النشر:
```bash
# تسجيل الدخول
heroku login

# إنشاء تطبيق
heroku create trading-bot-sa

# رفع الكود
git push heroku main

# فتح التطبيق
heroku open
```

#### ج) إضافة قاعدة بيانات:
```bash
# SQLite لن يعمل على Heroku، استخدم PostgreSQL
heroku addons:create heroku-postgresql:mini
```

---

## 4. PythonAnywhere (للمبتدئين)

### المميزات:
- ✅ سهل للمبتدئين
- ✅ مجاني (محدود)
- ✅ لا يحتاج Git
- ❌ بطيء في النسخة المجانية

### الخطوات:

1. اذهب إلى https://www.pythonanywhere.com
2. سجل حساب مجاني
3. اذهب إلى "Files" → ارفع ملفات المشروع
4. اذهب إلى "Web" → "Add a new web app"
5. اختر "Flask"
6. اضبط:
   - **Source code**: `/home/USERNAME/trading-bot`
   - **WSGI configuration**: عدّل ليشير لـ `web_app.py`

---

## 5. VPS/DigitalOcean (احترافي)

### المميزات:
- ✅ تحكم كامل
- ✅ أداء عالي
- ✅ لا ينام أبداً
- ❌ يحتاج خبرة تقنية
- ❌ مدفوع ($4-$12/شهر)

### الخطوات:

#### أ) إنشاء VPS:
1. اذهب إلى https://www.digitalocean.com
2. أنشئ Droplet (Ubuntu 22.04)
3. اختر الحجم ($4/شهر كافي للبداية)

#### ب) الاتصال بالسيرفر:
```bash
ssh root@YOUR_SERVER_IP
```

#### ج) تثبيت المتطلبات:
```bash
# تحديث النظام
apt update && apt upgrade -y

# تثبيت Python 3
apt install python3 python3-pip python3-venv nginx -y

# إنشاء مستخدم
adduser trading
usermod -aG sudo trading
su - trading
```

#### د) رفع الكود:
```bash
# على جهازك المحلي
scp -r "C:\Users\lenovo\Desktop\بوت" trading@YOUR_SERVER_IP:/home/trading/

# على السيرفر
cd /home/trading/بوت
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### هـ) تشغيل مع Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 web_app:app
```

#### و) تشغيل تلقائي (Systemd):
```bash
sudo nano /etc/systemd/system/trading-bot.service
```

محتوى الملف:
```ini
[Unit]
Description=Trading Bot Web Application
After=network.target

[Service]
User=trading
WorkingDirectory=/home/trading/بوت
Environment="PATH=/home/trading/بوت/venv/bin"
ExecStart=/home/trading/بوت/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 web_app:app

[Install]
WantedBy=multi-user.target
```

تفعيل:
```bash
sudo systemctl start trading-bot
sudo systemctl enable trading-bot
sudo systemctl status trading-bot
```

#### ز) إعداد Nginx:
```bash
sudo nano /etc/nginx/sites-available/trading-bot
```

محتوى الملف:
```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

تفعيل:
```bash
sudo ln -s /etc/nginx/sites-available/trading-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### ح) SSL مجاني (Let's Encrypt):
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

---

## 📱 الوصول من أي جهاز

بعد النشر، يمكن الوصول من:

### 1. الكمبيوتر:
```
https://your-app-name.onrender.com
```

### 2. الجوال:
- نفس الرابط
- أو استخدم تطبيق iOS الذي أنشأناه

### 3. التابلت:
- نفس الرابط
- يعمل responsive

---

## 🔒 الأمان

### متغيرات البيئة (Environment Variables):

لا تضع المفاتيح السرية في الكود! استخدم Environment Variables:

#### في Render/Railway:
```
DATABASE_URL=sqlite:///trading_bot.db
SECRET_KEY=your-secret-key-here
GREENAPI_INSTANCE=your-instance-id
GREENAPI_TOKEN=your-api-token
```

#### في الكود:
```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
GREENAPI_INSTANCE = os.environ.get('GREENAPI_INSTANCE')
```

---

## 🎯 التوصية النهائية

### للبداية السريعة (مجاني):
**استخدم Render.com**
- سهل جداً
- مجاني
- يعمل خلال 5 دقائق

### للإنتاج (احترافي):
**استخدم DigitalOcean VPS**
- أداء عالي
- تحكم كامل
- $4/شهر فقط

---

## 📞 روابط مفيدة

- Render: https://render.com
- Railway: https://railway.app
- Heroku: https://www.heroku.com
- PythonAnywhere: https://www.pythonanywhere.com
- DigitalOcean: https://www.digitalocean.com

---

**أي خيار تفضل؟ سأساعدك في نشره خطوة بخطوة! 🚀**
