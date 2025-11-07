"""
🤖 بوت التداول التلقائي - يشتري ويبيع تلقائياً
يدعم الأسهم الأمريكية والسعودية
"""

import time
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List
from colorama import init, Fore, Style
import config
from technical_analysis import TechnicalAnalyzer
from trading_strategy import CompositeStrategy
from risk_management import RiskManager, Position

init(autoreset=True)


class AutoTradingBot:
    """بوت التداول التلقائي الكامل"""
    
    def __init__(self, initial_capital: float = 10000):
        """تهيئة البوت"""
        self.watchlist = config.WATCHLIST
        self.strategy = CompositeStrategy()
        self.risk_manager = RiskManager(
            initial_capital=initial_capital,
            max_risk_per_trade=config.MAX_POSITION_SIZE,
            max_portfolio_risk=config.MAX_DAILY_LOSS,
            max_positions=config.MAX_OPEN_POSITIONS
        )
        
        self.scan_count = 0
        self.simulation_mode = config.SIMULATION_MODE
        self.min_confidence = config.MIN_CONFIDENCE
        self.auto_close = config.AUTO_CLOSE_ON_SIGNAL
        
        # إحصائيات
        self.total_signals = 0
        self.executed_trades = 0
        self.skipped_trades = 0
        
    def print_header(self):
        """طباعة رأس البوت"""
        mode_text = "محاكاة" if self.simulation_mode else "تداول حقيقي"
        mode_color = Fore.GREEN if self.simulation_mode else Fore.RED
        
        print("\n" + "=" * 90)
        print(f"{Fore.CYAN}{'🤖 بوت التداول التلقائي - يشتري ويبيع تلقائياً':^90}{Style.RESET_ALL}")
        print("=" * 90)
        print(f"الوضع: {mode_color}{mode_text}{Style.RESET_ALL} | "
              f"رأس المال: {Fore.GREEN}${self.risk_manager.current_capital:,.2f}{Style.RESET_ALL} | "
              f"الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 90 + "\n")
    
    def get_current_price(self, symbol: str) -> float:
        """الحصول على السعر الحالي"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            if not data.empty:
                return data['Close'].iloc[-1]
        except:
            pass
        return None
    
    def execute_buy(self, symbol: str, signal: Dict, latest: Dict):
        """تنفيذ أمر شراء"""
        current_price = latest['Close']
        atr = latest.get('ATR')
        
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
                self.executed_trades += 1
                print(f"{Fore.GREEN}✅ تم تنفيذ أمر شراء:{Style.RESET_ALL}")
                print(f"   {Fore.CYAN}{symbol}{Style.RESET_ALL}: {position_size} سهم @ ${current_price:.2f}")
                print(f"   وقف الخسارة: ${stop_loss:.2f} | جني الأرباح: ${take_profit:.2f}")
                print(f"   الثقة: {signal['confidence']:.0f}%\n")
                return True
        else:
            self.skipped_trades += 1
            print(f"{Fore.YELLOW}⚠️  تم تجاوز {symbol}: حجم المركز = 0{Style.RESET_ALL}\n")
        
        return False
    
    def execute_sell(self, symbol: str, signal: Dict):
        """تنفيذ أمر بيع"""
        if symbol in self.risk_manager.positions:
            current_price = self.get_current_price(symbol)
            if current_price:
                success = self.risk_manager.close_position(
                    symbol, 
                    current_price, 
                    f"إشارة بيع تلقائية (ثقة: {signal['confidence']:.0f}%)"
                )
                if success:
                    self.executed_trades += 1
                    print(f"{Fore.RED}🔴 تم تنفيذ أمر بيع:{Style.RESET_ALL}")
                    print(f"   {Fore.CYAN}{symbol}{Style.RESET_ALL} @ ${current_price:.2f}\n")
                    return True
        return False
    
    def scan_and_trade(self):
        """مسح السوق وتنفيذ الصفقات تلقائياً"""
        self.scan_count += 1
        print(f"{Fore.YELLOW}🔍 المسح #{self.scan_count} - {datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}\n")
        
        buy_opportunities = []
        sell_signals = []
        
        for symbol in self.watchlist:
            try:
                print(f"   📊 {symbol}...", end=" ")
                
                # التحليل
                analyzer = TechnicalAnalyzer(symbol, period="3mo")
                analyzer.fetch_data()
                analyzer.calculate_all_indicators()
                
                signal = self.strategy.generate_signal(analyzer)
                latest = analyzer.get_latest_values()
                
                # معالجة الإشارات
                if signal['action'] == 'BUY' and signal['confidence'] >= self.min_confidence:
                    print(f"{Fore.GREEN}✅ شراء ({signal['confidence']:.0f}%){Style.RESET_ALL}")
                    buy_opportunities.append((symbol, signal, latest))
                    self.total_signals += 1
                
                elif signal['action'] == 'SELL' and signal['confidence'] >= self.min_confidence:
                    print(f"{Fore.RED}❌ بيع ({signal['confidence']:.0f}%){Style.RESET_ALL}")
                    sell_signals.append((symbol, signal))
                    self.total_signals += 1
                
                else:
                    print(f"{Fore.WHITE}⚪ {signal['action']}{Style.RESET_ALL}")
                
                time.sleep(0.3)  # تجنب تجاوز حدود API
                
            except Exception as e:
                print(f"{Fore.RED}❌ خطأ{Style.RESET_ALL}")
                continue
        
        print()
        
        # تنفيذ أوامر البيع أولاً
        if sell_signals and self.auto_close:
            print(f"{Fore.RED}{'='*90}")
            print(f"{'🔴 تنفيذ أوامر البيع':^90}")
            print(f"{'='*90}{Style.RESET_ALL}\n")
            
            for symbol, signal in sell_signals:
                self.execute_sell(symbol, signal)
        
        # تنفيذ أوامر الشراء
        if buy_opportunities:
            print(f"{Fore.GREEN}{'='*90}")
            print(f"{'🟢 تنفيذ أوامر الشراء':^90}")
            print(f"{'='*90}{Style.RESET_ALL}\n")
            
            # ترتيب حسب الثقة
            buy_opportunities.sort(key=lambda x: x[1]['confidence'], reverse=True)
            
            for symbol, signal, latest in buy_opportunities:
                # التحقق من إمكانية التداول
                if not self.risk_manager.can_trade():
                    print(f"{Fore.YELLOW}⚠️  تم الوصول للحد الأقصى من الصفقات{Style.RESET_ALL}\n")
                    break
                
                # التحقق من عدم وجود مركز مفتوح
                if symbol not in self.risk_manager.positions:
                    self.execute_buy(symbol, signal, latest)
                else:
                    print(f"{Fore.YELLOW}⚠️  {symbol} لديه مركز مفتوح بالفعل{Style.RESET_ALL}\n")
    
    def update_positions(self):
        """تحديث المراكز المفتوحة"""
        if not self.risk_manager.positions:
            return
        
        print(f"{Fore.CYAN}{'='*90}")
        print(f"{'📈 تحديث المراكز المفتوحة':^90}")
        print(f"{'='*90}{Style.RESET_ALL}\n")
        
        current_prices = {}
        
        for symbol in list(self.risk_manager.positions.keys()):
            try:
                price = self.get_current_price(symbol)
                if price:
                    current_prices[symbol] = price
                    position = self.risk_manager.positions[symbol]
                    position.update_price(price)
                    
                    pl = position.get_profit_loss()
                    pl_pct = position.get_profit_loss_percent()
                    
                    # تحديد اللون
                    if pl > 0:
                        color = Fore.GREEN
                        emoji = "🟢"
                    elif pl < 0:
                        color = Fore.RED
                        emoji = "🔴"
                    else:
                        color = Fore.WHITE
                        emoji = "⚪"
                    
                    print(f"{emoji} {Fore.CYAN}{symbol}{Style.RESET_ALL}: "
                          f"${price:.2f} | "
                          f"ربح/خسارة: {color}{pl:+.2f}$ ({pl_pct:+.2f}%){Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"❌ خطأ في {symbol}: {str(e)}")
        
        print()
        
        # تحديث وإغلاق تلقائي
        self.risk_manager.update_positions(current_prices)
    
    def show_statistics(self):
        """عرض الإحصائيات"""
        summary = self.risk_manager.get_portfolio_summary()
        
        print(f"\n{Fore.CYAN}{'='*90}")
        print(f"{'📊 إحصائيات البوت':^90}")
        print(f"{'='*90}{Style.RESET_ALL}\n")
        
        # إحصائيات المحفظة
        return_color = Fore.GREEN if summary['total_return'] >= 0 else Fore.RED
        
        print(f"💰 رأس المال الأولي:    ${summary['initial_capital']:>12,.2f}")
        print(f"💵 رأس المال الحالي:    ${summary['current_capital']:>12,.2f}")
        print(f"📈 قيمة المراكز:         ${summary['open_positions_value']:>12,.2f}")
        print(f"💎 القيمة الإجمالية:     ${summary['total_value']:>12,.2f}")
        print(f"{return_color}📊 العائد:               {summary['total_return']:>12.2f}%{Style.RESET_ALL}")
        
        print()
        
        # إحصائيات التداول
        win_rate_color = Fore.GREEN if summary['win_rate'] >= 50 else Fore.RED
        
        print(f"🔢 عدد المسحات:          {self.scan_count:>12}")
        print(f"📡 إجمالي الإشارات:      {self.total_signals:>12}")
        print(f"✅ صفقات منفذة:          {self.executed_trades:>12}")
        print(f"⏭️  صفقات متجاوزة:       {self.skipped_trades:>12}")
        print(f"📈 إجمالي الصفقات:       {summary['total_trades']:>12}")
        print(f"🟢 صفقات رابحة:          {summary['winning_trades']:>12}")
        print(f"🔴 صفقات خاسرة:          {summary['losing_trades']:>12}")
        print(f"{win_rate_color}🎯 معدل النجاح:          {summary['win_rate']:>12.1f}%{Style.RESET_ALL}")
        
        # المراكز المفتوحة
        if self.risk_manager.positions:
            print(f"\n{Fore.YELLOW}📌 المراكز المفتوحة ({len(self.risk_manager.positions)}):{Style.RESET_ALL}")
            for symbol, pos in self.risk_manager.positions.items():
                pl = pos.get_profit_loss()
                pl_pct = pos.get_profit_loss_percent()
                emoji = "🟢" if pl > 0 else "🔴" if pl < 0 else "⚪"
                print(f"   {emoji} {symbol}: {pos.quantity:.0f} سهم @ ${pos.entry_price:.2f} "
                      f"(الحالي: ${pos.current_price:.2f}, ربح/خسارة: {pl:+.2f}$)")
        
        print(f"\n{Fore.CYAN}{'='*90}{Style.RESET_ALL}\n")
    
    def run_continuous(self, interval_minutes: int = 5, max_scans: int = None):
        """التشغيل المستمر"""
        self.print_header()
        
        if self.simulation_mode:
            print(f"{Fore.YELLOW}⚠️  وضع المحاكاة: لا يتم تنفيذ صفقات حقيقية{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}⚠️⚠️⚠️ وضع التداول الحقيقي - يتم تنفيذ صفقات بأموال حقيقية! ⚠️⚠️⚠️{Style.RESET_ALL}\n")
            confirm = input(f"{Fore.YELLOW}هل أنت متأكد؟ اكتب 'نعم' للمتابعة: {Style.RESET_ALL}")
            if confirm != "نعم":
                print(f"{Fore.RED}تم الإلغاء{Style.RESET_ALL}")
                return
        
        print(f"{Fore.GREEN}🚀 البوت يعمل الآن...{Style.RESET_ALL}")
        print(f"⏱️  الفاصل الزمني: {interval_minutes} دقيقة")
        print(f"📊 عدد الأسهم: {len(self.watchlist)}")
        print(f"🎯 الحد الأدنى للثقة: {self.min_confidence}%")
        print(f"⏹️  للإيقاف: اضغط Ctrl+C\n")
        print("=" * 90 + "\n")
        
        try:
            scan_num = 0
            while True:
                scan_num += 1
                
                # المسح والتداول
                self.scan_and_trade()
                
                # تحديث المراكز
                self.update_positions()
                
                # عرض الإحصائيات
                self.show_statistics()
                
                # التحقق من الحد الأقصى
                if max_scans and scan_num >= max_scans:
                    print(f"{Fore.YELLOW}✅ تم الوصول للحد الأقصى من المسحات ({max_scans}){Style.RESET_ALL}")
                    break
                
                # الانتظار
                next_scan = datetime.now() + timedelta(minutes=interval_minutes)
                print(f"{Fore.YELLOW}⏰ المسح التالي في: {next_scan.strftime('%H:%M:%S')}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}⏹️  للإيقاف: Ctrl+C{Style.RESET_ALL}\n")
                
                time.sleep(interval_minutes * 60)
        
        except KeyboardInterrupt:
            print(f"\n\n{Fore.RED}⏹️  إيقاف البوت بواسطة المستخدم{Style.RESET_ALL}\n")
        
        finally:
            self.shutdown()
    
    def shutdown(self):
        """إيقاف البوت"""
        print(f"{Fore.CYAN}{'='*90}")
        print(f"{'📊 تقرير نهائي':^90}")
        print(f"{'='*90}{Style.RESET_ALL}\n")
        
        # إغلاق المراكز المفتوحة
        if self.risk_manager.positions:
            print(f"{Fore.YELLOW}📌 المراكز المفتوحة ({len(self.risk_manager.positions)}):{Style.RESET_ALL}")
            for symbol in list(self.risk_manager.positions.keys()):
                pos = self.risk_manager.positions[symbol]
                print(f"   • {symbol}: {pos.quantity:.0f} سهم @ ${pos.entry_price:.2f}")
            
            close_all = input(f"\n{Fore.YELLOW}هل تريد إغلاق جميع المراكز؟ (نعم/لا): {Style.RESET_ALL}")
            if close_all.lower() in ['نعم', 'yes', 'y']:
                print(f"\n{Fore.RED}🔴 إغلاق جميع المراكز...{Style.RESET_ALL}\n")
                for symbol in list(self.risk_manager.positions.keys()):
                    try:
                        price = self.get_current_price(symbol)
                        if price:
                            self.risk_manager.close_position(symbol, price, "إغلاق يدوي")
                    except Exception as e:
                        print(f"❌ خطأ في إغلاق {symbol}: {str(e)}")
        
        # الملخص النهائي
        self.show_statistics()
        
        print(f"{Fore.GREEN}✅ تم إيقاف البوت بنجاح{Style.RESET_ALL}\n")


def main():
    """الدالة الرئيسية"""
    print(f"{Fore.CYAN}")
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║      🤖 بوت التداول التلقائي - يشتري ويبيع تلقائياً 🤖     ║
    ║                                                               ║
    ║          يدعم الأسهم الأمريكية والسعودية                    ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    print(Style.RESET_ALL)
    
    # إنشاء البوت
    bot = AutoTradingBot(initial_capital=10000)
    
    print(f"{Fore.CYAN}اختر وضع التشغيل:{Style.RESET_ALL}")
    print("1. تشغيل مستمر (فحص كل 5 دقائق)")
    print("2. تشغيل مستمر (فحص كل دقيقة)")
    print("3. فحص واحد فقط")
    print("4. 3 فحوصات للتجربة")
    
    choice = input(f"\n{Fore.GREEN}اختر (1-4): {Style.RESET_ALL}").strip()
    
    if choice == "1":
        bot.run_continuous(interval_minutes=5)
    elif choice == "2":
        bot.run_continuous(interval_minutes=1)
    elif choice == "3":
        bot.run_continuous(interval_minutes=1, max_scans=1)
    elif choice == "4":
        bot.run_continuous(interval_minutes=1, max_scans=3)
    else:
        print(f"{Fore.RED}اختيار غير صحيح!{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
