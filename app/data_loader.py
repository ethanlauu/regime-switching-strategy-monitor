import os
import pandas as pd
import yfinance as yf
from typing import Optional, cast

PARQUET_PATH = 'app/data_cache.parquet'
SYMBOL = os.getenv('SYMBOL', 'SPY')


def fetch_ohlcv(symbol: str = SYMBOL, period: str = '10y') -> pd.DataFrame:
    result = yf.download(symbol, period=period, auto_adjust=True)
    if result is not None and not result.empty:
        if isinstance(result, pd.Series):
            df = result.to_frame()
        else:
            df = pd.DataFrame(result)
        df = df[~df.index.duplicated(keep='first')]
        # --- ADD THIS HERE ---
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]
        # --- END ADD ---
        return df
    return pd.DataFrame()



def cache_data(df: pd.DataFrame, path: str = PARQUET_PATH) -> None:
    """
    Cache the DataFrame to a local parquet file.
    Args:
        df (pd.DataFrame): DataFrame to cache.
        path (str): Path to parquet file.
    """
    df.to_parquet(path)


def load_cached_data(path: str = PARQUET_PATH) -> pd.DataFrame:  # type: ignore
    """
    Load cached OHLCV data from parquet file if it exists.
    Args:
        path (str): Path to parquet file.
    Returns:
        pd.DataFrame: Loaded DataFrame or empty DataFrame if not found.
    """
    if os.path.exists(path):
        try:
            df = pd.read_parquet(path)
            if isinstance(df, pd.Series):
                df = df.to_frame()
            elif not isinstance(df, pd.DataFrame):
                df = pd.DataFrame(df)
            if df is not None and not df.empty:
                df = pd.DataFrame(df)
                df = df[~df.index.duplicated(keep='first')]
                return df  # type: ignore
        except Exception:
            pass
    return pd.DataFrame()


def get_latest_df(force_refresh: bool = False) -> pd.DataFrame:
    """
    Get the most recent OHLCV DataFrame, loading from cache or fetching if needed.
    Args:
        force_refresh (bool): If True, always fetch fresh data.
    Returns:
        pd.DataFrame: Latest OHLCV data, date-indexed, no duplicates.
    """
    if not force_refresh:
        df = load_cached_data()
        if not df.empty:
            return df
    df = fetch_ohlcv()
    cache_data(df)
    return df 