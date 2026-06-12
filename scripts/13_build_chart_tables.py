"""
Chart-ready tables for Power BI — no DAX needed.
Splits price into: before post | after post | highlight dot
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MARKET = ROOT / "data" / "processed" / "market_data.csv"
OUT = ROOT / "powerbi" / "chart_data"

CHARTS = [
    {
        "file": "btc_positive_oct2024.csv",
        "instrument": "bitcoin",
        "post_date": "2024-10-31",
        "start": "2024-09-15",
        "end": "2024-11-30",
    },
    {
        "file": "btc_negative_jul2019.csv",
        "instrument": "bitcoin",
        "post_date": "2019-07-12",
        "start": "2019-06-20",
        "end": "2019-07-26",
    },
]


def build(cfg: dict) -> pd.DataFrame:
    m = pd.read_csv(MARKET)
    m["date_only"] = pd.to_datetime(m["date_only"])
    post = pd.Timestamp(cfg["post_date"])
    sub = m[
        (m["instrument"] == cfg["instrument"])
        & (m["date_only"] >= cfg["start"])
        & (m["date_only"] <= cfg["end"])
    ].sort_values("date_only").copy()

    sub["close_before"] = sub["close"].where(sub["date_only"] <= post)
    sub["close_after"] = sub["close"].where(sub["date_only"] >= post)
    sub["post_day_dot"] = sub["close"].where(sub["date_only"] == post)
    sub["date_only"] = sub["date_only"].dt.strftime("%Y-%m-%d")
    return sub[
        ["date_only", "close", "close_before", "close_after", "post_day_dot"]
    ]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for cfg in CHARTS:
        path = OUT / cfg["file"]
        build(cfg).to_csv(path, index=False)
        print(f"Saved {path}")


if __name__ == "__main__":
    main()
