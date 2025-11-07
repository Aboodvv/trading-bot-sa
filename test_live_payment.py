"""
اختبار سريع لنظام الدفع - تأكد من أن كل شيء يعمل
"""

import requests
import json

print("="*70)
print("اختبار نظام الدفع - Payment System Test")
print("="*70)

# عنوان السيرفر
BASE_URL = "http://127.0.0.1:5000"

# 1. اختبار أن السيرفر يعمل
print("\n1. اختبار الاتصال بالسيرفر...")
try:
    response = requests.get(BASE_URL, timeout=5)
    if response.status_code == 200:
        print("   ✅ السيرفر يعمل بنجاح!")
    else:
        print(f"   ❌ السيرفر يرد بكود: {response.status_code}")
except Exception as e:
    print(f"   ❌ خطأ في الاتصال: {e}")
    print("\n⚠️ تأكد أن السيرفر يعمل بتشغيل: python web_app.py")
    exit(1)

# 2. اختبار API الدفع بالبطاقة
print("\n2. اختبار API الدفع بالبطاقة...")
card_data = {
    "amount": 100,
    "card_number": "4111111111111111",
    "cardholder_name": "TEST USER",
    "expiry": "12/25",
    "cvv": "123",
    "user_id": "test_user"
}

try:
    response = requests.post(
        f"{BASE_URL}/api/payment/card",
        json=card_data,
        headers={"Content-Type": "application/json"}
    )
    result = response.json()
    
    if result.get('success'):
        print("   ✅ API الدفع بالبطاقة يعمل!")
        print(f"   📝 رقم المعاملة: {result.get('transaction_id', 'N/A')}")
        print(f"   💳 البطاقة المخفية: {result.get('card_masked', 'N/A')}")
    else:
        print(f"   ⚠️ API يرد لكن فيه مشكلة: {result.get('message', 'Unknown')}")
except Exception as e:
    print(f"   ❌ خطأ: {e}")

# 3. اختبار API التحويل البنكي
print("\n3. اختبار API التحويل البنكي...")
bank_data = {
    "amount": 200,
    "iban": "SA0380000000608010167519",
    "account_name": "TEST USER",
    "user_id": "test_user"
}

try:
    response = requests.post(
        f"{BASE_URL}/api/payment/bank",
        json=bank_data,
        headers={"Content-Type": "application/json"}
    )
    result = response.json()
    
    if result.get('success'):
        print("   ✅ API التحويل البنكي يعمل!")
        print(f"   📝 رقم المعاملة: {result.get('transaction_id', 'N/A')}")
        print(f"   ⏱️ الحالة: {result.get('status', 'N/A')}")
    else:
        print(f"   ⚠️ API يرد لكن فيه مشكلة: {result.get('message', 'Unknown')}")
except Exception as e:
    print(f"   ❌ خطأ: {e}")

# 4. اختبار API المحفظة
print("\n4. اختبار API المحفظة...")
try:
    response = requests.get(f"{BASE_URL}/api/wallet/default_user")
    result = response.json()
    
    print(f"   ✅ API المحفظة يعمل!")
    print(f"   💰 الرصيد الحالي: ${result.get('balance', 0):,.2f}")
    print(f"   🏦 رأس المال الأولي: ${result.get('initial_capital', 0):,.2f}")
except Exception as e:
    print(f"   ❌ خطأ: {e}")

print("\n" + "="*70)
print("✅ انتهى الاختبار!")
print("="*70)

print("\n📌 ملاحظات:")
print("1. افتح المتصفح على: http://127.0.0.1:5000")
print("2. اذهب لقسم 'محفظة وإدارة رأس المال'")
print("3. ستجد قسم 'إيداع أموال آمن' مع طريقتين:")
print("   - 💳 بطاقة ائتمان")
print("   - 🏦 تحويل بنكي")
print("\n🎉 جرب الآن!")
