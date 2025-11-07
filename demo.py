"""
نسخة تجريبية سريعة للبوت
"""

import yfinance as yf
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

print(f"\n{Fore.CYAN}{'='*70}")
print(f"{'🤖 نسخة تجريبية - بوت التداول الآلي 🤖':^70}")
print(f"{'='*70}{Style.RESET_ALL}\n")

# قائمة أسهم للتجربة
stocks = ["AAPL", "MSFT", "GOOGL"]

print(f"{Fore.YELLOW}📊 جارٍ تحليل الأسهم...{Style.RESET_ALL}\n")

for symbol in stocks:
    try:
        # جلب البيانات
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d")
        
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            change = ((current_price - prev_price) / prev_price) * 100
            
            # تحديد اللون بناءً على التغيير
            if change > 0:
                color = Fore.GREEN
                arrow = "⬆️"
            elif change < 0:
                color = Fore.RED
                arrow = "⬇️"
            else:
                color = Fore.WHITE
                arrow = "➡️"
            
            print(f"{Fore.CYAN}📌 {symbol}{Style.RESET_ALL}")
            print(f"   السعر: {color}${current_price:.2f}{Style.RESET_ALL}")
            print(f"   التغيير: {color}{arrow} {change:.2f}%{Style.RESET_ALL}")
            
            # حساب RSI بسيط (تقريبي)
            if len(hist) >= 14:
                closes = hist['Close'].tail(14)
                gains = closes.diff().clip(lower=0)
                losses = -closes.diff().clip(upper=0)
                avg_gain = gains.mean()
                avg_loss = losses.mean()
                
                if avg_loss != 0:
                    rs = avg_gain / avg_loss
                    rsi = 100 - (100 / (1 + rs))
                    
                    if rsi < 30:
                        print(f"   RSI: {Fore.GREEN}{rsi:.2f} (فرصة شراء محتملة){Style.RESET_ALL}")
                    elif rsi > 70:
                        print(f"   RSI: {Fore.RED}{rsi:.2f} (تشبع شرائي){Style.RESET_ALL}")
                    else:
                        print(f"   RSI: {Fore.YELLOW}{rsi:.2f} (محايد){Style.RESET_ALL}")
            
            print()
            
    except Exception as e:
        print(f"{Fore.RED}❌ خطأ في تحليل {symbol}: {str(e)}{Style.RESET_ALL}\n")

print(f"{Fore.CYAN}{'='*70}")
print(f"{'✅ انتهى التحليل التجريبي':^70}")
print(f"{'='*70}{Style.RESET_ALL}\n")

print(f"{Fore.GREEN}🎉 البوت يعمل بنجاح!{Style.RESET_ALL}")
print(f"\n{Fore.YELLOW}للتشغيل الكامل:{Style.RESET_ALL}")
print(f"   1. شغّل: python bot.py")
print(f"   2. أو: python start.py (واجهة سهلة)")
print(f"   3. أو: python examples.py (أمثلة متقدمة)")

print(f"\n{Fore.CYAN}نصائح:{Style.RESET_ALL}")
print(f"   • ابدأ دائماً بوضع PAPER (المحاكاة)")
print(f"   • عدّل قائمة الأسهم في config.py")
print(f"   • اقرأ QUICKSTART.md للبدء السريع")
print(f"\n{Fore.GREEN}{'شكراً لتجربة البوت! 🚀':^70}{Style.RESET_ALL}\n")
