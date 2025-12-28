# 绘图 / 可视化模块
import mplfinance as mpf
import matplotlib as mpl
from matplotlib import font_manager
import pandas as pd

# 强制指定中文字体文件
font_path = r"C:\Windows\Fonts\msyh.ttc"
font_prop = font_manager.FontProperties(fname=font_path)

mpl.rcParams['font.family'] = font_prop.get_name()
mpl.rcParams['axes.unicode_minus'] = False


def plot_candlestick_with_indicators(ohlcv_df: pd.DataFrame, indicators: dict, stock_name: str = "Unknown"):
    if ohlcv_df.empty:
        print("No data available for plotting")
        return

    ma5 = indicators.get('ma5', pd.Series())
    ma10 = indicators.get('ma10', pd.Series())
    ma20 = indicators.get('ma20', pd.Series())
    macd = indicators.get('macd', pd.Series())
    signal = indicators.get('signal', pd.Series())
    histogram = indicators.get('histogram', pd.Series())

    ma5_valid = not ma5.empty and not ma5.isna().all()
    ma10_valid = not ma10.empty and not ma10.isna().all()
    ma20_valid = not ma20.empty and not ma20.isna().all()

    add_plots = []

    if ma5_valid:
        add_plots.append(mpf.make_addplot(ma5, color='#FF6B6B', width=1.2, label='MA5'))
    if ma10_valid:
        add_plots.append(mpf.make_addplot(ma10, color='#4ECDC4', width=1.2, label='MA10'))
    if ma20_valid:
        add_plots.append(mpf.make_addplot(ma20, color='#45B7D1', width=1.2, label='MA20'))

    mc = mpf.make_marketcolors(
        up='red',
        down='green',
        edge='inherit',
        wick='inherit',
        volume='inherit'
    )

    style = mpf.make_mpf_style(
        marketcolors=mc,
        gridstyle='--',
        gridcolor='lightgray',
        rc={'font.family': font_prop.get_name()}
    )

    panels = ['main', 'volume']
    if not macd.empty and not macd.isna().all():
        panels.append('lower')

    panel_ratios = [6, 2, 2] if len(panels) == 3 else [8, 2]

    macd_panel = None
    if not macd.empty and not macd.isna().all():
        macd_panel = [
            mpf.make_addplot(macd, panel='lower', color='#FF6B6B', width=1.2, ylabel='MACD'),
            mpf.make_addplot(signal, panel='lower', color='#4ECDC4', width=1.2),
            mpf.make_addplot(histogram, type='bar', panel='lower', color='#45B7D1', alpha=0.5)
        ]

    all_addplots = add_plots + (macd_panel if macd_panel else [])

    mpf.plot(
        ohlcv_df,
        type='candle',
        volume=True,
        style=style,
        title=f"{stock_name} 1-Min K-Line with MA & MACD",
        ylabel='Price',
        addplot=all_addplots,
        panel_ratios=panel_ratios,
        datetime_format='%H:%M',
        figsize=(14, 10)
    )


def plot_candlestick(ohlcv_df, stock_name: str = "Unknown"):
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
