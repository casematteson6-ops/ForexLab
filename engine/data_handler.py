from typing import List

from engine.events import MarketEvent
from engine.event_queue import EventQueue
from models.candle import Candle


class DataHandler:
    """
    Feeds one candle at a time into the event queue.
    """

    def __init__(self, candles: List[Candle], event_queue: EventQueue):
        self.candles = candles
        self.event_queue = event_queue
        self.current_index = 0

    def has_next(self) -> bool:
        """Return True if more candles remain."""
        return self.current_index < len(self.candles)

    def stream_next(self):
        """Send the next MarketEvent into the queue."""

        if self.has_next():
            candle = self.candles[self.current_index]

            event = MarketEvent(
                candle.symbol,
                candle.timestamp,
                candle,
            )

            self.event_queue.put(event)
            self.current_index += 1

    def current_candle(self) -> Candle:
        """Return the current candle."""
        return self.candles[self.current_index - 1]