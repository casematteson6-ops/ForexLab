from models.candle import Candle


class DataValidator:
    """
    Validates historical candle data before it is used
    in the backtesting engine.
    """

    def validate(self, candles):
        errors = []

        if not candles:
            errors.append("Dataset is empty.")
            return errors

        previous_time = None

        for i, candle in enumerate(candles):

            # Check OHLC integrity
            if candle.high < max(candle.open, candle.close):
                errors.append(
                    f"{candle.timestamp}: High is below Open/Close."
                )

            if candle.low > min(candle.open, candle.close):
                errors.append(
                    f"{candle.timestamp}: Low is above Open/Close."
                )

            if candle.high < candle.low:
                errors.append(
                    f"{candle.timestamp}: High is lower than Low."
                )

            # Check timestamps are increasing
            if previous_time and candle.timestamp <= previous_time:
                errors.append(
                    f"{candle.timestamp}: Duplicate or out-of-order timestamp."
                )

            previous_time = candle.timestamp

            # Check for negative volume
            if candle.volume is not None and candle.volume < 0:
                errors.append(
                    f"{candle.timestamp}: Negative volume."
                )

        return errors