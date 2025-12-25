#判断交易时间的辅助函数
from datetime import datetime
from config import (
    MORNING_START, MORNING_END,
    AFTERNOON_START, AFTERNOON_END
)


def is_trading_time() -> bool:
    now = datetime.now()
    h, m = now.hour, now.minute

    in_morning = (
        (h > MORNING_START[0] or (h == MORNING_START[0] and m >= MORNING_START[1])) and
        (h < MORNING_END[0] or (h == MORNING_END[0] and m <= MORNING_END[1]))
    )

    in_afternoon = (
        (h > AFTERNOON_START[0] or (h == AFTERNOON_START[0] and m >= AFTERNOON_START[1])) and
        (h < AFTERNOON_END[0] or (h == AFTERNOON_END[0] and m <= AFTERNOON_END[1]))
    )

    return in_morning or in_afternoon
