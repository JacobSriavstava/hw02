# Cross-validation Prompt A: count rows in fact_transactions.csv where
# txn_type equals exactly 'Buy'.

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "04_Data" / "Raw" / "fact_transactions.csv"

df = pd.read_csv(DATA_PATH)
buy_count = (df["txn_type"] == "Buy").sum()

print(f"Rows where txn_type == 'Buy': {buy_count:,}")
