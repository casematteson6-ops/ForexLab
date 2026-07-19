from engine.strategy import Strategy
from engine.events import SignalEvent, SignalType


class SMACrossoverStrategy(Strategy):
    """
    Simple Moving Average crossover strategy.
    """

    def __init__(
        self,
        symbol,
        event_queue,
        short_window=20,
        long_window=50,
    ):
        super().__init__(event_queue)

        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window

        self.prices = []
        self.in_market = False

    def on_market(self, event):

        # Store latest closing price
        self.prices.append(event.candle.close)

        # Wait until enough candles exist
        if len(self.prices) < self.long_window:
            return

        short_ma = sum(
            self.prices[-self.short_window:]
        ) / self.short_window

        long_ma = sum(
            self.prices[-self.long_window:]
        ) / self.long_window

        if short_ma > long_ma and not self.in_market:

            self.send_signal(
                SignalEvent(
                    self.symbol,
                    SignalType.BUY,
                )
            )

            self.in_market = True

        elif short_ma < long_ma and self.in_market:

            self.send_signal(
                SignalEvent(
                    self.symbol,
                    SignalType.SELL,
                )
            )

            self.in_market = False