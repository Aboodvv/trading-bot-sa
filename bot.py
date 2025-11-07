"""
🤖 بوت التداول الآلي الاحترافي
يجمع بين التحليل الفني والاستراتيجيات الذكية وإدارة المخاطر
"""

import time
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List
from colorama import init, Fore, Style
import config
from technical_analysis import TechnicalAnalyzer
from trading_strategy import CompositeStrategy
from risk_management import RiskManager

# تهيئة الألوان
init(autoreset=True)


class TradingBot:
    """البوت الرئيسي للتداول"""
    
    def __init__(self, watchlist: List[str], initial_capital: float = 10000, 
                 trading_mode: str = "PAPER"):
        """
        تهيئة البوت
        
        :param watchlist: قائمة الأسهم للمتابعة
        :param initial_capital: رأس المال الأولي
        :param trading_mode: وضع التداول (PAPER أو LIVE)
        """
        self.watchlist = watchlist
        self.trading_mode = trading_mode
        
        # تهيئة المكونات
        self.strategy = CompositeStrategy()
        self.risk_manager = RiskManager(
            initial_capital=initial_capital,
            max_risk_per_trade=config.MAX_POSITION_SIZE,
            max_portfolio_risk=config.MAX_DAILY_LOSS,
            max_positions=config.MAX_OPEN_POSITIONS
        )
        
        # تخزين التحليلات
        self.analyses: Dict[str, Dict] = {}
        self.last_update = None
        
        # إحصائيات
        self.scan_count = 0
        self.alerts = []
        
    def print_header(self):
        """طباعة رأس البوت"""
        print("\n" + "=" * 80)
        print(f"{Fore.CYAN}{'🤖 بوت التداول الآلي الاحترافي':^80}{Style.RESET_ALL}")
        print("=" * 80)
        print(f"وضع التداول: {Fore.GREEN if self.trading_mode == 'PAPER' else Fore.RED}{self.trading_mode}{Style.RESET_ALL}")
        print(f"رأس المال: {Fore.GREEN}${self.risk_manager.current_capital:,.2f}{Style.RESET_ALL}")
        print(f"الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80 + "\n")
    
    def scan_market(self):
        """مسح السوق وتحليل الأسهم"""
        self.scan_count += 1
        self.last_update = datetime.now()
        
        print(f"{Fore.YELLOW}🔍 جارٍ مسح السوق... (المسح #{self.scan_count}){Style.RESET_ALL}\n")
        
        opportunities = []
        
        for symbol in self.watchlist:
            try:
                print(f"   📊 تحليل {symbol}...", end=" ")
                
                # إنشاء المحلل
                analyzer = TechnicalAnalyzer(symbol, period="6mo")
                analyzer.fetch_data()
                analyzer.calculate_all_indicators()
                
                # توليد الإشارة
                signal = self.strategy.generate_signal(analyzer)
                latest = analyzer.get_latest_values()
                
                # تخزين التحليل
                self.analyses[symbol] = {
                    'signal': signal,
                    'latest': latest,
                    'timestamp': datetime.now()
                }
                
                # طباعة النتيجة
                if signal['action'] == 'BUY':
                    print(f"{Fore.GREEN}✅ إشارة شراء ({signal['confidence']:.0f}%){Style.RESET_ALL}")
                    opportunities.append((symbol, signal, latest))
                elif signal['action'] == 'SELL':
                    print(f"{Fore.RED}⚠️  إشارة بيع ({signal['confidence']:.0f}%){Style.RESET_ALL}")
                else:
                    print(f"{Fore.WHITE}⚪ لا توجد إشارة{Style.RESET_ALL}")
                
                time.sleep(0.5)  # تجنب تجاوز حدود API
                
            except Exception as e:
                print(f"{Fore.RED}❌ خطأ: {str(e)}{Style.RESET_ALL}")
        
        return opportunities
    
    def evaluate_opportunity(self, symbol: str, signal: Dict, latest: Dict) -> bool:
        """
        تقييم فرصة التداول
        
        :param symbol: رمز السهم
        :param signal: الإشارة المُولدة
        :param latest: أحدث البيانات
        :return: True إذا كانت الفرصة جيدة
        """
        # التحقق من قوة الإشارة
        if signal['confidence'] < 60:
            return False
        
        # التحقق من عدد الأصوات
        if signal['buy_votes'] <= signal['sell_votes']:
            return False
        
        # التحقق من إمكانية التداول
        if not self.risk_manager.can_trade():
            return False
        
        return True
    
    def execute_trade(self, symbol: str, action: str, signal: Dict, latest: Dict):
        """
        تنفيذ الصفقة
        
        :param symbol: رمز السهم
        :param action: الإجراء (BUY أو SELL)
        :param signal: الإشارة
        :param latest: أحدث البيانات
        """
        current_price = latest['Close']
        atr = latest.get('ATR')
        
        if action == 'BUY':
            # حساب وقف الخسارة وجني الأرباح
            stop_loss = self.risk_manager.calculate_stop_loss(
                current_price, 
                atr=atr,
                percent=config.STOP_LOSS_PERCENT
            )
            
            take_profit = self.risk_manager.calculate_take_profit(
                current_price,
                stop_loss,
                risk_reward_ratio=config.TAKE_PROFIT_PERCENT / config.STOP_LOSS_PERCENT
            )
            
            # حساب حجم المركز
            position_size = self.risk_manager.calculate_position_size(
                symbol,
                current_price,
                stop_loss
            )
            
            if position_size > 0:
                # فتح المركز
                success = self.risk_manager.open_position(
                    symbol,
                    position_size,
                    current_price,
                    stop_loss,
                    take_profit
                )
                
                if success:
                    self.alerts.append({
                        'timestamp': datetime.now(),
                        'type': 'TRADE',
                        'symbol': symbol,
                        'action': 'BUY',
                        'price': current_price,
                        'quantity': position_size,
                        'confidence': signal['confidence']
                    })
        
        elif action == 'SELL':
            # إغلاق المركز إذا كان موجوداً
            if symbol in self.risk_manager.positions:
                self.risk_manager.close_position(symbol, current_price, "إشارة بيع من الاستراتيجية")
    
    def update_positions(self):
        """تحديث المراكز المفتوحة"""
        if not self.risk_manager.positions:
            return
        
        print(f"\n{Fore.CYAN}📈 تحديث المراكز المفتوحة...{Style.RESET_ALL}")
        
        # جلب الأسعار الحالية
        current_prices = {}
        for symbol in self.risk_manager.positions.keys():
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period="1d", interval="1m")
                if not data.empty:
                    current_prices[symbol] = data['Close'].iloc[-1]
            except Exception as e:
                print(f"   ❌ خطأ في تحديث {symbol}: {str(e)}")
        
        # تحديث المراكز
        self.risk_manager.update_positions(current_prices)
    
    def print_opportunities(self, opportunities: List):
        """طباعة الفرص المتاحة"""
        if not opportunities:
            print(f"\n{Fore.YELLOW}💡 لا توجد فرص تداول حالياً{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}{'='*80}")
        print(f"🎯 الفرص المتاحة ({len(opportunities)})")
        print(f"{'='*80}{Style.RESET_ALL}")
        
        for symbol, signal, latest in opportunities:
            print(f"\n{Fore.CYAN}📌 {symbol}{Style.RESET_ALL}")
            print(f"   السعر: ${latest['Close']:.2f}")
            print(f"   الإجراء: {Fore.GREEN}{signal['action']}{Style.RESET_ALL}")
            print(f"   الثقة: {signal['confidence']:.0f}%")
            print(f"   أصوات الشراء: {signal['buy_votes']}")
            print(f"   أصوات البيع: {signal['sell_votes']}")
            
            # طباعة تفاصيل الاستراتيجيات
            for detail in signal['details']:
                if detail['action'] == 'BUY' and detail['reasons']:
                    print(f"   • {detail['strategy']}: {', '.join(detail['reasons'][:2])}")
    
    def run_once(self):
        """تشغيل دورة واحدة"""
        self.print_header()
        
        # مسح السوق
        opportunities = self.scan_market()
        
        # طباعة الفرص
        self.print_opportunities(opportunities)
        
        # تنفيذ الصفقات للفرص الجيدة
        for symbol, signal, latest in opportunities:
            if self.evaluate_opportunity(symbol, signal, latest):
                print(f"\n{Fore.GREEN}✨ تقييم إيجابي لـ {symbol} - جارٍ تنفيذ الصفقة...{Style.RESET_ALL}")
                self.execute_trade(symbol, signal['action'], signal, latest)
        
        # تحديث المراكز المفتوحة
        self.update_positions()
        
        # طباعة ملخص المحفظة
        self.risk_manager.print_portfolio_summary()
    
    def run_continuous(self, interval: int = 60):
        """
        تشغيل مستمر
        
        :param interval: الفاصل الزمني بين الفحوصات (بالثواني)
        """
        print(f"{Fore.CYAN}🚀 بدء البوت في وضع التشغيل المستمر{Style.RESET_ALL}")
        print(f"الفاصل الزمني: {interval} ثانية\n")
        
        try:
            while True:
                self.run_once()
                
                print(f"\n{Fore.YELLOW}⏰ الفحص التالي بعد {interval} ثانية...{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}اضغط Ctrl+C للإيقاف{Style.RESET_ALL}\n")
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}⏹️  توقف البوت بواسطة المستخدم{Style.RESET_ALL}")
            self.shutdown()
    
    def shutdown(self):
        """إيقاف البوت وحفظ البيانات"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print("📊 تقرير نهائي")
        print(f"{'='*80}{Style.RESET_ALL}\n")
        
        # إغلاق جميع المراكز المفتوحة
        if self.risk_manager.positions:
            print(f"{Fore.YELLOW}⚠️  إغلاق جميع المراكز المفتوحة...{Style.RESET_ALL}\n")
            
            for symbol in list(self.risk_manager.positions.keys()):
                try:
                    ticker = yf.Ticker(symbol)
                    current_price = ticker.history(period="1d")['Close'].iloc[-1]
                    self.risk_manager.close_position(symbol, current_price, "إيقاف البوت")
                except Exception as e:
                    print(f"خطأ في إغلاق {symbol}: {str(e)}")
        
        # طباعة الملخص النهائي
        self.risk_manager.print_portfolio_summary()
        
        print(f"\n{Fore.GREEN}✅ تم إيقاف البوت بنجاح{Style.RESET_ALL}\n")


def main():
    """الدالة الرئيسية"""
    print(f"{Fore.CYAN}")
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║           🤖 بوت التداول الآلي الاحترافي 🤖              ║
    ║                                                               ║
    ║  يحلل الأسهم باحترافية ويتداول بذكاء مع إدارة المخاطر     ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    print(Style.RESET_ALL)
    
    print(f"{Fore.YELLOW}⚙️  جارٍ تهيئة البوت...{Style.RESET_ALL}\n")
    
    # إنشاء البوت
    bot = TradingBot(
        watchlist=config.WATCHLIST,
        initial_capital=10000,  # يمكن تغييره
        trading_mode=config.TRADING_MODE
    )
    
    # اختيار وضع التشغيل
    print(f"{Fore.CYAN}اختر وضع التشغيل:{Style.RESET_ALL}")
    print("1. تشغيل مرة واحدة (فحص واحد)")
    print("2. تشغيل مستمر (فحص كل دقيقة)")
    print("3. تشغيل مستمر (فحص كل 5 دقائق)")
    
    choice = input(f"\n{Fore.GREEN}أدخل اختيارك (1-3): {Style.RESET_ALL}")
    
    if choice == "1":
        bot.run_once()
    elif choice == "2":
        bot.run_continuous(interval=60)
    elif choice == "3":
        bot.run_continuous(interval=300)
    else:
        print(f"{Fore.RED}اختيار غير صحيح!{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}شكراً لاستخدام البوت! 👋{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
