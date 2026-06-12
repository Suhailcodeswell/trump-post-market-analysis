"""
Export all Power BI tables into one Excel workbook (easier for beginners).
File: powerbi/Trump_Markets_Data.xlsx
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PBI = ROOT / "powerbi"
OUT = PBI / "Trump_Markets_Data.xlsx"

SHEETS = {
    "Featured_Events": PBI / "featured_events.csv",
    "Bitcoin_Events": PBI / "by_instrument" / "bitcoin_events.csv",
    "SP500_Events": PBI / "by_instrument" / "sp500_events.csv",
    "Nasdaq_Events": PBI / "by_instrument" / "nasdaq_events.csv",
    "Oil_Events": PBI / "by_instrument" / "oil_events.csv",
    "Gold_Events": PBI / "by_instrument" / "gold_events.csv",
    "Iran_Events": PBI / "by_topic" / "iran_geopolitics_events.csv",
    "Tariffs_Events": PBI / "by_topic" / "tariffs_china_events.csv",
    "Office_Compare": PBI / "in_office_comparison_by_instrument.csv",
    "Instrument_Summary": PBI / "instrument_summary.csv",
    "Market_Prices": ROOT / "data" / "processed" / "market_data.csv",
    "All_Events": PBI / "all_events.csv",
}

# Curated headline episodes for event-specific dashboard pages
FEATURED_EPISODES = [
    ("Bitcoin — Anti-crypto tweet", "2019-07-12", "bitcoin"),
    ("Bitcoin — Satoshi / Made in USA", "2024-10-31", "bitcoin"),
    ("Bitcoin — Nashville Conference", "2024-07-27", "bitcoin"),
    ("Bitcoin — US Crypto Reserve", "2025-03-02", "bitcoin"),
    ("Oil — Iran diplomacy (Jun 2025)", "2025-06-12", "oil"),
    ("Oil — Iran enrichment warning", "2025-06-02", "oil"),
    ("Oil — Iran strike threat (Apr 2020)", "2020-04-01", "oil"),
    ("S&P — Auto tariffs / jobs (Apr 2025)", "2025-04-08", "sp500"),
    ("S&P — COVID market post (Mar 2020)", "2020-03-22", "sp500"),
    ("Nasdaq — Election eve Big Tech", "2020-11-02", "nasdaq"),
    ("Nasdaq — Big Tech executive orders", "2020-07-29", "nasdaq"),
    ("Gold — Admin legal services (Apr 2025)", "2025-04-11", "gold"),
]


def build_featured_events() -> pd.DataFrame:
    all_ev = pd.read_csv(PBI / "all_events.csv")
    all_ev["event_date"] = pd.to_datetime(all_ev["event_date"]).dt.strftime("%Y-%m-%d")
    rows = []
    for title, dt, inst in FEATURED_EPISODES:
        match = all_ev[(all_ev["event_date"] == dt) & (all_ev["instrument"] == inst)]
        if match.empty:
            match = all_ev[(all_ev["event_date"] == dt)]
        if match.empty:
            continue
        row = match.iloc[0].to_dict()
        row["story_title"] = title
        rows.append(row)
    out = pd.DataFrame(rows)
    cols = ["story_title", "event_date", "instrument", "topic_display", "presidency_era",
            "in_office", "sentiment_label", "return_1w_pct", "return_1m_pct",
            "value_1w", "value_1m", "headline_text"]
    cols = [c for c in cols if c in out.columns]
    return out[cols]


def main() -> None:
    featured = build_featured_events()
    featured.to_csv(PBI / "featured_events.csv", index=False)
    n = 0
    out_path = OUT
    try:
        writer_ctx = pd.ExcelWriter(out_path, engine="openpyxl")
    except PermissionError:
        out_path = PBI / "Trump_Markets_Data_v2.xlsx"
        print(f"NOTE: {OUT.name} is open — writing {out_path.name} instead")
        writer_ctx = pd.ExcelWriter(out_path, engine="openpyxl")
    with writer_ctx as writer:
        for sheet, path in SHEETS.items():
            if path.exists():
                pd.read_csv(path).to_excel(writer, sheet_name=sheet[:31], index=False)
                n += 1
    print(f"Saved {out_path} ({n} sheets, {len(featured)} featured events)")


if __name__ == "__main__":
    main()
