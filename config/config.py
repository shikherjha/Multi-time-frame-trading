import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY  = os.getenv("BINANCE_API_KEY")
    API_SECRET = os.getenv("BINANCE_API_SECRET")
    
    TESTNET = False
    PAPER_TRADING = True
    
    SYMBOL = "BTCUSDT"
    TIMEFRAME_ENTRY = "15m"
    TIMEFRAME_CONFIRM = "1h"

    TESTNET_BASE_URL = "https://testnet.binance.vision/api/v3"
    PROD_BASE_URL = "https://api.binance.com/api/v3"
    QUANTITY = 0.001



