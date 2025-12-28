#绘图,可视化模块
import mplfinance as mpf


def plot_candlestick(ohlcv_df, stock_name: str):
    if ohlcv_df.empty:
        print("无有效数据，无法绘图")
        return

    mpf.plot(
        ohlcv_df,
        type='candle',
        volume=True,
        title=f"{stock_name} 分钟K线",
        style='charles',
        ylabel='Price',
        ylabel_lower='Volume'
    )
