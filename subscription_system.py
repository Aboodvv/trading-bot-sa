"""
نظام الباقات والاشتراكات
Subscription & Plans System
"""

from datetime import datetime, timedelta
import sqlite3
from enum import Enum

class SubscriptionPlan(Enum):
    """أنواع الباقات"""
    FREE = "free"
    SILVER = "silver"
    GOLD = "gold"

class SubscriptionManager:
    """إدارة الاشتراكات والباقات"""
    
    # تعريف الباقات ومميزاتها
    PLANS = {
        'free': {
            'name': 'باقة مجانية',
            'name_en': 'Free Plan',
            'price': 0,
            'duration_days': 30,
            'features': {
                'max_trades_per_day': 3,              # 3 صفقات يومياً
                'max_active_positions': 2,            # 2 صفقة مفتوحة
                'max_capital_per_trade': 500,         # $500 لكل صفقة
                'whatsapp_notifications': False,      # بدون إشعارات واتساب
                'auto_trading': False,                # بدون تداول تلقائي
                'technical_indicators': ['RSI', 'SMA'],  # 2 مؤشرات فقط
                'daily_analysis_limit': 5,            # 5 تحليلات يومياً
                'support_level': 'basic',             # دعم أساسي
                'advanced_charts': False,             # بدون رسوم بيانية متقدمة
            },
            'description': 'باقة مجانية للمبتدئين مع مميزات محدودة'
        },
        'silver': {
            'name': 'باقة فضية',
            'name_en': 'Silver Plan',
            'price': 250,
            'duration_days': 30,
            'features': {
                'max_trades_per_day': 15,             # 15 صفقة يومياً
                'max_active_positions': 5,            # 5 صفقات مفتوحة
                'max_capital_per_trade': 5000,        # $5,000 لكل صفقة
                'whatsapp_notifications': True,       # إشعارات واتساب ✅
                'auto_trading': True,                 # تداول تلقائي ✅
                'technical_indicators': ['RSI', 'MACD', 'SMA', 'EMA', 'Bollinger'],
                'daily_analysis_limit': 50,           # 50 تحليل يومياً
                'support_level': 'priority',          # دعم أولوية
                'advanced_charts': True,              # رسوم بيانية متقدمة ✅
            },
            'description': 'باقة احترافية للمتداولين الجادين'
        },
        'gold': {
            'name': 'باقة ذهبية',
            'name_en': 'Gold Plan',
            'price': 500,
            'duration_days': 30,
            'features': {
                'max_trades_per_day': 999,            # غير محدود
                'max_active_positions': 20,           # 20 صفقة مفتوحة
                'max_capital_per_trade': 50000,       # $50,000 لكل صفقة
                'whatsapp_notifications': True,       # إشعارات واتساب ✅
                'auto_trading': True,                 # تداول تلقائي ✅
                'technical_indicators': 'all',        # جميع المؤشرات ✅
                'daily_analysis_limit': 999,          # غير محدود
                'support_level': 'vip',               # دعم VIP
                'advanced_charts': True,              # رسوم بيانية متقدمة ✅
                'ai_predictions': True,               # توقعات AI ✅
                'custom_strategies': True,            # استراتيجيات مخصصة ✅
            },
            'description': 'باقة VIP مع جميع المميزات'
        }
    }
    
    def __init__(self, db_path='trading_bot.db'):
        self.db_path = db_path
        self.init_subscription_tables()
    
    def init_subscription_tables(self):
        """إنشاء جداول الاشتراكات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول الاشتراكات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan_type TEXT NOT NULL,
                start_date TIMESTAMP NOT NULL,
                end_date TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'active',
                auto_renew BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # جدول الدفعات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscription_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                subscription_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT,
                payment_status TEXT DEFAULT 'pending',
                transaction_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (subscription_id) REFERENCES subscriptions(id)
            )
        ''')
        
        # جدول استخدام المميزات (لتتبع الحدود اليومية)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feature_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                feature_name TEXT NOT NULL,
                usage_count INTEGER DEFAULT 0,
                usage_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, feature_name, usage_date)
            )
        ''')
        
        # إضافة عمود plan_type لجدول users إذا لم يكن موجوداً
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN plan_type TEXT DEFAULT "free"')
        except:
            pass  # العمود موجود مسبقاً
        
        conn.commit()
        conn.close()
        print("Subscription tables initialized")
    
    def create_subscription(self, user_id, plan_type, payment_method=None, transaction_id=None):
        """إنشاء اشتراك جديد"""
        if plan_type not in self.PLANS:
            return {'success': False, 'message': 'نوع الباقة غير صحيح'}
        
        plan = self.PLANS[plan_type]
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # حساب تواريخ الاشتراك
            start_date = datetime.now()
            end_date = start_date + timedelta(days=plan['duration_days'])
            
            # إلغاء الاشتراكات السابقة
            cursor.execute('''
                UPDATE subscriptions 
                SET status = 'cancelled'
                WHERE user_id = ? AND status = 'active'
            ''', (user_id,))
            
            # إنشاء اشتراك جديد
            cursor.execute('''
                INSERT INTO subscriptions (user_id, plan_type, start_date, end_date, status)
                VALUES (?, ?, ?, ?, 'active')
            ''', (user_id, plan_type, start_date, end_date))
            
            subscription_id = cursor.lastrowid
            
            # تحديث نوع الباقة في جدول المستخدمين
            cursor.execute('UPDATE users SET plan_type = ? WHERE id = ?', (plan_type, user_id))
            
            # تسجيل الدفعة (إذا لم تكن باقة مجانية)
            if plan['price'] > 0:
                cursor.execute('''
                    INSERT INTO subscription_payments 
                    (user_id, subscription_id, amount, payment_method, payment_status, transaction_id)
                    VALUES (?, ?, ?, ?, 'completed', ?)
                ''', (user_id, subscription_id, plan['price'], payment_method, transaction_id))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'message': f'تم الاشتراك في {plan["name"]} بنجاح',
                'subscription_id': subscription_id,
                'end_date': end_date.strftime('%Y-%m-%d')
            }
        except Exception as e:
            conn.close()
            return {'success': False, 'message': f'خطأ: {str(e)}'}
    
    def get_user_subscription(self, user_id):
        """الحصول على اشتراك المستخدم الحالي"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT plan_type, start_date, end_date, status
            FROM subscriptions
            WHERE user_id = ? AND status = 'active'
            ORDER BY created_at DESC
            LIMIT 1
        ''', (user_id,))
        
        subscription = cursor.fetchone()
        conn.close()
        
        if subscription:
            plan_type, start_date, end_date, status = subscription
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S.%f')
            
            # التحقق من انتهاء الاشتراك
            if datetime.now() > end_date_obj:
                self.expire_subscription(user_id)
                return self.get_default_subscription()
            
            return {
                'plan_type': plan_type,
                'plan_name': self.PLANS[plan_type]['name'],
                'start_date': start_date,
                'end_date': end_date,
                'status': status,
                'days_remaining': (end_date_obj - datetime.now()).days,
                'features': self.PLANS[plan_type]['features']
            }
        else:
            return self.get_default_subscription()
    
    def get_default_subscription(self):
        """الاشتراك الافتراضي (مجاني)"""
        return {
            'plan_type': 'free',
            'plan_name': self.PLANS['free']['name'],
            'status': 'active',
            'features': self.PLANS['free']['features']
        }
    
    def expire_subscription(self, user_id):
        """إنهاء اشتراك منتهي"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE subscriptions 
            SET status = 'expired'
            WHERE user_id = ? AND status = 'active' AND end_date < datetime('now')
        ''', (user_id,))
        
        # إرجاع المستخدم للباقة المجانية
        cursor.execute('UPDATE users SET plan_type = "free" WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
    
    def check_feature_limit(self, user_id, feature_name):
        """التحقق من حد استخدام ميزة معينة"""
        subscription = self.get_user_subscription(user_id)
        features = subscription['features']
        
        # الحصول على الحد الأقصى
        limit_key = f'{feature_name}_limit'
        if limit_key not in features:
            return {'allowed': True, 'remaining': 999}
        
        max_limit = features[limit_key]
        
        # الحصول على الاستخدام اليوم
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().date()
        cursor.execute('''
            SELECT usage_count FROM feature_usage
            WHERE user_id = ? AND feature_name = ? AND usage_date = ?
        ''', (user_id, feature_name, today))
        
        result = cursor.fetchone()
        current_usage = result[0] if result else 0
        conn.close()
        
        if current_usage >= max_limit:
            return {
                'allowed': False,
                'remaining': 0,
                'message': f'وصلت للحد الأقصى ({max_limit}) لهذه الميزة اليوم'
            }
        
        return {
            'allowed': True,
            'remaining': max_limit - current_usage
        }
    
    def increment_feature_usage(self, user_id, feature_name):
        """زيادة عداد استخدام ميزة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().date()
        
        cursor.execute('''
            INSERT INTO feature_usage (user_id, feature_name, usage_count, usage_date)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(user_id, feature_name, usage_date)
            DO UPDATE SET usage_count = usage_count + 1
        ''', (user_id, feature_name, today))
        
        conn.commit()
        conn.close()
    
    def can_trade(self, user_id):
        """التحقق من إمكانية فتح صفقة جديدة"""
        subscription = self.get_user_subscription(user_id)
        
        # التحقق من الحد اليومي
        daily_check = self.check_feature_limit(user_id, 'daily_trades')
        if not daily_check['allowed']:
            return {
                'can_trade': False,
                'reason': 'وصلت للحد الأقصى من الصفقات اليومية',
                'upgrade_suggestion': 'ترقية الباقة للحصول على صفقات أكثر'
            }
        
        # التحقق من عدد الصفقات المفتوحة
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM trades 
            WHERE user_id = ? AND status = 'open'
        ''', (user_id,))
        open_positions = cursor.fetchone()[0]
        conn.close()
        
        max_positions = subscription['features']['max_active_positions']
        
        if open_positions >= max_positions:
            return {
                'can_trade': False,
                'reason': f'وصلت للحد الأقصى من الصفقات المفتوحة ({max_positions})',
                'upgrade_suggestion': 'ترقية الباقة لفتح صفقات أكثر'
            }
        
        return {'can_trade': True}
    
    def get_all_plans(self):
        """الحصول على جميع الباقات"""
        return self.PLANS
    
    def get_plan_comparison(self):
        """جدول مقارنة الباقات"""
        comparison = {
            'features': [
                {'name': 'الصفقات اليومية', 'key': 'max_trades_per_day'},
                {'name': 'الصفقات المفتوحة', 'key': 'max_active_positions'},
                {'name': 'رأس المال لكل صفقة', 'key': 'max_capital_per_trade'},
                {'name': 'إشعارات واتساب', 'key': 'whatsapp_notifications'},
                {'name': 'تداول تلقائي', 'key': 'auto_trading'},
                {'name': 'التحليلات اليومية', 'key': 'daily_analysis_limit'},
                {'name': 'الدعم الفني', 'key': 'support_level'},
                {'name': 'رسوم بيانية متقدمة', 'key': 'advanced_charts'},
            ],
            'plans': {}
        }
        
        for plan_id, plan_data in self.PLANS.items():
            comparison['plans'][plan_id] = {
                'name': plan_data['name'],
                'price': plan_data['price'],
                'features': {}
            }
            
            for feature in comparison['features']:
                key = feature['key']
                value = plan_data['features'].get(key, '-')
                
                # تنسيق القيمة
                if isinstance(value, bool):
                    value = '✅' if value else '❌'
                elif isinstance(value, int) and value >= 999:
                    value = 'غير محدود'
                elif key == 'max_capital_per_trade':
                    value = f'${value:,}'
                
                comparison['plans'][plan_id]['features'][key] = value
        
        return comparison

# إنشاء instance عام
subscription_manager = SubscriptionManager()
