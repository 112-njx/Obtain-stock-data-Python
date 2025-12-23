# 行情数据获取模块
from xtquant import xtdata
from config import FIXED_PERIOD, DEFAULT_EXCHANGE


def fetch_market_data(
        stock_code: str,
        count: int
):
    """
    获取指定股票的原始行情数据（1分钟K线）
    :param stock_code: 6位股票代码，如 '600000'
    :param count: 获取K线条数
    :return: QMT 原始行情数据（dict）
    """

    full_code = f"{stock_code}.{DEFAULT_EXCHANGE}"

    data = xtdata.get_market_data(
        field_list=['open', 'high', 'low', 'close', 'volume'],
        stock_list=[full_code],
        period=FIXED_PERIOD,
        count=count
    )

    return data
