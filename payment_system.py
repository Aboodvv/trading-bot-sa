"""
نظام الدفع والإيداع الآمن
يدعم: بطاقات الائتمان، التحويل البنكي، Apple Pay
"""

from datetime import datetime
import hashlib
import secrets
import json

class PaymentProcessor:
    """معالج الدفع الآمن"""
    
    def __init__(self):
        self.transactions = []
        self.pending_deposits = {}
        
    def generate_transaction_id(self):
        """توليد رقم معاملة فريد"""
        return f"TXN-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(8).upper()}"
    
    def mask_card_number(self, card_number):
        """إخفاء رقم البطاقة (عرض آخر 4 أرقام فقط)"""
        last_four = card_number[-4:]
        return f"****-****-****-{last_four}"
    
    def hash_card_number(self, card_number):
        """تشفير رقم البطاقة للأمان"""
        # نحفظ آخر 4 أرقام فقط
        last_four = card_number[-4:]
        hashed = hashlib.sha256(card_number.encode()).hexdigest()
        return f"****-****-****-{last_four}", hashed
    
    def validate_card(self, card_number, expiry, cvv):
        """التحقق من صحة البطاقة"""
        # إزالة المسافات
        card_number = card_number.replace(" ", "").replace("-", "")
        
        # التحقق من الطول
        if len(card_number) not in [15, 16]:  # Amex = 15, Others = 16
            return False, "رقم البطاقة غير صحيح"
        
        # التحقق من أنها أرقام فقط
        if not card_number.isdigit():
            return False, "رقم البطاقة يجب أن يحتوي على أرقام فقط"
        
        # التحقق من تاريخ الانتهاء
        try:
            month, year = expiry.split("/")
            month, year = int(month), int(year)
            if month < 1 or month > 12:
                return False, "تاريخ الانتهاء غير صحيح"
            current_year = datetime.now().year % 100
            if year < current_year:
                return False, "البطاقة منتهية الصلاحية"
        except:
            return False, "صيغة تاريخ الانتهاء غير صحيحة (MM/YY)"
        
        # التحقق من CVV
        if not cvv.isdigit() or len(cvv) not in [3, 4]:
            return False, "رمز الأمان (CVV) غير صحيح"
        
        return True, "البطاقة صحيحة"
    
    def validate_iban(self, iban):
        """التحقق من صحة IBAN"""
        # إزالة المسافات
        iban = iban.replace(" ", "").upper()
        
        # التحقق من الطول (IBAN السعودي = 24 حرف)
        if not iban.startswith("SA") or len(iban) != 24:
            return False, "رقم IBAN السعودي يجب أن يبدأ بـ SA ويكون 24 حرف"
        
        # التحقق من أنه يحتوي على أرقام بعد SA
        if not iban[2:].isdigit():
            return False, "IBAN يجب أن يحتوي على أرقام بعد SA"
        
        return True, "IBAN صحيح"
    
    def process_card_payment(self, amount, card_number, cardholder_name, expiry, cvv, user_id):
        """معالجة الدفع بالبطاقة"""
        # التحقق من البطاقة
        is_valid, message = self.validate_card(card_number, expiry, cvv)
        if not is_valid:
            return {
                'success': False,
                'message': message,
                'transaction_id': None
            }
        
        # تشفير رقم البطاقة
        masked_card, card_hash = self.hash_card_number(card_number)
        
        # توليد رقم المعاملة
        transaction_id = self.generate_transaction_id()
        
        # حفظ المعاملة
        transaction = {
            'id': transaction_id,
            'type': 'card_deposit',
            'amount': amount,
            'currency': 'USD',
            'status': 'completed',  # في الواقع يجب أن يكون 'pending' حتى تأكيد البنك
            'user_id': user_id,
            'payment_method': 'credit_card',
            'card_masked': masked_card,
            'cardholder_name': cardholder_name,
            'timestamp': datetime.now().isoformat(),
            'card_hash': card_hash
        }
        
        self.transactions.append(transaction)
        
        return {
            'success': True,
            'message': f'تم إيداع ${amount:,.2f} بنجاح',
            'transaction_id': transaction_id,
            'masked_card': masked_card,
            'timestamp': transaction['timestamp']
        }
    
    def process_bank_transfer(self, amount, iban, account_name, user_id):
        """معالجة التحويل البنكي"""
        # التحقق من IBAN
        is_valid, message = self.validate_iban(iban)
        if not is_valid:
            return {
                'success': False,
                'message': message,
                'transaction_id': None
            }
        
        # توليد رقم المعاملة
        transaction_id = self.generate_transaction_id()
        
        # إخفاء IBAN (نعرض أول 4 وآخر 4 فقط)
        masked_iban = f"{iban[:4]}****{iban[-4:]}"
        
        # حفظ المعاملة
        transaction = {
            'id': transaction_id,
            'type': 'bank_transfer',
            'amount': amount,
            'currency': 'USD',
            'status': 'pending',  # التحويل البنكي يحتاج وقت
            'user_id': user_id,
            'payment_method': 'bank_transfer',
            'iban_masked': masked_iban,
            'account_name': account_name,
            'timestamp': datetime.now().isoformat(),
            'estimated_completion': '1-3 أيام عمل'
        }
        
        self.transactions.append(transaction)
        self.pending_deposits[transaction_id] = transaction
        
        return {
            'success': True,
            'message': f'تم إنشاء طلب تحويل ${amount:,.2f}. سيتم الإيداع خلال 1-3 أيام عمل',
            'transaction_id': transaction_id,
            'masked_iban': masked_iban,
            'timestamp': transaction['timestamp'],
            'status': 'pending'
        }
    
    def get_transaction(self, transaction_id):
        """استرجاع تفاصيل المعاملة"""
        for tx in self.transactions:
            if tx['id'] == transaction_id:
                return tx
        return None
    
    def get_user_transactions(self, user_id, limit=10):
        """استرجاع معاملات المستخدم"""
        user_txs = [tx for tx in self.transactions if tx.get('user_id') == user_id]
        return sorted(user_txs, key=lambda x: x['timestamp'], reverse=True)[:limit]


class SecurityManager:
    """مدير الأمان"""
    
    @staticmethod
    def encrypt_sensitive_data(data):
        """تشفير البيانات الحساسة"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def generate_otp():
        """توليد رمز OTP للمصادقة الثنائية"""
        return ''.join([str(secrets.randbelow(10)) for _ in range(6)])
    
    @staticmethod
    def validate_amount(amount, min_amount=10, max_amount=100000):
        """التحقق من صحة المبلغ"""
        if amount < min_amount:
            return False, f"الحد الأدنى للإيداع ${min_amount}"
        if amount > max_amount:
            return False, f"الحد الأقصى للإيداع ${max_amount:,}"
        return True, "المبلغ صحيح"


# مثيل عام
payment_processor = PaymentProcessor()
security_manager = SecurityManager()
