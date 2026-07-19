from engine.csv_loader import CSVLoader
from engine.validator import DataValidator
from engine.event_queue import EventQueue
from engine.data_handler import DataHandler
from engine.portfolio import Portfolio
from engine.execution import ExecutionHandler
from engine.backtest import BacktestEngine

from strategies.sma_cross import SMACrossoverStrategy


def main():

    loader = CSVLoader()

    candles = loader.load(
        "data/raw/eurchf_h1_MERGED_PARTIAL.csv",
        "EURCHF",
    )

    validator = DataValidator()
    errors = validator.validate(candles)

    print("=" * 55)
    print(f"Candles Loaded : {len(candles)}")
    print(f"Validation Errors : {len(errors)}")

    if errors:
        print("\nDataset FAILED validation!")
        return

    print("\nDataset PASSED validation!")
    print("=" * 55)

    event_queue = EventQueue()

    data_handler = DataHandler(
        candles,
        event_queue,
    )

    strategy = SMACrossoverStrategy(
        symbol="EURCHF",
        event_queue=event_queue,
    )

    portfolio = Portfolio()

    execution = ExecutionHandler()

    engine = BacktestEngine(
        data_handler=data_handler,
        event_queue=event_queue,
        strategy=strategy,
        portfolio=portfolio,
        execution=execution,
    )

    print("\nRunning Backtest...\n")

    engine.run()

    print("\nBacktest Complete!")

    print("\n" + "=" * 55)
    print("FOREXLAB PERFORMANCE REPORT")
    print("=" * 55)

    print(f"Starting Balance : ${portfolio.initial_balance:,.2f}")
    print(f"Ending Balance   : ${portfolio.cash:,.2f}")
    print(f"Net Profit       : ${portfolio.total_profit():,.2f}")
    print()

    print(f"Trades           : {portfolio.total_trades()}")
    print(f"Winning Trades   : {portfolio.winning_trades()}")
    print(f"Losing Trades    : {portfolio.losing_trades()}")

    if portfolio.total_trades() > 0:
        win_rate = (
            portfolio.winning_trades()
            / portfolio.total_trades()
        ) * 100

        print(f"Win Rate         : {win_rate:.2f}%")
    else:
        print("Win Rate         : N/A")

    print("=" * 55)


if __name__ == "__main__":
    main()