"""
صفحات HTML لنظام الباقات
Subscription Pages HTML Templates
"""

PLANS_PAGE = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الباقات والأسعار - بوت التداول</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 50px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .plans-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .plan-card {
            background: white;
            border-radius: 20px;
            padding: 40px 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: transform 0.3s, box-shadow 0.3s;
            position: relative;
            overflow: hidden;
        }
        
        .plan-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }
        
        .plan-card.featured {
            border: 3px solid #FFD700;
            transform: scale(1.05);
        }
        
        .plan-badge {
            position: absolute;
            top: 20px;
            left: 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }
        
        .plan-icon {
            font-size: 4em;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .plan-name {
            text-align: center;
            font-size: 2em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        
        .plan-price {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .price-amount {
            font-size: 3em;
            font-weight: bold;
            color: #667eea;
        }
        
        .price-period {
            color: #666;
            font-size: 1.1em;
        }
        
        .plan-description {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            min-height: 50px;
        }
        
        .features-list {
            list-style: none;
            margin-bottom: 30px;
        }
        
        .features-list li {
            padding: 12px 0;
            border-bottom: 1px solid #f0f0f0;
            color: #444;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .features-list li:last-child {
            border-bottom: none;
        }
        
        .feature-icon {
            font-size: 1.2em;
            min-width: 25px;
        }
        
        .feature-icon.check {
            color: #28a745;
        }
        
        .feature-icon.cross {
            color: #dc3545;
        }
        
        .subscribe-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .subscribe-btn:hover {
            background: linear-gradient(135deg, #764ba2, #667eea);
            transform: scale(1.05);
        }
        
        .subscribe-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .current-plan-badge {
            background: #28a745;
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .comparison-table {
            background: white;
            border-radius: 20px;
            padding: 40px;
            margin-top: 50px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .comparison-table h2 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2em;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th, td {
            padding: 15px;
            text-align: center;
            border-bottom: 1px solid #f0f0f0;
        }
        
        th {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            font-weight: bold;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .back-btn {
            display: inline-block;
            margin-bottom: 30px;
            padding: 10px 20px;
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            transition: all 0.3s;
        }
        
        .back-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        
        @media (max-width: 768px) {
            .plans-grid {
                grid-template-columns: 1fr;
            }
            
            .plan-card.featured {
                transform: scale(1);
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            table {
                font-size: 0.9em;
            }
            
            th, td {
                padding: 10px 5px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/dashboard" class="back-btn">← العودة للوحة التحكم</a>
        
        <div class="header">
            <h1>🎯 اختر الباقة المناسبة لك</h1>
            <p>جميع الباقات شهرية - يتم التجديد تلقائياً</p>
        </div>
        
        <div class="plans-grid">
            <!-- باقة مجانية -->
            <div class="plan-card">
                <div class="plan-icon">🆓</div>
                <h2 class="plan-name">باقة مجانية</h2>
                <div class="plan-price">
                    <div class="price-amount">$0</div>
                    <div class="price-period">/ شهرياً</div>
                </div>
                <p class="plan-description">مثالية للمبتدئين والتجربة</p>
                
                <ul class="features-list">
                    <li><span class="feature-icon check">✅</span> 3 صفقات يومياً</li>
                    <li><span class="feature-icon check">✅</span> 2 صفقة مفتوحة</li>
                    <li><span class="feature-icon check">✅</span> $500 لكل صفقة</li>
                    <li><span class="feature-icon check">✅</span> مؤشران فنيان</li>
                    <li><span class="feature-icon check">✅</span> 5 تحليلات يومياً</li>
                    <li><span class="feature-icon cross">❌</span> إشعارات واتساب</li>
                    <li><span class="feature-icon cross">❌</span> تداول تلقائي</li>
                    <li><span class="feature-icon cross">❌</span> رسوم متقدمة</li>
                </ul>
                
                <button class="subscribe-btn" onclick="subscribePlan('free')" id="btn-free">
                    البدء مجاناً
                </button>
            </div>
            
            <!-- باقة فضية -->
            <div class="plan-card featured">
                <div class="plan-badge">الأكثر شيوعاً</div>
                <div class="plan-icon">💎</div>
                <h2 class="plan-name">باقة فضية</h2>
                <div class="plan-price">
                    <div class="price-amount">$250</div>
                    <div class="price-period">/ شهرياً</div>
                </div>
                <p class="plan-description">للمتداولين الجادين والمحترفين</p>
                
                <ul class="features-list">
                    <li><span class="feature-icon check">✅</span> 15 صفقة يومياً</li>
                    <li><span class="feature-icon check">✅</span> 5 صفقات مفتوحة</li>
                    <li><span class="feature-icon check">✅</span> $5,000 لكل صفقة</li>
                    <li><span class="feature-icon check">✅</span> 5 مؤشرات فنية</li>
                    <li><span class="feature-icon check">✅</span> 50 تحليل يومياً</li>
                    <li><span class="feature-icon check">✅</span> إشعارات واتساب</li>
                    <li><span class="feature-icon check">✅</span> تداول تلقائي</li>
                    <li><span class="feature-icon check">✅</span> رسوم متقدمة</li>
                </ul>
                
                <button class="subscribe-btn" onclick="subscribePlan('silver')" id="btn-silver">
                    الاشتراك الآن
                </button>
            </div>
            
            <!-- باقة ذهبية -->
            <div class="plan-card">
                <div class="plan-badge">VIP</div>
                <div class="plan-icon">👑</div>
                <h2 class="plan-name">باقة ذهبية</h2>
                <div class="plan-price">
                    <div class="price-amount">$500</div>
                    <div class="price-period">/ شهرياً</div>
                </div>
                <p class="plan-description">جميع المميزات بلا حدود</p>
                
                <ul class="features-list">
                    <li><span class="feature-icon check">✅</span> صفقات غير محدودة</li>
                    <li><span class="feature-icon check">✅</span> 20 صفقة مفتوحة</li>
                    <li><span class="feature-icon check">✅</span> $50,000 لكل صفقة</li>
                    <li><span class="feature-icon check">✅</span> جميع المؤشرات</li>
                    <li><span class="feature-icon check">✅</span> تحليلات غير محدودة</li>
                    <li><span class="feature-icon check">✅</span> إشعارات واتساب</li>
                    <li><span class="feature-icon check">✅</span> تداول تلقائي</li>
                    <li><span class="feature-icon check">✅</span> توقعات AI</li>
                    <li><span class="feature-icon check">✅</span> دعم VIP</li>
                </ul>
                
                <button class="subscribe-btn" onclick="subscribePlan('gold')" id="btn-gold">
                    الاشتراك VIP
                </button>
            </div>
        </div>
        
        <!-- جدول المقارنة -->
        <div class="comparison-table">
            <h2>📊 مقارنة تفصيلية بين الباقات</h2>
            <table>
                <thead>
                    <tr>
                        <th>الميزة</th>
                        <th>🆓 مجانية</th>
                        <th>💎 فضية</th>
                        <th>👑 ذهبية</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>السعر الشهري</strong></td>
                        <td>مجاناً</td>
                        <td>$250</td>
                        <td>$500</td>
                    </tr>
                    <tr>
                        <td>الصفقات اليومية</td>
                        <td>3</td>
                        <td>15</td>
                        <td>غير محدود</td>
                    </tr>
                    <tr>
                        <td>الصفقات المفتوحة</td>
                        <td>2</td>
                        <td>5</td>
                        <td>20</td>
                    </tr>
                    <tr>
                        <td>رأس المال لكل صفقة</td>
                        <td>$500</td>
                        <td>$5,000</td>
                        <td>$50,000</td>
                    </tr>
                    <tr>
                        <td>المؤشرات الفنية</td>
                        <td>RSI, SMA</td>
                        <td>5 مؤشرات</td>
                        <td>جميع المؤشرات</td>
                    </tr>
                    <tr>
                        <td>التحليلات اليومية</td>
                        <td>5</td>
                        <td>50</td>
                        <td>غير محدود</td>
                    </tr>
                    <tr>
                        <td>إشعارات واتساب</td>
                        <td>❌</td>
                        <td>✅</td>
                        <td>✅</td>
                    </tr>
                    <tr>
                        <td>التداول التلقائي</td>
                        <td>❌</td>
                        <td>✅</td>
                        <td>✅</td>
                    </tr>
                    <tr>
                        <td>الرسوم البيانية المتقدمة</td>
                        <td>❌</td>
                        <td>✅</td>
                        <td>✅</td>
                    </tr>
                    <tr>
                        <td>توقعات AI</td>
                        <td>❌</td>
                        <td>❌</td>
                        <td>✅</td>
                    </tr>
                    <tr>
                        <td>استراتيجيات مخصصة</td>
                        <td>❌</td>
                        <td>❌</td>
                        <td>✅</td>
                    </tr>
                    <tr>
                        <td>الدعم الفني</td>
                        <td>أساسي</td>
                        <td>أولوية</td>
                        <td>VIP</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    
    <script>
        // عرض الباقة الحالية
        window.onload = async function() {
            try {
                const response = await fetch('/api/subscription/current');
                const data = await response.json();
                
                if (data.success && data.subscription) {
                    const currentPlan = data.subscription.plan_type;
                    
                    // تعطيل زر الباقة الحالية
                    const currentBtn = document.getElementById('btn-' + currentPlan);
                    if (currentBtn) {
                        currentBtn.disabled = true;
                        currentBtn.textContent = 'الباقة الحالية ✓';
                        currentBtn.style.background = '#28a745';
                    }
                    
                    // إضافة شارة للباقة الحالية
                    const currentCard = currentBtn.closest('.plan-card');
                    if (currentCard && !currentCard.querySelector('.current-plan-badge')) {
                        const badge = document.createElement('div');
                        badge.className = 'current-plan-badge';
                        badge.textContent = '✓ باقتك الحالية';
                        currentCard.appendChild(badge);
                    }
                }
            } catch (error) {
                console.error('خطأ في تحميل الباقة الحالية:', error);
            }
        };
        
        async function subscribePlan(planType) {
            if (!confirm(`هل أنت متأكد من الاشتراك في الباقة ${getPlanName(planType)}؟`)) {
                return;
            }
            
            try {
                const response = await fetch('/api/subscription/subscribe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        plan_type: planType,
                        payment_method: 'card'
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert('✅ ' + data.message);
                    window.location.reload();
                } else {
                    alert('❌ ' + data.message);
                }
            } catch (error) {
                alert('خطأ في الاشتراك: ' + error.message);
            }
        }
        
        function getPlanName(planType) {
            const names = {
                'free': 'المجانية',
                'silver': 'الفضية',
                'gold': 'الذهبية'
            };
            return names[planType] || planType;
        }
    </script>
</body>
</html>
"""

SUBSCRIPTION_STATUS_PAGE = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>حالة الاشتراك</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .status-card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .status-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .plan-icon-large {
            font-size: 5em;
            margin-bottom: 20px;
        }
        
        .plan-name-large {
            font-size: 2.5em;
            color: #333;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .status-badge {
            display: inline-block;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        
        .status-badge.active {
            background: #28a745;
            color: white;
        }
        
        .status-badge.expired {
            background: #dc3545;
            color: white;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .info-item {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .info-label {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        
        .info-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }
        
        .features-section {
            margin: 30px 0;
        }
        
        .features-section h3 {
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        
        .feature-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .feature-icon {
            font-size: 1.5em;
        }
        
        .buttons-section {
            margin-top: 30px;
            text-align: center;
        }
        
        .btn {
            display: inline-block;
            padding: 15px 30px;
            margin: 10px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            font-size: 1em;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .btn-primary:hover {
            transform: scale(1.05);
        }
        
        .btn-secondary {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }
        
        .btn-secondary:hover {
            background: #667eea;
            color: white;
        }
        
        .warning-box {
            background: #fff3cd;
            border-right: 5px solid #ffc107;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .warning-box h4 {
            color: #856404;
            margin-bottom: 10px;
        }
        
        .warning-box p {
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="status-card">
            <div class="status-header">
                <div class="plan-icon-large" id="planIcon">💎</div>
                <h1 class="plan-name-large" id="planName">جاري التحميل...</h1>
                <span class="status-badge active" id="statusBadge">نشط</span>
            </div>
            
            <div class="info-grid" id="infoGrid">
                <!-- يتم ملؤها بالجافاسكريبت -->
            </div>
            
            <div class="features-section">
                <h3>🎁 مميزات باقتك</h3>
                <div class="features-grid" id="featuresGrid">
                    <!-- يتم ملؤها بالجافاسكريبت -->
                </div>
            </div>
            
            <div id="warningSection"></div>
            
            <div class="buttons-section">
                <a href="/plans" class="btn btn-primary">ترقية الباقة</a>
                <a href="/dashboard" class="btn btn-secondary">العودة للوحة التحكم</a>
            </div>
        </div>
    </div>
    
    <script>
        window.onload = async function() {
            try {
                const response = await fetch('/api/subscription/current');
                const data = await response.json();
                
                if (data.success && data.subscription) {
                    displaySubscription(data.subscription);
                } else {
                    alert('خطأ في تحميل بيانات الاشتراك');
                }
            } catch (error) {
                alert('خطأ: ' + error.message);
            }
        };
        
        function displaySubscription(sub) {
            // الأيقونة والاسم
            const icons = {
                'free': '🆓',
                'silver': '💎',
                'gold': '👑'
            };
            document.getElementById('planIcon').textContent = icons[sub.plan_type] || '📦';
            document.getElementById('planName').textContent = sub.plan_name;
            
            // الحالة
            const statusBadge = document.getElementById('statusBadge');
            if (sub.status === 'active') {
                statusBadge.textContent = 'نشط ✓';
                statusBadge.className = 'status-badge active';
            } else {
                statusBadge.textContent = 'منتهي';
                statusBadge.className = 'status-badge expired';
            }
            
            // المعلومات
            const infoGrid = document.getElementById('infoGrid');
            infoGrid.innerHTML = '';
            
            if (sub.start_date) {
                infoGrid.innerHTML += `
                    <div class="info-item">
                        <div class="info-label">تاريخ البدء</div>
                        <div class="info-value">${new Date(sub.start_date).toLocaleDateString('ar-SA')}</div>
                    </div>
                `;
            }
            
            if (sub.end_date) {
                infoGrid.innerHTML += `
                    <div class="info-item">
                        <div class="info-label">تاريخ الانتهاء</div>
                        <div class="info-value">${new Date(sub.end_date).toLocaleDateString('ar-SA')}</div>
                    </div>
                `;
            }
            
            if (sub.days_remaining !== undefined) {
                infoGrid.innerHTML += `
                    <div class="info-item">
                        <div class="info-label">الأيام المتبقية</div>
                        <div class="info-value">${sub.days_remaining} يوم</div>
                    </div>
                `;
                
                // تحذير إذا كانت الأيام أقل من 7
                if (sub.days_remaining < 7 && sub.days_remaining > 0) {
                    document.getElementById('warningSection').innerHTML = `
                        <div class="warning-box">
                            <h4>⚠️ تنبيه: اشتراكك على وشك الانتهاء</h4>
                            <p>باقتك ستنتهي خلال ${sub.days_remaining} أيام. قم بالتجديد لتجنب انقطاع الخدمة.</p>
                        </div>
                    `;
                }
            }
            
            // المميزات
            const featuresGrid = document.getElementById('featuresGrid');
            featuresGrid.innerHTML = '';
            
            if (sub.features) {
                const features = sub.features;
                
                featuresGrid.innerHTML += `
                    <div class="feature-box">
                        <span class="feature-icon">📊</span>
                        <span>الصفقات اليومية: ${features.max_trades_per_day >= 999 ? 'غير محدود' : features.max_trades_per_day}</span>
                    </div>
                    <div class="feature-box">
                        <span class="feature-icon">📈</span>
                        <span>الصفقات المفتوحة: ${features.max_active_positions}</span>
                    </div>
                    <div class="feature-box">
                        <span class="feature-icon">💰</span>
                        <span>رأس المال: $${features.max_capital_per_trade.toLocaleString()}</span>
                    </div>
                    <div class="feature-box">
                        <span class="feature-icon">${features.whatsapp_notifications ? '✅' : '❌'}</span>
                        <span>إشعارات واتساب</span>
                    </div>
                    <div class="feature-box">
                        <span class="feature-icon">${features.auto_trading ? '✅' : '❌'}</span>
                        <span>تداول تلقائي</span>
                    </div>
                    <div class="feature-box">
                        <span class="feature-icon">${features.advanced_charts ? '✅' : '❌'}</span>
                        <span>رسوم متقدمة</span>
                    </div>
                `;
            }
        }
    </script>
</body>
</html>
"""
