from engine.events import OrderEvent, FillEvent


class ExecutionHandler:
    """
    Simulates a broker by converting orders into fills.
    Future versions will support slippage, spread, and partial fills.
    """

    def __init__(self, commission: float = 0.0):
        self.commission = commission

    def execute_order(self, order: OrderEvent, price: float) -> FillEvent:
        """
        Execute an order at the supplied market price.
        """

        fill = FillEvent(
            symbol=order.symbol,
            direction=order.direction,
            quantity=order.quantity,
            price=price,
            commission=self.commission,
        )

        return fill