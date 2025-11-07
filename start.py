"""
سكريبت بسيط لتشغيل البوت بسرعة
"""

import os
import sys


def check_requirements():
    """التحقق من تثبيت المكتبات"""
    try:
        import yfinance
        import pandas
        import numpy
        import ta
        import colorama
        return True
    except ImportError as e:
        print("❌ بعض المكتبات غير مثبتة!")
        print(f"الخطأ: {str(e)}")
        print("\nيرجى تشغيل:")
        print("pip install -r requirements.txt")
        return False


def show_menu():
    """عرض القائمة الرئيسية"""
    print("\n" + "=" * 70)
    print("🤖 بوت التداول الآلي - القائمة الرئيسية")
    print("=" * 70)
    print("\n1. تشغيل البوت الكامل")
    print("2. اختبار التحليل التقني")
    print("3. اختبار الاستراتيجيات")
    print("4. اختبار إدارة المخاطر")
    print("5. تشغيل الأمثلة المتقدمة")
    print("6. عرض التعليمات")
    print("0. خروج")
    print("\n" + "=" * 70)


def run_bot():
    """تشغيل البوت"""
    os.system("python bot.py")


def run_technical_analysis():
    """تشغيل التحليل التقني"""
    os.system("python technical_analysis.py")


def run_strategies():
    """تشغيل الاستراتيجيات"""
    os.system("python trading_strategy.py")


def run_risk_management():
    """تشغيل إدارة المخاطر"""
    os.system("python risk_management.py")


def run_examples():
    """تشغيل الأمثلة"""
    os.system("python examples.py")


def show_help():
    """عرض التعليمات"""
    print("\n" + "=" * 70)
    print("📚 دليل الاستخدام السريع")
    print("=" * 70)
    
    print("\n🎯 للمبتدئين:")
    print("  1. ابدأ بالخيار 2 لاختبار التحليل التقني")
    print("  2. جرب الخيار 3 لفهم الاستراتيجيات")
    print("  3. استخدم الخيار 1 لتشغيل البوت الكامل")
    
    print("\n⚙️ الإعدادات:")
    print("  - افتح ملف config.py لتعديل الإعدادات")
    print("  - غير قائمة WATCHLIST لأسهمك المفضلة")
    print("  - اضبط نسبة المخاطرة حسب رغبتك")
    
    print("\n📊 المؤشرات المستخدمة:")
    print("  - RSI: مؤشر القوة النسبية")
    print("  - MACD: تقارب/تباعد المتوسطات المتحركة")
    print("  - Bollinger Bands: نطاقات بولينجر")
    print("  - ATR: متوسط المدى الحقيقي")
    print("  - ADX: مؤشر الاتجاه")
    
    print("\n⚠️ تحذيرات:")
    print("  - استخدم وضع PAPER للتجربة أولاً")
    print("  - التداول يحمل مخاطر")
    print("  - لا تستثمر أموالاً لا تستطيع خسارتها")
    
    print("\n📖 ملفات مفيدة:")
    print("  - README.md: شرح شامل")
    print("  - QUICKSTART.md: البدء السريع")
    print("  - examples.py: أمثلة متقدمة")
    
    input("\nاضغط Enter للعودة للقائمة...")


def main():
    """الدالة الرئيسية"""
    # التحقق من المكتبات
    if not check_requirements():
        sys.exit(1)
    
    print("\n✅ جميع المكتبات مثبتة!")
    
    while True:
        show_menu()
        choice = input("\nاختر رقماً (0-6): ").strip()
        
        if choice == "1":
            run_bot()
        elif choice == "2":
            run_technical_analysis()
        elif choice == "3":
            run_strategies()
        elif choice == "4":
            run_risk_management()
        elif choice == "5":
            run_examples()
        elif choice == "6":
            show_help()
        elif choice == "0":
            print("\n👋 شكراً لاستخدام البوت!")
            break
        else:
            print("\n❌ اختيار غير صحيح! حاول مرة أخرى.")
        
        input("\nاضغط Enter للمتابعة...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ تم الإيقاف بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ حدث خطأ: {str(e)}")
