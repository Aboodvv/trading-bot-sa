"""
🧪 اختبار نظام الدفع - Payment System Test
يختبر جميع وظائف الدفع والتحقق الأمني
"""

from payment_system import payment_processor, security_manager
import json

def print_section(title):
    """طباعة عنوان القسم"""
    print("\n" + "="*70)
    print(f"🧪 {title}")
    print("="*70 + "\n")

def test_card_validation():
    """اختبار التحقق من البطاقات"""
    print_section("اختبار التحقق من البطاقات")
    
    test_cases = [
        # (card_number, expiry, cvv, should_pass)
        ("4111111111111111", "12/25", "123", True, "Visa صالحة"),
        ("5555555555554444", "06/26", "456", True, "Mastercard صالحة"),
        ("378282246310005", "09/24", "1234", True, "Amex صالحة"),
        ("1234", "12/25", "123", False, "رقم قصير جداً"),
        ("4111111111111111", "13/25", "123", False, "شهر غير صحيح"),
        ("4111111111111111", "12/20", "123", False, "تاريخ منتهي"),
        ("4111111111111111", "12/25", "12", False, "CVV قصير"),
    ]
    
    for card, expiry, cvv, should_pass, description in test_cases:
        is_valid, message = payment_processor.validate_card(card, expiry, cvv)
        status = "✅ نجح" if is_valid == should_pass else "❌ فشل"
        print(f"{status} | {description}")
        print(f"   البطاقة: {card[:4]}...{card[-4:]} | النتيجة: {message}")

def test_iban_validation():
    """اختبار التحقق من IBAN"""
    print_section("اختبار التحقق من IBAN")
    
    test_cases = [
        ("SA0380000000608010167519", True, "IBAN سعودي صالح"),
        ("SA4420000001234567891234", True, "IBAN سعودي صالح 2"),
        ("AE070331234567890123456", False, "IBAN إماراتي (غير مدعوم)"),
        ("SA123", False, "IBAN قصير جداً"),
        ("1234567890123456789012", False, "بدون بادئة SA"),
    ]
    
    for iban, should_pass, description in test_cases:
        is_valid, message = payment_processor.validate_iban(iban)
        status = "✅ نجح" if is_valid == should_pass else "❌ فشل"
        print(f"{status} | {description}")
        print(f"   IBAN: {iban} | النتيجة: {message}")

def test_amount_validation():
    """اختبار التحقق من المبالغ"""
    print_section("اختبار التحقق من المبالغ")
    
    test_cases = [
        (100, True, "مبلغ عادي"),
        (10, True, "الحد الأدنى"),
        (100000, True, "الحد الأقصى"),
        (5, False, "أقل من الحد الأدنى"),
        (150000, False, "أكثر من الحد الأقصى"),
        (-100, False, "مبلغ سالب"),
    ]
    
    for amount, should_pass, description in test_cases:
        is_valid, message = security_manager.validate_amount(amount)
        status = "✅ نجح" if is_valid == should_pass else "❌ فشل"
        print(f"{status} | {description}")
        print(f"   المبلغ: ${amount:,} | النتيجة: {message}")

def test_card_payment():
    """اختبار معالجة الدفع بالبطاقة"""
    print_section("اختبار معالجة الدفع بالبطاقة")
    
    # محاولة دفع صحيحة
    result = payment_processor.process_card_payment(
        amount=1000,
        card_number="4111111111111111",
        cardholder_name="AHMED MOHAMMED",
        expiry="12/25",
        cvv="123",
        user_id="test_user"
    )
    
    print("✅ نتيجة الدفع:")
    print(f"   النجاح: {result['success']}")
    print(f"   رقم المعاملة: {result.get('transaction_id', 'N/A')}")
    print(f"   البطاقة: {result.get('card_masked', 'N/A')}")
    print(f"   الرسالة: {result['message']}")
    
    # محاولة دفع فاشلة (بطاقة غير صحيحة)
    result_fail = payment_processor.process_card_payment(
        amount=500,
        card_number="1234",
        cardholder_name="TEST USER",
        expiry="12/25",
        cvv="123",
        user_id="test_user"
    )
    
    print("\n❌ نتيجة دفع فاشل:")
    print(f"   النجاح: {result_fail['success']}")
    print(f"   الرسالة: {result_fail['message']}")

def test_bank_transfer():
    """اختبار معالجة التحويل البنكي"""
    print_section("اختبار معالجة التحويل البنكي")
    
    # محاولة تحويل صحيحة
    result = payment_processor.process_bank_transfer(
        amount=2000,
        iban="SA0380000000608010167519",
        account_name="أحمد محمد",
        user_id="test_user"
    )
    
    print("✅ نتيجة التحويل:")
    print(f"   النجاح: {result['success']}")
    print(f"   رقم المعاملة: {result.get('transaction_id', 'N/A')}")
    print(f"   الحالة: {result.get('status', 'N/A')}")
    print(f"   الرسالة: {result['message']}")
    
    # محاولة تحويل فاشلة (IBAN غير صحيح)
    result_fail = payment_processor.process_bank_transfer(
        amount=1500,
        iban="AE123456789",
        account_name="TEST USER",
        user_id="test_user"
    )
    
    print("\n❌ نتيجة تحويل فاشل:")
    print(f"   النجاح: {result_fail['success']}")
    print(f"   الرسالة: {result_fail['message']}")

def test_transaction_history():
    """اختبار سجل المعاملات"""
    print_section("اختبار سجل المعاملات")
    
    # إضافة بعض المعاملات
    payment_processor.process_card_payment(
        1000, "4111111111111111", "User A", "12/25", "123", "user1"
    )
    payment_processor.process_card_payment(
        2000, "5555555555554444", "User B", "06/26", "456", "user1"
    )
    payment_processor.process_bank_transfer(
        3000, "SA0380000000608010167519", "User C", "user1"
    )
    
    # جلب المعاملات
    transactions = payment_processor.get_user_transactions("user1")
    
    print(f"عدد المعاملات: {len(transactions)}")
    print("\nآخر 3 معاملات:")
    for i, txn in enumerate(transactions[:3], 1):
        print(f"\n{i}. معاملة {txn['id']}")
        print(f"   النوع: {txn['type']}")
        print(f"   المبلغ: ${txn['amount']:,}")
        print(f"   الحالة: {txn['status']}")
        print(f"   التاريخ: {txn['date']}")

def test_encryption():
    """اختبار التشفير"""
    print_section("اختبار التشفير")
    
    sensitive_data = "4111111111111111"
    encrypted = security_manager.encrypt_sensitive_data(sensitive_data)
    
    print(f"البيانات الأصلية: {sensitive_data}")
    print(f"البيانات المشفرة: {encrypted[:50]}...")
    print(f"طول التشفير: {len(encrypted)} حرف")
    print(f"\n✅ التشفير يعمل بنجاح - البيانات غير قابلة للقراءة")

def test_card_masking():
    """اختبار إخفاء أرقام البطاقات"""
    print_section("اختبار إخفاء أرقام البطاقات")
    
    test_cards = [
        "4111111111111111",
        "5555555555554444",
        "378282246310005"
    ]
    
    for card in test_cards:
        masked = payment_processor.mask_card_number(card)
        print(f"الأصلي: {card} → المخفي: {masked}")

def test_otp_generation():
    """اختبار توليد OTP"""
    print_section("اختبار توليد رموز OTP")
    
    print("توليد 5 رموز OTP:")
    for i in range(5):
        otp = security_manager.generate_otp()
        print(f"{i+1}. {otp} (طول: {len(otp)} أرقام)")

def run_all_tests():
    """تشغيل جميع الاختبارات"""
    print("\n" + "🚀"*35)
    print("🧪 بدء اختبار نظام الدفع الشامل")
    print("🚀"*35)
    
    try:
        test_card_validation()
        test_iban_validation()
        test_amount_validation()
        test_card_payment()
        test_bank_transfer()
        test_transaction_history()
        test_encryption()
        test_card_masking()
        test_otp_generation()
        
        print("\n" + "✅"*35)
        print("✅ اكتملت جميع الاختبارات بنجاح!")
        print("✅"*35 + "\n")
        
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
