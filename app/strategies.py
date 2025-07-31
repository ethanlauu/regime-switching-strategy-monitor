import numpy as np
import pandas as pd
from typing import Dict, Any

def calculate_ma_crossover(df: pd.DataFrame, short_window: int = 50, long_window: int = 200) -> float:
    if len(df) < long_window:
        return 0.0
    close_prices = df['Close']
    if isinstance(close_prices, pd.DataFrame):
        close_prices = close_prices.iloc[:, 0]
    short_ma = close_prices.rolling(window=short_window).mean().iloc[-1]
    long_ma = close_prices.rolling(window=long_window).mean().iloc[-1]
    if pd.isna(short_ma) or pd.isna(long_ma):
        return 0.0
    if short_ma > long_ma:
        return 1.0
    else:
        return -1.0

def calculate_rsi(df: pd.DataFrame, window: int = 14) -> float:
    if len(df) < window + 1:
        return 50.0
    close_prices = df['Close']
    if isinstance(close_prices, pd.DataFrame):
        close_prices = close_prices.iloc[:, 0]
    delta = close_prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50.0

def bull_strategy(df: pd.DataFrame) -> float:
    return calculate_ma_crossover(df, 50, 200)

def bear_strategy(df: pd.DataFrame) -> float:
    rsi = calculate_rsi(df, 14)
    if rsi < 30:
        return 1.0
    elif rsi > 70:
        return -1.0
    else:
        return 0.0

def sideways_strategy(df: pd.DataFrame) -> float:
    return 0.0

def generate_signal(regime_probs: np.ndarray, df: pd.DataFrame) -> Dict[str, Any]:
    if len(regime_probs) != 3:
        raise ValueError("Expected 3 regime probabilities")
    bull_signal = bull_strategy(df)
    bear_signal = bear_strategy(df)
    sideways_signal = sideways_strategy(df)
    weighted_signal = (
        regime_probs[0] * bull_signal +
        regime_probs[1] * bear_signal +
        regime_probs[2] * sideways_signal
    )
    if weighted_signal > 0.3:
        action = "BUY"
        confidence = min(abs(weighted_signal), 1.0)
    elif weighted_signal < -0.3:
        action = "SELL"
        confidence = min(abs(weighted_signal), 1.0)
    else:
        action = "HOLD"
        confidence = 1.0 - min(abs(weighted_signal), 1.0)
    return {
        "action": action,
        "confidence": float(confidence),
        "regime_probs": regime_probs.tolist(),
        "weighted_signal": float(weighted_signal)
    }
