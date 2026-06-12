"""
STEP 7b — LOAD INTO REAL POSTGRESQL  (optional / run when ready)
======================================================================
Use this ONLY after PostgreSQL is installed. It:
  1. Connects to your PostgreSQL server.
  2. Runs sql_queries/01_create_schema.sql to build the star schema.
  3. Loads the processed CSVs into the tables.

Setup before running:
  1. Install PostgreSQL (https://www.postgresql.org/download/windows/).
  2. pip install sqlalchemy psycopg2-binary   (already in requirements.txt)
  3. Set your connection string in the DB_URL below or via the
     DATABASE_URL environment variable, e.g.:
        postgresql+psycopg2://postgres:YOURPASSWORD@localhost:5432/trump_market
  4. Create the database first:  createdb trump_market
  5. Run:  python scripts/07b_load_to_postgres.py

If PostgreSQL is not installed yet, you do NOT need this file — the
analysis and the DuckDB-verified SQL already work without it.
======================================================================
"""

import os
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROC = PROJECT_ROOT / "data" / "processed"
SCHEMA_SQL = PROJECT_ROOT / "sql_queries" / "01_create_schema.sql"

DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/trump_market",
)


def main() -> None:
    try:
        from sqlalchemy import create_engine, text
    except ImportError:
        raise SystemExit("Please run: pip install sqlalchemy psycopg2-binary")

    print(f"Connecting to: {DB_URL}")
    engine = create_engine(DB_URL)

    # 1. Build the schema
    with engine.begin() as con:
        con.execute(text(SCHEMA_SQL.read_text(encoding="utf-8")))
    print("Schema created from 01_create_schema.sql")

    # 2. Build the same dataframes as the DuckDB script
    posts = pd.read_csv(PROC / "posts_tagged.csv", low_memory=False)
    market = pd.read_csv(PROC / "market_data.csv")

    posts["date_key"] = pd.to_datetime(posts["date_only"]).dt.date
    posts["engagement"] = posts["favorite_count"] + posts["repost_count"]

    platforms = (
        pd.DataFrame({"platform_name": sorted(posts["platform"].unique())})
        .reset_index().rename(columns={"index": "platform_key"})
    )
    platforms["platform_key"] += 1

    fact_posts = posts.merge(
        platforms, left_on="platform", right_on="platform_name", how="left"
    )[[
        "id", "date_key", "platform_key", "sentiment_score", "sentiment_label",
        "favorite_count", "repost_count", "engagement", "word_count",
        "topic_bitcoin", "topic_sp500", "topic_nasdaq", "topic_tariffs_china",
    ]].rename(columns={"id": "post_id", "topic_tariffs_china": "topic_tariffs"})

    market["date_key"] = pd.to_datetime(market["date_only"]).dt.date
    fact_market = market.rename(columns={"close": "close_price"})[
        ["date_key", "instrument", "close_price", "daily_return", "volatility_7d"]
    ]

    all_dates = pd.Series(pd.to_datetime(pd.concat([
        pd.Series(fact_posts["date_key"]), pd.Series(fact_market["date_key"])
    ]).unique())).sort_values()
    dim_date = pd.DataFrame({"date_key": all_dates.dt.date})
    dim_date["year"] = all_dates.dt.year.values
    dim_date["quarter"] = all_dates.dt.quarter.values
    dim_date["month"] = all_dates.dt.month.values
    dim_date["month_name"] = all_dates.dt.month_name().values
    dim_date["day"] = all_dates.dt.day.values
    dim_date["day_of_week"] = all_dates.dt.day_name().values
    dim_date["is_weekend"] = all_dates.dt.dayofweek.isin([5, 6]).values

    # 3. Load (append into the created tables)
    dim_date.to_sql("dim_date", engine, if_exists="append", index=False)
    platforms.to_sql("dim_platform", engine, if_exists="append", index=False)
    fact_market.to_sql("fact_market", engine, if_exists="append", index=False)
    fact_posts.to_sql("fact_posts", engine, if_exists="append", index=False)

    print("Loaded: Dim_Date, Dim_Platform, Fact_Market, Fact_Posts")
    print("Done. You can now run sql_queries/02_analysis_queries.sql in psql / pgAdmin.")


if __name__ == "__main__":
    main()
