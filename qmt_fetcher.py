import sys
import os
import json
import pandas as pd
from xtquant import xtdata

FIXED_PERIOD = '1m'
DEFAULT_EXCHANGE = 'SH'

def prepare_market_data(stock_code: str):
    """确保行情数据已下载"""
    full_code = f"{stock_code}.{DEFAULT_EXCHANGE}"
    xtdata.download_history_data(full_code, FIXED_PERIOD)

def fetch_market_data(stock_code: str, count: int):
    """获取指定股票的原始行情数据（1分钟K线）"""
    prepare_market_data(stock_code)

    full_code = f"{stock_code}.{DEFAULT_EXCHANGE}"

    data = xtdata.get_market_data(
        field_list=['open', 'high', 'low', 'close', 'volume'],
        stock_list=[full_code],
        period=FIXED_PERIOD,
        count=count
    )

    return data

def standardize_ohlcv(raw_data: dict) -> pd.DataFrame:
    """将 QMT 返回的行情 dict 转换为标准 OHLCV DataFrame"""
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

def get_stock_name(stock_code: str) -> str:
    """获取股票名称"""
    try:
        detail = xtdata.get_instrument_detail(f"{stock_code}.{DEFAULT_EXCHANGE}")
        if isinstance(detail, dict):
            return detail.get("InstrumentName", "未知股票")
    except Exception:
        pass
    return "未知股票"

def main():
    if len(sys.argv) != 4:
        print("Usage: qmt_fetcher.py <stock_code> <count> <output_csv>")
        sys.exit(1)

    stock_code = sys.argv[1]
    count = int(sys.argv[2])
    output_csv = sys.argv[3]

    stock_name = get_stock_name(stock_code)

    print(f"QMT Python 环境获取数据...")
    print(f"股票代码：{stock_code}")
    print(f"股票名称：{stock_name}")
    print("-" * 40)

    raw_data = fetch_market_data(stock_code, count)

    if not raw_data or all(df.empty for df in raw_data.values()):
        print("未能获取到行情数据")
        sys.exit(1)

    ohlcv_df = standardize_ohlcv(raw_data)

    if ohlcv_df.empty:
        print("行情数据标准化失败")
        sys.exit(1)

    ohlcv_df.to_csv(output_csv, index_label='timestamp')

    meta_info = {
        "stock_code": stock_code,
        "stock_name": stock_name,
        "count": count,
        "csv_path": output_csv
    }

    meta_file = output_csv.replace('.csv', '_meta.json')
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(meta_info, f, ensure_ascii=False, indent=2)

    print(f"数据已保存到: {output_csv}")
    print(f"元信息已保存到: {meta_file}")

if __name__ == '__main__':
    main()
