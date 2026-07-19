from dataclasses import dataclass
from typing import Optional

from engine.events import (
    SignalEvent,
    OrderEvent,
    OrderDirection,
    SignalType,
    FillEvent,
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

        # Enter a long position
        if signal.signal == SignalType.BUY:

            if self.position is None:

                return OrderEvent(
                    symbol=signal.symbol,
                    direction=OrderDirection.BUY,
                    quantity=1.0,
                )

        # Exit the long position
        elif signal.signal == SignalType.SELL:

            if (
                self.position is not None
                and self.position.direction == OrderDirection.BUY
            ):

                return OrderEvent(
                    symbol=signal.symbol,
                    direction=OrderDirection.SELL,
                    quantity=self.position.quantity,
                )

        return None

    def process_fill(self, fill: FillEvent):
        """
        Update the portfolio after an order has been filled.
        """

        if fill.direction == OrderDirection.BUY:

            self.position = Position(
                symbol=fill.symbol,
                direction=fill.direction,
                quantity=fill.quantity,
                entry_price=fill.price,
            )

        elif fill.direction == OrderDirection.SELL:

            self.position = None