import pandas as pd


def standardize_ohlcv(data):
    if data is None or data.empty:
        return pd.DataFrame()

    if isinstance(data, pd.DataFrame):
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        if all(col in data.columns for col in required_columns):
            df = data.copy()
            if not isinstance(df.index, pd.DatetimeIndex):
                df.index = pd.to_datetime(df.index)
            return df

    return pd.DataFrame()
