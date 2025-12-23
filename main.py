# 程序入口，负责整体流程调度
from data_fetcher import fetch_market_data
from config import STOCK_CODE_LENGTH


def main():
    stock_code = input("请输入A股股票代码：").strip()
    count = int(input("请输入获取的K线条数："))

    if len(stock_code) != STOCK_CODE_LENGTH or not stock_code.isdigit():
        print("股票代码格式错误")
        return

    data = fetch_market_data(
        stock_code=stock_code,
        count=count
    )

    print("行情数据获取成功：")
    print(data)


if __name__ == '__main__':
    main()
