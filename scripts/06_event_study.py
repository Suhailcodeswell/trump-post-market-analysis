"""
STEP 5 + 6 — EVENT STUDY & INVESTOR CALCULATOR
======================================================================
THE BIG ONE. What this script does, in plain English:

  For each TOPIC (Bitcoin, S&P 500, Nasdaq, Tariffs/China):
    1. Treat every day Trump posted about that topic as an "EVENT".
    2. Pretend you BOUGHT the related market on that day (at the close
       of the first trading day on/after the post).
    3. Measure what happened 1 DAY, 1 WEEK, and 1 MONTH later:
          - the forward return (%)
          - what $100,000 invested that day would be worth
    4. Summarise across ALL events for that topic:
          - average return, median return
          - WIN RATE (how often it went up)
          - average ending value of $100,000

  This is a classic "event study" + an investor-style back-of-envelope
  return calculator. It answers the question your portfolio poses:
  "If you invested $100k the day Trump talked about Bitcoin, what would
   you have on average a week later?"

IMPORTANT HONESTY NOTE (kept in the output too):
  A market move after a post is an ASSOCIATION, not proof the post
  CAUSED it. We report the FULL set of events (not cherry-picked) and
  show win rates + averages so the picture is complete and fair.

Outputs:
  - output/events_detail.csv         (one row per event, all horizons)
  - output/event_study_summary.csv   (aggregates per topic + horizon)
  - output/charts/04_event_study_returns.png
======================================================================
"""

from pathlib import Path
from datetime import timedelta
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
POSTS_FILE = PROJECT_ROOT / "data" / "processed" / "posts_tagged.csv"
MARKET_FILE = PROJECT_ROOT / "data" / "processed" / "market_data.csv"
OUT_DIR = PROJECT_ROOT / "output"
CHART_DIR = OUT_DIR / "charts"

# topic -> instrument it trades against
TOPIC_INSTRUMENT = {
    "bitcoin": "bitcoin",
    "sp500": "sp500",
    "nasdaq": "nasdaq",
    "tariffs_china": "sp500",
}

# horizon label -> calendar days held
HORIZONS = {"1d": 1, "1w": 7, "1m": 30}

INVEST_AMOUNT = 100_000  # the headline "what if you invested $100k" figure


class PriceLookup:
    """Fast 'price on the first trading day on/after a date' lookup."""

    def __init__(self, market_df: pd.DataFrame, instrument: str):
        m = market_df[market_df["instrument"] == instrument].copy()
        m["date"] = pd.to_datetime(m["date_only"])
        m = m.sort_values("date")
        self.dates = m["date"].to_numpy(dtype="datetime64[ns]")
        self.closes = m["close"].to_numpy(dtype=float)

    def on_or_after(self, when: pd.Timestamp):
        """Return (trading_date, close) for first trading day >= when, or (None, None)."""
        target = np.datetime64(when, "ns")
        idx = np.searchsorted(self.dates, target, side="left")
        if idx >= len(self.dates):
            return None, None
        return pd.Timestamp(self.dates[idx]), float(self.closes[idx])


def build_events(posts: pd.DataFrame, topic: str) -> pd.DataFrame:
    """Collapse a topic's posts to ONE event per calendar day."""
    sub = posts[posts[f"topic_{topic}"]].copy()
    sub["date"] = pd.to_datetime(sub["date_only"])
    sub["engagement"] = sub["favorite_count"] + sub["repost_count"]

    # Representative post per day = the highest-engagement one (the "loudest").
    def headline(g):
        return g.loc[g["engagement"].idxmax(), "text"]

    events = (
        sub.groupby("date")
        .apply(
            lambda g: pd.Series(
                {
                    "post_count": len(g),
                    "avg_sentiment": g["sentiment_score"].mean(),
                    "total_engagement": int(g["engagement"].sum()),
                    "headline_text": str(headline(g))[:200],
                }
            ),
            include_groups=False,
        )
        .reset_index()
    )
    events["topic"] = topic
    return events


def main() -> None:
    print("=" * 60)
    print("STEP 5+6: EVENT STUDY & INVESTOR CALCULATOR")
    print("=" * 60)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    posts = pd.read_csv(POSTS_FILE, low_memory=False)
    market = pd.read_csv(MARKET_FILE)

    all_event_rows = []

    for topic, instrument in TOPIC_INSTRUMENT.items():
        events = build_events(posts, topic)
        prices = PriceLookup(market, instrument)

        for _, ev in events.iterrows():
            event_date = ev["date"]
            buy_date, buy_price = prices.on_or_after(event_date)
            if buy_price is None:
                continue

            row = {
                "topic": topic,
                "instrument": instrument,
                "event_date": event_date.date(),
                "buy_date": buy_date.date(),
                "buy_price": round(buy_price, 4),
                "post_count": int(ev["post_count"]),
                "avg_sentiment": round(float(ev["avg_sentiment"]), 4),
                "sentiment_label": "positive" if ev["avg_sentiment"] >= 0.05
                else ("negative" if ev["avg_sentiment"] <= -0.05 else "neutral"),
                "total_engagement": int(ev["total_engagement"]),
                "headline_text": ev["headline_text"],
            }

            for label, days in HORIZONS.items():
                sell_date, sell_price = prices.on_or_after(event_date + timedelta(days=days))
                if sell_price is None:
                    row[f"return_{label}_pct"] = np.nan
                    row[f"value_{label}"] = np.nan
                else:
                    ratio = sell_price / buy_price
                    row[f"return_{label}_pct"] = round((ratio - 1) * 100, 4)
                    row[f"value_{label}"] = round(INVEST_AMOUNT * ratio, 2)

            all_event_rows.append(row)

    detail = pd.DataFrame(all_event_rows)
    detail.to_csv(OUT_DIR / "events_detail.csv", index=False)
    print(f"\nBuilt {len(detail):,} events across {len(TOPIC_INSTRUMENT)} topics.")

    # ---- Aggregate summary per topic + horizon -----------------------
    summary_rows = []
    for topic in TOPIC_INSTRUMENT:
        t = detail[detail["topic"] == topic]
        for label in HORIZONS:
            r = t[f"return_{label}_pct"].dropna()
            v = t[f"value_{label}"].dropna()
            if len(r) == 0:
                continue
            summary_rows.append(
                {
                    "topic": topic,
                    "horizon": label,
                    "n_events": len(r),
                    "mean_return_pct": round(r.mean(), 3),
                    "median_return_pct": round(r.median(), 3),
                    "win_rate_pct": round((r > 0).mean() * 100, 1),
                    "best_return_pct": round(r.max(), 2),
                    "worst_return_pct": round(r.min(), 2),
                    "avg_value_of_100k": round(v.mean(), 2),
                }
            )
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(OUT_DIR / "event_study_summary.csv", index=False)

    print("\n--- EVENT STUDY SUMMARY ---")
    print(summary.to_string(index=False))

    # ---- Headline investor-calculator lines --------------------------
    print("\n--- INVESTOR CALCULATOR (avg outcome of $100,000) ---")
    for topic in TOPIC_INSTRUMENT:
        row = summary[(summary["topic"] == topic) & (summary["horizon"] == "1w")]
        if not row.empty:
            val = row.iloc[0]["avg_value_of_100k"]
            ret = row.iloc[0]["mean_return_pct"]
            wr = row.iloc[0]["win_rate_pct"]
            n = int(row.iloc[0]["n_events"])
            print(
                f"  {topic:<14}: $100,000 on each post, sold 1 week later -> "
                f"avg ${val:,.0f} ({ret:+.2f}%, win rate {wr:.0f}%, {n} events)"
            )

    # ---- Chart: mean forward return by topic & horizon ---------------
    pivot = summary.pivot(index="topic", columns="horizon", values="mean_return_pct")
    pivot = pivot[["1d", "1w", "1m"]]  # order
    ax = pivot.plot(kind="bar", figsize=(11, 6), width=0.8)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_ylabel("Average forward return (%)")
    ax.set_title("Average Market Return AFTER Trump Posts, by Topic & Horizon")
    ax.legend(title="Held for")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "04_event_study_returns.png", dpi=120)
    plt.close()

    print(f"\nSaved: events_detail.csv, event_study_summary.csv, and chart 04.")
    print("=" * 60)


if __name__ == "__main__":
    main()
