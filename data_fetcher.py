# 行情数据获取模块
from xtquant import xtdata
from config import FIXED_PERIOD, DEFAULT_EXCHANGE


def prepare_market_data(stock_code: str):
    '''确保行情数据已下载'''
    full_code = f"{stock_code}.{DEFAULT_EXCHANGE}"
    xtdata.download_history_data(full_code, FIXED_PERIOD)

def fetch_market_data(
        stock_code: str,
        count: int
):
    #获取指定股票的原始行情数据（1分钟K线）
    #准备股票数据
    prepare_market_data(stock_code)

    #尝试打印股票名称
    stock_name = "未知股票"
    try:
        detail = xtdata.get_instrument_detail(f"{stock_code}.{DEFAULT_EXCHANGE}")
        if isinstance(detail, dict):
            stock_name = detail.get("InstrumentName", stock_name)
    except Exception:
        pass

    print(f"股票代码：{stock_code}")
    print(f"股票名称：{stock_name}")
    print("-" * 40)
    full_code = f"{stock_code}.{DEFAULT_EXCHANGE}"

    data = xtdata.get_market_data(
        field_list=['open', 'high', 'low', 'close', 'volume'],
        stock_list=[full_code],
        period=FIXED_PERIOD,
        count=count
    )

    return data
