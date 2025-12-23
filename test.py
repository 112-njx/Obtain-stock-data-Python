from xtquant import xtdata

# 股票代码
stock_code = "601288.SH"

#获取，打印股票名称
detail = xtdata.get_instrument_detail(stock_code)
stock_name = detail.get("InstrumentName", "未知股票")

print(f"股票代码：{stock_code}")
print(f"股票名称：{stock_name}")
print("-" * 40)

# 下载历史日线数据
xtdata.download_history_data(
    stock_code=stock_code,
    period="1d",
    start_time="20251201",
    end_time=""
)

# 获取最近 5 根日线数据
data = xtdata.get_market_data(
    field_list=["open", "high", "low", "close", "volume"],
    stock_list=[stock_code],
    period="1d",
    count=5
)

print("日线行情数据获取结果：")
for k, v in data.items():
    print(f"{k}:\n{v}\n")
