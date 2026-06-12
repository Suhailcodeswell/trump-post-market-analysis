"""One-off: identify narrative episodes for the story dashboard."""
import pandas as pd
from pathlib import Path

posts = pd.read_csv("data/processed/posts_scored.csv", low_memory=False)
posts["date"] = pd.to_datetime(posts["date_only"])
market = pd.read_csv("data/processed/market_data.csv")
market["date"] = pd.to_datetime(market["date_only"])


def price_path(instrument: str, start: str):
    m = market[market["instrument"] == instrument].sort_values("date")
    idx = m["date"].searchsorted(pd.Timestamp(start))
    if idx >= len(m):
        return None
    base = float(m.iloc[idx]["close"])
    rets = {}
    for label, d in [("1d", 1), ("1w", 5), ("1m", 21)]:
        j = min(idx + d, len(m) - 1)
        rets[label] = round((float(m.iloc[j]["close"]) / base - 1) * 100, 2)
    return base, rets


episodes = [
    ("Bitcoin Nashville Conference", "2024-07-27", "bitcoin"),
    ("Crypto Pro-Pivot (May 2024)", "2024-05-25", "bitcoin"),
    ("Satoshi Anniversary / BTC Made in USA", "2024-10-31", "bitcoin"),
    ("US Crypto Reserve (Mar 2025)", "2025-03-02", "bitcoin"),
    ("First Bitcoin Transaction as President", "2024-09-18", "bitcoin"),
    ("Steel/Aluminum Tariffs Announced", "2018-03-05", "sp500"),
    ("G7 / Trudeau Tariff Fight", "2018-06-09", "sp500"),
    ("China STUPID TRADE Tariff Post", "2018-04-09", "sp500"),
    ("NASDAQ Crosses 8000", "2018-08-28", "nasdaq"),
    ("NASDAQ ATH — COVID Recovery", "2020-06-09", "nasdaq"),
    ("NASDAQ + Crypto Record Highs", "2025-07-10", "nasdaq"),
]

print("=== EPISODE MARKET IMPACTS ===")
for name, dt, inst in episodes:
    res = price_path(inst, dt)
    if res:
        base, rets = res
        print(f"{name} | {dt} | {inst} | base={base:.0f} | 1d={rets['1d']}% | 1w={rets['1w']}% | 1m={rets['1m']}%")

iran = posts[posts["text"].str.contains(r"\biran\b|hormuz|netanyahu|israel.*strike", case=False, na=False)]
print("\nIran/ME posts by year (top years):")
print(iran.groupby(iran["date"].dt.year).size().sort_values(ascending=False).head(8))

print("\nRecent Iran/ME posts (2024+):")
recent = iran[iran["date"] >= "2024-01-01"].sort_values("date")
for _, r in recent.head(12).iterrows():
    print(f"  {r['date'].date()} | {r['sentiment_score']:+.2f} | {str(r['text'])[:90]}")

tar2025 = posts[(posts["date"] >= "2025-01-01") & posts["text"].str.contains("tariff", case=False, na=False)]
print(f"\n2025 tariff posts: {len(tar2025)}")
for _, r in tar2025.sort_values("date").head(10).iterrows():
    print(f"  {r['date'].date()} | {str(r['text'])[:100]}")

ev = pd.read_csv("output/events_detail.csv")
for topic in ["nasdaq", "bitcoin", "tariffs_china"]:
    t = ev[ev["topic"] == topic]
    print(f"\n{topic}: events={len(t)} avg_1w={t['return_1w_pct'].mean():.2f}% win_1w={(t['return_1w_pct']>0).mean()*100:.0f}% avg_1m={t['return_1m_pct'].mean():.2f}%")
