from data_fetcher import fetch_market_data
from time_utils import is_trading_time
from data_formatter import standardize_ohlcv
from indicators import calculate_all_indicators
from strategy import generate_strategy, print_strategy_report
from plotter import plot_candlestick_with_ma, plot_macd


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

    print("\n" + "=" * 60)
    print(f"Stock: {stock_name} ({stock_code}) | Data Count: {len(ohlcv_df)}")
    print("=" * 60)
    print(ohlcv_df.tail(10))

    indicators = calculate_all_indicators(ohlcv_df)
    print("\n指标计算成功")

    strategy_result = generate_strategy(ohlcv_df, indicators)
    print_strategy_report(strategy_result, stock_name)

    print("\n生成 K 线与均线图表")
    plot_candlestick_with_ma(ohlcv_df, indicators, stock_name)

    print("\n生成 MACD 指标图表")
    plot_macd(ohlcv_df, indicators, stock_name)


if __name__ == '__main__':
    main()
