from engine.strategy import Strategy
from engine.events import SignalEvent, SignalType


class SMACrossoverStrategy(Strategy):

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
    """
    Receives each MarketEvent and stores the latest closing price.
    """

    # Store the newest closing price
    self.prices.append(event.candle.close)

    # Wait until we have enough candles
    if len(self.prices) < self.long_window:
        return