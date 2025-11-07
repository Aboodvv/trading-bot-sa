"""
محلل تقني متقدم للأسهم
يحتوي على مؤشرات فنية احترافية لتحليل الأسهم
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import ta
from typing import Dict, List, Tuple


class TechnicalAnalyzer:
    """محلل تقني شامل للأسهم"""
    
    def __init__(self, symbol: str, period: str = "1y", interval: str = "1d"):
        """
        تهيئة المحلل
        :param symbol: رمز السهم (مثل: AAPL)
        :param period: الفترة الزمنية (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        :param interval: الفاصل الزمني (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        """
        self.symbol = symbol
        self.period = period
        self.interval = interval
        self.data = None
        self.indicators = {}
        
    def fetch_data(self) -> pd.DataFrame:
        """جلب بيانات السهم"""
        try:
            ticker = yf.Ticker(self.symbol)
            self.data = ticker.history(period=self.period, interval=self.interval)
            
            if self.data.empty:
                raise ValueError(f"لا توجد بيانات للسهم {self.symbol}")
            
            return self.data
        except Exception as e:
            raise Exception(f"خطأ في جلب البيانات: {str(e)}")
    
    def calculate_moving_averages(self) -> Dict[str, pd.Series]:
        """حساب المتوسطات المتحركة"""
        if self.data is None:
            raise ValueError("يجب جلب البيانات أولاً")
        
        mas = {
            'SMA_20': ta.trend.sma_indicator(self.data['Close'], window=20),
            'SMA_50': ta.trend.sma_indicator(self.data['Close'], window=50),
            'SMA_200': ta.trend.sma_indicator(self.data['Close'], window=200),
            'EMA_12': ta.trend.ema_indicator(self.data['Close'], window=12),
            'EMA_26': ta.trend.ema_indicator(self.data['Close'], window=26),
            'EMA_50': ta.trend.ema_indicator(self.data['Close'], window=50),
        }
        
        self.indicators.update(mas)
        return mas
    
    def calculate_rsi(self, period: int = 14) -> pd.Series:
        """حساب مؤشر القوة النسبية RSI"""
        if self.data is None:
            raise ValueError("يجب جلب البيانات أولاً")
        
        rsi = ta.momentum.rsi(self.data['Close'], window=period)
        self.indicators['RSI'] = rsi
        return rsi
    
    def calculate_macd(self) -> Dict[str, pd.Series]:
        """حساب MACD"""
        if self.data is None:
            raise ValueError("يجب جلب البيانات أولاً")
        
        macd = ta.trend.MACD(self.data['Close'])
        macd_dict = {
            'MACD': macd.macd(),
            'MACD_Signal': macd.macd_signal(),
            'MACD_Diff': macd.macd_diff()
        }
        
        self.indicators.update(macd_dict)
        return macd_dict
    
    def calculate_bollinger_bands(self, period: int = 20, std: int = 2) -> Dict[str, pd.Series]:
        """حساب نطاقات بولينجر"""
        if self.data is None:
            raise ValueError("يجب جلب البيانات أولاً")
        
        bb = ta.volatility.BollingerBands(self.data['Close'], window=period, window_dev=std)
        bb_dict = {
            'BB_High': bb.bollinger_hband(),
            'BB_Mid': bb.bollinger_mavg(),
            'BB_Low': bb.bollinger_lband(),
            'BB_Width': bb.bollinger_wband()
        }
        
        self.indicators.update(bb_dict)
        return bb_dict
    
    def calculate_stochastic(self) -> Dict[str, pd.Series]:
        """حساب مؤشر الاستوكاستك"""
        if self.data is None:
            raise ValueError("يجب جلب البيانات أولاً")
        
        stoch = ta.momentum.StochasticOscillator(
            self.data['High'],
            self.data['Low'],
            self.data['Close']
        )
        
        stoch_dict = {
            'Stoch_K': stoch.stoch(),
            'Stoch_D': stoch.stoch_signal()
        }
        
        self.indicators.update(stoch_dict)
        return stoch_dict
    
    def calculate_atr(self, period: int = 14) -> pd.Series:
        """حساب متوسط المدى الحقيقي ATR"""
        if self.data is None:
            raise ValueError("يجب جلب البيانات أولاً")
        
        atr = ta.volatility.average_true_range(
            self.data['High'],
            self.data['Low'],
            self.data['Close'],
            window=period
        )
        
        self.indicators['ATR'] = atr
        return atr
    
    def calculate_adx(self, period: int = 14) -> Dict[str, pd.Series]:
        """حساب مؤشر الاتجاه ADX"""
        if self.data is None:
            raise ValueError("يجب جلب البيانات أولاً")
        
        adx = ta.trend.ADXIndicator(
            self.data['High'],
            self.data['Low'],
            self.data['Close'],
            window=period
        )
        
        adx_dict = {
            'ADX': adx.adx(),
            'ADX_Pos': adx.adx_pos(),
            'ADX_Neg': adx.adx_neg()
        }
        
        self.indicators.update(adx_dict)
        return adx_dict
    
    def calculate_volume_indicators(self) -> Dict[str, pd.Series]:
        """حساب مؤشرات الحجم"""
        if self.data is None:
            raise ValueError("يجب جلب البيانات أولاً")
        
        volume_dict = {
            'Volume_SMA': ta.trend.sma_indicator(self.data['Volume'], window=20),
            'OBV': ta.volume.on_balance_volume(self.data['Close'], self.data['Volume']),
            'Volume_Ratio': self.data['Volume'] / ta.trend.sma_indicator(self.data['Volume'], window=20)
        }
        
        self.indicators.update(volume_dict)
        return volume_dict
    
    def calculate_all_indicators(self):
        """حساب جميع المؤشرات دفعة واحدة"""
        if self.data is None:
            self.fetch_data()
        
        self.calculate_moving_averages()
        self.calculate_rsi()
        self.calculate_macd()
        self.calculate_bollinger_bands()
        self.calculate_stochastic()
        self.calculate_atr()
        self.calculate_adx()
        self.calculate_volume_indicators()
        
        return self.indicators
    
    def get_latest_values(self) -> Dict:
        """الحصول على أحدث قيم المؤشرات"""
        if not self.indicators:
            self.calculate_all_indicators()
        
        latest = {
            'Symbol': self.symbol,
            'Timestamp': self.data.index[-1],
            'Close': self.data['Close'].iloc[-1],
            'Volume': self.data['Volume'].iloc[-1],
        }
        
        for key, value in self.indicators.items():
            if isinstance(value, pd.Series):
                latest[key] = value.iloc[-1] if not pd.isna(value.iloc[-1]) else None
        
        return latest
    
    def get_trend_analysis(self) -> Dict:
        """تحليل الاتجاه العام"""
        latest = self.get_latest_values()
        
        # تحليل الاتجاه بناءً على المتوسطات المتحركة
        price = latest['Close']
        sma_20 = latest.get('SMA_20')
        sma_50 = latest.get('SMA_50')
        sma_200 = latest.get('SMA_200')
        
        trend = "محايد"
        strength = 0
        
        if sma_20 and sma_50 and sma_200:
            if price > sma_20 > sma_50 > sma_200:
                trend = "صاعد قوي"
                strength = 3
            elif price > sma_20 > sma_50:
                trend = "صاعد"
                strength = 2
            elif price > sma_20:
                trend = "صاعد ضعيف"
                strength = 1
            elif price < sma_20 < sma_50 < sma_200:
                trend = "هابط قوي"
                strength = -3
            elif price < sma_20 < sma_50:
                trend = "هابط"
                strength = -2
            elif price < sma_20:
                trend = "هابط ضعيف"
                strength = -1
        
        # تحليل RSI
        rsi = latest.get('RSI')
        rsi_signal = "محايد"
        if rsi:
            if rsi < 30:
                rsi_signal = "تشبع بيعي (فرصة شراء)"
            elif rsi > 70:
                rsi_signal = "تشبع شرائي (فرصة بيع)"
            elif 40 <= rsi <= 60:
                rsi_signal = "محايد"
        
        # تحليل MACD
        macd_signal = "محايد"
        macd = latest.get('MACD')
        macd_sig = latest.get('MACD_Signal')
        
        if macd and macd_sig:
            if macd > macd_sig and macd > 0:
                macd_signal = "إيجابي قوي"
            elif macd > macd_sig:
                macd_signal = "إيجابي"
            elif macd < macd_sig and macd < 0:
                macd_signal = "سلبي قوي"
            elif macd < macd_sig:
                macd_signal = "سلبي"
        
        return {
            'trend': trend,
            'trend_strength': strength,
            'rsi_signal': rsi_signal,
            'macd_signal': macd_signal,
            'rsi_value': rsi,
            'price': price,
            'volume_ratio': latest.get('Volume_Ratio')
        }
    
    def generate_signals(self) -> Dict:
        """توليد إشارات تداول"""
        analysis = self.get_trend_analysis()
        latest = self.get_latest_values()
        
        buy_signals = []
        sell_signals = []
        score = 0
        
        # إشارات الشراء
        if analysis['rsi_value'] and analysis['rsi_value'] < 30:
            buy_signals.append("RSI في منطقة التشبع البيعي")
            score += 2
        
        if analysis['trend_strength'] > 0:
            buy_signals.append(f"الاتجاه {analysis['trend']}")
            score += analysis['trend_strength']
        
        if analysis['macd_signal'] in ["إيجابي", "إيجابي قوي"]:
            buy_signals.append(f"MACD {analysis['macd_signal']}")
            score += 1 if analysis['macd_signal'] == "إيجابي" else 2
        
        price = latest['Close']
        bb_low = latest.get('BB_Low')
        if bb_low and price < bb_low:
            buy_signals.append("السعر تحت النطاق السفلي لبولينجر")
            score += 1
        
        # إشارات البيع
        if analysis['rsi_value'] and analysis['rsi_value'] > 70:
            sell_signals.append("RSI في منطقة التشبع الشرائي")
            score -= 2
        
        if analysis['trend_strength'] < 0:
            sell_signals.append(f"الاتجاه {analysis['trend']}")
            score += analysis['trend_strength']
        
        if analysis['macd_signal'] in ["سلبي", "سلبي قوي"]:
            sell_signals.append(f"MACD {analysis['macd_signal']}")
            score -= 1 if analysis['macd_signal'] == "سلبي" else 2
        
        bb_high = latest.get('BB_High')
        if bb_high and price > bb_high:
            sell_signals.append("السعر فوق النطاق العلوي لبولينجر")
            score -= 1
        
        # تحديد التوصية
        if score >= 3:
            recommendation = "شراء قوي"
        elif score >= 1:
            recommendation = "شراء"
        elif score <= -3:
            recommendation = "بيع قوي"
        elif score <= -1:
            recommendation = "بيع"
        else:
            recommendation = "انتظار"
        
        return {
            'symbol': self.symbol,
            'recommendation': recommendation,
            'score': score,
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'analysis': analysis,
            'timestamp': datetime.now()
        }


def analyze_stock(symbol: str, period: str = "6mo") -> Dict:
    """
    دالة سريعة لتحليل سهم
    """
    analyzer = TechnicalAnalyzer(symbol, period=period)
    analyzer.fetch_data()
    analyzer.calculate_all_indicators()
    return analyzer.generate_signals()


if __name__ == "__main__":
    # مثال على الاستخدام
    print("=" * 60)
    print("محلل الأسهم الاحترافي")
    print("=" * 60)
    
    symbols = ["AAPL", "MSFT", "GOOGL"]
    
    for symbol in symbols:
        try:
            result = analyze_stock(symbol)
            print(f"\n📊 تحليل {result['symbol']}:")
            print(f"   التوصية: {result['recommendation']} (النقاط: {result['score']})")
            print(f"   السعر الحالي: ${result['analysis']['price']:.2f}")
            print(f"   RSI: {result['analysis']['rsi_value']:.2f} - {result['analysis']['rsi_signal']}")
            print(f"   الاتجاه: {result['analysis']['trend']}")
            
            if result['buy_signals']:
                print(f"   ✅ إشارات شراء: {', '.join(result['buy_signals'])}")
            
            if result['sell_signals']:
                print(f"   ❌ إشارات بيع: {', '.join(result['sell_signals'])}")
            
        except Exception as e:
            print(f"\n❌ خطأ في تحليل {symbol}: {str(e)}")
    
    print("\n" + "=" * 60)
