"""
نظام إشعارات واتساب
WhatsApp Notification System
"""

import requests
import json
from datetime import datetime

class WhatsAppNotifier:
    """إرسال إشعارات واتساب للعملاء"""
    
    def __init__(self):
        # يمكنك استخدام أي من هذه الخدمات:
        # 1. Twilio WhatsApp API
        # 2. WhatsApp Business API
        # 3. WATI (WhatsApp Team Inbox)
        # 4. Green API
        
        # مثال باستخدام Green API (الأسهل)
        self.api_url = "https://api.green-api.com"
        self.instance_id = "YOUR_INSTANCE_ID"  # ضع instance_id الخاص بك
        self.api_token = "YOUR_API_TOKEN"      # ضع api_token الخاص بك
        
        # أو استخدام Twilio
        self.twilio_account_sid = "YOUR_TWILIO_ACCOUNT_SID"
        self.twilio_auth_token = "YOUR_TWILIO_AUTH_TOKEN"
        self.twilio_whatsapp_number = "whatsapp:+14155238886"  # رقم Twilio
    
    def format_phone_number(self, phone):
        """تنسيق رقم الهاتف للواتساب"""
        # إزالة المسافات والرموز
        phone = ''.join(filter(str.isdigit, phone))
        
        # إضافة كود الدولة إذا لم يكن موجود
        if not phone.startswith('966') and not phone.startswith('+966'):
            if phone.startswith('05'):
                phone = '966' + phone[1:]  # تحويل 05 إلى 9665
            elif phone.startswith('5'):
                phone = '966' + phone
        
        # إزالة + إذا موجود
        phone = phone.replace('+', '')
        
        return phone
    
    def send_via_greenapi(self, phone, message):
        """إرسال رسالة عبر Green API"""
        try:
            phone = self.format_phone_number(phone)
            
            url = f"{self.api_url}/waInstance{self.instance_id}/sendMessage/{self.api_token}"
            
            payload = {
                "chatId": f"{phone}@c.us",
                "message": message
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                return {'success': True, 'message': 'تم إرسال الإشعار'}
            else:
                return {'success': False, 'message': f'خطأ: {response.text}'}
        except Exception as e:
            return {'success': False, 'message': f'خطأ: {str(e)}'}
    
    def send_via_twilio(self, phone, message):
        """إرسال رسالة عبر Twilio"""
        try:
            from twilio.rest import Client
            
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            
            phone = self.format_phone_number(phone)
            
            message_obj = client.messages.create(
                body=message,
                from_=self.twilio_whatsapp_number,
                to=f'whatsapp:+{phone}'
            )
            
            return {'success': True, 'message': 'تم إرسال الإشعار', 'sid': message_obj.sid}
        except Exception as e:
            return {'success': False, 'message': f'خطأ: {str(e)}'}
    
    def send_notification(self, phone, message, method='console'):
        """إرسال إشعار (يمكن اختيار الطريقة)"""
        if method == 'greenapi':
            return self.send_via_greenapi(phone, message)
        elif method == 'twilio':
            return self.send_via_twilio(phone, message)
        else:
            # للتطوير: طباعة في Console
            print("\n" + "="*70)
            print("📱 WhatsApp Notification")
            print("="*70)
            print(f"To: {phone}")
            print(f"Message:\n{message}")
            print("="*70 + "\n")
            return {'success': True, 'message': 'تم طباعة الإشعار في Console'}
    
    def notify_buy(self, phone, symbol, quantity, price, total_cost):
        """إشعار شراء سهم"""
        message = f"""
🟢 *إشعار شراء* 🟢

📊 السهم: {symbol}
📈 الكمية: {quantity} سهم
💵 السعر: ${price:.2f}
💰 التكلفة الإجمالية: ${total_cost:.2f}

⏰ التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ تم تنفيذ الصفقة بنجاح!
"""
        return self.send_notification(phone, message.strip())
    
    def notify_sell(self, phone, symbol, quantity, entry_price, exit_price, profit):
        """إشعار بيع سهم"""
        profit_emoji = "🟢" if profit >= 0 else "🔴"
        profit_text = "ربح" if profit >= 0 else "خسارة"
        
        message = f"""
{profit_emoji} *إشعار بيع* {profit_emoji}

📊 السهم: {symbol}
📉 الكمية: {quantity} سهم
💵 سعر الشراء: ${entry_price:.2f}
💵 سعر البيع: ${exit_price:.2f}
{'💰' if profit >= 0 else '📉'} {profit_text}: ${abs(profit):.2f}

⏰ التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'✅ تهانينا! صفقة ناجحة!' if profit >= 0 else '⚠️ تم إغلاق الصفقة'}
"""
        return self.send_notification(phone, message.strip())
    
    def notify_profit_target(self, phone, symbol, profit_amount, profit_percent):
        """إشعار وصول لهدف الربح"""
        message = f"""
🎉 *تحقيق هدف الربح!* 🎉

📊 السهم: {symbol}
💰 الربح: ${profit_amount:.2f}
📈 النسبة: {profit_percent:.1f}%

⏰ التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ تهانينا! تم تحقيق الهدف المطلوب!
"""
        return self.send_notification(phone, message.strip())
    
    def notify_stop_loss(self, phone, symbol, loss_amount, loss_percent):
        """إشعار وقف الخسارة"""
        message = f"""
🛑 *تفعيل وقف الخسارة* 🛑

📊 السهم: {symbol}
📉 الخسارة: ${abs(loss_amount):.2f}
📊 النسبة: {abs(loss_percent):.1f}%

⏰ التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⚠️ تم إغلاق الصفقة تلقائياً لحماية رأس المال
"""
        return self.send_notification(phone, message.strip())
    
    def notify_daily_summary(self, phone, total_trades, wins, losses, total_profit):
        """إشعار الملخص اليومي"""
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        message = f"""
📊 *ملخص اليوم* 📊

📈 عدد الصفقات: {total_trades}
✅ صفقات رابحة: {wins}
❌ صفقات خاسرة: {losses}
📊 معدل النجاح: {win_rate:.1f}%

💰 الربح/الخسارة الإجمالي: ${total_profit:.2f}

⏰ التاريخ: {datetime.now().strftime('%Y-%m-%d')}

{'🎉 يوم رائع!' if total_profit >= 0 else '💪 غداً سيكون أفضل!'}
"""
        return self.send_notification(phone, message.strip())
    
    def notify_low_balance(self, phone, current_balance, minimum_balance):
        """إشعار انخفاض الرصيد"""
        message = f"""
⚠️ *تنبيه: انخفاض الرصيد* ⚠️

💰 الرصيد الحالي: ${current_balance:.2f}
📉 الحد الأدنى: ${minimum_balance:.2f}

⏰ التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 نوصي بإيداع مبلغ إضافي لمواصلة التداول
"""
        return self.send_notification(phone, message.strip())
    
    def notify_welcome(self, phone, username):
        """رسالة ترحيب للمستخدم الجديد"""
        message = f"""
👋 *مرحباً بك!* 👋

أهلاً {username}!

شكراً لانضمامك إلى بوت التداول الآلي 🤖

✅ تم تفعيل حسابك بنجاح
💰 رصيدك الابتدائي: $10,000
📱 الإشعارات على واتساب: مفعّلة

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🚀 استمتع بتجربة تداول احترافية!
"""
        return self.send_notification(phone, message.strip())
    
    def notify_deposit_success(self, phone, amount, new_balance):
        """إشعار نجاح الإيداع"""
        message = f"""
✅ *تم الإيداع بنجاح* ✅

💵 المبلغ المودع: ${amount:.2f}
💰 الرصيد الجديد: ${new_balance:.2f}

⏰ التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎉 تم إضافة المبلغ إلى حسابك!
"""
        return self.send_notification(phone, message.strip())

# إنشاء instance عام
whatsapp_notifier = WhatsAppNotifier()
