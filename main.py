from data_fetcher import fetch_market_data
from utils import is_trading_time


def main():
    stock_code = input("请输入股票代码（6位数字）：").strip()
    count = int(input("请输入获取的K线条数："))

    if not is_trading_time():
        print("当前不在A股交易时间，行情数据可能为空")

    data = fetch_market_data(stock_code, count)

    if not data or all(df.empty for df in data.values()):
        print("未能获取到行情数据，请确认是否在交易时间内运行程序")
        return

    stock_name = get_stock_name(stock_code)
    print(f"股票：{stock_name}（{stock_code}）")
    print(data)


if __name__ == '__main__':
    main()
