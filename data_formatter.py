import pandas as pd


def standardize_ohlcv(raw_data):
    """将数据转换为标准 OHLCV DataFrame"""
    if raw_data is None:
        return pd.DataFrame()

    if isinstance(raw_data, pd.DataFrame):
        if raw_data.empty:
            return pd.DataFrame()
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        if all(col in raw_data.columns for col in required_columns):
            return raw_data.copy()

    if isinstance(raw_data, dict):
        if not raw_data:
            return pd.DataFrame()

        sample_df = next(iter(raw_data.values()))
        if sample_df.empty:
            return pd.DataFrame()

        time_index = pd.to_datetime(sample_df.columns, format="%Y%m%d%H%M%S")

        ohlcv = pd.DataFrame(index=time_index)

        for field in ["open", "high", "low", "close", "volume"]:
            df = raw_data.get(field)
            if df is None or df.empty:
                ohlcv[field] = None
            else:
                ohlcv[field] = df.iloc[0].values

        ohlcv.sort_index(inplace=True)
        return ohlcv

    return pd.DataFrame()
