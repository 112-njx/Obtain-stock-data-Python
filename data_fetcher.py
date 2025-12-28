import subprocess
import sys
import os
import json
import pandas as pd

QMT_PYTHON = r"D:\国金QMT交易端模拟\bin.x64\pythonw.exe"
QMT_SCRIPT = r"D:\Obtain-stock-data-Python\Obtain-stock-data-Python\qmt_fetcher.py"


def fetch_market_data(stock_code: str, count: int):
    """通过QMT Python环境获取股票数据"""
    output_csv = f"data_{stock_code}.csv"
    meta_file = f"data_{stock_code}_meta.json"

    print(f"正在调用QMT Python环境获取数据...")

    try:
        result = subprocess.run(
            [QMT_PYTHON, QMT_SCRIPT, stock_code, str(count), output_csv],
            capture_output=True,
            text=True,
            encoding='gbk',
            timeout=300
        )

        if result.stdout:
            print(result.stdout)

        if result.returncode != 0:
            print(f"获取数据失败: {result.stderr}")
            return None, "Unknown"

        if not os.path.exists(output_csv):
            print("CSV文件未生成")
            return None, "Unknown"

        data = pd.read_csv(output_csv, index_col='timestamp', parse_dates=True)

        stock_name = "Unknown"
        if os.path.exists(meta_file):
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                    stock_name = meta.get('stock_name', 'Unknown')
            except Exception:
                pass

        print(f"成功获取 {len(data)} 条数据")
        print(f"股票名称: {stock_name}")
        print("-" * 40)

        return data, stock_name

    except subprocess.TimeoutExpired:
        print("获取数据超时")
        return None, "Unknown"
    except Exception as e:
        print(f"获取数据异常: {e}")
        return None, "Unknown"
