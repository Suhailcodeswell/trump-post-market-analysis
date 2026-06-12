"""
STEP 7 — BUILD & VERIFY THE SQL LAYER (DuckDB)
======================================================================
What this script does, in plain English:
  1. Creates a local SQL database file (DuckDB - no server install needed)
     with the SAME star schema described in sql_queries/01_create_schema.sql.
  2. Loads our processed CSVs into the Dim_Date, Dim_Platform, Fact_Posts
     and Fact_Market tables.
  3. Runs the key analytical queries (window functions, LEFT JOINs,
     CORR()) and prints the results to PROVE the SQL works.

Why DuckDB:
  DuckDB speaks almost the same SQL as PostgreSQL but runs as a single
  file with no server to install. It lets us verify the exact query
  logic now. The canonical PostgreSQL scripts live in /sql_queries and
  will run as-is once PostgreSQL is installed (see 07b_load_to_postgres).

Output: data/processed/trump_market.duckdb
======================================================================
"""

from pathlib import Path
import duckdb
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROC = PROJECT_ROOT / "data" / "processed"
DB_FILE = PROC / "trump_market.duckdb"


def main() -> None:
    print("=" * 60)
    print("STEP 7: BUILDING & VERIFYING THE SQL LAYER (DuckDB)")
    print("=" * 60)

    if DB_FILE.exists():
        DB_FILE.unlink()
    con = duckdb.connect(str(DB_FILE))

    posts = pd.read_csv(PROC / "posts_tagged.csv", low_memory=False)
    market = pd.read_csv(PROC / "market_data.csv")

    # ---- Prepare Fact_Posts -----------------------------------------
    posts["date_key"] = pd.to_datetime(posts["date_only"]).dt.date
    posts["engagement"] = posts["favorite_count"] + posts["repost_count"]
    fact_posts = posts[[
        "id", "date_key", "platform", "sentiment_score", "sentiment_label",
        "favorite_count", "repost_count", "engagement", "word_count",
        "topic_bitcoin", "topic_sp500", "topic_nasdaq", "topic_tariffs_china",
    ]].rename(columns={"id": "post_id", "topic_tariffs_china": "topic_tariffs"})

    # ---- Prepare Dim_Platform ---------------------------------------
    platforms = (
        pd.DataFrame({"platform_name": sorted(posts["platform"].unique())})
        .reset_index()
        .rename(columns={"index": "platform_key"})
    )
    platforms["platform_key"] += 1
    fact_posts = fact_posts.merge(
        platforms, left_on="platform", right_on="platform_name", how="left"
    ).drop(columns=["platform", "platform_name"])

    # ---- Prepare Fact_Market ----------------------------------------
    market["date_key"] = pd.to_datetime(market["date_only"]).dt.date
    fact_market = market.rename(columns={"close": "close_price"})[
        ["date_key", "instrument", "close_price", "daily_return", "volatility_7d"]
    ]

    # ---- Prepare Dim_Date (union of all dates we use) ---------------
    all_dates = pd.Series(
        pd.to_datetime(pd.concat([
            pd.Series(fact_posts["date_key"]), pd.Series(fact_market["date_key"])
        ]).unique())
    ).sort_values()
    dim_date = pd.DataFrame({"date_key": all_dates.dt.date})
    dim_date["year"] = all_dates.dt.year.values
    dim_date["quarter"] = all_dates.dt.quarter.values
    dim_date["month"] = all_dates.dt.month.values
    dim_date["month_name"] = all_dates.dt.month_name().values
    dim_date["day"] = all_dates.dt.day.values
    dim_date["day_of_week"] = all_dates.dt.day_name().values
    dim_date["is_weekend"] = all_dates.dt.dayofweek.isin([5, 6]).values

    # ---- Register & create tables -----------------------------------
    con.register("dim_date_df", dim_date)
    con.register("dim_platform_df", platforms)
    con.register("fact_posts_df", fact_posts)
    con.register("fact_market_df", fact_market)

    con.execute("CREATE TABLE Dim_Date     AS SELECT * FROM dim_date_df")
    con.execute("CREATE TABLE Dim_Platform AS SELECT * FROM dim_platform_df")
    con.execute("CREATE TABLE Fact_Posts   AS SELECT * FROM fact_posts_df")
    con.execute("CREATE TABLE Fact_Market  AS SELECT * FROM fact_market_df")

    print("\nTables created. Row counts:")
    for tbl in ["Dim_Date", "Dim_Platform", "Fact_Posts", "Fact_Market"]:
        n = con.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        print(f"  - {tbl:<13}: {n:,}")

    # ---- VERIFY: run a few of the analytical queries ----------------
    print("\n--- Q3: Correlation (sentiment vs S&P return / volatility) ---")
    q3 = con.execute("""
        WITH daily AS (
            SELECT date_key, AVG(sentiment_score) AS avg_sentiment
            FROM Fact_Posts GROUP BY date_key
        )
        SELECT ROUND(CORR(d.avg_sentiment, m.daily_return), 4)  AS corr_return,
               ROUND(CORR(d.avg_sentiment, m.volatility_7d), 4) AS corr_volatility,
               COUNT(*) AS n_days
        FROM Fact_Market m JOIN daily d ON d.date_key = m.date_key
        WHERE m.instrument = 'sp500'
    """).fetchdf()
    print(q3.to_string(index=False))

    print("\n--- Q4: Platform comparison (Twitter vs Truth Social) ---")
    q4 = con.execute("""
        SELECT p.platform_name, COUNT(*) AS total_posts,
               ROUND(AVG(f.sentiment_score), 4) AS avg_sentiment,
               ROUND(AVG(f.engagement), 1)      AS avg_engagement
        FROM Fact_Posts f JOIN Dim_Platform p ON p.platform_key = f.platform_key
        GROUP BY p.platform_name ORDER BY total_posts DESC
    """).fetchdf()
    print(q4.to_string(index=False))

    print("\n--- Q5: Bitcoin event study in SQL (first 5 events) ---")
    q5 = con.execute("""
        WITH btc AS (
            SELECT date_key, close_price,
                   LEAD(close_price, 7) OVER (ORDER BY date_key) AS price_1w_later
            FROM Fact_Market WHERE instrument = 'bitcoin'
        ),
        btc_events AS (SELECT DISTINCT date_key FROM Fact_Posts WHERE topic_bitcoin = TRUE)
        SELECT e.date_key AS event_date, b.close_price AS buy_price,
               ROUND(((b.price_1w_later / b.close_price) - 1) * 100, 2) AS return_1w_pct
        FROM btc_events e JOIN btc b ON b.date_key = e.date_key
        WHERE b.price_1w_later IS NOT NULL
        ORDER BY e.date_key LIMIT 5
    """).fetchdf()
    print(q5.to_string(index=False))

    con.close()
    print(f"\nSaved SQL database to: {DB_FILE}")
    print("All analytical queries ran successfully (SQL logic verified).")
    print("=" * 60)


if __name__ == "__main__":
    main()
