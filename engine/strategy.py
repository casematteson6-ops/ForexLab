from abc import ABC, abstractmethod

from engine.events import MarketEvent, SignalEvent


class Strategy(ABC):
    """
    Base class for all trading strategies.
    """

    def __init__(self, event_queue):
        self.event_queue = event_queue

    @abstractmethod
    def on_market(self, event: MarketEvent):
        """
        Called whenever a new market event arrives.
        """
        pass

    def send_signal(self, signal: SignalEvent):
        """
        Place a signal onto the event queue.
        """
        self.event_queue.put(signal)