# 绘图 / 可视化模块
import mplfinance as mpf
import matplotlib as mpl
from matplotlib import font_manager

# 强制指定中文字体文件
font_path = r"C:\Windows\Fonts\msyh.ttc"
font_prop = font_manager.FontProperties(fname=font_path)

mpl.rcParams['font.family'] = font_prop.get_name()
mpl.rcParams['axes.unicode_minus'] = False


def plot_candlestick(ohlcv_df, stock_name: str = "未知股票"):
    if ohlcv_df.empty:
        print("无可用于绘图的行情数据")
        return

    # A股：红涨绿跌
    market_colors = mpf.make_marketcolors(
        up='red',
        down='green',
        edge='inherit',
        wick='inherit',
        volume='inherit'
    )

    style = mpf.make_mpf_style(
        marketcolors=market_colors,
        gridstyle='--',
        gridcolor='lightgray',
        rc={
            'font.family': font_prop.get_name()
        }
    )

    mpf.plot(
        ohlcv_df,
        type='candle',
        volume=True,
        style=style,
        title=f"{stock_name} 一分钟K线",
        ylabel='价格',
        ylabel_lower='成交量',
        figsize=(14, 8),
        datetime_format='%H:%M'
    )
