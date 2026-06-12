"""
STEP 4b — EXPANDED TOPIC TAGGING (all market themes)
======================================================================
Tags every post with ALL topics it mentions. Each topic maps to the
market instrument we study in the event catalog / Power BI worksheets.

Topics are intentionally overlapping (one post can match Bitcoin AND
S&P). That is correct — we study each instrument's dashboard separately.
======================================================================
"""

from pathlib import Path
import re
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
IN_FILE = PROJECT_ROOT / "data" / "processed" / "posts_scored.csv"
OUT_FILE = PROJECT_ROOT / "data" / "processed" / "posts_tagged.csv"

# topic_key -> {instrument, keywords, display_name for Power BI}
TOPICS = {
    "bitcoin": {
        "instrument": "bitcoin",
        "display": "Bitcoin",
        "keywords": [
            "bitcoin", "btc", "crypto", "cryptocurrency", "cryptocurrencies",
            "digital asset", "digital assets", "coinbase", "stablecoin",
            "ethereum", "strategic bitcoin reserve", "crypto reserve",
            "blockchain", "genius act",
        ],
    },
    "sp500": {
        "instrument": "sp500",
        "display": "S&P 500",
        "keywords": [
            "s&p", "s&p 500", "sp500", "stock market", "stock markets",
            "the markets", "record high", "record highs", "all-time high",
            "wall street", "stocks", "equities", "401k", "401(k)",
        ],
    },
    "nasdaq": {
        "instrument": "nasdaq",
        "display": "Nasdaq",
        "keywords": [
            "nasdaq", "tech stocks", "technology stocks", "big tech",
            "semiconductor", "semiconductors", "chips act", "ai stocks",
            "nvidia", "magnificent seven",
        ],
    },
    "dow": {
        "instrument": "dow",
        "display": "Dow Jones",
        "keywords": [
            "dow jones", "the dow", "djia", "industrial average",
        ],
    },
    "tariffs_china": {
        "instrument": "sp500",
        "display": "Tariffs & China",
        "keywords": [
            "tariff", "tariffs", "china", "chinese", "beijing", "xi jinping",
            "trade deal", "trade war", "trade deficit", "import tax",
            "import taxes", "reciprocal tariff",
        ],
    },
    "oil_energy": {
        "instrument": "oil",
        "display": "Oil & Energy",
        "keywords": [
            "oil", "crude", "gas prices", "gasoline", "opec", "energy sector",
            "pipeline", "keystone", "drill baby drill", "hormuz", "barrel",
            "xle", "natural gas", "lng",
        ],
    },
    "iran_geopolitics": {
        "instrument": "oil",
        "display": "Iran & Geopolitics",
        "keywords": [
            "iran", "iranian", "tehran", "ayatollah", "khamenei", "hormuz",
            "nuclear facilities", "nuclear sites", "fordow", "natanz",
            "mullahs", "regime change",
        ],
    },
    "israel_mideast": {
        "instrument": "sp500",
        "display": "Israel & Middle East",
        "keywords": [
            "israel", "israeli", "gaza", "hamas", "netanyahu", "middle east",
            "ceasefire", "hostages", "hezbollah", "jerusalem", "palestinian",
        ],
    },
    "gold": {
        "instrument": "gold",
        "display": "Gold",
        "keywords": [
            "gold", "precious metal", "precious metals",
        ],
    },
    "fed_rates": {
        "instrument": "sp500",
        "display": "Fed & Interest Rates",
        "keywords": [
            "federal reserve", "the fed", "interest rate", "interest rates",
            "jerome powell", "rate cut", "rate hike", "monetary policy",
            "quantitative", "inflation",
        ],
    },
    "vix_fear": {
        "instrument": "vix",
        "display": "Market Fear / VIX",
        "keywords": [
            "volatility", "vix", "fear index", "market crash", "correction",
            "bear market", "panic",
        ],
    },
}


def build_pattern(keywords: list[str]) -> re.Pattern:
    escaped = [re.escape(k) for k in keywords]
    return re.compile(r"\b(?:" + "|".join(escaped) + r")\b", flags=re.IGNORECASE)


def main() -> None:
    print("=" * 60)
    print("STEP 4b: EXPANDED TOPIC TAGGING")
    print("=" * 60)

    df = pd.read_csv(IN_FILE, low_memory=False)
    text = df["text"].astype(str)
    print(f"Loaded scored posts: {len(df):,}")

    patterns = {topic: build_pattern(cfg["keywords"]) for topic, cfg in TOPICS.items()}

    for topic, pattern in patterns.items():
        df[f"topic_{topic}"] = text.str.contains(pattern)

    topic_cols = [f"topic_{t}" for t in TOPICS]
    df["topics"] = df[topic_cols].apply(
        lambda row: ",".join(t for t in TOPICS if row[f"topic_{t}"]), axis=1
    )
    df["is_topical"] = df["topics"] != ""

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_FILE, index=False)

    print("\nPosts matched per topic:")
    for topic, cfg in TOPICS.items():
        n = int(df[f"topic_{topic}"].sum())
        print(f"  - {cfg['display']:<22} ({topic:<18}): {n:,} posts  -> {cfg['instrument']}")

    print(f"\nTotal topical posts (any topic): {int(df['is_topical'].sum()):,}")
    print(f"Saved: {OUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
