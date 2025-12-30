# Quant Dev Assignment  Shikher Jha

Hi, this is my submission for the Quant Developer Intern assessment.

Since this is my first real project in the quant space (and my return to Python after a while), I focused heavily on the engineering side making sure the code is modular, runs without crashing, and most importantly, that the live trading matches the backtest exactly.

## Project Structure

I tried to keep the code clean, followed the same structure as given in the assignment and separated into logical folders:

`src/strategy`: Contains the logic. `multi_tf.py` is the main file here.

`src/trading`: Handles the live execution (`executor.py`) and Binance connections (`exchange.py`).

`src/backtesting`: Runs the historical data simulation.

`data`: Stores the CSV logs (`live_trades.csv` and `backtest_trades.csv`).

## My Strategy (The "Why")

I’ll be honest I didn't focus on creating a complex money-printing machine. I wanted a strategy that was easy to debug so I could prove the infrastructure works.

**Initial Idea:** I started with a simple SMA crossover. It was too laggy and didn't trigger enough trades for testing.

**Pivot:** I moved to an RSI-based mean reversion strategy.

**Final Version:** I added an ADX filter to make it "smarter." Basically, it checks if the trend is strong (ADX) before listening to the RSI signal.

Note: For the final submission, I hardcoded the parameters (like RSI periods and thresholds). I did this to guarantee that the Live Bot and the Backtester are using the exact same numbers. If I left the optimizer on, they might have drifted apart.

## How I Ensured Parity (Backtest vs Live)

The requirement to make sure live trades match backtest trades was the tricky part. Here is how I solved it:

Instead of writing separate logic for the live bot, I built a "State Sync" system.

Every 15 seconds, the Live Executor downloads the last 20 days of data.

It actually runs the backtest strategy on that data right there in the loop.

It checks: "What does the strategy say my position should be?" vs "What is actually in my wallet?"

If they don't match, it executes a trade to fix it.

This means the live bot literally is the backtester running in realtime. There's no way for the logic to be different.

## Usage

1. Setup
   Make sure you have the requirements installed:

```bash
pip install r requirements.txt
```

Update `config/config.py` with your API keys.

2. Run the Backtest
   This generates the `backtest_trades.csv` file using the last 30 days of data.

```bash
python m src.backtesting.backtest
```

3. Run Live Trading
   This starts the bot. It will log every action to the console and save trades to `live_trades.csv`.

```bash
python m src.trading.executor
```

## Observations

**Live Test:** I ran the bot on the Testnet. Since the market was pretty flat during my testing window, the bot correctly identified a "HOLD" or "FLAT" state.

**Logs:** You can see in the logs that it successfully syncs the wallet (e.g., seeing 0 balance and matching it with 0 target position).

## Conclusion

This assessment was a great learning experience. It forced me to think about system reliability rather than just staring at charts. The code is structured in a way that I can easily swap out the strategy file for something more complex later on without breaking the execution logic.
