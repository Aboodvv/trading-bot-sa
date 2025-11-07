"""
بوت تداول تلقائي مبسط - يشتري ويبيع
"""

import sys
import time
from datetime import datetime
from technical_analysis import analyze_stock
from trading_strategy import CompositeStrategy
from risk_management import RiskManager
import config

# تجنب مشاكل الترميز
sys.stdout.reconfigure(encoding='utf-8')

class SimpleTradingBot:
    def __init__(self):
        self.rm = RiskManager(10000, max_risk_per_trade=0.02, max_positions=5)
        self.strategy = CompositeStrategy()
        self.watchlist = config.WATCHLIST
        
    def run_once(self):
        """فحص واحد وتداول"""
        print("\n" + "="*70)
        print("بوت التداول التلقائي - يشتري ويبيع تلقائيا")
        print("="*70)
        print(f"الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"راس المال: ${self.rm.current_capital:,.2f}")
        print("="*70 + "\n")
        
        print("جاري تحليل الاسهم...\n")
        
        opportunities = []
        
        # تحليل كل سهم
        for symbol in self.watchlist[:8]:  # أول 8 أسهم فقط
            try:
                print(f"  تحليل {symbol}...", end=" ")
                
                result = analyze_stock(symbol, period="3mo")
                
                if "شراء" in result['recommendation'] and result['score'] >= 2:
                    print(f"فرصة شراء! (نقاط: {result['score']})")
                    opportunities.append({
                        'symbol': symbol,
                        'price': result['analysis']['price'],
                        'score': result['score'],
                        'rsi': result['analysis']['rsi_value']
                    })
                else:
                    print("محايد")
                
                time.sleep(0.3)
                
            except Exception as e:
                print(f"خطأ: {str(e)[:30]}")
        
        # تنفيذ الشراء
        if opportunities:
            print("\n" + "="*70)
            print(f"تم اكتشاف {len(opportunities)} فرصة!")
            print("="*70 + "\n")
            
            for opp in opportunities[:3]:  # أفضل 3 فرص
                if self.rm.can_trade():
                    symbol = opp['symbol']
                    price = opp['price']
                    stop_loss = price * 0.98
                    take_profit = price * 1.05
                    
                    size = self.rm.calculate_position_size(symbol, price, stop_loss)
                    
                    if size > 0:
                        print(f"\nشراء {symbol}:")
                        print(f"  السعر: ${price:.2f}")
                        print(f"  الكمية: {size} سهم")
                        print(f"  وقف الخسارة: ${stop_loss:.2f}")
                        print(f"  جني الارباح: ${take_profit:.2f}")
                        
                        success = self.rm.open_position(
                            symbol, size, price, stop_loss, take_profit
                        )
                        
                        if success:
                            print(f"  تم فتح المركز!")
        else:
            print("\nلا توجد فرص شراء حاليا")
        
        # ملخص
        print("\n" + "="*70)
        print("ملخص المحفظة")
        print("="*70)
        
        summary = self.rm.get_portfolio_summary()
        print(f"\nراس المال الحالي: ${summary['current_capital']:,.2f}")
        print(f"قيمة المراكز: ${summary['open_positions_value']:,.2f}")
        print(f"العائد: ${summary['total_return_amount']:,.2f} ({summary['total_return']:.2f}%)")
        print(f"عدد الصفقات: {summary['total_trades']}")
        print(f"معدل النجاح: {summary['win_rate']:.1f}%")
        print(f"مراكز مفتوحة: {summary['open_positions']}/{self.rm.max_positions}")
        
        if self.rm.positions:
            print("\nالمراكز المفتوحة:")
            for symbol, pos in self.rm.positions.items():
                pl = pos.get_profit_loss()
                pl_pct = pos.get_profit_loss_percent()
                emoji = "+" if pl > 0 else "-"
                print(f"  {emoji} {symbol}: {pos.quantity} سهم @ ${pos.entry_price:.2f}")
                print(f"     ربح/خسارة: ${pl:.2f} ({pl_pct:+.2f}%)")
        
        print("\n" + "="*70 + "\n")

# تشغيل
if __name__ == "__main__":
    bot = SimpleTradingBot()
    bot.run_once()
