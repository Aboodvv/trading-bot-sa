"""
أمثلة متقدمة لاستخدام البوت
"""

from technical_analysis import TechnicalAnalyzer, analyze_stock
from trading_strategy import CompositeStrategy, backtest_strategy, MomentumStrategy
from risk_management import RiskManager
import pandas as pd


def example_1_basic_analysis():
    """مثال 1: تحليل سريع لسهم واحد"""
    print("=" * 70)
    print("مثال 1: تحليل سريع لسهم")
    print("=" * 70)
    
    result = analyze_stock("AAPL")
    
    print(f"\nرمز السهم: {result['symbol']}")
    print(f"التوصية: {result['recommendation']}")
    print(f"النقاط: {result['score']}")
    print(f"السعر: ${result['analysis']['price']:.2f}")
    print(f"RSI: {result['analysis']['rsi_value']:.2f}")
    print(f"الاتجاه: {result['analysis']['trend']}")


def example_2_detailed_analysis():
    """مثال 2: تحليل مفصل مع جميع المؤشرات"""
    print("\n" + "=" * 70)
    print("مثال 2: تحليل مفصل مع جميع المؤشرات")
    print("=" * 70)
    
    analyzer = TechnicalAnalyzer("MSFT", period="1y")
    analyzer.fetch_data()
    analyzer.calculate_all_indicators()
    
    latest = analyzer.get_latest_values()
    
    print(f"\nالسهم: {latest['Symbol']}")
    print(f"التاريخ: {latest['Timestamp']}")
    print(f"السعر: ${latest['Close']:.2f}")
    print(f"\nالمؤشرات:")
    print(f"  RSI: {latest['RSI']:.2f}")
    print(f"  MACD: {latest['MACD']:.4f}")
    print(f"  MACD Signal: {latest['MACD_Signal']:.4f}")
    print(f"  SMA 20: ${latest['SMA_20']:.2f}")
    print(f"  SMA 50: ${latest['SMA_50']:.2f}")
    print(f"  BB High: ${latest['BB_High']:.2f}")
    print(f"  BB Low: ${latest['BB_Low']:.2f}")
    print(f"  ADX: {latest['ADX']:.2f}")
    print(f"  ATR: ${latest['ATR']:.2f}")


def example_3_multiple_stocks():
    """مثال 3: مقارنة عدة أسهم"""
    print("\n" + "=" * 70)
    print("مثال 3: مقارنة عدة أسهم")
    print("=" * 70)
    
    stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    results = []
    
    for symbol in stocks:
        try:
            result = analyze_stock(symbol)
            results.append({
                'Symbol': symbol,
                'Price': result['analysis']['price'],
                'Recommendation': result['recommendation'],
                'Score': result['score'],
                'RSI': result['analysis']['rsi_value']
            })
        except Exception as e:
            print(f"خطأ في {symbol}: {str(e)}")
    
    # إنشاء DataFrame
    df = pd.DataFrame(results)
    df = df.sort_values('Score', ascending=False)
    
    print("\nترتيب الأسهم حسب النقاط:")
    print(df.to_string(index=False))
    
    # أفضل فرصة
    best = df.iloc[0]
    print(f"\n🏆 أفضل فرصة: {best['Symbol']}")
    print(f"   التوصية: {best['Recommendation']}")
    print(f"   النقاط: {best['Score']}")


def example_4_composite_strategy():
    """مثال 4: استخدام الاستراتيجية المركبة"""
    print("\n" + "=" * 70)
    print("مثال 4: الاستراتيجية المركبة")
    print("=" * 70)
    
    composite = CompositeStrategy()
    analysis = composite.get_detailed_analysis("NVDA")
    
    print(f"\nالسهم: {analysis['symbol']}")
    print(f"السعر: ${analysis['price']:.2f}")
    print(f"\nالإشارة المركبة:")
    print(f"  الإجراء: {analysis['signal']['action']}")
    print(f"  الثقة: {analysis['signal']['confidence']:.1f}%")
    print(f"  أصوات الشراء: {analysis['signal']['buy_votes']}")
    print(f"  أصوات البيع: {analysis['signal']['sell_votes']}")
    
    print("\nتفاصيل الاستراتيجيات:")
    for detail in analysis['signal']['details']:
        print(f"\n  • {detail['strategy']}")
        print(f"    الإجراء: {detail['action']} ({detail['confidence']:.0f}%)")
        if detail.get('reasons'):
            print(f"    الأسباب: {', '.join(detail['reasons'][:2])}")


def example_5_backtest():
    """مثال 5: اختبار خلفي لاستراتيجية"""
    print("\n" + "=" * 70)
    print("مثال 5: اختبار خلفي لاستراتيجية")
    print("=" * 70)
    
    strategy = MomentumStrategy()
    result = backtest_strategy("AAPL", strategy, period="1y", initial_capital=10000)
    
    print(f"\nالاستراتيجية: {result['strategy']}")
    print(f"السهم: {result['symbol']}")
    print(f"رأس المال الأولي: ${result['initial_capital']:,.2f}")
    print(f"رأس المال النهائي: ${result['final_capital']:,.2f}")
    print(f"العائد الإجمالي: {result['total_return']:.2f}%")
    print(f"عدد الصفقات: {result['num_trades']}")
    
    if result['trades']:
        print(f"\nآخر 3 صفقات:")
        for trade in result['trades'][-3:]:
            print(f"  {trade['date'].strftime('%Y-%m-%d')} - {trade['action']}")
            print(f"    السعر: ${trade['price']:.2f}")
            if 'value' in trade:
                print(f"    القيمة: ${trade['value']:.2f}")


def example_6_risk_management():
    """مثال 6: محاكاة كاملة مع إدارة المخاطر"""
    print("\n" + "=" * 70)
    print("مثال 6: محاكاة مع إدارة المخاطر")
    print("=" * 70)
    
    # إنشاء مدير المخاطر
    rm = RiskManager(initial_capital=10000, max_risk_per_trade=0.02, max_positions=3)
    
    # سيناريو 1: فتح مركز AAPL
    print("\n📍 سيناريو 1: فتح مركز AAPL")
    analyzer = TechnicalAnalyzer("AAPL")
    analyzer.fetch_data()
    analyzer.calculate_all_indicators()
    latest = analyzer.get_latest_values()
    
    entry_price = latest['Close']
    atr = latest['ATR']
    stop_loss = rm.calculate_stop_loss(entry_price, atr)
    take_profit = rm.calculate_take_profit(entry_price, stop_loss, 2.0)
    position_size = rm.calculate_position_size("AAPL", entry_price, stop_loss)
    
    print(f"السعر: ${entry_price:.2f}")
    print(f"وقف الخسارة: ${stop_loss:.2f} ({((stop_loss-entry_price)/entry_price*100):.2f}%)")
    print(f"جني الأرباح: ${take_profit:.2f} ({((take_profit-entry_price)/entry_price*100):.2f}%)")
    print(f"حجم المركز: {position_size} سهم")
    
    rm.open_position("AAPL", position_size, entry_price, stop_loss, take_profit)
    
    # سيناريو 2: محاكاة ارتفاع السعر
    print("\n📍 سيناريو 2: السعر يرتفع")
    new_price = entry_price * 1.03  # ارتفاع 3%
    rm.update_positions({"AAPL": new_price})
    
    # طباعة الملخص
    rm.print_portfolio_summary()


def example_7_find_opportunities():
    """مثال 7: البحث عن فرص في قائمة أسهم"""
    print("\n" + "=" * 70)
    print("مثال 7: البحث عن أفضل الفرص")
    print("=" * 70)
    
    stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "JPM"]
    opportunities = []
    
    composite = CompositeStrategy()
    
    print("\nجارٍ البحث...\n")
    
    for symbol in stocks:
        try:
            analyzer = TechnicalAnalyzer(symbol, period="6mo")
            analyzer.fetch_data()
            analyzer.calculate_all_indicators()
            
            signal = composite.generate_signal(analyzer)
            latest = analyzer.get_latest_values()
            
            if signal['action'] == 'BUY' and signal['confidence'] >= 60:
                opportunities.append({
                    'Symbol': symbol,
                    'Price': latest['Close'],
                    'Action': signal['action'],
                    'Confidence': signal['confidence'],
                    'Buy_Votes': signal['buy_votes'],
                    'Sell_Votes': signal['sell_votes']
                })
                print(f"✅ {symbol}: {signal['action']} ({signal['confidence']:.0f}%)")
            else:
                print(f"⚪ {symbol}: {signal['action']} ({signal['confidence']:.0f}%)")
        
        except Exception as e:
            print(f"❌ {symbol}: خطأ - {str(e)}")
    
    if opportunities:
        df = pd.DataFrame(opportunities)
        df = df.sort_values('Confidence', ascending=False)
        
        print("\n" + "=" * 70)
        print("🎯 الفرص المكتشفة (مرتبة حسب الثقة):")
        print("=" * 70)
        print(df.to_string(index=False))
    else:
        print("\n⚠️ لم يتم العثور على فرص جيدة حالياً")


def example_8_monitor_positions():
    """مثال 8: مراقبة المراكز المفتوحة"""
    print("\n" + "=" * 70)
    print("مثال 8: مراقبة المراكز المفتوحة")
    print("=" * 70)
    
    rm = RiskManager(initial_capital=10000)
    
    # فتح عدة مراكز
    positions_data = [
        ("AAPL", 150.0, 147.0, 156.0, 30),
        ("MSFT", 380.0, 372.4, 395.2, 10),
        ("GOOGL", 140.0, 137.2, 145.6, 25)
    ]
    
    print("\n🔓 فتح مراكز...\n")
    for symbol, entry, stop, profit, qty in positions_data:
        rm.open_position(symbol, qty, entry, stop, profit)
    
    # محاكاة أسعار جديدة
    print("\n📊 تحديث الأسعار...\n")
    new_prices = {
        "AAPL": 152.5,  # ربح
        "MSFT": 375.0,  # خسارة طفيفة
        "GOOGL": 138.0  # خسارة
    }
    
    rm.update_positions(new_prices)
    rm.print_portfolio_summary()


if __name__ == "__main__":
    print("=" * 70)
    print("أمثلة متقدمة لاستخدام بوت التداول")
    print("=" * 70)
    
    # قائمة الأمثلة
    examples = [
        ("1", "تحليل سريع لسهم واحد", example_1_basic_analysis),
        ("2", "تحليل مفصل مع جميع المؤشرات", example_2_detailed_analysis),
        ("3", "مقارنة عدة أسهم", example_3_multiple_stocks),
        ("4", "استخدام الاستراتيجية المركبة", example_4_composite_strategy),
        ("5", "اختبار خلفي لاستراتيجية", example_5_backtest),
        ("6", "محاكاة مع إدارة المخاطر", example_6_risk_management),
        ("7", "البحث عن أفضل الفرص", example_7_find_opportunities),
        ("8", "مراقبة المراكز المفتوحة", example_8_monitor_positions),
        ("0", "تشغيل جميع الأمثلة", None)
    ]
    
    print("\nاختر مثالاً:")
    for num, desc, _ in examples:
        print(f"  {num}. {desc}")
    
    choice = input("\nأدخل رقم المثال: ").strip()
    
    if choice == "0":
        # تشغيل جميع الأمثلة
        for num, desc, func in examples[:-1]:  # ما عدا الخيار 0
            try:
                func()
                input("\nاضغط Enter للمتابعة...")
            except Exception as e:
                print(f"\n❌ خطأ في المثال {num}: {str(e)}")
    else:
        # تشغيل مثال محدد
        for num, desc, func in examples:
            if num == choice and func:
                try:
                    func()
                except Exception as e:
                    print(f"\n❌ خطأ: {str(e)}")
                break
        else:
            print("اختيار غير صحيح!")
    
    print("\n" + "=" * 70)
    print("انتهى!")
    print("=" * 70)
