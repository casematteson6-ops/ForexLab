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


@dataclass
class Trade:
    symbol: str
    entry_price: float
    exit_price: float
    quantity: float
    profit: float


class Portfolio:
    """
    Tracks positions, completed trades, and account balance.
    """

    def __init__(self, initial_balance: float = 10000.0):
        self.initial_balance = initial_balance
        self.cash = initial_balance

        self.position: Optional[Position] = None

        # Store every completed trade
        self.trades = []

    def process_signal(self, signal: SignalEvent) -> Optional[OrderEvent]:
        """
        Convert strategy signals into executable orders.
        """

        # BUY
        if signal.signal == SignalType.BUY:

            if self.position is None:

                return OrderEvent(
                    symbol=signal.symbol,
                    direction=OrderDirection.BUY,
                    quantity=1.0,
                )

        # SELL
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
        Update the portfolio after a fill.
        """

        # Opening a position
        if fill.direction == OrderDirection.BUY:

            self.position = Position(
                symbol=fill.symbol,
                direction=fill.direction,
                quantity=fill.quantity,
                entry_price=fill.price,
            )

        # Closing a position
        elif fill.direction == OrderDirection.SELL:

            if self.position is not None:

                profit = (
                    fill.price - self.position.entry_price
                ) * fill.quantity

                self.cash += profit

                self.trades.append(
                    Trade(
                        symbol=fill.symbol,
                        entry_price=self.position.entry_price,
                        exit_price=fill.price,
                        quantity=fill.quantity,
                        profit=profit,
                    )
                )

                self.position = None

    def total_profit(self):
        return self.cash - self.initial_balance

    def total_trades(self):
        return len(self.trades)

    def winning_trades(self):
        return sum(1 for trade in self.trades if trade.profit > 0)

    def losing_trades(self):
        return sum(1 for trade in self.trades if trade.profit <= 0)