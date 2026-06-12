"""
STEP 4 — BASELINE CORRELATION ANALYSIS
======================================================================
What this script does, in plain English:
  1. Loads the scored posts (Step 2) and the market data (Step 3).
  2. Collapses the posts to ONE row per day:
        - avg_sentiment : average sentiment of all posts that day
        - post_count    : how many posts that day
        - total_engagement : likes + reposts that day
  3. Joins that daily sentiment to the S&P 500 and Bitcoin by date.
  4. Measures correlation between Trump's daily sentiment and:
        - the market's daily return (does it go up/down with him?)
        - the market's volatility   (does it get jumpier?)
     ...both SAME-DAY and with a 1-day LAG (his post today vs the
        market TOMORROW), which is the more causally interesting test.
  5. Saves a merged daily table (for SQL / dashboards) and writes
     three charts to output/charts/.

Why a "daily" view:
  Markets only have one price per day, but Trump may post many times a
  day. To compare them we summarise each day's posts into one number.

Reading the correlation numbers (Pearson r, range -1..+1):
   0.0      = no linear relationship
   +/-0.1   = weak    | +/-0.3 = moderate | +/-0.5+ = strong
  The SIGN says direction (positive = move together).
======================================================================
"""

from pathlib import Path
import pandas as pd
from scipy.stats import pearsonr
import matplotlib
matplotlib.use("Agg")  # write charts to files, no GUI needed
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[1]
POSTS_FILE = PROJECT_ROOT / "data" / "processed" / "posts_scored.csv"
MARKET_FILE = PROJECT_ROOT / "data" / "processed" / "market_data.csv"
DAILY_OUT = PROJECT_ROOT / "data" / "processed" / "daily_merged.csv"
CHART_DIR = PROJECT_ROOT / "output" / "charts"


def safe_corr(x: pd.Series, y: pd.Series) -> tuple[float, float, int]:
    """Pearson correlation that ignores missing pairs. Returns (r, p, n)."""
    pair = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(pair) < 3:
        return float("nan"), float("nan"), len(pair)
    r, p = pearsonr(pair["x"], pair["y"])
    return r, p, len(pair)


def build_daily_sentiment() -> pd.DataFrame:
    posts = pd.read_csv(POSTS_FILE, low_memory=False)
    posts["engagement"] = posts["favorite_count"] + posts["repost_count"]
    daily = (
        posts.groupby("date_only")
        .agg(
            avg_sentiment=("sentiment_score", "mean"),
            post_count=("sentiment_score", "size"),
            total_engagement=("engagement", "sum"),
        )
        .reset_index()
    )
    daily["date_only"] = pd.to_datetime(daily["date_only"])
    return daily


def main() -> None:
    print("=" * 60)
    print("STEP 4: BASELINE CORRELATION ANALYSIS")
    print("=" * 60)
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    daily = build_daily_sentiment()
    print(f"Daily sentiment rows: {len(daily):,} days with posts")

    market = pd.read_csv(MARKET_FILE)
    market["date_only"] = pd.to_datetime(market["date_only"])

    results = []
    merged_frames = {}

    for instrument in ["sp500", "bitcoin"]:
        m = market[market["instrument"] == instrument].copy()
        # LEFT JOIN sentiment onto trading days only (markets are closed weekends).
        merged = m.merge(daily, on="date_only", how="left").sort_values("date_only")
        merged["avg_sentiment"] = merged["avg_sentiment"]  # NaN on days with no posts
        merged_frames[instrument] = merged

        # Same-day correlations
        r_ret, p_ret, n = safe_corr(merged["avg_sentiment"], merged["daily_return"])
        r_vol, p_vol, _ = safe_corr(merged["avg_sentiment"], merged["volatility_7d"])

        # 1-day lag: sentiment today vs the market's NEXT trading day
        merged["next_return"] = merged["daily_return"].shift(-1)
        r_lag, p_lag, n_lag = safe_corr(merged["avg_sentiment"], merged["next_return"])

        results.append(
            {
                "instrument": instrument,
                "n_days": n,
                "corr_sentiment_vs_return_sameday": round(r_ret, 4),
                "p_return_sameday": round(p_ret, 4),
                "corr_sentiment_vs_volatility": round(r_vol, 4),
                "p_volatility": round(p_vol, 4),
                "corr_sentiment_vs_return_nextday": round(r_lag, 4),
                "p_return_nextday": round(p_lag, 4),
            }
        )

    res_df = pd.DataFrame(results)
    print("\nCorrelation results (Pearson r, with p-values):")
    print(res_df.to_string(index=False))
    res_df.to_csv(PROJECT_ROOT / "output" / "correlation_results.csv", index=False)

    # Save the S&P merged daily table (used by SQL + dashboards later)
    sp = merged_frames["sp500"].copy()
    sp.to_csv(DAILY_OUT, index=False)
    print(f"\nSaved merged daily table to: {DAILY_OUT}")

    # ---- CHART 1: monthly sentiment vs S&P 500 price over time -------
    sp_plot = sp.copy()
    sp_plot["month"] = sp_plot["date_only"].dt.to_period("M").dt.to_timestamp()
    monthly = sp_plot.groupby("month").agg(
        avg_sentiment=("avg_sentiment", "mean"), close=("close", "mean")
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(13, 6))
    ax1.plot(monthly["month"], monthly["close"], color="#1f77b4", label="S&P 500 (price)")
    ax1.set_ylabel("S&P 500 price", color="#1f77b4")
    ax2 = ax1.twinx()
    ax2.plot(monthly["month"], monthly["avg_sentiment"], color="#d62728", alpha=0.7, label="Avg sentiment")
    ax2.set_ylabel("Avg monthly sentiment", color="#d62728")
    ax2.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.title("Trump Monthly Sentiment vs S&P 500 (2009-2025)")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "01_sentiment_vs_sp500_timeline.png", dpi=120)
    plt.close(fig)

    # ---- CHART 2: scatter sentiment vs same-day S&P return -----------
    fig, ax = plt.subplots(figsize=(8, 6))
    sub = sp.dropna(subset=["avg_sentiment", "daily_return"])
    ax.scatter(sub["avg_sentiment"], sub["daily_return"], s=8, alpha=0.3, color="#2ca02c")
    ax.axhline(0, color="gray", lw=0.8)
    ax.axvline(0, color="gray", lw=0.8)
    ax.set_xlabel("Daily average sentiment")
    ax.set_ylabel("S&P 500 daily return (%)")
    ax.set_title("Daily Sentiment vs Same-Day S&P 500 Return")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "02_sentiment_return_scatter.png", dpi=120)
    plt.close(fig)

    # ---- CHART 3: correlation heatmap --------------------------------
    heat_cols = ["avg_sentiment", "post_count", "total_engagement", "daily_return", "volatility_7d"]
    corr_matrix = sp[heat_cols].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Correlation Heatmap: Sentiment & Market (S&P 500)")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "03_correlation_heatmap.png", dpi=120)
    plt.close(fig)

    print(f"\nSaved 3 charts to: {CHART_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
