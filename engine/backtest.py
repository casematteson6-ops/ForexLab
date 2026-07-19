from engine.events import EventType


class BacktestEngine:
    """
    Coordinates the event-driven backtest.
    """

    def __init__(
        self,
        data_handler,
        event_queue,
        strategy,
        portfolio,
        execution,
    ):
        self.data_handler = data_handler
        self.event_queue = event_queue
        self.strategy = strategy
        self.portfolio = portfolio
        self.execution = execution

    def run(self):
        """
        Main event loop.
        """

        while self.data_handler.has_next():

            # Stream one candle
            self.data_handler.stream_next()

            # Process all events generated from that candle
            while not self.event_queue.empty():

                event = self.event_queue.get()

                if event.event_type == EventType.MARKET:
                    self.strategy.on_market(event)

                elif event.event_type == EventType.SIGNAL:

                    order = self.portfolio.process_signal(event)

                    if order is not None:
                        self.event_queue.put(order)

                elif event.event_type == EventType.ORDER:

                    candle = self.data_handler.current_candle()

                    fill = self.execution.execute_order(
                        order=event,
                        price=candle.close
                    )

                    self.event_queue.put(fill)

                elif event.event_type == EventType.FILL:

                    print(
                        f"FILLED: "
                        f"{event.symbol} "
                        f"{event.direction.name} "
                        f"{event.quantity} @ "
                        f"{event.price}"
                    )