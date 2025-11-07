"""
استراتيجيات التداول المتقدمة
يحتوي على عدة استراتيجيات للتداول الآلي
"""

from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd
from technical_analysis import TechnicalAnalyzer


class TradingStrategy:
    """استراتيجية التداول الأساسية"""
    
    def __init__(self, name: str):
        self.name = name
        
    def generate_signal(self, analyzer: TechnicalAnalyzer) -> Dict:
        """توليد إشارة تداول"""
        raise NotImplementedError("يجب تطبيق هذه الدالة في الفئة المشتقة")


class MomentumStrategy(TradingStrategy):
    """
    استراتيجية الزخم
    تعتمد على RSI و MACD لتحديد نقاط الدخول والخروج
    """
    
    def __init__(self):
        super().__init__("Momentum Strategy")
        self.rsi_oversold = 30
        self.rsi_overbought = 70
        
    def generate_signal(self, analyzer: TechnicalAnalyzer) -> Dict:
        latest = analyzer.get_latest_values()
        
        signal = {
            'strategy': self.name,
            'action': 'HOLD',
            'confidence': 0,
            'reasons': []
        }
        
        rsi = latest.get('RSI')
        macd = latest.get('MACD')
        macd_signal = latest.get('MACD_Signal')
        
        # شروط الشراء
        buy_score = 0
        if rsi and rsi < self.rsi_oversold:
            buy_score += 2
            signal['reasons'].append(f"RSI منخفض ({rsi:.2f})")
        
        if macd and macd_signal and macd > macd_signal:
            buy_score += 2
            signal['reasons'].append("MACD صاعد")
        
        # شروط البيع
        sell_score = 0
        if rsi and rsi > self.rsi_overbought:
            sell_score += 2
            signal['reasons'].append(f"RSI مرتفع ({rsi:.2f})")
        
        if macd and macd_signal and macd < macd_signal:
            sell_score += 2
            signal['reasons'].append("MACD هابط")
        
        # اتخاذ القرار
        if buy_score >= 3:
            signal['action'] = 'BUY'
            signal['confidence'] = min(buy_score * 25, 100)
        elif sell_score >= 3:
            signal['action'] = 'SELL'
            signal['confidence'] = min(sell_score * 25, 100)
        
        return signal


class TrendFollowingStrategy(TradingStrategy):
    """
    استراتيجية متابعة الاتجاه
    تعتمد على المتوسطات المتحركة
    """
    
    def __init__(self):
        super().__init__("Trend Following Strategy")
        
    def generate_signal(self, analyzer: TechnicalAnalyzer) -> Dict:
        latest = analyzer.get_latest_values()
        
        signal = {
            'strategy': self.name,
            'action': 'HOLD',
            'confidence': 0,
            'reasons': []
        }
        
        price = latest.get('Close')
        sma_20 = latest.get('SMA_20')
        sma_50 = latest.get('SMA_50')
        ema_12 = latest.get('EMA_12')
        ema_26 = latest.get('EMA_26')
        
        if not all([price, sma_20, sma_50, ema_12, ema_26]):
            return signal
        
        buy_score = 0
        sell_score = 0
        
        # إشارات الشراء
        if price > sma_20:
            buy_score += 1
            signal['reasons'].append("السعر فوق SMA 20")
        
        if price > sma_50:
            buy_score += 1
            signal['reasons'].append("السعر فوق SMA 50")
        
        if ema_12 > ema_26:
            buy_score += 2
            signal['reasons'].append("EMA 12 عبر فوق EMA 26")
        
        if sma_20 > sma_50:
            buy_score += 1
            signal['reasons'].append("SMA 20 فوق SMA 50 (اتجاه صاعد)")
        
        # إشارات البيع
        if price < sma_20:
            sell_score += 1
            signal['reasons'].append("السعر تحت SMA 20")
        
        if price < sma_50:
            sell_score += 1
            signal['reasons'].append("السعر تحت SMA 50")
        
        if ema_12 < ema_26:
            sell_score += 2
            signal['reasons'].append("EMA 12 عبر تحت EMA 26")
        
        if sma_20 < sma_50:
            sell_score += 1
            signal['reasons'].append("SMA 20 تحت SMA 50 (اتجاه هابط)")
        
        # اتخاذ القرار
        if buy_score >= 3 and buy_score > sell_score:
            signal['action'] = 'BUY'
            signal['confidence'] = min(buy_score * 20, 100)
        elif sell_score >= 3 and sell_score > buy_score:
            signal['action'] = 'SELL'
            signal['confidence'] = min(sell_score * 20, 100)
        
        return signal


class BreakoutStrategy(TradingStrategy):
    """
    استراتيجية الاختراق
    تعتمد على نطاقات بولينجر والحجم
    """
    
    def __init__(self):
        super().__init__("Breakout Strategy")
        
    def generate_signal(self, analyzer: TechnicalAnalyzer) -> Dict:
        latest = analyzer.get_latest_values()
        
        signal = {
            'strategy': self.name,
            'action': 'HOLD',
            'confidence': 0,
            'reasons': []
        }
        
        price = latest.get('Close')
        bb_high = latest.get('BB_High')
        bb_low = latest.get('BB_Low')
        bb_width = latest.get('BB_Width')
        volume_ratio = latest.get('Volume_Ratio')
        
        if not all([price, bb_high, bb_low, volume_ratio]):
            return signal
        
        # اختراق صعودي
        if price > bb_high and volume_ratio > 1.5:
            signal['action'] = 'BUY'
            signal['confidence'] = 75
            signal['reasons'].append(f"اختراق صعودي بحجم كبير (نسبة الحجم: {volume_ratio:.2f})")
        
        # اختراق هبوطي
        elif price < bb_low and volume_ratio > 1.5:
            signal['action'] = 'SELL'
            signal['confidence'] = 75
            signal['reasons'].append(f"اختراق هبوطي بحجم كبير (نسبة الحجم: {volume_ratio:.2f})")
        
        # نطاق ضيق (احتمال اختراق قريب)
        elif bb_width and bb_width < 0.1:
            signal['action'] = 'WATCH'
            signal['confidence'] = 50
            signal['reasons'].append("نطاق بولينجر ضيق - ترقب اختراق")
        
        return signal


class MeanReversionStrategy(TradingStrategy):
    """
    استراتيجية العودة للمتوسط
    تعتمد على افتراض أن السعر يعود للمتوسط
    """
    
    def __init__(self):
        super().__init__("Mean Reversion Strategy")
        
    def generate_signal(self, analyzer: TechnicalAnalyzer) -> Dict:
        latest = analyzer.get_latest_values()
        
        signal = {
            'strategy': self.name,
            'action': 'HOLD',
            'confidence': 0,
            'reasons': []
        }
        
        price = latest.get('Close')
        bb_high = latest.get('BB_High')
        bb_low = latest.get('BB_Low')
        bb_mid = latest.get('BB_Mid')
        rsi = latest.get('RSI')
        
        if not all([price, bb_high, bb_low, bb_mid, rsi]):
            return signal
        
        # شراء عند التشبع البيعي
        if price < bb_low and rsi < 30:
            signal['action'] = 'BUY'
            signal['confidence'] = 80
            signal['reasons'].append("السعر تحت النطاق السفلي مع RSI منخفض")
        
        # بيع عند التشبع الشرائي
        elif price > bb_high and rsi > 70:
            signal['action'] = 'SELL'
            signal['confidence'] = 80
            signal['reasons'].append("السعر فوق النطاق العلوي مع RSI مرتفع")
        
        # الاقتراب من المتوسط
        elif abs(price - bb_mid) / bb_mid < 0.01:
            signal['action'] = 'HOLD'
            signal['confidence'] = 60
            signal['reasons'].append("السعر قريب من المتوسط")
        
        return signal


class CompositeStrategy:
    """
    استراتيجية مركبة - تجمع عدة استراتيجيات
    """
    
    def __init__(self):
        self.strategies = [
            MomentumStrategy(),
            TrendFollowingStrategy(),
            BreakoutStrategy(),
            MeanReversionStrategy()
        ]
        
    def generate_signal(self, analyzer: TechnicalAnalyzer) -> Dict:
        """توليد إشارة مجمعة من جميع الاستراتيجيات"""
        
        signals = []
        for strategy in self.strategies:
            try:
                signal = strategy.generate_signal(analyzer)
                signals.append(signal)
            except Exception as e:
                print(f"خطأ في استراتيجية {strategy.name}: {str(e)}")
        
        # تجميع الإشارات
        buy_votes = sum(1 for s in signals if s['action'] == 'BUY')
        sell_votes = sum(1 for s in signals if s['action'] == 'SELL')
        hold_votes = sum(1 for s in signals if s['action'] == 'HOLD')
        
        total_buy_confidence = sum(s['confidence'] for s in signals if s['action'] == 'BUY')
        total_sell_confidence = sum(s['confidence'] for s in signals if s['action'] == 'SELL')
        
        # القرار النهائي
        composite_signal = {
            'strategy': 'Composite Strategy',
            'action': 'HOLD',
            'confidence': 0,
            'buy_votes': buy_votes,
            'sell_votes': sell_votes,
            'hold_votes': hold_votes,
            'details': signals
        }
        
        if buy_votes > sell_votes and buy_votes > hold_votes:
            composite_signal['action'] = 'BUY'
            composite_signal['confidence'] = min(total_buy_confidence / buy_votes if buy_votes > 0 else 0, 100)
        elif sell_votes > buy_votes and sell_votes > hold_votes:
            composite_signal['action'] = 'SELL'
            composite_signal['confidence'] = min(total_sell_confidence / sell_votes if sell_votes > 0 else 0, 100)
        else:
            composite_signal['action'] = 'HOLD'
            composite_signal['confidence'] = 50
        
        return composite_signal
    
    def get_detailed_analysis(self, symbol: str) -> Dict:
        """تحليل شامل مع جميع الاستراتيجيات"""
        analyzer = TechnicalAnalyzer(symbol)
        analyzer.fetch_data()
        analyzer.calculate_all_indicators()
        
        signal = self.generate_signal(analyzer)
        latest = analyzer.get_latest_values()
        
        return {
            'symbol': symbol,
            'timestamp': datetime.now(),
            'price': latest['Close'],
            'signal': signal,
            'technical_analysis': analyzer.generate_signals()
        }


def backtest_strategy(symbol: str, strategy: TradingStrategy, 
                     period: str = "1y", initial_capital: float = 10000) -> Dict:
    """
    اختبار خلفي لاستراتيجية على بيانات تاريخية
    """
    analyzer = TechnicalAnalyzer(symbol, period=period)
    analyzer.fetch_data()
    analyzer.calculate_all_indicators()
    
    capital = initial_capital
    shares = 0
    trades = []
    
    data = analyzer.data
    
    for i in range(50, len(data)):  # نبدأ من 50 لضمان وجود بيانات كافية للمؤشرات
        # إنشاء محلل مؤقت للبيانات حتى هذه النقطة
        temp_analyzer = TechnicalAnalyzer(symbol)
        temp_analyzer.data = data.iloc[:i+1]
        temp_analyzer.calculate_all_indicators()
        
        signal = strategy.generate_signal(temp_analyzer)
        current_price = data['Close'].iloc[i]
        
        # تنفيذ الإشارة
        if signal['action'] == 'BUY' and signal['confidence'] > 60 and shares == 0:
            shares = capital / current_price
            capital = 0
            trades.append({
                'date': data.index[i],
                'action': 'BUY',
                'price': current_price,
                'shares': shares,
                'confidence': signal['confidence']
            })
        
        elif signal['action'] == 'SELL' and signal['confidence'] > 60 and shares > 0:
            capital = shares * current_price
            trades.append({
                'date': data.index[i],
                'action': 'SELL',
                'price': current_price,
                'shares': shares,
                'value': capital,
                'confidence': signal['confidence']
            })
            shares = 0
    
    # إغلاق أي مركز مفتوح
    final_price = data['Close'].iloc[-1]
    if shares > 0:
        capital = shares * final_price
        shares = 0
    
    # حساب النتائج
    total_return = ((capital - initial_capital) / initial_capital) * 100
    num_trades = len([t for t in trades if t['action'] == 'BUY'])
    
    return {
        'strategy': strategy.name,
        'symbol': symbol,
        'initial_capital': initial_capital,
        'final_capital': capital,
        'total_return': total_return,
        'num_trades': num_trades,
        'trades': trades
    }


if __name__ == "__main__":
    # مثال على الاستخدام
    print("=" * 70)
    print("اختبار استراتيجيات التداول")
    print("=" * 70)
    
    symbol = "AAPL"
    
    # اختبار الاستراتيجية المركبة
    composite = CompositeStrategy()
    analysis = composite.get_detailed_analysis(symbol)
    
    print(f"\n📊 تحليل {analysis['symbol']}:")
    print(f"   السعر الحالي: ${analysis['price']:.2f}")
    print(f"\n🎯 الإشارة المركبة:")
    print(f"   الإجراء: {analysis['signal']['action']}")
    print(f"   الثقة: {analysis['signal']['confidence']:.1f}%")
    print(f"   أصوات الشراء: {analysis['signal']['buy_votes']}")
    print(f"   أصوات البيع: {analysis['signal']['sell_votes']}")
    print(f"   أصوات الانتظار: {analysis['signal']['hold_votes']}")
    
    print(f"\n📋 تفاصيل الاستراتيجيات:")
    for detail in analysis['signal']['details']:
        if detail['action'] != 'HOLD':
            print(f"\n   • {detail['strategy']}:")
            print(f"     الإجراء: {detail['action']} ({detail['confidence']:.1f}%)")
            if detail['reasons']:
                print(f"     الأسباب: {', '.join(detail['reasons'])}")
    
    print("\n" + "=" * 70)
