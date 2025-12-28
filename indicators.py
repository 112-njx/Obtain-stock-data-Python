import pandas as pd
import numpy as np


def calculate_ma(close_prices: pd.Series, window: int) -> pd.Series:
    if len(close_prices) < window:
        return pd.Series(np.nan, index=close_prices.index)
    return close_prices.rolling(window=window).mean()


def calculate_ma5(ohlcv_df: pd.DataFrame) -> pd.Series:
    if ohlcv_df is None or ohlcv_df.empty or 'close' not in ohlcv_df.columns:
        return pd.Series(dtype=float)
    return calculate_ma(ohlcv_df['close'], 5)


def calculate_ma10(ohlcv_df: pd.DataFrame) -> pd.Series:
    if ohlcv_df is None or ohlcv_df.empty or 'close' not in ohlcv_df.columns:
        return pd.Series(dtype=float)
    return calculate_ma(ohlcv_df['close'], 10)


def calculate_ma20(ohlcv_df: pd.DataFrame) -> pd.Series:
    if ohlcv_df is None or ohlcv_df.empty or 'close' not in ohlcv_df.columns:
        return pd.Series(dtype=float)
    return calculate_ma(ohlcv_df['close'], 20)


def calculate_macd(close_prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> dict:
    if close_prices is None or len(close_prices) < slow + signal:
        return {
            'macd': pd.Series(dtype=float),
            'signal': pd.Series(dtype=float),
            'histogram': pd.Series(dtype=float)
        }

    ema_fast = close_prices.ewm(span=fast, adjust=False).mean()
    ema_slow = close_prices.ewm(span=slow, adjust=False).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    return {
        'macd': macd_line,
        'signal': signal_line,
        'histogram': histogram
    }


def calculate_all_indicators(ohlcv_df: pd.DataFrame) -> dict:
    if ohlcv_df is None or ohlcv_df.empty:
        return {}

    result = {
        'ma5': calculate_ma5(ohlcv_df),
        'ma10': calculate_ma10(ohlcv_df),
        'ma20': calculate_ma20(ohlcv_df)
    }

    if 'close' in ohlcv_df.columns:
        macd_result = calculate_macd(ohlcv_df['close'])
        result.update(macd_result)

    return result
