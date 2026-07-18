from collections import deque
from typing import Optional

from engine.events import Event


class EventQueue:
    """
    FIFO queue for the event-driven backtesting engine.
    """

    def __init__(self):
        self._queue = deque()

    def put(self, event: Event):
        """Add an event to the queue."""
        self._queue.append(event)

    def get(self) -> Optional[Event]:
        """Retrieve the next event."""
        if self._queue:
            return self._queue.popleft()
        return None

    def empty(self) -> bool:
        """Return True if queue is empty."""
        return len(self._queue) == 0

    def size(self) -> int:
        """Return number of events waiting."""
        return len(self._queue)

    def clear(self):
        """Remove all pending events."""
        self._queue.clear()