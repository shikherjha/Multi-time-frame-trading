from backtesting import Backtest
import backtesting
import multiprocessing
from binance.client import Client

from src.strategy.multi_tf import SmartStrategy
from src.utils.data import DataLoader
from config.config import Config
from backtesting.lib import Strategy
from src.backtesting.analyzer import Analyzer
class Backtesting:
    def __init__(self,symbol = Config.SYMBOL):
        self.symbol = symbol
        self.client = Client(Config.API_KEY,Config.API_SECRET,testnet=True)
        self.data_loader = DataLoader(self.client)
        
    def run(self,days_back=30):
        lookback = f"{days_back} days ago"

        df_15m = self.data_loader.load_data(self.symbol,Config.TIMEFRAME_ENTRY,lookback)
        df_1h = self.data_loader.load_data(self.symbol,Config.TIMEFRAME_CONFIRM,lookback)

        df = self.data_loader.merge_data(df_15m,df_1h)
        '''
        low_cutoff = df['Close'].quantile(0.01)
        high_cutoff = df['Close'].quantile(0.99)
        df_clean = df[(df['Close'] > low_cutoff) & (df['Close'] < high_cutoff)]
        df = df_clean
        '''
        bt = Backtest(df,SmartStrategy,cash=10000000,commission=0.001, finalize_trades=True)
        
        # Enable multiprocessing
        backtesting.Pool = multiprocessing.Pool
        '''
        stats, heatmap = bt.optimize(
            n1 = range(10,20,5),
            n2 = range(40,50,5),
            #rsi_period = range(14,21,2),
            rsi_lower_bound = range(20,50,5),
            rsi_upper_bound = range(60,70,5),
            #adx_period = range(14,21,2),
            adx_threshold = range(15,60,5),

            constraint = lambda p: p.n1 < p.n2 and p.rsi_lower_bound < p.rsi_upper_bound,
            maximize = 'Return [%]',
            return_heatmap = True
        )
        '''
        stats = bt.run()
        #Analyzer.print_summary(stats)
        #Analyzer.save_trades(stats)

        return bt,stats

    

        