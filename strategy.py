import pandas as pd
from typing import Tuple, List, Optional


def get_latest_value(series: pd.Series) -> Optional[float]:
    if series is None or series.empty or series.isna().all():
        return None
    valid_values = series.dropna()
    if valid_values.empty:
        return None
    return valid_values.iloc[-1]


def analyze_ma_trend(ma5: pd.Series, ma10: pd.Series, ma20: pd.Series) -> dict:
    ma5_val = get_latest_value(ma5)
    ma10_val = get_latest_value(ma10)
    ma20_val = get_latest_value(ma20)

    if ma20_val is None:
        return {'trend': 'unknown', 'score': 0, 'reason': '数据不足，无法判断趋势'}

    ma5_above_ma20 = ma5_val > ma20_val if ma5_val else False
    ma10_above_ma20 = ma10_val > ma20_val if ma10_val else False

    if ma5_val and ma10_val:
        if ma5_val > ma10_val > ma20_val:
            trend = 'strong_bullish'
            score = 3
            reason = 'MA5 > MA10 > MA20，形成多头排列'
        elif ma5_val > ma10_val and ma10_val < ma20_val:
            trend = 'weak_bullish'
            score = 1
            reason = 'MA5 上穿 MA20，但 MA10 仍在 MA20 下方'
        elif ma5_val < ma10_val and ma5_val > ma20_val:
            trend = 'neutral'
            score = 0
            reason = 'MA5 与 MA10 交叉，暂观望'
        elif ma5_val < ma10_val < ma20_val:
            trend = 'bearish'
            score = -2
            reason = 'MA5 < MA10，形成死叉趋势'
        else:
            trend = 'neutral'
            score = 0
            reason = '均线纠结，方向不明确'
    else:
        trend = 'unknown'
        score = 0
        reason = '均线数据不足'

    return {'trend': trend, 'score': score, 'reason': reason, 'ma_values': {'ma5': ma5_val, 'ma10': ma10_val, 'ma20': ma20_val}}


def analyze_macd_signal(macd: pd.Series, signal: pd.Series, histogram: pd.Series) -> dict:
    macd_val = get_latest_value(macd)
    signal_val = get_latest_value(signal)
    hist_val = get_latest_value(histogram)

    if macd_val is None or signal_val is None:
        return {'signal': 'unknown', 'score': 0, 'reason': 'MACD 数据不足'}

    if hist_val is None:
        hist_val = macd_val - signal_val

    macd_above_signal = macd_val > signal_val
    hist_positive = hist_val > 0

    if macd_above_signal and hist_positive:
        signal = 'bullish'
        score = 2
        reason = f'MACD({macd_val:.4f}) > SIGNAL({signal_val:.4f})，柱状图为正'
    elif macd_above_signal and not hist_positive:
        signal = 'weak_bullish'
        score = 1
        reason = f'MACD > SIGNAL，但柱状图为负，可能形成死叉'
    elif not macd_above_signal and hist_positive:
        signal = 'weak_bearish'
        score = -1
        reason = f'MACD < SIGNAL，但柱状图为正，可能形成金叉'
    else:
        signal = 'bearish'
        score = -2
        reason = f'MACD({macd_val:.4f}) < SIGNAL({signal_val:.4f})，柱状图为负'

    return {'signal': signal, 'score': score, 'reason': reason, 'values': {'macd': macd_val, 'signal': signal_val, 'histogram': hist_val}}


def generate_strategy(ohlcv_df: pd.DataFrame, indicators: dict) -> dict:
    if ohlcv_df is None or ohlcv_df.empty:
        return {
            'action': 'HOLD',
            'confidence': 0,
            'reason': '无有效数据',
            'details': {}
        }

    ma5 = indicators.get('ma5', pd.Series())
    ma10 = indicators.get('ma10', pd.Series())
    ma20 = indicators.get('ma20', pd.Series())
    macd = indicators.get('macd', pd.Series())
    signal = indicators.get('signal', pd.Series())
    histogram = indicators.get('histogram', pd.Series())

    ma_analysis = analyze_ma_trend(ma5, ma10, ma20)
    macd_analysis = analyze_macd_signal(macd, signal, histogram)

    total_score = ma_analysis['score'] + macd_analysis['score']

    if total_score >= 4:
        action = 'BUY'
        confidence = min(100, (total_score / 6) * 100)
        reason = '均线多头排列且 MACD 金叉，看涨信号较强'
    elif total_score >= 2:
        action = 'BUY'
        confidence = min(100, (total_score / 6) * 100)
        reason = '技术指标偏多，可考虑买入'
    elif total_score >= 0:
        action = 'HOLD'
        confidence = 50
        reason = '技术指标中性，建议观望'
    elif total_score >= -2:
        action = 'SELL'
        confidence = min(100, abs(total_score) / 6 * 100)
        reason = '技术指标偏空，建议减仓'
    else:
        action = 'SELL'
        confidence = min(100, abs(total_score) / 6 * 100)
        reason = '均线死叉且 MACD 死叉，下跌风险较大'

    latest_close = get_latest_value(ohlcv_df['close']) if 'close' in ohlcv_df.columns else None

    return {
        'action': action,
        'confidence': round(confidence, 1),
        'reason': reason,
        'ma_analysis': ma_analysis,
        'macd_analysis': macd_analysis,
        'latest_close': latest_close,
        'details': {
            'ma_trend': ma_analysis['trend'],
            'ma_reason': ma_analysis['reason'],
            'macd_signal': macd_analysis['signal'],
            'macd_reason': macd_analysis['reason'],
            'total_score': total_score
        }
    }


def print_strategy_report(strategy_result: dict, stock_name: str = "Unknown"):
    print("\n" + "=" * 60)
    print(f"【{stock_name}】策略分析报告")
    print("=" * 60)

    action = strategy_result.get('action', 'N/A')
    confidence = strategy_result.get('confidence', 0)
    reason = strategy_result.get('reason', '无数据')

    action_zh = {'BUY': '买入', 'SELL': '卖出', 'HOLD': '持有'}.get(action, action)
    print(f"操作建议: 【{action_zh}】 置信度: {confidence}%")
    print(f"综合理由: {reason}")
    print("-" * 60)

    details = strategy_result.get('details', {})
    ma_trend = details.get('ma_trend', 'unknown')
    ma_reason = details.get('ma_reason', '无')
    macd_signal = details.get('macd_signal', 'unknown')
    macd_reason = details.get('macd_reason', '无')

    trend_zh = {
        'strong_bullish': '强势多头',
        'weak_bullish': '偏多',
        'neutral': '中性',
        'bearish': '偏空',
        'unknown': '数据不足'
    }.get(ma_trend, ma_trend)

    signal_zh = {
        'bullish': '金叉（看涨）',
        'weak_bullish': '潜在金叉',
        'weak_bearish': '潜在死叉',
        'bearish': '死叉（看跌）',
        'unknown': '数据不足'
    }.get(macd_signal, macd_signal)

    print(f"均线分析: {trend_zh}")
    print(f"{ma_reason}")
    print(f"MACD分析: {signal_zh}")
    print(f"{macd_reason}")
    print("=" * 60)

    latest_close = strategy_result.get('latest_close')
    if latest_close:
        print(f"当前收盘价: {latest_close:.2f}")
    print()
