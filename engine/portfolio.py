from dataclasses import dataclass
from typing import Optional

from engine.events import (
    SignalEvent,
    OrderEvent,
    OrderDirection,
    SignalType,
)


@dataclass
class Position:
    symbol: str
    direction: OrderDirection
    quantity: float
    entry_price: float = 0.0


class Portfolio:
    """
    Tracks positions and converts trading signals into orders.
    """

    def __init__(self, initial_balance: float = 10000.0):
        self.initial_balance = initial_balance
        self.cash = initial_balance
        self.position: Optional[Position] = None

    def process_signal(self, signal: SignalEvent) -> Optional[OrderEvent]:
        """
        Convert a strategy signal into an order.
        """

        # Buy
        if signal.signal == SignalType.BUY:

            if self.position is None:

                return OrderEvent(
                    symbol=signal.symbol,
                    direction=OrderDirection.BUY,
                    quantity=1.0,
                )

        # Sell
        elif signal.signal == SignalType.SELL:

            if self.position is None:

                return OrderEvent(
                    symbol=signal.symbol,
                    direction=OrderDirection.SELL,
                    quantity=1.0,
                )

        return None