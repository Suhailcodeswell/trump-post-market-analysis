"""
STEP 10 — FULL EVENT CATALOG FOR POWER BI (per stock / per topic)
======================================================================
Builds EVERY event-day we can study, grouped for Power BI worksheets:

  powerbi/by_topic/          one CSV per topic (every time he posted about it)
  powerbi/by_instrument/     one CSV per market instrument (merged topics)
  powerbi/era_comparison.csv president vs not-president stats per topic
  powerbi/instrument_era_comparison.csv same, grouped by tradeable instrument
  powerbi/topic_summary.csv  headline stats per topic
  powerbi/instrument_summary.csv headline stats per instrument

Each event row includes:
  - post text (headline), date, sentiment, platform
  - presidency era (4-way) + in_office (yes/no)
  - forward returns + $100k values at 1d / 1w / 1m
  - instrument price on event day

Presidency eras:
  Pre-2017           not president (businessman / candidate)
  1st Term           Jan 20 2017 – Jan 19 2021
  Out of office      Jan 20 2021 – Jan 19 2025
  2nd Term           Jan 20 2025+
======================================================================
"""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
POSTS_FILE = PROJECT_ROOT / "data" / "processed" / "posts_tagged.csv"
MARKET_FILE = PROJECT_ROOT / "data" / "processed" / "market_data.csv"
PBI_DIR = PROJECT_ROOT / "powerbi"

# Import topic config from tagging script
import sys
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
from importlib import import_module
tagging = import_module("05_topic_tagging")
TOPICS = tagging.TOPICS

HORIZONS = {"1d": 1, "1w": 7, "1m": 30}
INVEST = 100_000

TERM_1_START = pd.Timestamp("2017-01-20")
TERM_1_END = pd.Timestamp("2021-01-20")
TERM_2_START = pd.Timestamp("2025-01-20")


def presidency_era(dt) -> str:
    d = pd.Timestamp(dt)
    if d < TERM_1_START:
        return "Not President (Pre-2017)"
    if d < TERM_1_END:
        return "President — 1st Term (2017–2021)"
    if d < TERM_2_START:
        return "Not President (2021–2024)"
    return "President — 2nd Term (2025+)"


def in_office(dt) -> str:
    d = pd.Timestamp(dt)
    if TERM_1_START <= d < TERM_1_END or d >= TERM_2_START:
        return "In Office"
    return "Not In Office"


class PriceLookup:
    def __init__(self, market_df: pd.DataFrame, instrument: str):
        m = market_df[market_df["instrument"] == instrument].copy()
        m["date"] = pd.to_datetime(m["date_only"])
        m = m.sort_values("date")
        self.dates = m["date"].to_numpy(dtype="datetime64[ns]")
        self.closes = m["close"].to_numpy(dtype=float)

    def on_or_after(self, when: pd.Timestamp):
        target = np.datetime64(when, "ns")
        idx = np.searchsorted(self.dates, target, side="left")
        if idx >= len(self.dates):
            return None, None
        return pd.Timestamp(self.dates[idx]), float(self.closes[idx])


def build_topic_events(posts: pd.DataFrame, topic: str) -> pd.DataFrame:
    col = f"topic_{topic}"
    sub = posts[posts[col]].copy()
    if sub.empty:
        return pd.DataFrame()

    sub["date"] = pd.to_datetime(sub["date_only"])
    sub["engagement"] = sub["favorite_count"] + sub["repost_count"]
    cfg = TOPICS[topic]

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
                    "platform": g["platform"].mode().iloc[0] if len(g) else "",
                    "headline_text": str(headline(g))[:300],
                }
            ),
            include_groups=False,
        )
        .reset_index()
    )
    events["topic"] = topic
    events["topic_display"] = cfg["display"]
    events["instrument"] = cfg["instrument"]
    return events


def enrich_events(events: pd.DataFrame, prices: PriceLookup) -> pd.DataFrame:
    rows = []
    for _, ev in events.iterrows():
        event_date = ev["date"]
        buy_date, buy_price = prices.on_or_after(event_date)
        if buy_price is None:
            continue

        sent = float(ev["avg_sentiment"])
        row = {
            "event_date": event_date.date(),
            "buy_date": buy_date.date(),
            "topic": ev["topic"],
            "topic_display": ev["topic_display"],
            "instrument": ev["instrument"],
            "post_count": int(ev["post_count"]),
            "avg_sentiment": round(sent, 4),
            "sentiment_label": "positive" if sent >= 0.05 else ("negative" if sent <= -0.05 else "neutral"),
            "total_engagement": int(ev["total_engagement"]),
            "platform": ev["platform"],
            "headline_text": ev["headline_text"],
            "buy_price": round(buy_price, 4),
            "presidency_era": presidency_era(event_date),
            "in_office": in_office(event_date),
        }

        for label, days in HORIZONS.items():
            sell_date, sell_price = prices.on_or_after(event_date + timedelta(days=days))
            if sell_price is None:
                row[f"return_{label}_pct"] = np.nan
                row[f"value_{label}"] = np.nan
            else:
                ratio = sell_price / buy_price
                row[f"return_{label}_pct"] = round((ratio - 1) * 100, 4)
                row[f"value_{label}"] = round(INVEST * ratio, 2)

        rows.append(row)
    return pd.DataFrame(rows)


def summarize(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    out = []
    for keys, g in df.groupby(group_cols):
        if not isinstance(keys, tuple):
            keys = (keys,)
        for horizon in HORIZONS:
            col = f"return_{horizon}_pct"
            r = g[col].dropna()
            v = g[f"value_{horizon}"].dropna()
            if len(r) == 0:
                continue
            row = dict(zip(group_cols, keys))
            row.update(
                {
                    "horizon": horizon,
                    "n_events": len(r),
                    "mean_return_pct": round(r.mean(), 3),
                    "median_return_pct": round(r.median(), 3),
                    "win_rate_pct": round((r > 0).mean() * 100, 1),
                    "best_return_pct": round(r.max(), 2),
                    "worst_return_pct": round(r.min(), 2),
                    "avg_value_of_100k": round(v.mean(), 2),
                }
            )
            out.append(row)
    return pd.DataFrame(out)


def main() -> None:
    print("=" * 60)
    print("STEP 10: FULL POWER BI EVENT CATALOG")
    print("=" * 60)

    posts = pd.read_csv(POSTS_FILE, low_memory=False)
    market = pd.read_csv(MARKET_FILE)
    price_cache: dict[str, PriceLookup] = {}

    def get_prices(inst: str) -> PriceLookup:
        if inst not in price_cache:
            price_cache[inst] = PriceLookup(market, inst)
        return price_cache[inst]

    all_events: list[pd.DataFrame] = []

    topic_dir = PBI_DIR / "by_topic"
    topic_dir.mkdir(parents=True, exist_ok=True)

    print("\nBuilding per-topic event files:")
    for topic, cfg in TOPICS.items():
        raw = build_topic_events(posts, topic)
        if raw.empty:
            print(f"  {cfg['display']:<22} — no events")
            continue
        enriched = enrich_events(raw, get_prices(cfg["instrument"]))
        if enriched.empty:
            continue
        enriched = enriched.sort_values("event_date")
        path = topic_dir / f"{topic}_events.csv"
        enriched.to_csv(path, index=False)
        all_events.append(enriched)
        print(f"  {cfg['display']:<22} -> {len(enriched):,} events -> {path.name}")

    combined = pd.concat(all_events, ignore_index=True)
    combined.to_csv(PBI_DIR / "all_events.csv", index=False)

    # Per instrument: merge all topics, dedupe same calendar day (keep highest engagement)
    print("\nBuilding per-instrument event files:")
    inst_dir = PBI_DIR / "by_instrument"
    inst_dir.mkdir(parents=True, exist_ok=True)

    for inst in sorted(combined["instrument"].unique()):
        sub = combined[combined["instrument"] == inst].copy()
        sub = sub.sort_values(["event_date", "total_engagement"], ascending=[True, False])
        sub = sub.drop_duplicates(subset=["event_date"], keep="first")
        sub = sub.sort_values("event_date")
        path = inst_dir / f"{inst}_events.csv"
        sub.to_csv(path, index=False)
        print(f"  {inst:<10} -> {len(sub):,} unique event-days -> {path.name}")

    # Summaries
    topic_summary = summarize(combined, ["topic", "topic_display", "instrument", "presidency_era"])
    topic_summary.to_csv(PBI_DIR / "era_comparison_by_topic.csv", index=False)

    inst_combined = combined.sort_values(["instrument", "event_date", "total_engagement"], ascending=[True, True, False])
    inst_combined = inst_combined.drop_duplicates(subset=["instrument", "event_date"], keep="first")

    inst_era = summarize(inst_combined, ["instrument", "presidency_era"])
    inst_era.to_csv(PBI_DIR / "era_comparison_by_instrument.csv", index=False)

    # Binary in_office comparison (the key user ask)
    office_compare = summarize(combined, ["topic", "topic_display", "instrument", "in_office"])
    office_compare.to_csv(PBI_DIR / "in_office_comparison_by_topic.csv", index=False)

    inst_office = summarize(inst_combined, ["instrument", "in_office"])
    inst_office.to_csv(PBI_DIR / "in_office_comparison_by_instrument.csv", index=False)

    topic_summary_all = summarize(combined, ["topic", "topic_display", "instrument"])
    topic_summary_all.to_csv(PBI_DIR / "topic_summary.csv", index=False)

    inst_summary = summarize(inst_combined, ["instrument"])
    inst_summary.to_csv(PBI_DIR / "instrument_summary.csv", index=False)

    # Print presidency comparison highlights
    print("\n--- IN OFFICE vs NOT IN OFFICE (1-week avg return, selected topics) ---")
    oc = office_compare[office_compare["horizon"] == "1w"].sort_values("topic")
    for topic in TOPICS:
        t = oc[oc["topic"] == topic]
        if t.empty:
            continue
        in_o = t[t["in_office"] == "In Office"]
        out_o = t[t["in_office"] == "Not In Office"]
        if not in_o.empty and not out_o.empty:
            print(
                f"  {TOPICS[topic]['display']:<22}  "
                f"In office: {in_o.iloc[0]['mean_return_pct']:+.2f}% (n={int(in_o.iloc[0]['n_events'])})  |  "
                f"Not in office: {out_o.iloc[0]['mean_return_pct']:+.2f}% (n={int(out_o.iloc[0]['n_events'])})"
            )

    print(f"\nTotal event rows (all topics): {len(combined):,}")
    print(f"Output folder: {PBI_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
