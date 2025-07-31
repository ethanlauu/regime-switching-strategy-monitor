import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM
import pickle
import os
from typing import Optional

MODEL_PATH = '/tmp/model.pkl'

class RegimeHMM:
    def __init__(self, n_states: int = 3):
        self.n_states = n_states
        self.model: Optional[GaussianHMM] = None

    def fit(self, df: pd.DataFrame, n_states: Optional[int] = None) -> None:
        n_states = n_states or self.n_states
        close_prices = df['Close']
        if isinstance(close_prices, pd.DataFrame):
            close_prices = close_prices.iloc[:, 0]
        close_prices = close_prices.dropna()
        if len(close_prices) < 100:
            # No exception, just skip fitting.
            print("[HMM fit] Insufficient data for HMM fitting (need 100, got %d). Skipping." % len(close_prices))
            self.model = None
            return

        log_prices = np.log(close_prices)
        returns_series = pd.Series(log_prices, index=close_prices.index).diff().dropna()

        if len(returns_series) < 50:
            print("[HMM fit] Insufficient returns data for HMM fitting (need 50, got %d). Skipping." % len(returns_series))
            self.model = None
            return

        returns = returns_series.values.reshape(-1, 1)
        if np.isnan(returns).any() or np.isinf(returns).any():
            print("[HMM fit] Invalid returns data (NaN or Inf). Skipping.")
            self.model = None
            return

        self.model = GaussianHMM(
            n_components=n_states,
            covariance_type='full',
            n_iter=1000,
            random_state=42
        )
        self.model.fit(returns)

    def predict_proba(self, df_tail: pd.DataFrame) -> np.ndarray:
        # Always return a valid probability vector.
        if self.model is None:
            print("[predict_proba] Model not fitted, returning uniform probs.")
            return np.array([1.0/self.n_states] * self.n_states)

        close_prices_tail = df_tail['Close']
        if isinstance(close_prices_tail, pd.DataFrame):
            close_prices_tail = close_prices_tail.iloc[:, 0]

        # Must have at least 2 data points for a return.
        if len(close_prices_tail.dropna()) < 2:
            print("[predict_proba] Not enough data for returns, returning uniform probs.")
            return np.array([1.0/self.n_states] * self.n_states)

        log_prices_tail = np.log(close_prices_tail.dropna())
        log_returns_tail_series = pd.Series(log_prices_tail, index=close_prices_tail.dropna().index).diff().dropna()
        if len(log_returns_tail_series) == 0:
            print("[predict_proba] Not enough data for returns (diff empty), returning uniform probs.")
            return np.array([1.0/self.n_states] * self.n_states)

        log_returns_tail = log_returns_tail_series.values.reshape(-1, 1)
        try:
            probs = self.model.predict_proba(log_returns_tail)
            return probs[-1]
        except Exception as e:
            print(f"[predict_proba] Exception: {e}. Returning uniform probs.")
            return np.array([1.0/self.n_states] * self.n_states)

    def save(self, path: str = MODEL_PATH) -> None:
        if self.model is None:
            raise ValueError('Model not fitted.')
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, path: str = MODEL_PATH) -> None:
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
