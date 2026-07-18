from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Candle:
    symbol: str
    timestamp: datetime

    open: float
    high: float
    low: float
    close: float

    volume: Optional[float] = None