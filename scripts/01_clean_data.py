"""
STEP 1 — DATA CLEANING
======================================================================
What this script does, in plain English:
  1. Loads the raw posts CSV (90,343 rows, 2009-2025).
  2. Converts the True/False flag columns from text into real booleans.
  3. Parses the 'date' column into a proper datetime + a plain date.
  4. Removes rows we don't want for sentiment analysis:
        - deleted posts        (deleted_flag = True)
        - pure reposts/retweets (repost_flag  = True)  -> not Trump's own words
        - rows with empty text  (nothing to score)
  5. Removes duplicate post IDs.
  6. Saves a clean file to data/processed/posts_clean.csv
  7. Prints a before/after report so we can see exactly what changed.

Why we do this:
  Sentiment analysis should run on Trump's OWN words. Reposts and deleted
  posts add noise. Clean input = trustworthy sentiment scores later.
======================================================================
"""

from pathlib import Path
import pandas as pd

# --- File locations (relative to project root) -----------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "djt_posts_dec2025.csv"
OUT_FILE = PROJECT_ROOT / "data" / "processed" / "posts_clean.csv"

# The columns that are stored as the text "True"/"False" in the CSV.
FLAG_COLUMNS = ["quote_flag", "repost_flag", "deleted_flag"]


def to_bool(series: pd.Series) -> pd.Series:
    """Turn a column of the strings 'True'/'False' into real True/False."""
    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .map({"true": True, "false": False})
        .fillna(False)
    )


def main() -> None:
    print("=" * 60)
    print("STEP 1: CLEANING THE POSTS DATA")
    print("=" * 60)

    # 1. Load -----------------------------------------------------------
    df = pd.read_csv(RAW_FILE, dtype=str)  # read everything as text first, parse deliberately
    start_rows = len(df)
    print(f"Loaded raw file: {start_rows:,} rows")

    # 2. Flags text -> boolean -----------------------------------------
    for col in FLAG_COLUMNS:
        df[col] = to_bool(df[col])

    # 3. Parse dates ----------------------------------------------------
    # The dates look like: 2025-12-31 21:54:21+00:00 (UTC).
    df["datetime_utc"] = pd.to_datetime(df["date"], utc=True, errors="coerce")
    df["date_only"] = df["datetime_utc"].dt.date  # the calendar day, used to join to markets

    # Numeric engagement columns
    df["favorite_count"] = pd.to_numeric(df["favorite_count"], errors="coerce").fillna(0).astype(int)
    df["repost_count"] = pd.to_numeric(df["repost_count"], errors="coerce").fillna(0).astype(int)

    # 4. Filtering ------------------------------------------------------
    removed = {}

    before = len(df)
    df = df[~df["deleted_flag"]]
    removed["deleted posts"] = before - len(df)

    before = len(df)
    df = df[~df["repost_flag"]]
    removed["pure reposts"] = before - len(df)

    before = len(df)
    df = df[df["text"].notna() & (df["text"].astype(str).str.strip() != "")]
    removed["empty text"] = before - len(df)

    before = len(df)
    df = df[df["datetime_utc"].notna()]
    removed["unparseable dates"] = before - len(df)

    # 5. De-duplicate by post id ---------------------------------------
    before = len(df)
    df = df.drop_duplicates(subset=["id"], keep="first")
    removed["duplicate ids"] = before - len(df)

    # 6. Save -----------------------------------------------------------
    df = df.sort_values("datetime_utc").reset_index(drop=True)
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_FILE, index=False)

    # 7. Report ---------------------------------------------------------
    print("\nRows removed during cleaning:")
    for reason, count in removed.items():
        print(f"  - {reason:<20}: {count:,}")
    print(f"\nFinal clean rows: {len(df):,}  (started with {start_rows:,})")
    print("\nPosts by platform (after cleaning):")
    print(df["platform"].value_counts().to_string())
    print(f"\nDate range: {df['date_only'].min()}  ->  {df['date_only'].max()}")
    print(f"\nSaved clean file to: {OUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
