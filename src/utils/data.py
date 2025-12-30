import pandas as pd
from binance.client import Client

class DataLoader:
    def __init__(self,client):
        self.client = client
    def load_data(self,symbol,tf,lookback="1 month ago"):
        klines = self.client.get_historical_klines(symbol, tf, lookback)
        df = pd.DataFrame(klines)

        df.columns = [
            'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 
            'Close_time', 'Quote_asset_vol', 'Num_trades', 
            'Taker_buy_base', 'Taker_buy_quote', 'Ignore'
        ]

        num_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        df[num_cols] = df[num_cols].apply(pd.to_numeric)

        df['Time'] = pd.to_datetime(df['Time'],unit = 'ms')
        df.set_index('Time',inplace=True)

        return df[num_cols]
    def merge_data(self,df1,df2) :
        df2_renamed = df2.add_suffix('_1h')

        df2_aligned = df2_renamed.reindex(df1.index)
        df2_aligned = df2_aligned.ffill()

        m_df = pd.concat([df1,df2_aligned],axis=1)
        return m_df.dropna()
