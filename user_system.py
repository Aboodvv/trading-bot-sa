"""
نظام المستخدمين وقاعدة البيانات
User Management & Database System
"""

import sqlite3
import hashlib
import secrets
from datetime import datetime
import json

class UserDatabase:
    """إدارة قاعدة بيانات المستخدمين"""
    
    def __init__(self, db_path='trading_bot.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """إنشاء جداول قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                phone TEXT,
                whatsapp_number TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                balance REAL DEFAULT 10000,
                initial_capital REAL DEFAULT 10000,
                whatsapp_notifications BOOLEAN DEFAULT 1
            )
        ''')
        
        # جدول الجلسات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # جدول المعاملات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # جدول الصفقات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                symbol TEXT NOT NULL,
                action TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                entry_price REAL NOT NULL,
                exit_price REAL,
                profit_loss REAL,
                status TEXT DEFAULT 'open',
                opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                closed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    
    def hash_password(self, password):
        """تشفير كلمة المرور"""
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${pwd_hash.hex()}"
    
    def verify_password(self, password, password_hash):
        """التحقق من كلمة المرور"""
        try:
            salt, pwd_hash = password_hash.split('$')
            new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return new_hash.hex() == pwd_hash
        except:
            return False
    
    def create_user(self, username, email, password, full_name='', phone='', whatsapp_number=''):
        """إنشاء مستخدم جديد"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, phone, whatsapp_number)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, full_name, phone, whatsapp_number))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return {'success': True, 'user_id': user_id, 'message': 'تم إنشاء الحساب بنجاح'}
        except sqlite3.IntegrityError as e:
            conn.close()
            if 'username' in str(e):
                return {'success': False, 'message': 'اسم المستخدم موجود مسبقاً'}
            elif 'email' in str(e):
                return {'success': False, 'message': 'البريد الإلكتروني موجود مسبقاً'}
            else:
                return {'success': False, 'message': 'خطأ في إنشاء الحساب'}
    
    def login_user(self, username, password):
        """تسجيل دخول المستخدم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, password_hash, is_active, full_name, email FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return {'success': False, 'message': 'اسم المستخدم أو كلمة المرور غير صحيحة'}
        
        user_id, password_hash, is_active, full_name, email = user
        
        if not is_active:
            conn.close()
            return {'success': False, 'message': 'الحساب معطل'}
        
        if not self.verify_password(password, password_hash):
            conn.close()
            return {'success': False, 'message': 'اسم المستخدم أو كلمة المرور غير صحيحة'}
        
        # إنشاء session token
        session_token = secrets.token_urlsafe(32)
        cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', (datetime.now(), user_id))
        cursor.execute('''
            INSERT INTO sessions (user_id, session_token, expires_at)
            VALUES (?, ?, datetime('now', '+7 days'))
        ''', (user_id, session_token))
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'session_token': session_token,
            'user_id': user_id,
            'username': username,
            'full_name': full_name,
            'email': email,
            'message': 'تم تسجيل الدخول بنجاح'
        }
    
    def verify_session(self, session_token):
        """التحقق من صلاحية الجلسة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.user_id, u.username, u.full_name, u.email, u.balance, u.whatsapp_number
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.session_token = ? AND s.expires_at > datetime('now')
        ''', (session_token,))
        
        session = cursor.fetchone()
        conn.close()
        
        if session:
            return {
                'valid': True,
                'user_id': session[0],
                'username': session[1],
                'full_name': session[2],
                'email': session[3],
                'balance': session[4],
                'whatsapp_number': session[5]
            }
        return {'valid': False}
    
    def logout_user(self, session_token):
        """تسجيل خروج المستخدم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE session_token = ?', (session_token,))
        conn.commit()
        conn.close()
        return {'success': True, 'message': 'تم تسجيل الخروج'}
    
    def get_user_info(self, user_id):
        """الحصول على معلومات المستخدم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT username, email, full_name, phone, whatsapp_number, 
                   balance, initial_capital, created_at, whatsapp_notifications
            FROM users WHERE id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'username': user[0],
                'email': user[1],
                'full_name': user[2],
                'phone': user[3],
                'whatsapp_number': user[4],
                'balance': user[5],
                'initial_capital': user[6],
                'created_at': user[7],
                'whatsapp_notifications': user[8]
            }
        return None
    
    def update_balance(self, user_id, new_balance):
        """تحديث رصيد المستخدم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
        conn.commit()
        conn.close()
    
    def add_transaction(self, user_id, transaction_type, amount, description=''):
        """إضافة معاملة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (user_id, transaction_type, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (user_id, transaction_type, amount, description))
        conn.commit()
        conn.close()
    
    def record_trade(self, user_id, symbol, action, quantity, entry_price):
        """تسجيل صفقة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO trades (user_id, symbol, action, quantity, entry_price)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, symbol, action, quantity, entry_price))
        trade_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return trade_id
    
    def close_trade(self, trade_id, exit_price):
        """إغلاق صفقة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT quantity, entry_price FROM trades WHERE id = ?', (trade_id,))
        trade = cursor.fetchone()
        
        if trade:
            quantity, entry_price = trade
            profit_loss = (exit_price - entry_price) * quantity
            
            cursor.execute('''
                UPDATE trades 
                SET exit_price = ?, profit_loss = ?, status = 'closed', closed_at = ?
                WHERE id = ?
            ''', (exit_price, profit_loss, datetime.now(), trade_id))
            
            conn.commit()
            conn.close()
            return profit_loss
        
        conn.close()
        return 0
    
    def get_user_trades(self, user_id, limit=10):
        """الحصول على صفقات المستخدم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, symbol, action, quantity, entry_price, exit_price, 
                   profit_loss, status, opened_at, closed_at
            FROM trades 
            WHERE user_id = ?
            ORDER BY opened_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        trades = cursor.fetchall()
        conn.close()
        
        return [{
            'id': t[0],
            'symbol': t[1],
            'action': t[2],
            'quantity': t[3],
            'entry_price': t[4],
            'exit_price': t[5],
            'profit_loss': t[6],
            'status': t[7],
            'opened_at': t[8],
            'closed_at': t[9]
        } for t in trades]

# إنشاء instance عام
user_db = UserDatabase()
