import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from .data_loader import get_latest_df
from .model import RegimeHMM
from .strategies import generate_signal

def calculate_returns(df: pd.DataFrame) -> pd.Series:
    close_prices = df['Close']
    if isinstance(close_prices, pd.DataFrame):
        close_prices = close_prices.iloc[:, 0]
    return close_prices.pct_change().dropna()

def calculate_strategy_returns(df: pd.DataFrame, signals: pd.Series) -> pd.Series:
    returns = calculate_returns(df)
    strategy_returns = signals.shift(1) * returns
    return strategy_returns.fillna(0)

def calculate_metrics(returns: pd.Series) -> Dict[str, float]:
    if len(returns) == 0:
        return {
            "annualized_return": 0.0,
            "sharpe_ratio": 0.0,
            "max_drawdown": 0.0,
            "volatility": 0.0
        }
    total_return = (1 + returns).prod() - 1
    years = len(returns) / 252
    annualized_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
    excess_returns = returns - 0.02 / 252
    sharpe_ratio = np.sqrt(252) * excess_returns.mean() / returns.std() if returns.std() > 0 else 0
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    volatility = returns.std() * np.sqrt(252)
    return {
        "annualized_return": float(annualized_return),
        "sharpe_ratio": float(sharpe_ratio),
        "max_drawdown": float(max_drawdown),
        "volatility": float(volatility)
    }

def run_backtest(years: int = 10, lookback_years: int = 3) -> Dict[str, Any]:
    df = get_latest_df()
    if df.empty:
        print("Backtest error: No data available")
        return {"error": "No data available"}
    min_valid_obs = 100
    lookback_days = max(int(lookback_years * 252), min_valid_obs + 1)
    signals = []
    regime_probs = []
    dates = []

    for i in range(lookback_days, len(df)):
        lookback_df = df.iloc[i - lookback_days : i]
        close_prices = lookback_df['Close']

        # Window must be correct size and no NaNs
        if len(lookback_df) != lookback_days or close_prices.isnull().any():
            print(f"Backtest error on day {i}: Invalid window (len={len(lookback_df)}), skipping")
            continue

        # Returns must have at least min_valid_obs (so at least min_valid_obs + 1 prices)
        returns = close_prices.pct_change().dropna()
        if len(returns) < min_valid_obs:
            print(f"Backtest error on day {i}: Not enough returns in window (returns={len(returns)}), skipping")
            continue

        try:
            hmm = RegimeHMM(n_states=3)
            hmm.fit(lookback_df)
            # >>>> Always use last two rows for predict_proba <<<<
            current_df = df.iloc[i-1:i+1]
            if len(current_df) < 2 or current_df.isnull().any().any():
                print(f"Backtest error on day {i}: Current df not enough rows or contains NaNs")
                continue
            # This ensures .diff() in predict_proba will have at least 1 value
            probs = hmm.predict_proba(current_df)
            regime_probs.append(probs)
            signal_data = generate_signal(probs, lookback_df)
            if signal_data["action"] == "BUY":
                signals.append(1)
            elif signal_data["action"] == "SELL":
                signals.append(-1)
            else:
                signals.append(0)
            dates.append(df.index[i])
        except Exception as e:
            print(f"Backtest error on day {i}: {e}")
            continue

    if len(signals) == 0:
        print("Backtest error: No valid backtest results generated")
        return {"error": "No valid backtest results generated"}
    signals_series = pd.Series(signals, index=dates)
    backtest_df = df.loc[dates]
    strategy_returns = calculate_strategy_returns(backtest_df, signals_series)
    benchmark_returns = calculate_returns(backtest_df)
    strategy_metrics = calculate_metrics(strategy_returns)
    benchmark_metrics = calculate_metrics(benchmark_returns)
    strategy_cumulative = (1 + strategy_returns).cumprod()
    benchmark_cumulative = (1 + benchmark_returns).cumprod()
    return {
        "strategy_metrics": strategy_metrics,
        "benchmark_metrics": benchmark_metrics,
        "strategy_cumulative": strategy_cumulative.tolist(),
        "benchmark_cumulative": benchmark_cumulative.tolist(),
        "dates": [d.strftime('%Y-%m-%d') for d in dates],
        "signals": signals,
        "regime_probs": [probs.tolist() for probs in regime_probs]
    }
