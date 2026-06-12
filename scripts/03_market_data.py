"""
STEP 3 — MARKET DATA
======================================================================
Downloads daily prices for all instruments used in the per-stock
Power BI worksheets (S&P, Nasdaq, Dow, VIX, Bitcoin, Oil, Gold, ETFs).
======================================================================
"""

from pathlib import Path
import pandas as pd
import yfinance as yf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_FILE = PROJECT_ROOT / "data" / "processed" / "market_data.csv"

START_DATE = "2009-01-01"
END_DATE = "2026-01-01"

INSTRUMENTS = {
    "sp500": "^GSPC",
    "nasdaq": "^IXIC",
    "dow": "^DJI",
    "vix": "^VIX",
    "bitcoin": "BTC-USD",
    "oil": "CL=F",
    "gold": "GC=F",
    "xle": "XLE",
    "qqq": "QQQ",
    "spy": "SPY",
}


def fetch_one(name: str, ticker: str) -> pd.DataFrame:
    print(f"  Downloading {name} ({ticker}) ...")
    raw = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False, auto_adjust=True)
    if raw.empty:
        print(f"    WARNING: no data for {ticker}")
        return pd.DataFrame()

    close = raw["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    out = pd.DataFrame({"date_only": close.index.date, "instrument": name, "close": close.values})
    out["daily_return"] = out["close"].pct_change() * 100
    out["volatility_7d"] = out["daily_return"].rolling(window=7).std()
    out["close"] = out["close"].round(4)
    out["daily_return"] = out["daily_return"].round(4)
    out["volatility_7d"] = out["volatility_7d"].round(4)
    print(f"    got {len(out):,} trading days")
    return out


def main() -> None:
    print("=" * 60)
    print("STEP 3: DOWNLOADING MARKET DATA")
    print("=" * 60)
    frames = [fetch_one(n, t) for n, t in INSTRUMENTS.items()]
    frames = [f for f in frames if not f.empty]
    market = pd.concat(frames, ignore_index=True)
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    market.to_csv(OUT_FILE, index=False)
    print("\nRows per instrument:")
    print(market["instrument"].value_counts().to_string())
    print(f"\nSaved: {OUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
