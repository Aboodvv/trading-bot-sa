"""
صفحات HTML لنظام تسجيل الدخول
Login/Register HTML Pages
"""

LOGIN_PAGE = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول - بوت التداول</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .login-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            width: 100%;
            max-width: 450px;
            animation: slideIn 0.5s ease;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .logo-icon {
            font-size: 4em;
            margin-bottom: 10px;
        }
        
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2em;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            color: #333;
            font-weight: bold;
            margin-bottom: 8px;
        }
        
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            transition: all 0.3s;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 10px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn-secondary {
            background: #f5f5f5;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #e0e0e0;
        }
        
        .divider {
            text-align: center;
            margin: 20px 0;
            color: #999;
            position: relative;
        }
        
        .divider::before,
        .divider::after {
            content: '';
            position: absolute;
            top: 50%;
            width: 40%;
            height: 1px;
            background: #e0e0e0;
        }
        
        .divider::before {
            right: 0;
        }
        
        .divider::after {
            left: 0;
        }
        
        .alert {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: none;
        }
        
        .alert-error {
            background: #ffe0e0;
            color: #c00;
            border: 2px solid #ffc0c0;
        }
        
        .alert-success {
            background: #e0ffe0;
            color: #0c0;
            border: 2px solid #c0ffc0;
        }
        
        .remember-forgot {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 15px 0;
            font-size: 0.9em;
        }
        
        .remember-me {
            display: flex;
            align-items: center;
        }
        
        .remember-me input {
            margin-left: 5px;
        }
        
        a {
            color: #667eea;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        .footer-text {
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <div class="logo-icon">🤖</div>
            <h1>بوت التداول الآلي</h1>
            <p class="subtitle">تسجيل الدخول إلى حسابك</p>
        </div>
        
        <div id="alert" class="alert"></div>
        
        <form id="loginForm" onsubmit="handleLogin(event)">
            <div class="form-group">
                <label>اسم المستخدم</label>
                <input type="text" id="username" name="username" required 
                       placeholder="أدخل اسم المستخدم">
            </div>
            
            <div class="form-group">
                <label>كلمة المرور</label>
                <input type="password" id="password" name="password" required 
                       placeholder="أدخل كلمة المرور">
            </div>
            
            <div class="remember-forgot">
                <label class="remember-me">
                    <input type="checkbox" id="remember">
                    <span>تذكرني</span>
                </label>
                <a href="#" onclick="alert('تواصل مع الإدارة لاستعادة كلمة المرور')">
                    نسيت كلمة المرور؟
                </a>
            </div>
            
            <button type="submit" class="btn btn-primary">
                🔐 تسجيل الدخول
            </button>
        </form>
        
        <div class="divider">أو</div>
        
        <button onclick="goToRegister()" class="btn btn-secondary">
            ✨ إنشاء حساب جديد
        </button>
        
        <p class="footer-text">
            © 2024 بوت التداول الآلي - جميع الحقوق محفوظة
        </p>
    </div>
    
    <script>
        function showAlert(message, type) {
            const alert = document.getElementById('alert');
            alert.className = `alert alert-${type}`;
            alert.textContent = message;
            alert.style.display = 'block';
            
            setTimeout(() => {
                alert.style.display = 'none';
            }, 5000);
        }
        
        async function handleLogin(event) {
            event.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username, password})
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showAlert('✅ تم تسجيل الدخول بنجاح! جاري التحويل...', 'success');
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 1000);
                } else {
                    showAlert('❌ ' + result.message, 'error');
                }
            } catch (error) {
                showAlert('❌ خطأ في الاتصال بالخادم', 'error');
            }
        }
        
        function goToRegister() {
            window.location.href = '/register';
        }
    </script>
</body>
</html>
"""

REGISTER_PAGE = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>إنشاء حساب - بوت التداول</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .register-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            width: 100%;
            max-width: 500px;
            animation: slideIn 0.5s ease;
            max-height: 90vh;
            overflow-y: auto;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .logo-icon {
            font-size: 3em;
            margin-bottom: 10px;
        }
        
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 1.8em;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            color: #333;
            font-weight: bold;
            margin-bottom: 8px;
        }
        
        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            transition: all 0.3s;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 10px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn-secondary {
            background: #f5f5f5;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #e0e0e0;
        }
        
        .alert {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: none;
        }
        
        .alert-error {
            background: #ffe0e0;
            color: #c00;
            border: 2px solid #ffc0c0;
        }
        
        .alert-success {
            background: #e0ffe0;
            color: #0c0;
            border: 2px solid #c0ffc0;
        }
        
        .info-box {
            background: #e3f2fd;
            border: 2px solid #2196f3;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            font-size: 0.9em;
        }
        
        .footer-text {
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }
        
        a {
            color: #667eea;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="register-container">
        <div class="logo">
            <div class="logo-icon">✨</div>
            <h1>إنشاء حساب جديد</h1>
            <p class="subtitle">انضم إلى بوت التداول الآلي</p>
        </div>
        
        <div id="alert" class="alert"></div>
        
        <div class="info-box">
            📱 <strong>إشعارات واتساب:</strong> سنرسل لك إشعارات عن كل صفقة (شراء/بيع/ربح/خسارة)
        </div>
        
        <form id="registerForm" onsubmit="handleRegister(event)">
            <div class="form-group">
                <label>الاسم الكامل *</label>
                <input type="text" id="fullname" required placeholder="أحمد محمد">
            </div>
            
            <div class="form-group">
                <label>اسم المستخدم *</label>
                <input type="text" id="username" required 
                       placeholder="اسم فريد للدخول" pattern="[a-zA-Z0-9_]{3,20}">
                <small style="color: #666;">أحرف إنجليزية وأرقام فقط (3-20 حرف)</small>
            </div>
            
            <div class="form-group">
                <label>البريد الإلكتروني *</label>
                <input type="email" id="email" required 
                       placeholder="example@email.com">
            </div>
            
            <div class="form-group">
                <label>كلمة المرور *</label>
                <input type="password" id="password" required 
                       placeholder="كلمة مرور قوية" minlength="6">
                <small style="color: #666;">على الأقل 6 أحرف</small>
            </div>
            
            <div class="form-group">
                <label>تأكيد كلمة المرور *</label>
                <input type="password" id="confirm_password" required 
                       placeholder="أعد كتابة كلمة المرور">
            </div>
            
            <div class="form-group">
                <label>رقم الجوال (اختياري)</label>
                <input type="tel" id="phone" placeholder="0501234567">
            </div>
            
            <div class="form-group">
                <label>رقم واتساب للإشعارات *</label>
                <input type="tel" id="whatsapp" required 
                       placeholder="966501234567 أو 0501234567">
                <small style="color: #666;">مثال: 966501234567 أو 0501234567</small>
            </div>
            
            <button type="submit" class="btn btn-primary">
                ✨ إنشاء الحساب
            </button>
        </form>
        
        <button onclick="goToLogin()" class="btn btn-secondary">
            🔙 لديك حساب؟ تسجيل الدخول
        </button>
        
        <p class="footer-text">
            بإنشاء حساب، أنت توافق على <a href="#">الشروط والأحكام</a>
        </p>
    </div>
    
    <script>
        function showAlert(message, type) {
            const alert = document.getElementById('alert');
            alert.className = `alert alert-${type}`;
            alert.textContent = message;
            alert.style.display = 'block';
            
            setTimeout(() => {
                alert.style.display = 'none';
            }, 5000);
        }
        
        async function handleRegister(event) {
            event.preventDefault();
            
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            
            if (password !== confirmPassword) {
                showAlert('❌ كلمتا المرور غير متطابقتين', 'error');
                return;
            }
            
            const data = {
                username: document.getElementById('username').value,
                email: document.getElementById('email').value,
                password: password,
                full_name: document.getElementById('fullname').value,
                phone: document.getElementById('phone').value,
                whatsapp_number: document.getElementById('whatsapp').value
            };
            
            try {
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showAlert('✅ ' + result.message + ' جاري تسجيل الدخول...', 'success');
                    setTimeout(() => {
                        window.location.href = '/login';
                    }, 2000);
                } else {
                    showAlert('❌ ' + result.message, 'error');
                }
            } catch (error) {
                showAlert('❌ خطأ في الاتصال بالخادم', 'error');
            }
        }
        
        function goToLogin() {
            window.location.href = '/login';
        }
    </script>
</body>
</html>
"""
