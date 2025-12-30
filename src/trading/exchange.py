import os
import csv
from datetime import datetime
from binance.client import Client
from config.config import Config
from binance.enums import *
from src.utils.logger import Setup_logger

logger = Setup_logger("Exchange")

class Exchange:
    def __init__(self):
        self.client = Client(Config.API_KEY,Config.API_SECRET,testnet=True)
        self.symbol = Config.SYMBOL
        self.csv_file = "data/live_trades.csv"
        
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Symbol", "Side", "Price", "Quantity", "OrderId"])

    def curr_pos(self):
        base_asset = self.symbol.replace("USDT","")
        try:
            balance = self.client.get_asset_balance(asset=base_asset)
            return float(balance['free'])
        except Exception as e:
            logger.error(f"Error getting current position: {e}")
            return 0.0

    def log_trade(self,side,price,qty,order_id):
        with open(self.csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    self.symbol,
                    side,
                    price,
                    qty,
                    order_id
                ]
            )
        logger.info(f"Trade logged: {side} {self.symbol} @ {price} x {qty} = {price * qty}")
    
    def execute(self,side,qty):
        try:
            order = self.client.create_order(
                symbol = self.symbol,
                side = side,
                type = Client.ORDER_TYPE_MARKET,
                quantity = qty
            )
            fill_price = float(order['fills'][0]['price']) if order['fills'] else 0.0
            self.log_trade(side,fill_price,qty,order['orderId'])
            return True
        except Exception as e:
            logger.error(f"Error executing order: {e}")
            return False
           
