from engine.csv_loader import CSVLoader
from engine.validator import DataValidator

loader = CSVLoader()

candles = loader.load(
    "data/raw/eurchf_h1_MERGED_PARTIAL.csv",
    "EURCHF"
)

validator = DataValidator()

errors = validator.validate(candles)

print("=" * 50)
print(f"Candles Loaded : {len(candles)}")
print(f"Validation Errors : {len(errors)}")

if errors:
    print("\nFirst Errors:")
    for error in errors[:10]:
        print(error)
else:
    print("\nDataset PASSED validation!")

print("=" * 50)