"""
واجهة ويب تفاعلية للبوت - يشتري ويبيع تلقائياً
"""

from flask import Flask, render_template_string, jsonify, request, session, redirect, url_for
from technical_analysis import TechnicalAnalyzer, analyze_stock
from trading_strategy import CompositeStrategy
from risk_management import RiskManager
from payment_system import payment_processor, security_manager
from user_system import user_db
from whatsapp_notifications import whatsapp_notifier
from subscription_system import subscription_manager
import config
from datetime import datetime
import threading
import webbrowser
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # للجلسات الآمنة

# متغير عام للبوت
trading_bot = None
auto_trading_active = False

# نظام المستخدمين البسيط (في الواقع يجب استخدام قاعدة بيانات)
users_wallets = {
    'default_user': {
        'balance': 10000,
        'initial_capital': 10000
    }
}

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="بوت التداول">
    <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect fill='%23667eea' width='100' height='100'/><text y='70' x='50' text-anchor='middle' font-size='60' fill='white'>📈</text></svg>">
    <meta name="theme-color" content="#667eea">
    <title>🤖 بوت التداول الآلي</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            direction: rtl;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .controls {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.1em;
            border-radius: 10px;
            cursor: pointer;
            transition: transform 0.2s;
            font-weight: bold;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            font-size: 1.2em;
            color: #667eea;
        }
        
        .results {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .stock-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }
        
        .stock-card:hover {
            transform: translateY(-5px);
        }
        
        .stock-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .stock-symbol {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stock-price {
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }
        
        .stock-info {
            margin: 10px 0;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .stock-info strong {
            color: #667eea;
        }
        
        .recommendation {
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            font-size: 1.2em;
            margin-top: 15px;
        }
        
        .recommendation.buy {
            background: #d4edda;
            color: #155724;
            border: 2px solid #c3e6cb;
        }
        
        .recommendation.sell {
            background: #f8d7da;
            color: #721c24;
            border: 2px solid #f5c6cb;
        }
        
        .recommendation.hold {
            background: #fff3cd;
            color: #856404;
            border: 2px solid #ffeaa7;
        }
        
        .signals {
            margin-top: 15px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .signals h4 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .signal-item {
            padding: 8px;
            margin: 5px 0;
            background: white;
            border-radius: 5px;
            font-size: 0.9em;
        }
        
        .best-opportunity {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-top: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .best-opportunity h2 {
            font-size: 2em;
            margin-bottom: 20px;
        }
        
        .risk-info {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        
        .risk-info div {
            margin: 10px 0;
            font-size: 1.1em;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        .footer {
            text-align: center;
            color: white;
            margin-top: 30px;
            padding: 20px;
        }
        
        .auto-trading-controls {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .status-badge {
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: bold;
        }
        
        .status-active {
            background: #d4edda;
            color: #155724;
        }
        
        .status-inactive {
            background: #f8d7da;
            color: #721c24;
        }
        
        .btn-success {
            background: #28a745;
        }
        
        .btn-danger {
            background: #dc3545;
        }
        
        .portfolio-summary {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .portfolio-stat {
            display: inline-block;
            margin: 10px 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .portfolio-stat strong {
            color: #667eea;
            font-size: 1.2em;
        }
        
        @keyframes slideDown {
            from {
                transform: translate(-50%, -100px);
                opacity: 0;
            }
            to {
                transform: translate(-50%, 0);
                opacity: 1;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 بوت التداول الآلي الاحترافي</h1>
            <p>تحليل ذكي للأسهم مع إشارات تداول احترافية</p>
            <div style="margin-top: 15px; display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                <a href="/subscription" style="padding: 10px 20px; background: rgba(255,255,255,0.2); color: white; text-decoration: none; border-radius: 8px; font-weight: bold; transition: all 0.3s;">
                    📊 اشتراكي
                </a>
                <a href="/plans" style="padding: 10px 20px; background: linear-gradient(135deg, #FFD700, #FFA500); color: white; text-decoration: none; border-radius: 8px; font-weight: bold; transition: all 0.3s; box-shadow: 0 3px 10px rgba(255,215,0,0.3);">
                    ⬆️ ترقية الباقة
                </a>
                <button onclick="logout()" style="padding: 10px 20px; background: rgba(255,255,255,0.2); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">
                    🚪 تسجيل الخروج
                </button>
            </div>
        </div>
        
        <!-- Wallet Section -->
        <div class="portfolio-summary">
            <h3 style="color: #333; margin-bottom: 20px; text-align: center; font-size: 1.5em;">💰 المحفظة والرصيد</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                <!-- Current Balance -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; box-shadow: 0 5px 15px rgba(0,0,0,0.3);">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 5px;">الرصيد الحالي</div>
                        <div id="current-balance" style="font-size: 2.5em; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">$10,000</div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.3);">
                        <div style="text-align: center;">
                            <div style="font-size: 0.8em; opacity: 0.8;">رأس المال</div>
                            <div id="initial-capital" style="font-size: 1.2em; font-weight: bold;">$10,000</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 0.8em; opacity: 0.8;">الأرباح/الخسائر</div>
                            <div id="profit-loss" style="font-size: 1.2em; font-weight: bold;">$0</div>
                        </div>
                    </div>
                </div>
                
                <!-- Deposit Section -->
                <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
                    <h4 style="color: #667eea; margin-bottom: 20px; text-align: center;">� إيداع أموال آمن</h4>
                    
                    <!-- Payment Method Selection -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px;">
                        <button onclick="selectPaymentMethod('card')" id="btn-card" style="padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">
                            💳 بطاقة ائتمان
                        </button>
                        <button onclick="selectPaymentMethod('bank')" id="btn-bank" style="padding: 12px; background: #e0e0e0; color: #666; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">
                            🏦 تحويل بنكي
                        </button>
                    </div>
                    
                    <!-- Card Payment Form -->
                    <div id="card-payment-form" style="display: block;">
                        <div style="margin-bottom: 15px;">
                            <label style="display: block; color: #333; font-weight: bold; margin-bottom: 10px;">المبلغ (دولار)</label>
                            <input type="number" id="card-deposit-amount" value="1000" min="10" max="100000" step="100"
                                   style="width: 100%; padding: 12px; border: 2px solid #667eea; border-radius: 8px; font-size: 1.1em; text-align: center; font-weight: bold;">
                        </div>
                        <div style="margin-bottom: 15px;">
                            <label style="display: block; color: #333; font-weight: bold; margin-bottom: 10px;">رقم البطاقة</label>
                            <input type="text" id="card-number" placeholder="1234 5678 9012 3456" maxlength="19"
                                   style="width: 100%; padding: 12px; border: 2px solid #667eea; border-radius: 8px; font-size: 1.1em;">
                        </div>
                        <div style="margin-bottom: 15px;">
                            <label style="display: block; color: #333; font-weight: bold; margin-bottom: 10px;">اسم حامل البطاقة</label>
                            <input type="text" id="cardholder-name" placeholder="AHMED MOHAMMED"
                                   style="width: 100%; padding: 12px; border: 2px solid #667eea; border-radius: 8px; font-size: 1.1em; text-transform: uppercase;">
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                            <div>
                                <label style="display: block; color: #333; font-weight: bold; margin-bottom: 10px;">تاريخ الانتهاء</label>
                                <input type="text" id="card-expiry" placeholder="MM/YY" maxlength="5"
                                       style="width: 100%; padding: 12px; border: 2px solid #667eea; border-radius: 8px; font-size: 1.1em;">
                            </div>
                            <div>
                                <label style="display: block; color: #333; font-weight: bold; margin-bottom: 10px;">CVV</label>
                                <input type="password" id="card-cvv" placeholder="123" maxlength="4"
                                       style="width: 100%; padding: 12px; border: 2px solid #667eea; border-radius: 8px; font-size: 1.1em;">
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 15px;">
                            <button onclick="setCardAmount(500)" style="padding: 10px; background: #e3f2fd; border: 2px solid #2196f3; border-radius: 8px; cursor: pointer; font-weight: bold; color: #1976d2;">$500</button>
                            <button onclick="setCardAmount(1000)" style="padding: 10px; background: #e3f2fd; border: 2px solid #2196f3; border-radius: 8px; cursor: pointer; font-weight: bold; color: #1976d2;">$1,000</button>
                            <button onclick="setCardAmount(5000)" style="padding: 10px; background: #e3f2fd; border: 2px solid #2196f3; border-radius: 8px; cursor: pointer; font-weight: bold; color: #1976d2;">$5,000</button>
                        </div>
                        <button onclick="processCardPayment()" style="width: 100%; padding: 15px; background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%); color: white; border: none; border-radius: 10px; font-size: 1.1em; font-weight: bold; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.2); transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                            🔒 إيداع آمن الآن
                        </button>
                        <div style="margin-top: 10px; text-align: center; font-size: 0.85em; color: #666;">
                            🔐 محمي بتشفير SSL 256-bit | لن نحفظ بياناتك البنكية
                        </div>
                    </div>
                    
                    <!-- Bank Transfer Form -->
                    <div id="bank-payment-form" style="display: none;">
                        <div style="margin-bottom: 15px;">
                            <label style="display: block; color: #333; font-weight: bold; margin-bottom: 10px;">المبلغ (دولار)</label>
                            <input type="number" id="bank-deposit-amount" value="1000" min="10" max="100000" step="100"
                                   style="width: 100%; padding: 12px; border: 2px solid #667eea; border-radius: 8px; font-size: 1.1em; text-align: center; font-weight: bold;">
                        </div>
                        <div style="margin-bottom: 15px;">
                            <label style="display: block; color: #333; font-weight: bold; margin-bottom: 10px;">رقم الآيبان (IBAN)</label>
                            <input type="text" id="iban-number" placeholder="SA00 0000 0000 0000 0000 0000" maxlength="26"
                                   style="width: 100%; padding: 12px; border: 2px solid #667eea; border-radius: 8px; font-size: 1.1em; text-transform: uppercase;">
                        </div>
                        <div style="margin-bottom: 15px;">
                            <label style="display: block; color: #333; font-weight: bold; margin-bottom: 10px;">اسم صاحب الحساب</label>
                            <input type="text" id="account-name" placeholder="أحمد محمد"
                                   style="width: 100%; padding: 12px; border: 2px solid #667eea; border-radius: 8px; font-size: 1.1em;">
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 15px;">
                            <button onclick="setBankAmount(500)" style="padding: 10px; background: #e3f2fd; border: 2px solid #2196f3; border-radius: 8px; cursor: pointer; font-weight: bold; color: #1976d2;">$500</button>
                            <button onclick="setBankAmount(1000)" style="padding: 10px; background: #e3f2fd; border: 2px solid #2196f3; border-radius: 8px; cursor: pointer; font-weight: bold; color: #1976d2;">$1,000</button>
                            <button onclick="setBankAmount(5000)" style="padding: 10px; background: #e3f2fd; border: 2px solid #2196f3; border-radius: 8px; cursor: pointer; font-weight: bold; color: #1976d2;">$5,000</button>
                        </div>
                        <button onclick="processBankTransfer()" style="width: 100%; padding: 15px; background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%); color: white; border: none; border-radius: 10px; font-size: 1.1em; font-weight: bold; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.2); transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                            🏦 تحويل الآن
                        </button>
                        <div style="margin-top: 10px; text-align: center; font-size: 0.85em; color: #666;">
                            ⏱️ التحويل البنكي يستغرق 1-3 أيام عمل للتأكيد
                        </div>
                    </div>
                </div>
                
                <!-- Withdraw Section -->
                <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
                    <h4 style="color: #dc3545; margin-bottom: 20px; text-align: center;">💸 سحب أموال</h4>
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; color: #333; font-weight: bold; margin-bottom: 10px;">المبلغ (دولار)</label>
                        <input type="number" id="withdraw-amount" value="500" min="100" step="100"
                               style="width: 100%; padding: 15px; border: 2px solid #dc3545; border-radius: 10px; font-size: 1.2em; text-align: center; font-weight: bold;">
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 20px;">
                        <button onclick="setWithdrawAmount(200)" style="padding: 10px; background: #ffebee; border: 2px solid #f44336; border-radius: 8px; cursor: pointer; font-weight: bold; color: #c62828;">$200</button>
                        <button onclick="setWithdrawAmount(500)" style="padding: 10px; background: #ffebee; border: 2px solid #f44336; border-radius: 8px; cursor: pointer; font-weight: bold; color: #c62828;">$500</button>
                        <button onclick="setWithdrawAmount(1000)" style="padding: 10px; background: #ffebee; border: 2px solid #f44336; border-radius: 8px; cursor: pointer; font-weight: bold; color: #c62828;">$1,000</button>
                    </div>
                    <button onclick="withdrawMoney()" style="width: 100%; padding: 15px; background: linear-gradient(135deg, #f44336 0%, #e57373 100%); color: white; border: none; border-radius: 10px; font-size: 1.1em; font-weight: bold; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.2); transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                        💸 سحب الآن
                    </button>
                </div>
            </div>
            
            <!-- Transaction History -->
            <div style="margin-top: 25px; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
                <h4 style="color: #333; margin-bottom: 20px; text-align: center;">📜 سجل المعاملات</h4>
                <div id="transaction-history" style="max-height: 300px; overflow-y: auto;">
                    <div style="text-align: center; padding: 30px; color: #999;">
                        لا توجد معاملات بعد
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Auto Trading Controls -->
        <div class="auto-trading-controls">
            <div>
                <h3 style="margin: 0; color: #333;">التداول التلقائي</h3>
                <span class="status-badge status-inactive" id="status-badge">
                    <span id="status-text">متوقف ⭕</span>
                </span>
            </div>
            <button class="btn btn-success" id="toggle-trading" onclick="toggleAutoTrading()">
                <span id="toggle-text">🚀 تشغيل التداول التلقائي</span>
            </button>
        </div>
        
        <!-- Portfolio Summary -->
        <div class="portfolio-summary" id="portfolio-summary" style="display: none;">
            <h3 style="color: #333; margin-bottom: 15px;">📊 ملخص المحفظة</h3>
            <div id="portfolio-stats"></div>
            <div id="open-positions" style="margin-top: 20px;"></div>
        </div>
        
        <!-- Watchlist Display -->
        <div class="portfolio-summary">
            <h3 style="color: #333; margin-bottom: 20px; text-align: center; font-size: 1.5em;">📋 قائمة الأسهم المراقبة</h3>
            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
                <div style="background: linear-gradient(135deg, #00c853 0%, #64dd17 100%); padding: 20px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.3);">
                    <h4 style="color: white; margin-bottom: 15px; text-align: center; font-size: 1.3em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🇸🇦 الأسهم السعودية</h4>
                    <div id="saudi-stocks" style="background: rgba(255,255,255,0.95); padding: 20px; border-radius: 10px; min-height: 500px; max-height: 600px; overflow-y: auto;">
                        <div style="text-align: center; padding: 20px; color: #666;">جاري التحميل...</div>
                    </div>
                </div>
                <div style="background: linear-gradient(135deg, #1976d2 0%, #42a5f5 100%); padding: 20px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.3);">
                    <h4 style="color: white; margin-bottom: 15px; text-align: center; font-size: 1.3em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🇺🇸 الأسهم الأمريكية</h4>
                    <div id="us-stocks" style="background: rgba(255,255,255,0.95); padding: 20px; border-radius: 10px; min-height: 500px;">
                        <div style="text-align: center; padding: 20px; color: #666;">جاري التحميل...</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Investment Calculator -->
        <div class="portfolio-summary">
            <h3 style="color: #333; margin-bottom: 20px;">💰 حاسبة الاستثمار والعائد المتوقع</h3>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px;">
                    <div>
                        <label style="display: block; color: #667eea; font-weight: bold; margin-bottom: 10px;">💵 مبلغ الاستثمار (ريال)</label>
                        <input type="number" id="investment-amount" value="10000" 
                               style="width: 100%; padding: 12px; border: 2px solid #667eea; border-radius: 8px; font-size: 1.1em;"
                               oninput="calculateReturns()">
                    </div>
                    <div>
                        <label style="display: block; color: #667eea; font-weight: bold; margin-bottom: 10px;">📅 مدة الاستثمار (أشهر)</label>
                        <input type="number" id="investment-period" value="6" min="1" max="60"
                               style="width: 100%; padding: 12px; border: 2px solid #667eea; border-radius: 8px; font-size: 1.1em;"
                               oninput="calculateReturns()">
                    </div>
                    <div>
                        <label style="display: block; color: #667eea; font-weight: bold; margin-bottom: 10px;">📈 نسبة العائد المتوقع (%)</label>
                        <input type="number" id="expected-return" value="15" min="1" max="100" step="0.5"
                               style="width: 100%; padding: 12px; border: 2px solid #667eea; border-radius: 8px; font-size: 1.1em;"
                               oninput="calculateReturns()">
                    </div>
                </div>
                
                <div id="calculator-results" style="background: white; padding: 25px; border-radius: 10px; border: 3px solid #667eea;">
                    <h4 style="color: #667eea; margin-bottom: 20px; text-align: center; font-size: 1.3em;">📊 نتائج الاستثمار</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                        <div style="text-align: center; padding: 15px; background: #e8f5e9; border-radius: 10px;">
                            <div style="color: #666; font-size: 0.9em; margin-bottom: 5px;">المبلغ المستثمر</div>
                            <div id="invested-amount" style="color: #667eea; font-size: 1.8em; font-weight: bold;">10,000 ريال</div>
                        </div>
                        <div style="text-align: center; padding: 15px; background: #fff3cd; border-radius: 10px;">
                            <div style="color: #666; font-size: 0.9em; margin-bottom: 5px;">الربح المتوقع</div>
                            <div id="expected-profit" style="color: #28a745; font-size: 1.8em; font-weight: bold;">+1,500 ريال</div>
                        </div>
                        <div style="text-align: center; padding: 15px; background: #e3f2fd; border-radius: 10px;">
                            <div style="color: #666; font-size: 0.9em; margin-bottom: 5px;">المبلغ النهائي</div>
                            <div id="final-amount" style="color: #667eea; font-size: 1.8em; font-weight: bold;">11,500 ريال</div>
                        </div>
                        <div style="text-align: center; padding: 15px; background: #f8d7da; border-radius: 10px;">
                            <div style="color: #666; font-size: 0.9em; margin-bottom: 5px;">الربح الشهري</div>
                            <div id="monthly-profit" style="color: #dc3545; font-size: 1.8em; font-weight: bold;">250 ريال/شهر</div>
                        </div>
                    </div>
                    
                    <div style="margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 10px; text-align: center;">
                        <div style="color: #666; margin-bottom: 10px;">العائد السنوي المتوقع</div>
                        <div id="yearly-return" style="color: #667eea; font-size: 2em; font-weight: bold;">30%</div>
                    </div>
                    
                    <div style="margin-top: 20px; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; text-align: center;">
                        <div style="font-size: 0.9em; margin-bottom: 5px;">⚠️ ملاحظة مهمة</div>
                        <div style="font-size: 0.85em;">هذه التوقعات تقريبية بناءً على التحليل الفني. السوق قد يتحرك بشكل مختلف. استثمر بحذر!</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <button class="btn" onclick="analyzeStocks()" id="analyzeBtn">
                🔍 تحليل الأسهم الآن
            </button>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>جارٍ تحليل الأسهم...</p>
            </div>
        </div>
        
        <div id="resultsContainer"></div>
        
        <div class="footer">
            <p>⚠️ هذا البوت للأغراض التعليمية | التداول يحمل مخاطر</p>
            <p>صُنع بـ ❤️ للمتداولين العرب</p>
        </div>
    </div>
    
    <script>
        // Wallet Management
        let walletBalance = 10000;
        let initialCapital = 10000;
        let transactions = [];
        
        function formatMoney(amount) {
            return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
        }
        
        function updateWalletDisplay() {
            document.getElementById('current-balance').textContent = formatMoney(walletBalance);
            document.getElementById('initial-capital').textContent = formatMoney(initialCapital);
            const profitLoss = walletBalance - initialCapital;
            const profitLossElement = document.getElementById('profit-loss');
            profitLossElement.textContent = formatMoney(profitLoss);
            profitLossElement.style.color = profitLoss >= 0 ? '#4caf50' : '#f44336';
        }
        
        // Payment Method Selection
        function selectPaymentMethod(method) {
            const cardForm = document.getElementById('card-payment-form');
            const bankForm = document.getElementById('bank-payment-form');
            const cardBtn = document.getElementById('btn-card');
            const bankBtn = document.getElementById('btn-bank');
            
            if (method === 'card') {
                cardForm.style.display = 'block';
                bankForm.style.display = 'none';
                cardBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                cardBtn.style.color = 'white';
                bankBtn.style.background = '#e0e0e0';
                bankBtn.style.color = '#666';
            } else {
                cardForm.style.display = 'none';
                bankForm.style.display = 'block';
                bankBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                bankBtn.style.color = 'white';
                cardBtn.style.background = '#e0e0e0';
                cardBtn.style.color = '#666';
            }
        }
        
        // Amount setters
        function setCardAmount(amount) {
            document.getElementById('card-deposit-amount').value = amount;
        }
        
        function setBankAmount(amount) {
            document.getElementById('bank-deposit-amount').value = amount;
        }
        
        function setDepositAmount(amount) {
            document.getElementById('deposit-amount').value = amount;
        }
        
        function setWithdrawAmount(amount) {
            document.getElementById('withdraw-amount').value = amount;
        }
        
        // Card Number Formatting
        document.addEventListener('DOMContentLoaded', function() {
            const cardInput = document.getElementById('card-number');
            if (cardInput) {
                cardInput.addEventListener('input', function(e) {
                    let value = e.target.value.replace(/\\s/g, '');
                    let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
                    e.target.value = formattedValue;
                });
            }
            
            const expiryInput = document.getElementById('card-expiry');
            if (expiryInput) {
                expiryInput.addEventListener('input', function(e) {
                    let value = e.target.value.replace(/\\D/g, '');
                    if (value.length >= 2) {
                        value = value.slice(0, 2) + '/' + value.slice(2, 4);
                    }
                    e.target.value = value;
                });
            }
            
            const ibanInput = document.getElementById('iban-number');
            if (ibanInput) {
                ibanInput.addEventListener('input', function(e) {
                    let value = e.target.value.replace(/\\s/g, '').toUpperCase();
                    let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
                    e.target.value = formattedValue;
                });
            }
        });
        
        // Card Payment Processing
        async function processCardPayment() {
            const amount = parseFloat(document.getElementById('card-deposit-amount').value);
            const cardNumber = document.getElementById('card-number').value.replace(/\\s/g, '');
            const cardholderName = document.getElementById('cardholder-name').value;
            const expiry = document.getElementById('card-expiry').value;
            const cvv = document.getElementById('card-cvv').value;
            
            // Validation
            if (isNaN(amount) || amount < 10) {
                alert('⚠️ الحد الأدنى للإيداع هو $10');
                return;
            }
            
            if (amount > 100000) {
                alert('⚠️ الحد الأقصى للإيداع هو $100,000');
                return;
            }
            
            if (!cardNumber || cardNumber.length < 15 || cardNumber.length > 16) {
                alert('⚠️ رقم البطاقة غير صحيح (15-16 رقم)');
                return;
            }
            
            if (!cardholderName || cardholderName.length < 3) {
                alert('⚠️ الرجاء إدخال اسم حامل البطاقة');
                return;
            }
            
            if (!expiry || !expiry.match(/^\\d{2}\\/\\d{2}$/)) {
                alert('⚠️ تاريخ الانتهاء غير صحيح (MM/YY)');
                return;
            }
            
            if (!cvv || cvv.length < 3 || cvv.length > 4) {
                alert('⚠️ رمز CVV غير صحيح (3-4 أرقام)');
                return;
            }
            
            // Send to API
            try {
                const response = await fetch('/api/payment/card', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        amount: amount,
                        card_number: cardNumber,
                        cardholder_name: cardholderName,
                        expiry: expiry,
                        cvv: cvv,
                        user_id: 'default_user'
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    walletBalance += amount;
                    initialCapital += amount;
                    updateWalletDisplay();
                    
                    alert(`✅ تم الإيداع بنجاح!\n\nالمبلغ: ${formatMoney(amount)}\nرقم المعاملة: ${result.transaction_id}\nالبطاقة: ${result.card_masked}\n\nالرصيد الجديد: ${formatMoney(walletBalance)}`);
                    
                    // Clear form
                    document.getElementById('card-number').value = '';
                    document.getElementById('cardholder-name').value = '';
                    document.getElementById('card-expiry').value = '';
                    document.getElementById('card-cvv').value = '';
                } else {
                    alert('❌ فشل الإيداع: ' + result.message);
                }
            } catch (error) {
                alert('❌ خطأ في الاتصال: ' + error.message);
            }
        }
        
        // Bank Transfer Processing
        async function processBankTransfer() {
            const amount = parseFloat(document.getElementById('bank-deposit-amount').value);
            const iban = document.getElementById('iban-number').value.replace(/\\s/g, '');
            const accountName = document.getElementById('account-name').value;
            
            // Validation
            if (isNaN(amount) || amount < 10) {
                alert('⚠️ الحد الأدنى للإيداع هو $10');
                return;
            }
            
            if (amount > 100000) {
                alert('⚠️ الحد الأقصى للإيداع هو $100,000');
                return;
            }
            
            if (!iban || !iban.startsWith('SA') || iban.length !== 24) {
                alert('⚠️ رقم الآيبان غير صحيح (يجب أن يبدأ بـ SA ويتكون من 24 حرف)');
                return;
            }
            
            if (!accountName || accountName.length < 3) {
                alert('⚠️ الرجاء إدخال اسم صاحب الحساب');
                return;
            }
            
            // Send to API
            try {
                const response = await fetch('/api/payment/bank', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        amount: amount,
                        iban: iban,
                        account_name: accountName,
                        user_id: 'default_user'
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert(`✅ تم إنشاء طلب التحويل بنجاح!\n\nالمبلغ: ${formatMoney(amount)}\nرقم المعاملة: ${result.transaction_id}\nالحالة: قيد الانتظار\n\n⏱️ سيتم إضافة المبلغ إلى رصيدك خلال 1-3 أيام عمل بعد تأكيد البنك`);
                    
                    // Clear form
                    document.getElementById('iban-number').value = '';
                    document.getElementById('account-name').value = '';
                } else {
                    alert('❌ فشل إنشاء التحويل: ' + result.message);
                }
            } catch (error) {
                alert('❌ خطأ في الاتصال: ' + error.message);
            }
        }
        
        function depositMoney() {
            const amount = parseFloat(document.getElementById('deposit-amount').value);
            if (isNaN(amount) || amount <= 0) {
                alert('⚠️ الرجاء إدخال مبلغ صحيح');
                return;
            }
            
            walletBalance += amount;
            initialCapital += amount;
            
            // Add transaction
            const transaction = {
                type: 'deposit',
                amount: amount,
                date: new Date().toLocaleString('ar-SA'),
                balance: walletBalance
            };
            transactions.unshift(transaction);
            
            updateWalletDisplay();
            updateTransactionHistory();
            
            // Success message
            showNotification(`✅ تم إيداع ${formatMoney(amount)} بنجاح!`, 'success');
        }
        
        function withdrawMoney() {
            const amount = parseFloat(document.getElementById('withdraw-amount').value);
            if (isNaN(amount) || amount <= 0) {
                alert('⚠️ الرجاء إدخال مبلغ صحيح');
                return;
            }
            
            if (amount > walletBalance) {
                alert('❌ الرصيد غير كافٍ للسحب!');
                return;
            }
            
            walletBalance -= amount;
            
            // Add transaction
            const transaction = {
                type: 'withdraw',
                amount: amount,
                date: new Date().toLocaleString('ar-SA'),
                balance: walletBalance
            };
            transactions.unshift(transaction);
            
            updateWalletDisplay();
            updateTransactionHistory();
            
            // Success message
            showNotification(`✅ تم سحب ${formatMoney(amount)} بنجاح!`, 'success');
        }
        
        function updateTransactionHistory() {
            const historyDiv = document.getElementById('transaction-history');
            
            if (transactions.length === 0) {
                historyDiv.innerHTML = '<div style="text-align: center; padding: 30px; color: #999;">لا توجد معاملات بعد</div>';
                return;
            }
            
            historyDiv.innerHTML = transactions.map(tx => {
                const isDeposit = tx.type === 'deposit';
                const icon = isDeposit ? '💰' : '💸';
                const color = isDeposit ? '#4caf50' : '#f44336';
                const label = isDeposit ? 'إيداع' : 'سحب';
                const sign = isDeposit ? '+' : '-';
                
                return `
                    <div style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 10px; border-right: 4px solid ${color}; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: bold; color: #333; margin-bottom: 5px;">${icon} ${label}</div>
                            <div style="font-size: 0.9em; color: #666;">${tx.date}</div>
                        </div>
                        <div style="text-align: left;">
                            <div style="font-size: 1.3em; font-weight: bold; color: ${color};">${sign}${formatMoney(tx.amount)}</div>
                            <div style="font-size: 0.85em; color: #666;">الرصيد: ${formatMoney(tx.balance)}</div>
                        </div>
                    </div>
                `;
            }).join('');
        }
        
        function showNotification(message, type) {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: ${type === 'success' ? '#4caf50' : '#f44336'};
                color: white;
                padding: 15px 30px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                z-index: 10000;
                font-weight: bold;
                font-size: 1.1em;
                animation: slideDown 0.3s ease;
            `;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }
        
        // Calculate investment returns
        function calculateReturns() {
            const amount = parseFloat(document.getElementById('investment-amount').value) || 0;
            const period = parseFloat(document.getElementById('investment-period').value) || 1;
            const returnRate = parseFloat(document.getElementById('expected-return').value) || 0;
            
            // Calculate returns
            const profit = (amount * returnRate) / 100;
            const finalAmount = amount + profit;
            const monthlyProfit = profit / period;
            const yearlyReturn = (returnRate / period) * 12;
            
            // Format numbers with commas
            const formatNumber = (num) => {
                return new Intl.NumberFormat('ar-SA').format(Math.round(num));
            };
            
            // Update display
            document.getElementById('invested-amount').textContent = formatNumber(amount) + ' ريال';
            document.getElementById('expected-profit').textContent = '+' + formatNumber(profit) + ' ريال';
            document.getElementById('final-amount').textContent = formatNumber(finalAmount) + ' ريال';
            document.getElementById('monthly-profit').textContent = formatNumber(monthlyProfit) + ' ريال/شهر';
            document.getElementById('yearly-return').textContent = yearlyReturn.toFixed(1) + '%';
            
            // Color coding for profit
            const profitElement = document.getElementById('expected-profit');
            if (profit > 0) {
                profitElement.style.color = '#28a745';
            } else {
                profitElement.style.color = '#dc3545';
            }
        }
        
        async function loadWatchlist() {
            try {
                const response = await fetch('/api/watchlist');
                const data = await response.json();
                
                console.log('📊 Watchlist API Response:', data);
                console.log('🇸🇦 Saudi stocks loaded:', data.saudi?.length || 0);
                console.log('🇺🇸 US stocks loaded:', data.us?.length || 0);
                
                const saudiDiv = document.getElementById('saudi-stocks');
                const usDiv = document.getElementById('us-stocks');
                
                // عرض الأسهم السعودية
                if (data.saudi && data.saudi.length > 0) {
                    const stockNames = {
                        '2222.SR': 'أرامكو السعودية',
                        '1120.SR': 'مصرف الراجحي',
                        '1180.SR': 'الصحراء',
                        '1010.SR': 'الرياض',
                        '1050.SR': 'المجموعة السعودية',
                        '1150.SR': 'الاتصالات السعودية',
                        '1211.SR': 'معادن',
                        '2030.SR': 'مصرف الإنماء',
                        '2050.SR': 'صافولا',
                        '2060.SR': 'التصنيع',
                        '2010.SR': 'سابك',
                        '4190.SR': 'جرير',
                        '4164.SR': 'النهدي',
                        '4001.SR': 'أسواق العثيم',
                        '4002.SR': 'المواساة',
                        '4004.SR': 'دله الصحية',
                        '4008.SR': 'ساكو'
                    };
                    
                    saudiDiv.innerHTML = `
                        <div style="background: linear-gradient(135deg, #00c853 0%, #64dd17 100%); color: white; padding: 15px; margin-bottom: 15px; border-radius: 10px; font-weight: bold; text-align: center; font-size: 1.2em; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                            ✅ إجمالي الأسهم: ${data.saudi.length} سهم سعودي
                        </div>
                        <div style="max-height: 450px; overflow-y: auto; padding: 5px;">
                            ${data.saudi.map((stock, index) => {
                                const colors = ['#1a237e', '#0d47a1', '#01579b', '#006064', '#004d40', '#1b5e20', '#33691e'];
                                const color = colors[index % colors.length];
                                const name = stockNames[stock] || stock.replace('.SR', '');
                                return `<div style="background: linear-gradient(90deg, ${color} 0%, ${color}dd 100%); color: white; padding: 12px 15px; margin: 8px 0; border-radius: 8px; font-weight: bold; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.2); transition: transform 0.2s; cursor: pointer;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
                                    <div style="flex: 1;">
                                        <div style="font-size: 1.1em; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${stock}</div>
                                        <div style="font-size: 0.85em; opacity: 0.9; margin-top: 3px;">${name}</div>
                                    </div>
                                    <span style="background: rgba(255,255,255,0.3); padding: 5px 12px; border-radius: 15px; font-size: 0.85em;">#${index + 1}</span>
                                </div>`;
                            }).join('')}
                        </div>
                    `;
                } else {
                    saudiDiv.innerHTML = `
                        <div style="background: #ffebee; color: #c62828; text-align: center; padding: 30px; border-radius: 10px; font-size: 1.1em; border: 2px dashed #c62828;">
                            <div style="font-size: 3em; margin-bottom: 10px;">❌</div>
                            <div style="font-weight: bold; margin-bottom: 10px;">لا توجد أسهم سعودية في قائمة المراقبة</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">تحقق من ملف config.py</div>
                        </div>
                    `;
                }
                
                // عرض الأسهم الأمريكية
                if (data.us && data.us.length > 0) {
                    const stockNames = {
                        'AAPL': 'Apple',
                        'MSFT': 'Microsoft',
                        'GOOGL': 'Google',
                        'NVDA': 'NVIDIA',
                        'TSLA': 'Tesla',
                        'AMZN': 'Amazon',
                        'META': 'Meta/Facebook',
                        'NFLX': 'Netflix'
                    };
                    
                    usDiv.innerHTML = `
                        <div style="background: linear-gradient(135deg, #1976d2 0%, #42a5f5 100%); color: white; padding: 15px; margin-bottom: 15px; border-radius: 10px; font-weight: bold; text-align: center; font-size: 1.2em; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                            ✅ إجمالي الأسهم: ${data.us.length} سهم أمريكي
                        </div>
                        <div style="max-height: 450px; overflow-y: auto; padding: 5px;">
                            ${data.us.map((stock, index) => {
                                const colors = ['#b71c1c', '#c62828', '#d32f2f', '#e53935', '#f44336'];
                                const color = colors[index % colors.length];
                                const name = stockNames[stock] || stock;
                                return `<div style="background: linear-gradient(90deg, ${color} 0%, ${color}dd 100%); color: white; padding: 12px 15px; margin: 8px 0; border-radius: 8px; font-weight: bold; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.2); transition: transform 0.2s; cursor: pointer;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                                    <div style="flex: 1;">
                                        <div style="font-size: 1.1em; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${stock}</div>
                                        <div style="font-size: 0.85em; opacity: 0.9; margin-top: 3px;">${name}</div>
                                    </div>
                                    <span style="background: rgba(255,255,255,0.3); padding: 5px 12px; border-radius: 15px; font-size: 0.85em;">#${index + 1}</span>
                                </div>`;
                            }).join('')}
                        </div>
                    `;
                } else {
                    usDiv.innerHTML = `
                        <div style="background: #ffebee; color: #c62828; text-align: center; padding: 30px; border-radius: 10px; font-size: 1.1em; border: 2px dashed #c62828;">
                            <div style="font-size: 3em; margin-bottom: 10px;">❌</div>
                            <div style="font-weight: bold; margin-bottom: 10px;">لا توجد أسهم أمريكية في قائمة المراقبة</div>
                            <div style="font-size: 0.9em; opacity: 0.8;">تحقق من ملف config.py</div>
                        </div>
                    `;
                }
            } catch (error) {
                console.error('❌ Error loading watchlist:', error);
                document.getElementById('saudi-stocks').innerHTML = `
                    <div style="background: #fff3e0; color: #e65100; text-align: center; padding: 30px; border-radius: 10px; border: 2px solid #ff9800;">
                        <div style="font-size: 2.5em; margin-bottom: 10px;">⚠️</div>
                        <div style="font-weight: bold;">خطأ في تحميل الأسهم السعودية</div>
                        <div style="font-size: 0.85em; margin-top: 10px; opacity: 0.8;">${error.message}</div>
                    </div>
                `;
                document.getElementById('us-stocks').innerHTML = `
                    <div style="background: #fff3e0; color: #e65100; text-align: center; padding: 30px; border-radius: 10px; border: 2px solid #ff9800;">
                        <div style="font-size: 2.5em; margin-bottom: 10px;">⚠️</div>
                        <div style="font-weight: bold;">خطأ في تحميل الأسهم الأمريكية</div>
                        <div style="font-size: 0.85em; margin-top: 10px; opacity: 0.8;">${error.message}</div>
                    </div>
                `;
            }
        }
        
        async function toggleAutoTrading() {
            const btn = document.getElementById('toggle-trading');
            const statusBadge = document.getElementById('status-badge');
            const statusText = document.getElementById('status-text');
            const toggleText = document.getElementById('toggle-text');
            
            try {
                const response = await fetch('/api/toggle-trading', { method: 'POST' });
                const data = await response.json();
                
                if (data.active) {
                    statusBadge.className = 'status-badge status-active';
                    statusText.textContent = 'نشط ✅';
                    toggleText.textContent = '⏸️ إيقاف التداول';
                    btn.className = 'btn btn-danger';
                    document.getElementById('portfolio-summary').style.display = 'block';
                } else {
                    statusBadge.className = 'status-badge status-inactive';
                    statusText.textContent = 'متوقف ⭕';
                    toggleText.textContent = '🚀 تشغيل التداول التلقائي';
                    btn.className = 'btn btn-success';
                }
                
                updatePortfolio();
            } catch (error) {
                alert('خطأ: ' + error.message);
            }
        }
        
        async function updatePortfolio() {
            try {
                const response = await fetch('/api/portfolio');
                const data = await response.json();
                
                if (data.active && data.positions.length > 0) {
                    document.getElementById('portfolio-summary').style.display = 'block';
                    
                    const statsDiv = document.getElementById('portfolio-stats');
                    statsDiv.innerHTML = `
                        <div class="portfolio-stat">
                            <strong>${data.positions.length}</strong><br>
                            مراكز مفتوحة
                        </div>
                        <div class="portfolio-stat">
                            <strong>$${data.total_invested.toFixed(2)}</strong><br>
                            إجمالي الاستثمار
                        </div>
                        <div class="portfolio-stat">
                            <strong>${data.total_profit >= 0 ? '+' : ''}$${data.total_profit.toFixed(2)}</strong><br>
                            <span style="color: ${data.total_profit >= 0 ? 'green' : 'red'};">
                                (${data.total_profit_percent >= 0 ? '+' : ''}${data.total_profit_percent.toFixed(2)}%)
                            </span><br>
                            الربح/الخسارة
                        </div>
                    `;
                    
                    const positionsDiv = document.getElementById('open-positions');
                    positionsDiv.innerHTML = '<h4 style="color: #333;">المراكز المفتوحة:</h4>' + 
                        data.positions.map(pos => `
                            <div style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 10px; border-left: 4px solid ${pos.profit >= 0 ? '#28a745' : '#dc3545'};">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <strong style="font-size: 1.2em; color: #333;">${pos.symbol}</strong><br>
                                        <span style="color: #666;">${pos.quantity} سهم @ $${pos.entry_price.toFixed(2)}</span>
                                    </div>
                                    <div style="text-align: right;">
                                        <div style="font-size: 1.3em; font-weight: bold; color: ${pos.profit >= 0 ? '#28a745' : '#dc3545'};">
                                            ${pos.profit >= 0 ? '+' : ''}$${pos.profit.toFixed(2)}
                                        </div>
                                        <div style="color: ${pos.profit >= 0 ? '#28a745' : '#dc3545'};">
                                            (${pos.profit_percent >= 0 ? '+' : ''}${pos.profit_percent.toFixed(2)}%)
                                        </div>
                                    </div>
                                </div>
                                <div style="margin-top: 10px; font-size: 0.9em; color: #666;">
                                    🛑 وقف الخسارة: $${pos.stop_loss.toFixed(2)} | 🎯 جني الربح: $${pos.take_profit.toFixed(2)}
                                </div>
                            </div>
                        `).join('');
                }
            } catch (error) {
                console.error('Error updating portfolio:', error);
            }
        }
        
        async function analyzeStocks() {
            const btn = document.getElementById('analyzeBtn');
            const loading = document.getElementById('loading');
            const resultsContainer = document.getElementById('resultsContainer');
            
            btn.disabled = true;
            loading.style.display = 'block';
            resultsContainer.innerHTML = '';
            
            try {
                const response = await fetch('/analyze');
                const data = await response.json();
                
                if (data.error) {
                    resultsContainer.innerHTML = `
                        <div class="stock-card" style="grid-column: 1/-1;">
                            <h3 style="color: red;">❌ خطأ: ${data.error}</h3>
                        </div>
                    `;
                } else {
                    displayResults(data);
                }
            } catch (error) {
                resultsContainer.innerHTML = `
                    <div class="stock-card" style="grid-column: 1/-1;">
                        <h3 style="color: red;">❌ خطأ في الاتصال</h3>
                    </div>
                `;
            } finally {
                btn.disabled = false;
                loading.style.display = 'none';
            }
        }
        
        function displayResults(data) {
            const resultsContainer = document.getElementById('resultsContainer');
            
            // عرض الأسهم
            let html = '<div class="results">';
            
            data.stocks.forEach(stock => {
                let recClass = 'hold';
                if (stock.recommendation.includes('شراء')) recClass = 'buy';
                else if (stock.recommendation.includes('بيع')) recClass = 'sell';
                
                html += `
                    <div class="stock-card">
                        <div class="stock-header">
                            <div class="stock-symbol">${stock.symbol}</div>
                            <div class="stock-price">$${stock.price.toFixed(2)}</div>
                        </div>
                        
                        <div class="stock-info">
                            <strong>RSI:</strong> ${stock.rsi.toFixed(2)}
                        </div>
                        
                        <div class="stock-info">
                            <strong>النقاط:</strong> ${stock.score}
                        </div>
                        
                        <div class="recommendation ${recClass}">
                            ${stock.recommendation}
                        </div>
                        
                        ${stock.buy_signals && stock.buy_signals.length > 0 ? `
                            <div class="signals">
                                <h4>✅ إشارات الشراء:</h4>
                                ${stock.buy_signals.map(s => `<div class="signal-item">${s}</div>`).join('')}
                            </div>
                        ` : ''}
                        
                        ${stock.sell_signals && stock.sell_signals.length > 0 ? `
                            <div class="signals">
                                <h4>❌ إشارات البيع:</h4>
                                ${stock.sell_signals.map(s => `<div class="signal-item">${s}</div>`).join('')}
                            </div>
                        ` : ''}
                    </div>
                `;
            });
            
            html += '</div>';
            
            // أفضل فرصة
            if (data.best_opportunity) {
                const best = data.best_opportunity;
                html += `
                    <div class="best-opportunity">
                        <h2>🏆 أفضل فرصة: ${best.symbol}</h2>
                        <h3>السعر: $${best.price.toFixed(2)}</h3>
                        
                        <div class="risk-info">
                            <h3>📊 محاكاة إدارة المخاطر</h3>
                            <div><strong>حجم المركز:</strong> ${best.position_size} سهم</div>
                            <div><strong>القيمة الإجمالية:</strong> $${best.total_value.toFixed(2)}</div>
                            <div><strong>وقف الخسارة:</strong> $${best.stop_loss.toFixed(2)} (-2%)</div>
                            <div><strong>جني الأرباح:</strong> $${best.take_profit.toFixed(2)} (+5%)</div>
                            <div><strong>المخاطرة المالية:</strong> $${best.risk_amount.toFixed(2)}</div>
                        </div>
                    </div>
                `;
            }
            
            resultsContainer.innerHTML = html;
        }
        
        // تحليل تلقائي عند التحميل
        window.onload = function() {
            updateWalletDisplay(); // Initialize wallet
            updateTransactionHistory(); // Initialize transaction history
            loadWatchlist(); // تحميل قائمة الأسهم المراقبة
            updatePortfolio();
            calculateReturns(); // Initialize calculator
            analyzeStocks(); // تحليل الأسهم
            loadSubscriptionInfo(); // تحميل معلومات الاشتراك
            setInterval(updatePortfolio, 5000); // Update every 5 seconds
        };
        
        // تسجيل الخروج
        async function logout() {
            if (!confirm('هل أنت متأكد من تسجيل الخروج؟')) {
                return;
            }
            
            try {
                const response = await fetch('/api/logout', {
                    method: 'POST'
                });
                
                if (response.ok) {
                    window.location.href = '/login';
                } else {
                    alert('خطأ في تسجيل الخروج');
                }
            } catch (error) {
                console.error('خطأ:', error);
                window.location.href = '/login';
            }
        }
        
        // تحميل معلومات الاشتراك
        async function loadSubscriptionInfo() {
            try {
                const response = await fetch('/api/subscription/current');
                const data = await response.json();
                
                if (data.success && data.subscription) {
                    const sub = data.subscription;
                    
                    // عرض تنبيه إذا كانت الباقة المجانية
                    if (sub.plan_type === 'free') {
                        const header = document.querySelector('.header');
                        const warning = document.createElement('div');
                        warning.style.cssText = 'background: #fff3cd; color: #856404; padding: 15px; border-radius: 10px; margin-top: 15px; text-align: center; border: 2px solid #ffc107;';
                        warning.innerHTML = `
                            <strong>⚠️ أنت تستخدم الباقة المجانية</strong><br>
                            الحد اليومي: ${sub.features.max_trades_per_day} صفقات | 
                            رأس مال محدود: $${sub.features.max_capital_per_trade.toLocaleString()}<br>
                            <a href="/plans" style="color: #667eea; font-weight: bold;">⬆️ ترقية الآن للحصول على مميزات أكثر</a>
                        `;
                        header.appendChild(warning);
                    }
                    
                    // عرض تنبيه إذا كان الاشتراك على وشك الانتهاء
                    if (sub.days_remaining !== undefined && sub.days_remaining < 7 && sub.days_remaining > 0) {
                        const header = document.querySelector('.header');
                        const warning = document.createElement('div');
                        warning.style.cssText = 'background: #f8d7da; color: #721c24; padding: 15px; border-radius: 10px; margin-top: 15px; text-align: center; border: 2px solid #f5c6cb;';
                        warning.innerHTML = `
                            <strong>⏰ تنبيه: اشتراكك ينتهي خلال ${sub.days_remaining} أيام!</strong><br>
                            قم بالتجديد الآن لتجنب فقدان المميزات المدفوعة.
                        `;
                        header.appendChild(warning);
                    }
                }
            } catch (error) {
                console.error('خطأ في تحميل معلومات الاشتراك:', error);
            }
        }
        
        // التحقق من إمكانية التداول (يتم استدعاؤها قبل فتح صفقة)
        async function checkCanTrade() {
            try {
                const response = await fetch('/api/subscription/can_trade');
                const data = await response.json();
                
                if (data.success && data.can_trade.can_trade === false) {
                    alert(`❌ ${data.can_trade.reason}\n\n💡 ${data.can_trade.upgrade_suggestion}\n\nانتقل لصفحة الباقات للترقية.`);
                    
                    if (confirm('هل تريد الانتقال لصفحة الباقات الآن؟')) {
                        window.location.href = '/plans';
                    }
                    
                    return false;
                }
                
                return true;
            } catch (error) {
                console.error('خطأ في التحقق من حدود التداول:', error);
                return true; // السماح بالتداول في حالة الخطأ
            }
        }
    </script>
</body>
</html>
"""

# ==================== Authentication Routes ====================

@app.route('/login', methods=['GET'])
def login_page():
    """صفحة تسجيل الدخول"""
    from login_pages import LOGIN_PAGE
    return render_template_string(LOGIN_PAGE)

@app.route('/register', methods=['GET'])
def register_page():
    """صفحة التسجيل"""
    from login_pages import REGISTER_PAGE
    return render_template_string(REGISTER_PAGE)

@app.route('/api/register', methods=['POST'])
def api_register():
    """API تسجيل مستخدم جديد"""
    try:
        data = request.json
        username = data.get('username', '')
        email = data.get('email', '')
        password = data.get('password', '')
        full_name = data.get('full_name', '')
        phone = data.get('phone', '')
        whatsapp_number = data.get('whatsapp_number', '')
        
        # التحقق من البيانات
        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'الرجاء ملء جميع الحقول المطلوبة'})
        
        # إنشاء المستخدم
        result = user_db.create_user(username, email, password, full_name, phone, whatsapp_number)
        
        # إرسال رسالة ترحيب على واتساب
        if result['success'] and whatsapp_number:
            whatsapp_notifier.notify_welcome(whatsapp_number, full_name or username)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ: {str(e)}'})

@app.route('/api/login', methods=['POST'])
def api_login():
    """API تسجيل دخول"""
    try:
        data = request.json
        username = data.get('username', '')
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'الرجاء إدخال اسم المستخدم وكلمة المرور'})
        
        result = user_db.login_user(username, password)
        
        if result['success']:
            # حفظ session token في الجلسة
            session['token'] = result['session_token']
            session['user_id'] = result['user_id']
            session['username'] = result['username']
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ: {str(e)}'})

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """API تسجيل خروج"""
    try:
        token = session.get('token')
        if token:
            user_db.logout_user(token)
        session.clear()
        return jsonify({'success': True, 'message': 'تم تسجيل الخروج'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ: {str(e)}'})

@app.route('/')
def index():
    """الصفحة الرئيسية - تحويل لتسجيل الدخول"""
    token = session.get('token')
    if token:
        # التحقق من صلاحية الجلسة
        session_data = user_db.verify_session(token)
        if session_data['valid']:
            return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    """لوحة التحكم - الصفحة الرئيسية بعد تسجيل الدخول"""
    token = session.get('token')
    if not token:
        return redirect(url_for('login_page'))
    
    session_data = user_db.verify_session(token)
    if not session_data['valid']:
        session.clear()
        return redirect(url_for('login_page'))
    
    # إضافة بيانات المستخدم للصفحة
    return render_template_string(HTML_TEMPLATE, user_data=session_data)

@app.route('/analyze')
def analyze():
    """تحليل الأسهم وإرجاع النتائج"""
    try:
        # الأسهم من config
        watchlist = getattr(config, 'WATCHLIST', ["AAPL", "MSFT", "GOOGL", "TSLA"])[:6]
        
        results = []
        
        for symbol in watchlist:
            try:
                # تحليل السهم
                result = analyze_stock(symbol)
                
                stock_data = {
                    'symbol': symbol,
                    'price': result['analysis']['price'],
                    'recommendation': result['recommendation'],
                    'score': result['score'],
                    'rsi': result['analysis']['rsi_value'],
                    'buy_signals': result.get('buy_signals', []),
                    'sell_signals': result.get('sell_signals', [])
                }
                
                results.append(stock_data)
                
            except Exception as e:
                print(f"خطأ في {symbol}: {str(e)}")
                continue
        
        # ترتيب حسب النقاط
        results.sort(key=lambda x: x['score'], reverse=True)
        
        # أفضل فرصة
        best = None
        if results and results[0]['score'] > 0:
            best_stock = results[0]
            
            # حساب إدارة المخاطر
            rm = RiskManager(initial_capital=10000, max_risk_per_trade=0.02)
            entry_price = best_stock['price']
            stop_loss = entry_price * 0.98
            take_profit = entry_price * 1.05
            position_size = rm.calculate_position_size(best_stock['symbol'], entry_price, stop_loss)
            
            if position_size > 0:
                best = {
                    'symbol': best_stock['symbol'],
                    'price': entry_price,
                    'position_size': position_size,
                    'total_value': position_size * entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'risk_amount': position_size * (entry_price - stop_loss)
                }
        
        return jsonify({
            'stocks': results,
            'best_opportunity': best,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/watchlist')
def get_watchlist():
    """إرجاع قائمة الأسهم المراقبة"""
    try:
        # فصل الأسهم السعودية والأمريكية
        saudi_stocks = [s for s in config.WATCHLIST if s.endswith('.SR')]
        us_stocks = [s for s in config.WATCHLIST if not s.endswith('.SR')]
        
        print(f"📊 Watchlist loaded: {len(saudi_stocks)} Saudi stocks, {len(us_stocks)} US stocks")
        
        return jsonify({
            'success': True,
            'saudi': saudi_stocks,
            'us': us_stocks,
            'total': len(config.WATCHLIST)
        })
    except Exception as e:
        print(f"❌ Error loading watchlist: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'saudi': [],
            'us': []
        })

@app.route('/api/toggle-trading', methods=['POST'])
def toggle_trading():
    """تشغيل/إيقاف التداول التلقائي"""
    global auto_trading_active, trading_bot
    
    auto_trading_active = not auto_trading_active
    
    if auto_trading_active:
        # إنشاء البوت
        if trading_bot is None:
            from simple_auto_bot import SimpleTradingBot
            trading_bot = SimpleTradingBot()
        
        # تشغيل التداول في خيط منفصل
        def run_trading():
            while auto_trading_active:
                try:
                    trading_bot.run_once()
                    import time
                    time.sleep(60)  # كل دقيقة
                except Exception as e:
                    print(f"خطأ في التداول: {e}")
        
        threading.Thread(target=run_trading, daemon=True).start()
    
    return jsonify({
        'active': auto_trading_active,
        'message': 'تم تشغيل التداول التلقائي' if auto_trading_active else 'تم إيقاف التداول'
    })

@app.route('/api/portfolio')
def get_portfolio():
    """الحصول على معلومات المحفظة"""
    global trading_bot, auto_trading_active
    
    if not auto_trading_active or trading_bot is None:
        return jsonify({
            'active': False,
            'positions': [],
            'total_invested': 0,
            'total_profit': 0,
            'total_profit_percent': 0
        })
    
    positions_data = []
    total_invested = 0
    total_profit = 0
    
    for pos in trading_bot.rm.positions:
        # جلب السعر الحالي
        try:
            import yfinance as yf
            ticker = yf.Ticker(pos.symbol)
            current_price = ticker.history(period='1d')['Close'].iloc[-1]
            
            profit = (current_price - pos.entry_price) * pos.quantity
            profit_percent = ((current_price - pos.entry_price) / pos.entry_price) * 100
            
            positions_data.append({
                'symbol': pos.symbol,
                'quantity': pos.quantity,
                'entry_price': pos.entry_price,
                'current_price': float(current_price),
                'stop_loss': pos.stop_loss,
                'take_profit': pos.take_profit,
                'profit': float(profit),
                'profit_percent': float(profit_percent)
            })
            
            total_invested += pos.entry_price * pos.quantity
            total_profit += profit
        except:
            continue
    
    total_profit_percent = (total_profit / total_invested * 100) if total_invested > 0 else 0
    
    return jsonify({
        'active': True,
        'positions': positions_data,
        'total_invested': float(total_invested),
        'total_profit': float(total_profit),
        'total_profit_percent': float(total_profit_percent),
        'available_capital': float(trading_bot.rm.current_capital)
    })

@app.route('/api/payment/card', methods=['POST'])
def process_card_payment():
    """معالجة الدفع بالبطاقة"""
    try:
        data = request.json
        amount = float(data.get('amount', 0))
        card_number = data.get('card_number', '')
        cardholder_name = data.get('cardholder_name', '')
        expiry = data.get('expiry', '')
        cvv = data.get('cvv', '')
        user_id = data.get('user_id', 'default_user')
        
        # التحقق من المبلغ
        is_valid, msg = security_manager.validate_amount(amount)
        if not is_valid:
            return jsonify({'success': False, 'message': msg})
        
        # معالجة الدفع
        result = payment_processor.process_card_payment(
            amount, card_number, cardholder_name, expiry, cvv, user_id
        )
        
        # إذا نجح الدفع، أضف للمحفظة
        if result['success']:
            if user_id not in users_wallets:
                users_wallets[user_id] = {'balance': 0, 'initial_capital': 0}
            users_wallets[user_id]['balance'] += amount
            users_wallets[user_id]['initial_capital'] += amount
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ: {str(e)}'})

@app.route('/api/payment/bank', methods=['POST'])
def process_bank_transfer():
    """معالجة التحويل البنكي"""
    try:
        data = request.json
        amount = float(data.get('amount', 0))
        iban = data.get('iban', '')
        account_name = data.get('account_name', '')
        user_id = data.get('user_id', 'default_user')
        
        # التحقق من المبلغ
        is_valid, msg = security_manager.validate_amount(amount)
        if not is_valid:
            return jsonify({'success': False, 'message': msg})
        
        # معالجة التحويل
        result = payment_processor.process_bank_transfer(
            amount, iban, account_name, user_id
        )
        
        # ملاحظة: التحويل البنكي يبقى pending حتى يتأكد البنك
        # في الواقع، يجب استخدام webhook من البنك لتأكيد الاستلام
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ: {str(e)}'})

@app.route('/api/transactions/<user_id>')
def get_user_transactions(user_id):
    """استرجاع معاملات المستخدم"""
    transactions = payment_processor.get_user_transactions(user_id)
    return jsonify({'transactions': transactions})

@app.route('/api/wallet/<user_id>')
def get_wallet_balance(user_id):
    """الحصول على رصيد المحفظة"""
    wallet = users_wallets.get(user_id, {'balance': 10000, 'initial_capital': 10000})
    return jsonify(wallet)

# ==================== نظام الباقات ====================

@app.route('/plans')
def plans_page():
    """صفحة الباقات والأسعار"""
    from subscription_pages import PLANS_PAGE
    return PLANS_PAGE

@app.route('/subscription')
def subscription_status_page():
    """صفحة حالة الاشتراك"""
    # التحقق من تسجيل الدخول
    token = session.get('token')
    if not token:
        return redirect('/login')
    
    user_info = user_db.verify_session(token)
    if not user_info['valid']:
        return redirect('/login')
    
    from subscription_pages import SUBSCRIPTION_STATUS_PAGE
    return SUBSCRIPTION_STATUS_PAGE

@app.route('/api/subscription/current', methods=['GET'])
def get_current_subscription():
    """الحصول على اشتراك المستخدم الحالي"""
    try:
        # التحقق من تسجيل الدخول
        token = session.get('token')
        if not token:
            return jsonify({'success': False, 'message': 'يجب تسجيل الدخول'})
        
        user_info = user_db.verify_session(token)
        if not user_info['valid']:
            return jsonify({'success': False, 'message': 'جلسة غير صالحة'})
        
        user_id = user_info['user_id']
        subscription = subscription_manager.get_user_subscription(user_id)
        
        return jsonify({
            'success': True,
            'subscription': subscription
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ: {str(e)}'})

@app.route('/api/subscription/subscribe', methods=['POST'])
def subscribe_to_plan():
    """الاشتراك في باقة جديدة"""
    try:
        # التحقق من تسجيل الدخول
        token = session.get('token')
        if not token:
            return jsonify({'success': False, 'message': 'يجب تسجيل الدخول'})
        
        user_info = user_db.verify_session(token)
        if not user_info['valid']:
            return jsonify({'success': False, 'message': 'جلسة غير صالحة'})
        
        user_id = user_info['user_id']
        data = request.get_json()
        plan_type = data.get('plan_type')
        payment_method = data.get('payment_method', 'card')
        
        # إنشاء الاشتراك
        result = subscription_manager.create_subscription(
            user_id, plan_type, payment_method
        )
        
        # إرسال إشعار واتساب
        if result['success'] and user_info.get('whatsapp_number'):
            plan = subscription_manager.PLANS[plan_type]
            whatsapp_notifier.send_notification(
                user_info['whatsapp_number'],
                f"🎉 *تم الاشتراك بنجاح!*\n\n"
                f"✅ الباقة: {plan['name']}\n"
                f"💰 المبلغ: ${plan['price']}\n"
                f"📅 صالحة لمدة: {plan['duration_days']} يوم\n\n"
                f"شكراً لاشتراكك معنا!"
            )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ: {str(e)}'})

@app.route('/api/subscription/check_limit/<feature_name>', methods=['GET'])
def check_feature_limit(feature_name):
    """التحقق من حد استخدام ميزة"""
    try:
        token = session.get('token')
        if not token:
            return jsonify({'success': False, 'message': 'يجب تسجيل الدخول'})
        
        user_info = user_db.verify_session(token)
        if not user_info['valid']:
            return jsonify({'success': False, 'message': 'جلسة غير صالحة'})
        
        user_id = user_info['user_id']
        limit_check = subscription_manager.check_feature_limit(user_id, feature_name)
        
        return jsonify({
            'success': True,
            'limit_check': limit_check
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ: {str(e)}'})

@app.route('/api/subscription/can_trade', methods=['GET'])
def check_can_trade():
    """التحقق من إمكانية فتح صفقة جديدة"""
    try:
        token = session.get('token')
        if not token:
            return jsonify({'success': False, 'message': 'يجب تسجيل الدخول'})
        
        user_info = user_db.verify_session(token)
        if not user_info['valid']:
            return jsonify({'success': False, 'message': 'جلسة غير صالحة'})
        
        user_id = user_info['user_id']
        can_trade = subscription_manager.can_trade(user_id)
        
        return jsonify({
            'success': True,
            'can_trade': can_trade
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ: {str(e)}'})

def open_browser():
    """فتح المتصفح تلقائياً"""
    import time
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌐 بوت التداول الآلي - واجهة الويب")
    print("="*70)
    print("\n✅ الخادم يعمل على: http://127.0.0.1:5000")
    print("🌐 المتصفح سيفتح تلقائياً...\n")
    print("⚠️ لإيقاف الخادم: اضغط Ctrl+C\n")
    print("="*70 + "\n")
    
    # فتح المتصفح في خيط منفصل
    threading.Timer(1.5, open_browser).start()
    
    # تشغيل الخادم - متاح على الشبكة المحلية
    app.run(debug=False, host='0.0.0.0', port=5000)
