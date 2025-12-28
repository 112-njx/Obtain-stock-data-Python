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


def plot_candlestick_with_ma(ohlcv_df: pd.DataFrame, indicators: dict, stock_name: str = "Unknown"):
    """绘制 K 线和均线组合图表（不含 MACD）"""
    if ohlcv_df.empty:
        print("No data available for plotting")
        return

    ma5 = indicators.get('ma5', pd.Series())
    ma10 = indicators.get('ma10', pd.Series())
    ma20 = indicators.get('ma20', pd.Series())

    ma5_valid = not ma5.empty and not ma5.isna().all()
    ma10_valid = not ma10.empty and not ma10.isna().all()
    ma20_valid = not ma20.empty and not ma20.isna().all()

    add_plots = []

    if ma5_valid:
        add_plots.append(mpf.make_addplot(ma5, color='#FF6B6B', width=1.5, label='MA5'))
    if ma10_valid:
        add_plots.append(mpf.make_addplot(ma10, color='#4ECDC4', width=1.5, label='MA10'))
    if ma20_valid:
        add_plots.append(mpf.make_addplot(ma20, color='#45B7D1', width=1.5, label='MA20'))

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

    mpf.plot(
        ohlcv_df,
        type='candle',
        volume=True,
        style=style,
        title=f"{stock_name} -- K线与均线",
        ylabel='价格',
        ylabel_lower='成交量',
        addplot=add_plots,
        panel_ratios=(8, 3),
        datetime_format='%H:%M',
        figsize=(16, 10)
    )

def plot_macd(ohlcv_df: pd.DataFrame, indicators: dict, stock_name: str = "Unknown"):
    """绘制独立的 MACD 指标图表"""
    if ohlcv_df.empty:
        print("No data available for MACD chart")
        return

    macd = indicators.get('macd', pd.Series())
    signal = indicators.get('signal', pd.Series())
    histogram = indicators.get('histogram', pd.Series())

    if macd.empty or macd.isna().all():
        print("MACD data is not available")
        return

    style = mpf.make_mpf_style(
        gridstyle='--',
        gridcolor='lightgray',
        rc={'font.family': font_prop.get_name()}
    )

    mc = mpf.make_marketcolors(
        up='red',
        down='green',
        edge='inherit',
        wick='inherit',
        volume='inherit'
    )

    style_with_colors = mpf.make_mpf_style(
        marketcolors=mc,
        gridstyle='--',
        gridcolor='lightgray',
        rc={'font.family': font_prop.get_name()}
    )

    macd_panel = [
        mpf.make_addplot(macd, panel='lower', color='#FF6B6B', width=1.5, ylabel='MACD'),
        mpf.make_addplot(signal, panel='lower', color='#4ECDC4', width=1.5),
        mpf.make_addplot(histogram, type='bar', panel='lower', color='#45B7D1', alpha=0.7)
    ]

    mpf.plot(
        ohlcv_df,
        type='candle',
        volume=False,
        style=style_with_colors,
        title=f"{stock_name} --MACD 指标",
        ylabel='价格',
        addplot=macd_panel,
        panel_ratios=(4, 2),
        datetime_format='%H:%M',
        figsize=(14, 8)
    )
