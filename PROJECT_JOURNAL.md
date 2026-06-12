# Project Journal — Trump Social Media & Market Correlation

> **Purpose of this document:** A living, plain-English record of *everything* we do on this project — every decision, every step, every tool, and *why*. It is updated continuously as the project progresses. If you read this top-to-bottom, you should understand the entire project without needing any prior context.

**Owner:** Suhail Ahmed
**Goal:** A flagship data-analyst / business-intelligence portfolio project, posted to GitHub and embedded in a personal portfolio website.
**Last updated:** 2026-06-10

---

## 1. The Big Idea (in one sentence)

> Do Donald Trump's social media posts correlate with movements and volatility in financial markets (S&P 500, Bitcoin, etc.)?

We answer this by turning 16 years of his posts into **sentiment scores** (numbers), lining those numbers up against **market price data** by date, and measuring whether they move together.

---

## 2. Glossary — Key Concepts Explained Simply

### Sentiment Analysis
A technique that reads text and assigns it an emotional score: positive, negative, or neutral, and how strongly. We use a scale of **−1.0 (very negative) → 0 (neutral) → +1.0 (very positive)**.

- *"GREAT day for America, the economy is BOOMING!"* → ~ **+0.8**
- *"The Fed is destroying our country."* → ~ **−0.7**

### Sentiment Engine (a.k.a. "sentiment agent")
The actual tool/model that produces the score. Options we're considering:
- **VADER** — fast, rule-based, tuned for social media. Runs instantly, no big download.
- **FinBERT** — an AI model trained on financial text; more finance-aware but slower (~400 MB download).

### Why we do sentiment analysis (the point of it)
The posts are **unstructured text** — a computer can't plot words against a stock chart. Sentiment analysis is the **bridge**: it converts each post into a **number** we can chart and run statistics on. Without it, there is nothing numeric to correlate with the market.

### Correlation
A statistical measure of whether two things move together. We'll check whether spikes in sentiment line up with spikes in market movement/volatility.

### Volatility
How much a price swings up and down. Big swings = high volatility (often = market nervousness). We'll likely use the **VIX** index and/or daily price-change size as our volatility measures.

### Star Schema (data modeling term)
A common way to organize data for analytics. One central **fact** table (the measurements) surrounded by **dimension** tables (the descriptive context). Ours:
- **Fact_Posts** — one row per post: date, sentiment score, engagement (likes/reposts).
- **Dim_Date** — calendar info per date (day, month, year, weekday, is-trading-day).
- **Dim_Market** — market prices per date (S&P 500, Bitcoin, etc.).

### Window Functions (SQL)
SQL features that calculate across a "window" of rows — e.g. a **7-day rolling average** of sentiment. Good for smoothing noisy daily data into trends.

---

## 3. The Data We Have

**File:** `djt_posts_dec2025.csv` (despite the name, it's the FULL historical dataset)

- **90,343 posts total**
- **Date range:** 2009-05-04 → 2025-12-31 (~16 years)
- **Platforms:** Twitter (58,851) and Truth Social (31,492)
- **Handle:** all `realDonaldTrump`
- **Columns:** `id, date, platform, handle, text, favorite_count, repost_count, quote_flag, repost_flag, deleted_flag, word_count, hashtags, urls, user_mentions, media_count, media_urls, post_url, in_reply_to`

**Market data:** pulled programmatically (no file needed) via the **`yfinance`** Python library — free, no API key. Tickers we'll use include `^GSPC` (S&P 500), `^VIX` (volatility), `BTC-USD` (Bitcoin), and others as topics require.

---

## 4. The Plan (high-level pipeline)

1. **Clean** the posts in Python (handle flags like `deleted_flag`, `quote_flag`; dedupe; parse dates).
2. **Score sentiment** for every post (VADER and/or FinBERT) → adds a `sentiment_score` column.
3. **Pull market data** with `yfinance` (S&P 500, VIX, Bitcoin, etc.).
4. **Model the data** into a PostgreSQL **star schema** (Fact_Posts + Dim_Date + Dim_Market).
5. **Analyze correlation:**
   - *Baseline:* overall sentiment vs S&P 500 + VIX.
   - *Topic-aware layer:* classify posts by topic (Bitcoin, tariffs/China, oil, Fed) and correlate each topic against the market it actually moves.
6. **Visualize:**
   - A **Power BI** dashboard (`.pbix`) — I prep the data + write the DAX + give a build guide; you assemble and "Publish to web."
   - A **live web dashboard** (Plotly/Next.js) that I build and deploy to Vercel for a guaranteed-working portfolio link.
7. **Document & deploy:** GitHub repo with `README.md`, `/sql_queries` folder, and the live dashboard links on the Next.js portfolio site.

---

## 5. Decisions Log

| Date | Decision | Choice | Why |
|------|----------|--------|-----|
| 2026-06-10 | Finance data source | **Yahoo Finance (`yfinance`)** | Free, no API key, covers stocks + crypto + volatility in one library |
| 2026-06-10 | Analysis depth | **Baseline first, then topic-aware layer** | Get a working pipeline fast, then add the differentiator |
| 2026-06-10 | Dashboard approach | **Both Power BI + live web dashboard** | Power BI = résumé keyword recruiters want; web dashboard = reliable live portfolio link |
| 2026-06-10 | Sentiment engine | **VADER (to start)** | Fast, no big download, tuned for social media; FinBERT can be added later for comparison |
| 2026-06-10 | First build target | **Python pipeline** | Get a working end-to-end flow before SQL/dashboards |
| 2026-06-10 | Cleaning rules | **Drop deleted + pure reposts + empty text** | Sentiment should reflect Trump's OWN words |
| 2026-06-10 | **Project direction (major)** | **Pivot to event-study + investor calculator** | Aggregate correlation was weak; the signal lives in specific events. More compelling + reframes it as a finance project |
| 2026-06-10 | Focus topics | **Bitcoin, S&P 500, Nasdaq, Tariffs/China** | Match the user's examples + highest-impact themes |
| 2026-06-10 | Methodology order | **Score sentiment BEFORE looking at market** | Avoids circular reasoning / data snooping |
| 2026-06-10 | SQL scope | **Lightweight artifact, DuckDB-verified** | SQL is a portfolio skill-showcase, not a technical necessity here |

---

## 6. Tech Stack (planned)

- **Python** — pandas (data), `yfinance` (market data), VADER/FinBERT (sentiment), matplotlib/seaborn/Plotly (charts)
- **PostgreSQL** — star-schema data modeling + SQL analysis (window functions, joins)
- **Power BI Desktop** (free) — interactive dashboard, published via "Publish to web"
- **Next.js + Vercel** — portfolio website hosting the live web dashboard and project links
- **Git/GitHub** — version control + project repo

---

## 7. Step-by-Step Build Log

> This section grows as we actually do the work. Each entry: what we did, the file(s) involved, and the outcome.

- **2026-06-10 — Project kickoff.** Reviewed the roadmap PDF and inspected the dataset (confirmed full 2009–2025, both platforms). Created this journal. Explained sentiment analysis. Locked in finance source (`yfinance`), analysis depth (baseline → topic-aware), and dashboard approach (Power BI + web).
- **2026-06-10 — Environment + project structure.** Confirmed Python 3.13.7. Created folders (`scripts/`, `data/raw`, `data/processed`, `sql_queries/`, `output/charts`), a virtual environment (`.venv`), and `requirements.txt`. Installed pandas, numpy, vaderSentiment, matplotlib, seaborn, scipy, yfinance. Moved the raw CSV to `data/raw/`.
- **2026-06-10 — STEP 1: Data cleaning.** Script `scripts/01_clean_data.py`. Converted flag columns to booleans, parsed dates (UTC + calendar day), removed deleted posts (2,810), pure reposts (14,153), empty text (0), duplicate ids (0). **Result: 73,380 clean posts** (Twitter 47,975 / Truth Social 25,405), 2009-05-04 → 2025-12-31. Output: `data/processed/posts_clean.csv`.
- **2026-06-10 — STEP 2: Sentiment scoring (VADER).** Script `scripts/02_sentiment_vader.py`. Added `sentiment_score` (−1..+1) and `sentiment_label` to every post. **Results:** overall avg **+0.177**; 47.5% positive / 30.3% neutral / 22.2% negative. By platform: Twitter **+0.220**, Truth Social **+0.097**. Output: `data/processed/posts_scored.csv`.
- **2026-06-10 — STEP 3: Market data (yfinance).** Script `scripts/03_market_data.py`. Downloaded daily history (2009→2025) for S&P 500 (`^GSPC`), VIX (`^VIX`), Bitcoin (`BTC-USD`); computed `daily_return` and `volatility_7d` (7-day rolling std of returns). Rows: S&P 4,276 / VIX 4,276 / Bitcoin 4,124 trading days. Output: `data/processed/market_data.csv`.
- **2026-06-10 — STEP 4: Baseline correlation analysis.** Script `scripts/04_correlation_analysis.py`. Aggregated posts to daily sentiment (4,850 active days), LEFT-joined onto trading days, computed Pearson correlations (same-day, next-day lag, vs volatility). Generated 3 charts in `output/charts/`. Outputs: `data/processed/daily_merged.csv`, `output/correlation_results.csv`.
  - **Key finding (honest result):** Trump's *aggregate daily* sentiment has **essentially no correlation with same-day or next-day S&P 500 returns** (r ≈ 0.00, not significant). There is a **small but statistically significant link to volatility** — S&P volatility r = −0.036 (p=0.03) and **Bitcoin volatility r = +0.095 (p<0.0001)**. Interpretation: markets don't move with his overall mood, but Bitcoin gets measurably jumpier around his more positive posts. This nuance is exactly the kind of finding the topic-aware layer (Step 4b) is designed to sharpen.
- **2026-06-10 — Market data extended.** Added Nasdaq (`^IXIC`) and Dow (`^DJI`) to `scripts/03_market_data.py` for the topic studies.
- **2026-06-10 — STEP 4b: Topic tagging.** Script `scripts/05_topic_tagging.py`. Keyword/regex tagging of posts by topic. **Matched:** Bitcoin 31, S&P/market 438, Nasdaq 83, Tariffs/China 1,748 (2,228 topical posts total). Avg sentiment by topic: Bitcoin **+0.51** (very positive), S&P +0.11, Nasdaq +0.06, Tariffs/China +0.11. Output: `data/processed/posts_tagged.csv`.
- **2026-06-10 — STEP 5+6: Event study + investor calculator.** Script `scripts/06_event_study.py`. For each topic, treated each posting-day as an event, "bought" the related instrument, measured forward returns at +1 day / +1 week / +1 month, and computed the average value of a $100,000 investment. Built **1,589 events**. Outputs: `output/events_detail.csv`, `output/event_study_summary.csv`, `output/charts/04_event_study_returns.png`.
  - **Headline findings ($100k held 1 week, avg):** Bitcoin **−2.0%** (44% win rate) — short-term "buy the rumor, sell the news"; S&P **+0.27%** (61%); Nasdaq **+0.27%** (56%); Tariffs/China **+0.33%** (62%).
  - **1-MONTH is where it gets interesting:** Nasdaq **+2.73% (79% win rate)**, Tariffs/China +1.46% (71%), S&P +1.11% (71%), Bitcoin +1.44%. Equities tend to drift up in the month after he posts about them; Bitcoin dips short-term then recovers.
  - **Honesty caveat (documented in script + will be in README):** association, not proven causation; uses ALL events (no cherry-picking); partly reflects the general market uptrend over 2009–2025.
- **2026-06-10 — STEP 7: SQL layer (star schema).** Wrote PostgreSQL DDL (`sql_queries/01_create_schema.sql`: Dim_Date, Dim_Platform, Fact_Posts, Fact_Market) and analytical queries (`sql_queries/02_analysis_queries.sql`: rolling-average window functions, LEFT JOINs for non-trading days, `CORR()`, an in-SQL Bitcoin event study). Built + verified everything in DuckDB via `scripts/07_build_sql_db.py` (no install needed) → `data/processed/trump_market.duckdb`. **SQL `CORR()` result exactly matched the Python correlation (0.0005 / −0.0362), confirming consistency.** Added `scripts/07b_load_to_postgres.py` for real PostgreSQL when installed.
- **2026-06-10 — STEP 8: Interactive web dashboard.** Script `scripts/08_build_dashboard.py` generates a self-contained `dashboard/index.html` (Plotly + vanilla JS, data embedded). Features: KPI cards, the **interactive Investor Calculator** (pick topic / amount / horizon / sentiment → average ending value + win rate + distribution histogram), an event-study overview bar chart, a sentiment-vs-S&P timeline, and a sortable per-topic Event Explorer table. Deployable as a static page to GitHub Pages / Vercel.
- **2026-06-10 — STEP 10: Full Power BI event catalog.** Expanded topics (11 themes) and instruments (10 markets). Script `scripts/10_build_powerbi_catalog.py` → **`powerbi/`** folder.
- **2026-06-10 — STEP 11: LIVE web dashboard (no Power BI cloud).** Script `scripts/11_build_live_dashboard.py` → **`docs/index.html`** (GitHub Pages) + `dashboard/index.html`. Per-stock tabs (Bitcoin, S&P, Nasdaq, Oil, Gold), presidency era filters, in-office comparison charts, full event tables, investor calculator. Deploy guide: `DEPLOY_LIVE_DASHBOARD.md`.

---

## 8. Open Questions / To Decide

- [x] ~~Dashboard direction~~ → **Story-first Power BI** (see `DASHBOARD_STORY_PLAN.md`). Website deferred.
- [ ] Add oil (`CL=F`) data for Iran/Middle East chapter
- [ ] Build curated `story_episodes.csv` for Power BI
- [ ] User builds `.pbix` following the story plan

## 9. Direction change (2026-06-10)

User feedback: previous dashboard was too fast and too technical. New priority:
1. **Narrative dashboard** — claim → proof → investor takeaway, repeated per topic
2. **Named real-world episodes** (Bitcoin rise, tariffs, Nasdaq, Iran June 2025)
3. **Power BI** as the primary visual deliverable (not a website yet)
4. Living docs: `PROJECT_JOURNAL.md` + `DASHBOARD_STORY_PLAN.md`
