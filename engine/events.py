from dataclasses import dataclass
from enum import Enum, auto

from models.candle import Candle


class EventType(Enum):
    MARKET = auto()
    SIGNAL = auto()
    ORDER = auto()
    FILL = auto()


@dataclass
class Event:
    event_type: EventType


@dataclass
class MarketEvent(Event):
    symbol: str
    timestamp: int
    candle: Candle

    def __init__(self, symbol: str, timestamp, candle: Candle):
        self.event_type = EventType.MARKET
        self.symbol = symbol
        self.timestamp = timestamp
        self.candle = candle


class SignalType(Enum):
    BUY = auto()
    SELL = auto()
    EXIT = auto()


@dataclass
class SignalEvent(Event):
    symbol: str
    signal: SignalType
    strength: float = 1.0

    def __init__(self, symbol: str, signal: SignalType, strength: float = 1.0):
        self.event_type = EventType.SIGNAL
        self.symbol = symbol
        self.signal = signal
        self.strength = strength


class OrderDirection(Enum):
    BUY = auto()
    SELL = auto()


@dataclass
class OrderEvent(Event):
    symbol: str
    direction: OrderDirection
    quantity: float

    def __init__(self, symbol: str, direction: OrderDirection, quantity: float):
        self.event_type = EventType.ORDER
        self.symbol = symbol
        self.direction = direction
        self.quantity = quantity


@dataclass
class FillEvent(Event):
    symbol: str
    direction: OrderDirection
    quantity: float
    price: float
    commission: float

    def __init__(
        self,
        symbol: str,
        direction: OrderDirection,
        quantity: float,
        price: float,
        commission: float,
    ):
        self.event_type = EventType.FILL
        self.symbol = symbol
        self.direction = direction
        self.quantity = quantity
        self.price = price
        self.commission = commission