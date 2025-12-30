import time
import pandas as pd
from backtesting import Backtest
from binance.client import Client
from binance.enums import *

from config.config import Config
from src.strategy.multi_tf import SmartStrategy
from src.utils.data import DataLoader
from src.utils.logger import Setup_logger
from src.trading.exchange import Exchange

logger = Setup_logger("Executor")

class Executor:
    def __init__(self):
        self.client = Client(Config.API_KEY,Config.API_SECRET,testnet=Config.TESTNET)
        self.symbol = Config.SYMBOL
        self.exchange = Exchange()
        self.loader = DataLoader(self.client)
        self.quantity = Config.QUANTITY
        '''
        self.params = {
            "n1": 10,
            "n2": 45,
            "rsi_lower_bound" : 25,
            "rsi_upper_bound" : 65,
            "adx_threshold" : 55
        }
        logger.info(f"Params: {self.params}")
        '''
    
    def sync_state(self):
        logger.info("Syncing state...")
        try:
            df = self.loader.load_data(self.symbol,Config.TIMEFRAME_ENTRY,"5 day ago")
            '''
            low_cutoff = df['Close'].quantile(0.01)
            high_cutoff = df['Close'].quantile(0.99)
            df_clean = df[(df['Close'] > low_cutoff) & (df['Close'] < high_cutoff)]
            df = df_clean
            '''
            #mini backtest
            bt = Backtest(df,SmartStrategy,cash=10000000,commission=0.001,finalize_trades=False)
            stats = bt.run()
            strategy_inst = stats['_strategy']

            target_pos = strategy_inst.position.size > 0
            curr_qty = self.exchange.curr_pos()
            has_pos = curr_qty > 0.0001

            logger.info(f"Strategy: {'BUY/HOLD' if target_pos else 'SELL/FLAT'} | Wallet: {curr_qty:.4f}")

            if target_pos and not has_pos:
                logger.warning("Buy")
                self.exchange.execute(Client.SIDE_BUY,self.quantity)
            elif not target_pos and has_pos:
                logger.warning(f"Sell Signal - Closing Entire Position ({curr_qty})")
                qty_to_close = round(curr_qty, 3) 
                
                if qty_to_close > 0:
                    self.exchange.execute(SIDE_SELL, qty_to_close)
            else:
                logger.info("No action")
        except Exception as e:
            logger.error(f"Error syncing state: {e}")

    def run(self):
        logger.info("Starting executor...")
        while True:
            try:
                self.sync_state()
                logger.info("Sleeping for 15s")
                time.sleep(15)
            except Exception as e:
                logger.error(f"Error in executor: {e}")
                time.sleep(5)
        
if __name__ == "__main__":
    executor = Executor()
    executor.run()
