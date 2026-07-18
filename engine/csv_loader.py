import csv
from datetime import datetime, timezone

from models.candle import Candle


class CSVLoader:

    def load(self, filepath, symbol):

        candles = []

        with open(filepath, "r", newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                timestamp = datetime.fromtimestamp(
                    int(row["timestamp"]) / 1000,
                    tz=timezone.utc
                )

                volume = None

                if "volume" in row and row["volume"] != "":
                    volume = float(row["volume"])

                candle = Candle(
                    symbol=symbol,
                    timestamp=timestamp,
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=volume
                )

                candles.append(candle)

        return candles