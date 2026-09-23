# ==============================================================================
# Script:      hw02_eda.py
# Dataset:     fact_transactions.csv (Wildcat Capital transaction portfolio)
# Author:      Jacob Srivastava
# Generated:   2026-09-21
# Course:      MIS3060 - Business Intelligence with AI, Villanova University
#
# Purpose:     Single-run exploratory data analysis (EDA) script that loads,
#              validates, profiles, and visualizes the fact_transactions
#              dataset per hw02/specification.md. Prints all findings to the
#              terminal, writes a plain-text profile to hw02_profile.txt, and
#              saves three charts to hw02/charts/.
# ==============================================================================

import sys
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ------------------------------------------------------------------------------
# Paths (resolved relative to this script's location, so it runs correctly
# whether invoked as `python hw02_eda.py` from inside hw02/, or as
# `python hw02/hw02_eda.py` from the repo root).
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "04_Data" / "Raw" / "fact_transactions.csv"
CHARTS_DIR = BASE_DIR / "charts"
PROFILE_PATH = BASE_DIR / "hw02_profile.txt"
EXPECTED_SHAPE = (298772, 9)

CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# Validated categorical palette (dataviz skill default, fixed hue order).
CAT_COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
GRID_COLOR = "#e1e0d9"

plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.edgecolor": "#c3c2b7",
    "axes.labelcolor": INK_PRIMARY,
    "text.color": INK_PRIMARY,
    "xtick.color": INK_SECONDARY,
    "ytick.color": INK_SECONDARY,
    "figure.facecolor": "#fcfcfb",
    "axes.facecolor": "#fcfcfb",
})

# ------------------------------------------------------------------------------
# Summary buffer: items 2-13 are printed to the terminal AND captured here so
# they can be written verbatim to hw02_profile.txt (item 16).
# ------------------------------------------------------------------------------
summary_lines = []


def log(text=""):
    """Print to terminal and capture into the profile-file buffer."""
    print(text)
    summary_lines.append(text)


def section(title):
    log("")
    log("=" * 78)
    log(title)
    log("=" * 78)


# ==============================================================================
# 1. Load the data
# ==============================================================================
print(f"Loading data from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)
print("Load complete.")

# ==============================================================================
# 2. Shape
# ==============================================================================
section("2. DATASET SHAPE")
log(f"Rows x Columns: {df.shape[0]:,} x {df.shape[1]}")

# ==============================================================================
# 3. Column names and data types
# ==============================================================================
section("3. COLUMN NAMES AND DATA TYPES")
for col, dtype in df.dtypes.items():
    log(f"  {col:<15} {dtype}")

# ==============================================================================
# 4. Missing value counts per column
# ==============================================================================
section("4. MISSING VALUES PER COLUMN")
missing = df.isnull().sum()
for col, cnt in missing.items():
    log(f"  {col:<15} {cnt:,}")

# ==============================================================================
# 5. Descriptive statistics for numeric columns
# ==============================================================================
section("5. DESCRIPTIVE STATISTICS (NUMERIC COLUMNS)")
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
desc = df[numeric_cols].describe().T
desc = desc.rename(columns={
    "count": "Count", "mean": "Mean", "std": "Std Dev", "min": "Min",
    "25%": "25th Pct", "50%": "Median", "75%": "75th Pct", "max": "Max",
})
log(desc.to_string())

# ==============================================================================
# 6. Value counts and percentages for txn_type (most to least frequent)
# ==============================================================================
section("6. TXN_TYPE VALUE COUNTS AND PERCENTAGES")
type_counts = df["txn_type"].value_counts()
type_pcts = df["txn_type"].value_counts(normalize=True) * 100
log(f"  Unique txn_type values: {df['txn_type'].nunique()}")
log("")
for t in type_counts.index:
    log(f"  {t:<15} {type_counts[t]:>8,}   ({type_pcts[t]:>5.2f}%)")

# ==============================================================================
# 7. Unique counts of clients, advisors, securities
# ==============================================================================
section("7. UNIQUE ENTITY COUNTS")
log(f"  Unique clients:    {df['client_id'].nunique():,}")
log(f"  Unique advisors:   {df['advisor_id'].nunique():,}")
log(f"  Unique securities: {df['security_id'].nunique():,}")

# ==============================================================================
# 8. Date range (txn_date)
# ==============================================================================
section("8. TXN_DATE RANGE")
log(f"  Earliest txn_date: {df['txn_date'].min()}")
log(f"  Latest txn_date:   {df['txn_date'].max()}")

# ==============================================================================
# 9. Duplicate rows by txn_id
# ==============================================================================
section("9. DUPLICATE TXN_ID CHECK")
dup_count = df["txn_id"].duplicated().sum()
log(f"  Duplicate txn_id count: {dup_count:,}")

# ==============================================================================
# 10. Mean, median, skewness of amount
# ==============================================================================
section("10. AMOUNT: MEAN, MEDIAN, SKEWNESS")
amount_mean = df["amount"].mean()
amount_median = df["amount"].median()
amount_skew = df["amount"].skew()
log(f"  Mean amount:     ${amount_mean:,.2f}")
log(f"  Median amount:   ${amount_median:,.2f}")
log(f"  Skewness:        {amount_skew:.2f}")

# ==============================================================================
# 11. Group by txn_type: count, mean, median amount (sorted by mean desc)
# ==============================================================================
section("11. AMOUNT BY TXN_TYPE (SORTED BY MEAN DESCENDING)")
grouped = df.groupby("txn_type")["amount"].agg(
    Count="count", Mean="mean", Median="median"
)
grouped["Mean"] = grouped["Mean"].round(2)
grouped["Median"] = grouped["Median"].round(2)
grouped = grouped.sort_values("Mean", ascending=False)
log(grouped.to_string())

# ==============================================================================
# 12. Correlation matrix for shares, price, amount + top 3 strongest pairs
# ==============================================================================
section("12. CORRELATION MATRIX (shares, price, amount)")
corr = df[["shares", "price", "amount"]].corr().round(2)
log(corr.to_string())

log("")
log("Three strongest correlations (excluding self-correlation):")
corr_pairs = (
    corr.where(~np.eye(len(corr), dtype=bool))
    .stack()
    .reset_index()
)
corr_pairs.columns = ["Var 1", "Var 2", "Correlation"]
corr_pairs["pair_key"] = corr_pairs.apply(
    lambda r: tuple(sorted([r["Var 1"], r["Var 2"]])), axis=1
)
corr_pairs = corr_pairs.drop_duplicates(subset="pair_key").drop(columns="pair_key")
corr_pairs["AbsCorrelation"] = corr_pairs["Correlation"].abs()
corr_pairs = corr_pairs.sort_values("AbsCorrelation", ascending=False).head(3)
for _, row in corr_pairs.iterrows():
    log(f"  {row['Var 1']} <-> {row['Var 2']}: {row['Correlation']:.2f}")

# ==============================================================================
# 13. Shares: min, max, negative count by txn_type
# ==============================================================================
section("13. SHARES BY TXN_TYPE (MIN, MAX, NEGATIVE COUNT)")
shares_by_type = df.groupby("txn_type")["shares"].agg(
    Min="min", Max="max",
    **{"Negative Count": lambda s: (s < 0).sum()}
)
log(shares_by_type.to_string())

# ==============================================================================
# 14. Shape warning
# ==============================================================================
if df.shape != EXPECTED_SHAPE:
    print("")
    print(f"WARNING: Dataset shape {df.shape} does not match expected shape {EXPECTED_SHAPE}.")
else:
    print("")
    print(f"Shape check OK: dataset shape matches expected {EXPECTED_SHAPE}.")

# ==============================================================================
# 15. Charts
# ==============================================================================
print("")
print("Generating charts...")

# --- Chart 1: Histogram of amount with mean/median lines -------------------
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.hist(df["amount"].dropna(), bins=80, color=CAT_COLORS[0], alpha=0.85, edgecolor="white", linewidth=0.3)
ax.axvline(amount_mean, color=CAT_COLORS[1], linestyle="--", linewidth=2,
           label=f"Mean: ${amount_mean:,.2f}")
ax.axvline(amount_median, color=CAT_COLORS[5], linestyle="--", linewidth=2,
           label=f"Median: ${amount_median:,.2f}")
ax.set_title("Distribution of Transaction Amount", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Amount ($)", fontsize=11)
ax.set_ylabel("Number of Transactions", fontsize=11)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.grid(axis="y", color=GRID_COLOR, linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
ax.legend(frameon=False, fontsize=10)
fig.tight_layout()
fig.savefig(CHARTS_DIR / "hist_amount.png", dpi=150)
plt.close(fig)

# --- Chart 2: Horizontal box plot of amount by txn_type ---------------------
type_order = df.groupby("txn_type")["amount"].median().sort_values(ascending=False).index.tolist()
box_data = [df.loc[df["txn_type"] == t, "amount"].dropna().values for t in type_order]

fig, ax = plt.subplots(figsize=(9, 5.5))
bp = ax.boxplot(
    box_data, orientation="horizontal", tick_labels=type_order, patch_artist=True,
    showfliers=False, widths=0.6,
    medianprops=dict(color=INK_PRIMARY, linewidth=1.8),
    whiskerprops=dict(color=INK_SECONDARY),
    capprops=dict(color=INK_SECONDARY),
)
for patch, color in zip(bp["boxes"], (CAT_COLORS * 2)[: len(type_order)]):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)
    patch.set_edgecolor(INK_SECONDARY)
ax.set_title("Transaction Amount by Type", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Amount ($)", fontsize=11)
ax.set_ylabel("")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.grid(axis="x", color=GRID_COLOR, linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
fig.tight_layout()
fig.savefig(CHARTS_DIR / "box_amount_by_type.png", dpi=150)
plt.close(fig)

# --- Chart 3: Scatter of shares vs amount, colored by txn_type -------------
fig, ax = plt.subplots(figsize=(9.5, 6))
scatter_types = df["txn_type"].dropna().unique().tolist()
scatter_types.sort()
color_map = {t: CAT_COLORS[i % len(CAT_COLORS)] for i, t in enumerate(scatter_types)}

# Shuffle rows before plotting so overlapping points from different
# categories interleave in draw order, rather than letting whichever
# category is drawn last visually dominate the dense region.
plot_df = df.dropna(subset=["shares", "amount", "txn_type"]).sample(
    frac=1, random_state=42
)
point_colors = plot_df["txn_type"].map(color_map)
ax.scatter(
    plot_df["shares"], plot_df["amount"], s=6, alpha=0.15,
    color=point_colors, linewidths=0, rasterized=True,
)
legend_handles = [
    plt.Line2D([0], [0], marker="o", linestyle="", markersize=7,
               markerfacecolor=color_map[t], markeredgewidth=0, label=t)
    for t in scatter_types
]
ax.set_title("Shares vs. Amount by Transaction Type", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Shares", fontsize=11)
ax.set_ylabel("Amount ($)", fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.grid(color=GRID_COLOR, linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
legend = ax.legend(handles=legend_handles, frameon=False, fontsize=10, loc="upper left", bbox_to_anchor=(1.01, 1.0))
fig.tight_layout()
fig.savefig(CHARTS_DIR / "scatter_shares_amount.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print(f"Charts saved to: {CHARTS_DIR}")

# ==============================================================================
# 16. Save plain-text summary of items 2-13
# ==============================================================================
header = [
    "HW02 EDA PROFILE - fact_transactions.csv (Wildcat Capital)",
    f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    f"Author: Jacob Srivastava",
]
with open(PROFILE_PATH, "w") as f:
    f.write("\n".join(header) + "\n")
    f.write("\n".join(summary_lines) + "\n")

print(f"Profile summary saved to: {PROFILE_PATH}")
print("")
print("EDA script complete.")
