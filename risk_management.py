"""
نظام إدارة المخاطر المتقدم
يحمي رأس المال ويدير المراكز بذكاء
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
from dataclasses import dataclass


@dataclass
class Position:
    """فئة لتمثيل مركز تداول"""
    symbol: str
    quantity: float
    entry_price: float
    entry_time: datetime
    stop_loss: float = None
    take_profit: float = None
    current_price: float = None
    
    def update_price(self, new_price: float):
        """تحديث السعر الحالي"""
        self.current_price = new_price
    
    def get_profit_loss(self) -> float:
        """حساب الربح/الخسارة"""
        if self.current_price:
            return (self.current_price - self.entry_price) * self.quantity
        return 0
    
    def get_profit_loss_percent(self) -> float:
        """حساب نسبة الربح/الخسارة"""
        if self.current_price:
            return ((self.current_price - self.entry_price) / self.entry_price) * 100
        return 0
    
    def should_stop_loss(self) -> bool:
        """التحقق من وقف الخسارة"""
        if self.stop_loss and self.current_price:
            return self.current_price <= self.stop_loss
        return False
    
    def should_take_profit(self) -> bool:
        """التحقق من جني الأرباح"""
        if self.take_profit and self.current_price:
            return self.current_price >= self.take_profit
        return False


class RiskManager:
    """مدير المخاطر الشامل"""
    
    def __init__(self, initial_capital: float, max_risk_per_trade: float = 0.02,
                 max_portfolio_risk: float = 0.1, max_positions: int = 5):
        """
        تهيئة مدير المخاطر
        
        :param initial_capital: رأس المال الأولي
        :param max_risk_per_trade: أقصى مخاطرة لكل صفقة (نسبة مئوية)
        :param max_portfolio_risk: أقصى مخاطرة للمحفظة (نسبة مئوية)
        :param max_positions: أقصى عدد للمراكز المفتوحة
        """
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.max_risk_per_trade = max_risk_per_trade
        self.max_portfolio_risk = max_portfolio_risk
        self.max_positions = max_positions
        
        self.positions: Dict[str, Position] = {}
        self.closed_positions: List[Position] = []
        self.trade_history: List[Dict] = []
        
        # إحصائيات التداول
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_profit = 0
        self.total_loss = 0
        self.max_drawdown = 0
        self.peak_capital = initial_capital
        
        # حماية من الخسائر الكبيرة
        self.daily_loss = 0
        self.max_daily_loss = max_portfolio_risk
        self.last_reset_date = datetime.now().date()
    
    def reset_daily_counters(self):
        """إعادة تعيين العدادات اليومية"""
        current_date = datetime.now().date()
        if current_date > self.last_reset_date:
            self.daily_loss = 0
            self.last_reset_date = current_date
    
    def can_trade(self) -> bool:
        """التحقق من إمكانية التداول"""
        self.reset_daily_counters()
        
        # التحقق من عدد المراكز المفتوحة
        if len(self.positions) >= self.max_positions:
            return False
        
        # التحقق من الخسارة اليومية
        if abs(self.daily_loss / self.current_capital) >= self.max_daily_loss:
            return False
        
        return True
    
    def calculate_position_size(self, symbol: str, entry_price: float, 
                               stop_loss_price: float) -> float:
        """
        حساب حجم المركز المناسب
        
        :param symbol: رمز السهم
        :param entry_price: سعر الدخول
        :param stop_loss_price: سعر وقف الخسارة
        :return: عدد الأسهم
        """
        if not self.can_trade():
            return 0
        
        # حساب المخاطرة المالية لكل سهم
        risk_per_share = abs(entry_price - stop_loss_price)
        
        if risk_per_share == 0:
            return 0
        
        # حساب المبلغ المخاطر به
        risk_amount = self.current_capital * self.max_risk_per_trade
        
        # حساب عدد الأسهم
        position_size = risk_amount / risk_per_share
        
        # التأكد من عدم تجاوز رأس المال المتاح
        max_shares_by_capital = (self.current_capital * 0.9) / entry_price
        position_size = min(position_size, max_shares_by_capital)
        
        return int(position_size)
    
    def calculate_stop_loss(self, entry_price: float, atr: float = None, 
                           percent: float = 0.02) -> float:
        """
        حساب مستوى وقف الخسارة
        
        :param entry_price: سعر الدخول
        :param atr: متوسط المدى الحقيقي (ATR)
        :param percent: نسبة وقف الخسارة الافتراضية
        :return: سعر وقف الخسارة
        """
        if atr:
            # استخدام ATR لوقف خسارة ديناميكي
            stop_loss = entry_price - (2 * atr)
        else:
            # وقف خسارة بنسبة ثابتة
            stop_loss = entry_price * (1 - percent)
        
        return stop_loss
    
    def calculate_take_profit(self, entry_price: float, stop_loss: float,
                             risk_reward_ratio: float = 2.0) -> float:
        """
        حساب مستوى جني الأرباح
        
        :param entry_price: سعر الدخول
        :param stop_loss: سعر وقف الخسارة
        :param risk_reward_ratio: نسبة المخاطرة إلى العائد
        :return: سعر جني الأرباح
        """
        risk = entry_price - stop_loss
        take_profit = entry_price + (risk * risk_reward_ratio)
        return take_profit
    
    def open_position(self, symbol: str, quantity: float, entry_price: float,
                     stop_loss: float = None, take_profit: float = None) -> bool:
        """
        فتح مركز جديد
        
        :param symbol: رمز السهم
        :param quantity: عدد الأسهم
        :param entry_price: سعر الدخول
        :param stop_loss: سعر وقف الخسارة
        :param take_profit: سعر جني الأرباح
        :return: True إذا تم فتح المركز بنجاح
        """
        if not self.can_trade():
            print(f"❌ لا يمكن فتح مركز جديد: تجاوز الحدود المسموح بها")
            return False
        
        if symbol in self.positions:
            print(f"❌ يوجد مركز مفتوح بالفعل لـ {symbol}")
            return False
        
        # حساب التكلفة
        cost = quantity * entry_price
        
        if cost > self.current_capital * 0.9:
            print(f"❌ رأس المال غير كافٍ لفتح المركز")
            return False
        
        # إنشاء المركز
        position = Position(
            symbol=symbol,
            quantity=quantity,
            entry_price=entry_price,
            entry_time=datetime.now(),
            stop_loss=stop_loss,
            take_profit=take_profit,
            current_price=entry_price
        )
        
        self.positions[symbol] = position
        self.current_capital -= cost
        
        # تسجيل الصفقة
        self.trade_history.append({
            'timestamp': datetime.now(),
            'action': 'OPEN',
            'symbol': symbol,
            'quantity': quantity,
            'price': entry_price,
            'cost': cost,
            'stop_loss': stop_loss,
            'take_profit': take_profit
        })
        
        print(f"✅ تم فتح مركز {symbol}: {quantity} سهم @ ${entry_price:.2f}")
        return True
    
    def close_position(self, symbol: str, exit_price: float, reason: str = "") -> bool:
        """
        إغلاق مركز
        
        :param symbol: رمز السهم
        :param exit_price: سعر الخروج
        :param reason: سبب الإغلاق
        :return: True إذا تم إغلاق المركز بنجاح
        """
        if symbol not in self.positions:
            print(f"❌ لا يوجد مركز مفتوح لـ {symbol}")
            return False
        
        position = self.positions[symbol]
        
        # حساب الربح/الخسارة
        proceeds = position.quantity * exit_price
        cost = position.quantity * position.entry_price
        profit_loss = proceeds - cost
        profit_loss_percent = (profit_loss / cost) * 100
        
        # تحديث رأس المال
        self.current_capital += proceeds
        
        # تحديث الإحصائيات
        self.total_trades += 1
        if profit_loss > 0:
            self.winning_trades += 1
            self.total_profit += profit_loss
        else:
            self.losing_trades += 1
            self.total_loss += abs(profit_loss)
            self.daily_loss += abs(profit_loss)
        
        # تحديث أقصى انخفاض
        if self.current_capital > self.peak_capital:
            self.peak_capital = self.current_capital
        
        drawdown = (self.peak_capital - self.current_capital) / self.peak_capital
        self.max_drawdown = max(self.max_drawdown, drawdown)
        
        # تسجيل الصفقة
        self.trade_history.append({
            'timestamp': datetime.now(),
            'action': 'CLOSE',
            'symbol': symbol,
            'quantity': position.quantity,
            'entry_price': position.entry_price,
            'exit_price': exit_price,
            'profit_loss': profit_loss,
            'profit_loss_percent': profit_loss_percent,
            'reason': reason,
            'holding_time': (datetime.now() - position.entry_time).total_seconds() / 3600
        })
        
        # نقل المركز للمراكز المغلقة
        self.closed_positions.append(position)
        del self.positions[symbol]
        
        emoji = "🟢" if profit_loss > 0 else "🔴"
        print(f"{emoji} تم إغلاق مركز {symbol}: ربح/خسارة ${profit_loss:.2f} ({profit_loss_percent:.2f}%) - {reason}")
        
        return True
    
    def update_positions(self, prices: Dict[str, float]):
        """
        تحديث جميع المراكز المفتوحة
        
        :param prices: قاموس بأسعار الأسهم الحالية
        """
        positions_to_close = []
        
        for symbol, position in self.positions.items():
            if symbol in prices:
                position.update_price(prices[symbol])
                
                # التحقق من وقف الخسارة
                if position.should_stop_loss():
                    positions_to_close.append((symbol, prices[symbol], "وقف خسارة"))
                
                # التحقق من جني الأرباح
                elif position.should_take_profit():
                    positions_to_close.append((symbol, prices[symbol], "جني أرباح"))
        
        # إغلاق المراكز المطلوبة
        for symbol, price, reason in positions_to_close:
            self.close_position(symbol, price, reason)
    
    def get_portfolio_summary(self) -> Dict:
        """الحصول على ملخص المحفظة"""
        
        # حساب قيمة المراكز المفتوحة
        open_positions_value = sum(
            pos.current_price * pos.quantity if pos.current_price else pos.entry_price * pos.quantity
            for pos in self.positions.values()
        )
        
        total_value = self.current_capital + open_positions_value
        total_return = ((total_value - self.initial_capital) / self.initial_capital) * 100
        
        win_rate = (self.winning_trades / self.total_trades * 100) if self.total_trades > 0 else 0
        
        avg_profit = self.total_profit / self.winning_trades if self.winning_trades > 0 else 0
        avg_loss = self.total_loss / self.losing_trades if self.losing_trades > 0 else 0
        
        profit_factor = self.total_profit / self.total_loss if self.total_loss > 0 else 0
        
        return {
            'initial_capital': self.initial_capital,
            'current_capital': self.current_capital,
            'open_positions_value': open_positions_value,
            'total_value': total_value,
            'total_return': total_return,
            'total_return_amount': total_value - self.initial_capital,
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'win_rate': win_rate,
            'avg_profit': avg_profit,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'max_drawdown': self.max_drawdown * 100,
            'open_positions': len(self.positions),
            'daily_loss': self.daily_loss
        }
    
    def print_portfolio_summary(self):
        """طباعة ملخص المحفظة"""
        summary = self.get_portfolio_summary()
        
        print("\n" + "=" * 70)
        print("📊 ملخص المحفظة")
        print("=" * 70)
        print(f"رأس المال الأولي:        ${summary['initial_capital']:,.2f}")
        print(f"رأس المال الحالي:        ${summary['current_capital']:,.2f}")
        print(f"قيمة المراكز المفتوحة:    ${summary['open_positions_value']:,.2f}")
        print(f"القيمة الإجمالية:         ${summary['total_value']:,.2f}")
        print(f"العائد الإجمالي:          ${summary['total_return_amount']:,.2f} ({summary['total_return']:.2f}%)")
        print(f"\nعدد الصفقات:            {summary['total_trades']}")
        print(f"صفقات رابحة:            {summary['winning_trades']}")
        print(f"صفقات خاسرة:            {summary['losing_trades']}")
        print(f"معدل النجاح:            {summary['win_rate']:.2f}%")
        print(f"متوسط الربح:            ${summary['avg_profit']:.2f}")
        print(f"متوسط الخسارة:          ${summary['avg_loss']:.2f}")
        print(f"عامل الربح:             {summary['profit_factor']:.2f}")
        print(f"أقصى انخفاض:            {summary['max_drawdown']:.2f}%")
        print(f"مراكز مفتوحة:           {summary['open_positions']}/{self.max_positions}")
        print("=" * 70)
        
        # طباعة المراكز المفتوحة
        if self.positions:
            print("\n📈 المراكز المفتوحة:")
            for symbol, pos in self.positions.items():
                pl = pos.get_profit_loss()
                pl_pct = pos.get_profit_loss_percent()
                emoji = "🟢" if pl > 0 else "🔴" if pl < 0 else "⚪"
                print(f"   {emoji} {symbol}: {pos.quantity:.0f} أسهم @ ${pos.entry_price:.2f}")
                print(f"      السعر الحالي: ${pos.current_price:.2f}")
                print(f"      ربح/خسارة: ${pl:.2f} ({pl_pct:.2f}%)")
                if pos.stop_loss:
                    print(f"      وقف الخسارة: ${pos.stop_loss:.2f}")
                if pos.take_profit:
                    print(f"      جني الأرباح: ${pos.take_profit:.2f}")


if __name__ == "__main__":
    # مثال على الاستخدام
    print("اختبار نظام إدارة المخاطر\n")
    
    # إنشاء مدير مخاطر برأس مال 10,000$
    rm = RiskManager(initial_capital=10000, max_risk_per_trade=0.02, max_positions=3)
    
    # حساب حجم المركز
    entry_price = 150.0
    stop_loss = 147.0
    position_size = rm.calculate_position_size("AAPL", entry_price, stop_loss)
    take_profit = rm.calculate_take_profit(entry_price, stop_loss, 2.0)
    
    print(f"حجم المركز المقترح: {position_size} سهم")
    print(f"وقف الخسارة: ${stop_loss:.2f}")
    print(f"جني الأرباح: ${take_profit:.2f}\n")
    
    # فتح مركز
    rm.open_position("AAPL", position_size, entry_price, stop_loss, take_profit)
    
    # تحديث السعر
    rm.update_positions({"AAPL": 152.0})
    
    # طباعة الملخص
    rm.print_portfolio_summary()
