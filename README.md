# Trump Social Media & The Markets — An Event Study

> **Do Donald Trump's social media posts move financial markets?**
> A data pipeline that analyses **73,380 cleaned posts (2009–2025)**, scores their
> sentiment, and runs an **event study** measuring what Bitcoin, the S&P 500, Nasdaq,
> and the market did *after* he posted — including an interactive "what if I'd invested
> $100,000" calculator.

**Skills demonstrated:** Python data engineering · NLP sentiment analysis · SQL star-schema
modeling (PostgreSQL) · window functions · financial event-study methodology · interactive
data visualization.

---

## The Business Problem

Markets react to information, and few individuals generate as much market-relevant
commentary as Donald Trump. This project asks a concrete, testable question:
**when Trump posts about a specific market (Bitcoin, the S&P 500, Nasdaq, tariffs/China),
what does that market do over the following day, week, and month?**

Rather than a vague "sentiment vs. market" correlation, it uses a **topic-specific event
study** — the approach that actually surfaces signal.

## Methodology

1. **Clean** (`scripts/01_clean_data.py`) — 90,343 → 73,380 posts. Removes deleted posts,
   pure reposts, and empty text so only Trump's own words are analysed.
2. **Sentiment** (`scripts/02_sentiment_vader.py`) — VADER scores each post −1.0 … +1.0.
   *Scored before any market data is examined, to avoid bias.*
3. **Market data** (`scripts/03_market_data.py`) — daily prices for S&P 500, Nasdaq, Dow,
   VIX, and Bitcoin via Yahoo Finance; computes daily returns and 7-day volatility.
4. **Topic tagging** (`scripts/05_topic_tagging.py`) — regex keyword tagging by topic.
5. **Event study + investor calculator** (`scripts/06_event_study.py`) — for each
   posting-day event, measures forward returns at +1d / +1w / +1m and the average outcome
   of a $100,000 investment.
6. **SQL layer** (`sql_queries/`, `scripts/07_build_sql_db.py`) — a PostgreSQL star schema
   (Fact_Posts, Fact_Market, Dim_Date, Dim_Platform) with window-function and `CORR()`
   queries, verified in DuckDB.
7. **Dashboard** (`scripts/08_build_dashboard.py`) — an interactive web dashboard
   (`dashboard/index.html`).
8. **Portfolio website** (`website/public/`) — minimal white Vercel site with Power BI
   chart exports, narrative sections, and an investment calculator.

## Key Findings

Average outcome of **$100,000 invested on every event** (all events, no cherry-picking):

| Topic | 1 week | 1 month | 1-month win rate | Events |
|-------|-------:|--------:|-----------------:|-------:|
| Bitcoin | −2.0% | +1.4% | 44% | 25 |
| S&P 500 | +0.3% | +1.1% | 71% | ~378 |
| Nasdaq | +0.3% | **+2.7%** | **79%** | 68 |
| Tariffs / China | +0.3% | +1.5% | 71% | ~1,113 |

- **Equities tend to drift up** in the month after Trump posts about them (Nasdaq rose
  79% of the time).
- **Bitcoin behaves oppositely** — it dips ~2% in the week after his (very positive) crypto
  posts before recovering: a "buy the rumor, sell the news" pattern.
- **Aggregate daily sentiment alone shows almost no correlation** with returns — confirming
  that the signal lives in *specific events*, not the daily average.

> **Honesty note:** these are *associations, not proof of causation*. Other news and macro
> factors move markets, and results partly reflect the 2009–2025 bull market. This is an
> analytical back-test, not financial advice.

## How to Run

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows  (use: source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt

python scripts/01_clean_data.py
python scripts/02_sentiment_vader.py
python scripts/03_market_data.py        # needs internet (Yahoo Finance)
python scripts/05_topic_tagging.py
python scripts/06_event_study.py
python scripts/07_build_sql_db.py
python scripts/08_build_dashboard.py     # then open dashboard/index.html
```

## Project Structure

```
data/raw/            Original posts dataset
data/processed/      Cleaned, scored, tagged data + market data + DuckDB
scripts/             Numbered pipeline (run in order)
sql_queries/         PostgreSQL star-schema DDL + analytical queries
output/              Correlation results, event study, charts
dashboard/           Interactive web dashboard (index.html)
PROJECT_JOURNAL.md   Full step-by-step build log
```

## Tech Stack

Python (pandas, vaderSentiment, yfinance, scipy, matplotlib) · SQL (PostgreSQL / DuckDB) ·
Plotly · HTML/CSS/JS.

---
*Built by Suhail Ahmed.*
