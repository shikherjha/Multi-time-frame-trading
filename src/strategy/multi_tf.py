import talib
from backtesting.lib import crossover
from src.strategy.base import BaseStrategy
'''
class MTFStrategy(BaseStrategy):
    n1 = 20 #fast
    n2 = 50 #sceptical
    n3 = 200 #trend

    def init(self):
        self.sma_fast = self.I(talib.SMA,self.data.Close,self.n1)
        self.sma_sceptical = self.I(talib.SMA,self.data.Close,self.n2)
        self.sma_trend = self.I(talib.SMA,self.data.Close,self.n3)

    def next(self):
        price = self.data.Close[-1]
        trend_ma = self.sma_trend[-1]
        
        cross_up = crossover(self.sma_fast, self.sma_sceptical)
        cross_down = crossover(self.sma_sceptical,self.sma_fast)

        if cross_up and price > trend_ma:
            if not self.position: self.buy()
        elif cross_down:
            if self.position: self.position.close()

class RSIStrategy(BaseStrategy):
    n = 14
    lower_bound = 30
    upper_bound = 70
    def init(self):
        self.rsi  = self.I(talib.RSI,self.data.Close,self.n)

    def next(self):
        if crossover(self.rsi,self.lower_bound):
            if not self.position: self.buy()
        elif crossover(self.upper_bound,self.rsi):
            if self.position: self.position.close()
'''
class SmartStrategy(BaseStrategy):
    n1 = 10 #fast
    n2 = 45 #sceptical
    n3 = 200 #trend
    rsi_period = 14
    rsi_lower_bound = 25
    rsi_upper_bound = 65
    adx_period = 14
    adx_threshold = 55
    def init(self):
        self.sma_fast = self.I(talib.SMA,self.data.Close,self.n1)
        self.sma_sceptical = self.I(talib.SMA,self.data.Close,self.n2)
        self.sma_trend = self.I(talib.SMA,self.data.Close,self.n3)
        self.rsi  = self.I(talib.RSI,self.data.Close,self.rsi_period)
        self.adx = self.I(talib.ADX,self.data.High,self.data.Low,self.data.Close,self.adx_period)
    def next(self):
        price = self.data.Close[-1]
        trend_ma = self.sma_trend[-1]

        is_choppy = self.adx[-1] < self.adx_threshold
        
        cross_up = crossover(self.sma_fast, self.sma_sceptical)
        cross_down = crossover(self.sma_sceptical,self.sma_fast)

        if is_choppy:
            if crossover(self.rsi,self.rsi_lower_bound):
                if not self.position: self.buy()
            elif crossover(self.rsi_upper_bound,self.rsi):
                if self.position: self.position.close()
        elif not is_choppy:
            if cross_up and price > trend_ma:
                if not self.position: self.buy()
            elif cross_down:
                if self.position: self.position.close()
