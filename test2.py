#接口能力检查
from xtquant import xtdata
import inspect

print("=== xtdata 接口能力检查 ===")

check_funcs = [
    "get_market_data",
    "download_history_data",
    "get_instrument_detail",
    "get_stock_info"
]

for func in check_funcs:
    if hasattr(xtdata, func):
        print(f"[✓] 支持接口: {func}")
        try:
            sig = inspect.signature(getattr(xtdata, func))
            print(f"    参数签名: {sig}")
        except Exception:
            pass
    else:
        print(f"[✗] 不支持接口: {func}")
