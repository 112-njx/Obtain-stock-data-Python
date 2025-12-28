from data_fetcher import fetch_market_data
from time_utils import is_trading_time
from data_formatter import standardize_ohlcv
from plotter import plot_candlestick

def main():
    stock_code = input("请输入股票代码（6位数字）：").strip()
    count = int(input("请输入获取的K线条数："))

    if not is_trading_time():
        print("当前不在A股交易时间，行情数据可能为空")

    data, stock_name = fetch_market_data(stock_code, count)

    if data is None or data.empty:
        print("未能获取到行情数据，请确认是否在交易时间内运行程序")
        return

    ohlcv_df = standardize_ohlcv(data)

    if ohlcv_df.empty:
        print("行情数据标准化失败")
        return

    print(ohlcv_df)

    plot_candlestick(ohlcv_df, stock_name=stock_name)


if __name__ == '__main__':
    main()
