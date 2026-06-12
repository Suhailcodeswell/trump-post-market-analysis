# Power BI Data Pack — Per-Stock Worksheets

**Build the report:** follow **[POWERBI_VISUAL_GUIDE.md](../POWERBI_VISUAL_GUIDE.md)** (cover page, Trump photo, dark/gold theme).

| Quick start file | What it is |
|------------------|------------|
| `Trump_Markets_Data.xlsx` | Load this in Power BI (all sheets in one file) |
| `themes/TrumpMarkets-Portfolio.json` | View → Themes → Browse |
| `assets/trump_official_portrait.jpg` | Insert → Image on Cover page |
| `reports/Trump_Markets.pbix` | Save your report here when built |

Load these files into **Power BI Desktop** to build one dashboard (or tab group) per market instrument.

## Folder structure

```
powerbi/
├── all_events.csv                      # everything (3,352 event rows)
├── topic_summary.csv                   # avg returns per topic
├── instrument_summary.csv              # avg returns per instrument
├── era_comparison_by_topic.csv         # 4 presidency eras × topic
├── era_comparison_by_instrument.csv    # 4 presidency eras × instrument
├── in_office_comparison_by_topic.csv   # IN OFFICE vs NOT IN OFFICE × topic
├── in_office_comparison_by_instrument.csv
├── by_topic/                           # one worksheet source per THEME
│   ├── bitcoin_events.csv
│   ├── sp500_events.csv
│   ├── nasdaq_events.csv
│   ├── tariffs_china_events.csv
│   ├── iran_geopolitics_events.csv
│   ├── oil_energy_events.csv
│   ├── israel_mideast_events.csv
│   ├── fed_rates_events.csv
│   ├── gold_events.csv
│   └── ...
└── by_instrument/                      # one dashboard per TRADEABLE MARKET
    ├── bitcoin_events.csv      (28 events)
    ├── sp500_events.csv        (1,773 events)
    ├── nasdaq_events.csv       (74 events)
    ├── dow_events.csv          (15 events)
    ├── oil_events.csv          (705 events)
    ├── gold_events.csv         (94 events)
    └── vix_events.csv            (29 events)
```

## Presidency eras (column: `presidency_era`)

| Era | Dates | Meaning |
|-----|-------|---------|
| Not President (Pre-2017) | Before Jan 20 2017 | Businessman / candidate |
| President — 1st Term | Jan 2017 – Jan 2021 | In office |
| Not President (2021–2024) | Jan 2021 – Jan 2025 | Between terms / Truth Social |
| President — 2nd Term | Jan 2025+ | In office again |

**Binary column `in_office`:** `In Office` vs `Not In Office` (combines both non-president periods).

## Recommended Power BI workbook layout

### One **report** with pages grouped by instrument:

| Page group | Data file | What to show |
|------------|-----------|--------------|
| **Bitcoin** | `by_instrument/bitcoin_events.csv` + `market_data` (bitcoin) | Every crypto post; office vs not office |
| **S&P 500** | `by_instrument/sp500_events.csv` | All broad-market + tariffs + Fed + Israel posts |
| **Nasdaq** | `by_instrument/nasdaq_events.csv` | Tech / Nasdaq posts |
| **Oil** | `by_instrument/oil_events.csv` | Energy + Iran geopolitics |
| **Gold** | `by_instrument/gold_events.csv` | Gold / safe-haven posts |
| **Dow** | `by_instrument/dow_events.csv` | Dow-specific posts |
| **VIX / Fear** | `by_instrument/vix_events.csv` | Crash / volatility rhetoric |

### Within EACH instrument page (story template):

1. **Headline claim** (text box)
2. **KPI cards** — avg 1-week return, win rate, event count
3. **Clustered bar** — `in_office` vs average return (the presidency comparison)
4. **Line chart** — instrument price over time; table cross-filters to event dates
5. **Table** — every event: date, headline, sentiment, returns, $100k values
6. **Slicer** — `presidency_era` or `in_office`

### Optional sub-pages per topic (deeper worksheets):

Use `by_topic/tariffs_china_events.csv` as a **drill-through** from the S&P page — same layout, narrower story.

## Key columns in event files

| Column | Use |
|--------|-----|
| `event_date` | When he posted |
| `headline_text` | The post (proof) |
| `presidency_era` / `in_office` | President comparison |
| `return_1w_pct` | Market move 1 week later |
| `value_1w` | $100,000 → value after 1 week |
| `sentiment_label` | positive / neutral / negative |
| `total_engagement` | Sort by "loudest" posts |

## Load market prices for line charts

Also load `data/processed/market_data.csv` and relate on date:

- Create a `Date` table in Power BI
- Relate `Date[date]` → `market_data[date_only]` and `events[event_date]`

## Honesty disclaimer

Put on every page: *Historical association, not causation. Not financial advice.*
