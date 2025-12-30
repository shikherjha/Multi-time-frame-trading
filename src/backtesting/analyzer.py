import pandas as pd

class Analyzer:
    @staticmethod
    def print_summary(stats):
        print("\n=== BACKTEST RESULTS ===")
        print(f"Return:          {stats['Return [%]']:.2f}%")
        print(f"Win Rate:        {stats['Win Rate [%]']:.2f}%")
        print(f"Max Drawdown:    {stats['Max. Drawdown [%]']:.2f}%")
        print(f"Sharpe Ratio:    {stats['Sharpe Ratio']:.2f}")
        print(f"Total Trades:    {stats['# Trades']}")
        print("========================\n")

    @staticmethod
    def save_trades(stats, filename="data/backtest_trades.csv"):
        trades = stats['_trades']
        if not trades.empty:
            trades.to_csv(filename)
            print(f"Trade log saved to {filename}")
        else:
            print("No trades were made.")