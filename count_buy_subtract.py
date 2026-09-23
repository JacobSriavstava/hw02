# Cross-validation Prompt B: count the total rows in fact_transactions.csv,
# then subtract the count of rows where txn_type is Sell, Deposit,
# Withdrawal, Dividend, or Advisory Fee. The remainder should equal the
# count of Buy transactions.

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "04_Data" / "Raw" / "fact_transactions.csv"

df = pd.read_csv(DATA_PATH)

total_rows = len(df)
other_types = ["Sell", "Deposit", "Withdrawal", "Dividend", "Advisory Fee"]
other_count = df["txn_type"].isin(other_types).sum()

buy_count_by_subtraction = total_rows - other_count

print(f"Total rows:                          {total_rows:,}")
print(f"Rows where txn_type is one of {other_types}: {other_count:,}")
print(f"Total - other types (implied Buy count): {buy_count_by_subtraction:,}")
