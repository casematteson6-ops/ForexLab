from engine.csv_loader import CSVLoader
from engine.validator import DataValidator
from engine.event_queue import EventQueue
from engine.data_handler import DataHandler

loader = CSVLoader()

candles = loader.load(
    "data/raw/eurchf_h1_MERGED_PARTIAL.csv",
    "EURCHF"
)

validator = DataValidator()
errors = validator.validate(candles)

print("=" * 55)
print(f"Candles Loaded : {len(candles)}")
print(f"Validation Errors : {len(errors)}")

if len(errors) == 0:
    print("\nDataset PASSED validation!")
else:
    print("\nDataset FAILED validation!")

print("=" * 55)

queue = EventQueue()

handler = DataHandler(candles, queue)

print("\nStreaming first five candles...\n")

for _ in range(5):
    handler.stream_next()

    event = queue.get()

    print(
        handler.current_candle().timestamp,
        event.event_type
    )