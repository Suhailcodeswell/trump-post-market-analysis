# Dashboard Story Plan — Power BI Narrative Dashboard

> **Status:** Planning phase (we are NOT building the website yet).  
> **Goal:** A visually polished Power BI dashboard that reads like a **story** — each section opens with a plain-English **claim**, then shows **proof** underneath. A viewer should understand the finding in 10 seconds and explore the evidence if they want.

**Last updated:** 2026-06-10

---

## Why we are changing direction

The first dashboard was a **single technical page** (calculator + charts). That is useful, but it does **not** tell a story.

What you actually need:

```
┌─────────────────────────────────────────────────────────┐
│  CLAIM (headline sentence anyone can understand)        │
├─────────────────────────────────────────────────────────┤
│  PROOF 1 — KPI cards (avg return, win rate, $100k)      │
│  PROOF 2 — Chart (price path around the event)          │
│  PROOF 3 — Table (specific posts + dates + returns)     │
│  INVESTOR NOTE — "If you had invested $X on this day…"  │
└─────────────────────────────────────────────────────────┘
        ↓  (next story chapter)
```

We already have the **data** and **analysis**. The next step is **designing Power BI around these chapters**, not building another website.

---

## Data you already have (for Power BI)

Load these CSV files into Power BI Desktop (**Home → Get data → Text/CSV**):

| File | What it contains | Use in dashboard |
|------|------------------|------------------|
| `data/processed/posts_scored.csv` | Every post + sentiment | Post text, dates, mood |
| `data/processed/posts_tagged.csv` | Posts + topic flags | Filter Bitcoin / Nasdaq / tariffs |
| `data/processed/market_data.csv` | S&P, Nasdaq, Dow, VIX, Bitcoin daily prices | Price lines, returns |
| `output/events_detail.csv` | **1,589 event-days** with forward returns (+1d/+1w/+1m) and $100k values | KPIs, tables, investor math |
| `output/event_study_summary.csv` | Aggregates per topic + horizon | Headline stats for claims |

**Still to add (next data step):** Oil prices (`CL=F` via yfinance) for the Iran / Middle East chapter — geopolitical episodes move oil more than the S&P.

---

## The story structure (recommended pages)

Build **one Power BI page per chapter**. Use a dark, clean theme; large headline text boxes; max 2–3 visuals per page so it never feels crowded.

### Page 0 — Cover / The Question

**Headline:** *"When Trump posts about a market, does money follow?"*

**Subtext:** 73,380 posts · 2009–2025 · Event-study methodology

**Visuals:**
- 3 KPI cards: total posts, topics tracked, years covered
- One sentence methodology note (association ≠ causation)

**Power BI:** Text box + Card visuals. No chart needed.

---

### Page 1 — NASDAQ: "Tech rallies after he talks about Nasdaq"

#### The claim (put this as a large text box at the top)

> **When Donald Trump posts about the Nasdaq or tech stocks, the index rises +0.3% on average within one week, and +2.7% within one month — rising 79% of the time.**

#### Why this claim works
- Based on **68 distinct event-days** where he mentioned Nasdaq/tech (not cherry-picked single days).
- Honest nuance: the **1-week** move is small; the **1-month** pattern is stronger.

#### Specific episodes to highlight in the table (proof rows)

| Date | What he said (short) | Nasdaq 1 week | Nasdaq 1 month | $100k → 1 month |
|------|----------------------|---------------|----------------|-----------------|
| 2018-08-28 | "NASDAQ has just gone above 8000 for the first time" | −0.4% | +0.2% | ~$100,200 |
| 2020-06-09 | "NASDAQ HITS ALL-TIME HIGH!" (COVID recovery) | −0.6% | **+6.0%** | ~$106,000 |
| 2025-07-10 | "NASDAQ HIT ALL-TIME RECORD HIGHS… CRYPTO through the roof" | **+1.2%** | **+4.0%** | ~$104,000 |

#### Power BI visuals for this page

1. **Card (3):** Avg 1-week return · Avg 1-month return · Win rate (1 month)
2. **Clustered bar chart:** X = horizon (1 day / 1 week / 1 month), Y = avg return %. Filter: `topic = nasdaq`.
3. **Line chart with event markers:** Nasdaq price (daily). Add vertical lines or shaded bands on the 3 dates above. Use a **Date** slicer.
4. **Table:** From `events_detail.csv`, filter `topic = nasdaq`, columns: date, headline, sentiment, return_1w_pct, return_1m_pct, value_1m.
5. **Investor card (DAX):** See "Investor DAX" section below.

#### How to capitalize (investor callout text box)

> *Pattern:* Equities drift up over **~1 month** after Nasdaq-related posts.  
> *Tactical idea:* A 30-day hold on QQQ (Nasdaq ETF) after a high-engagement Nasdaq post — not a day-trade.  
> *Risk:* 21% of events still lost money over 1 month; this is an average, not a guarantee.

---

### Page 2 — TARIFFS: "Markets shake, then recover"

#### The claim

> **When Trump escalates tariff rhetoric (especially on China), the S&P 500 dips briefly — then gains +0.3% in a week and +1.5% in a month, winning 62–71% of the time.**

#### Why this claim works
- **1,117 tariff/China event-days** — the largest sample in the dataset.
- Tariff posts are often **negative in tone** but markets still tend to **recover** — a counter-intuitive finding that makes a strong story.

#### Specific episodes to highlight

| Date | Event | S&P 1 week | S&P 1 month |
|------|-------|------------|-------------|
| 2018-03-05 | Steel & aluminum tariffs announced | **+2.3%** | −2.8% |
| 2018-04-09 | "STUPID TRADE" — 25% China car tariff rant | **+2.5%** | +2.3% |
| 2018-06-09 | G7 blow-up with Trudeau over tariffs | −0.3% | −0.3% |
| 2025-01-01+ | "Tariffs alone created vast wealth" (Truth Social era) | (filter 2025 in table) | |

#### Power BI visuals

1. **Cards:** Win rate 1 week (62%) · Avg 1-month return (+1.5%)
2. **Line chart:** S&P 500 with **shaded band** Mar–Jun 2018 (tariff war period). Annotate March 5 and June 9.
3. **Scatter plot:** X = sentiment, Y = 1-week S&P return. Shows tariff posts aren't all negative → positive.
4. **Table:** Top 20 highest-engagement tariff posts + forward returns.
5. **Key insight text box:** "Markets often **price in** tariff threats quickly; recovery follows when rhetoric stabilizes."

#### Investor callout

> *Tactical idea:* After a sharp **tariff headline day** when VIX spikes, historical data shows the S&P was higher **1 month later** ~71% of the time.  
> *Instrument:* SPY (S&P 500 ETF).  
> *Caution:* 2018 G7 episode shows exceptions — always show the **distribution**, not just winners.

---

### Page 3 — BITCOIN: "Pro-crypto Trump = volatility, then a rally"

#### The claim

> **Trump's Bitcoin posts are his most positive (avg sentiment +0.51) — but Bitcoin often **dips ~2% in the first week** ("sell the news"), then **recovers +1.4% over a month**. The biggest win: +37% in the month after his Oct 2024 "Made in the USA" Bitcoin post.**

#### Why this is the most interesting chapter
- Bitcoin behaves **opposite** to Nasdaq — short-term pain, medium-term gain on pro-crypto pivots.
- Only **31 Bitcoin-tagged posts** — smaller sample, so we lead with **named episodes**, not just averages.

#### Must-show episodes

| Date | Event | BTC 1 week | BTC 1 month |
|------|-------|------------|-------------|
| 2019-07-12 | "I am NOT a fan of Bitcoin" (negative) | **−10.9%** | −2.5% |
| 2024-05-25 | "VERY POSITIVE… cryptocurrency companies" (pivot) | −2.3% | −13.0% |
| 2024-07-27 | Bitcoin Conference Nashville | −3.6% | −12.3% |
| **2024-10-31** | Satoshi White Paper anniversary — "Bitcoin MADE IN THE USA" | **+8.1%** | **+37.4%** |
| 2024-09-18 | "First President to send a transaction using Bitcoin" | +2.4% | +11.0% |
| 2025-03-02 | US Crypto Reserve executive order | −7.9% | −8.7% |

#### Power BI visuals

1. **Cards:** Avg 1-week (−2.0%) · Avg 1-month (+1.4%) · Sentiment (+0.51)
2. **Waterfall or bar chart:** Return by episode (sorted by date) — shows the narrative arc from skeptic → champion.
3. **Line chart:** Bitcoin price Jul–Dec 2024 with markers on Nashville (Jul 27) and Satoshi post (Oct 31).
4. **Table:** All 25 Bitcoin events from `events_detail.csv`.
5. **Sentiment slicer:** Compare positive vs negative Bitcoin posts (DAX split).

#### Investor callout

> *Pattern:* Short-term **sell-the-news** after pro-Bitcoin speeches; strongest gains on **policy/campaign** posts (Oct 2024).  
> *Tactical idea:* Don't FOMO-buy on announcement day. Historical avg: wait 1–2 weeks or scale in.  
> *Best historical trade:* $100k on 2024-10-31 → **$137,362** one month later (best single event).

---

### Page 4 — IRAN / MIDDLE EAST (June 2025): "War scare → VIX spike → rally on ceasefire"

#### The claim

> **During the June 2025 Iran crisis, Trump's posts tracked the escalation from ultimatum to strike to ceasefire. The VIX fear gauge jumped, then fell −4.8% in 5 days after the Jun 13 ultimatum as markets priced a resolution. The S&P gained +1.7% in the 5 days after the Jun 24 ceasefire announcement.**

#### Important note for your story
This chapter uses **geopolitical keyword posts** (Iran, Israel, Netanyahu, Hormuz) — not the automated topic tagger. We have **89 Iran-related posts in 2025 alone**, with a dense cluster **June 2–25, 2025**.

#### Timeline to show (table + annotations on chart)

| Date | Post theme | Market note |
|------|------------|-------------|
| Jun 12–13 | "60 day ultimatum… Today is day 61" | VIX ~20.8 |
| Jun 17 | "Complete control of skies over Iran" | Uncertainty peak |
| **Jun 21** | "Successful attack on three Nuclear sites" | BTC dips; volatility |
| **Jun 22** | Address to Nation / retaliation warning | |
| **Jun 24** | "CEASEFIRE… Israel and Iran" | S&P +1.7% over next 5 days |
| Jun 25+ | Aftermath / Nobel Peace Prize talk | VIX falls toward 17.5 |

#### Power BI visuals

1. **Timeline table:** Date · truncated post text · sentiment · S&P return next 5 days
2. **Dual-axis line chart:** S&P 500 (left) + VIX (right), Jun 1–Jul 15 2025. Use **play axis** or bookmarks stepping through key dates.
3. **Card:** VIX change Jun 13 → Jun 18 (−4.8% in 5 days)
4. **Card:** S&P gain after ceasefire (Jun 24 → +1.7% in 5 days)
5. *(After we add oil data)* Oil price line for the same window.

#### Investor callout

> *Pattern:* Geopolitical shocks → **VIX up, equities wobble**, then **relief rally** on de-escalation.  
> *Tactical idea:* Historical "ceasefire day" trades favored **buying the S&P** once headlines shift from strike → peace.  
> *Hedge:* VIX-related instruments spike during the crisis phase.

**Data gap:** We still need to pull **WTI Crude Oil (`CL=F`)** into `market_data.csv` for this page. I will add that in the next data step.

---

### Page 5 — INVESTOR PLAYBOOK (interactive)

#### The claim

> **Pick a topic, pick a day he posted, pick how long you hold — here's what history says $100,000 would have become on average.**

#### Power BI visuals

1. **Slicer:** Topic (Bitcoin / Nasdaq / Tariffs / S&P)
2. **Slicer:** Holding period (1 day / 1 week / 1 month)
3. **What-if parameter:** Investment amount (default $100,000)
4. **Card:** Average ending value (DAX)
5. **Card:** Win rate %
6. **Histogram:** Distribution of returns (use `return_1w_pct` etc. in a bar chart with bins — or export bins from Python)
7. **Table:** All events for selected topic

---

## DAX measures you need (copy into Power BI)

Create a `Metrics` table (Enter data → blank row) and add these measures:

```dax
Selected Return % =
VAR H = SELECTEDVALUE('Horizon'[Horizon], "1w")
RETURN
SWITCH(
    H,
    "1d", AVERAGE('events_detail'[return_1d_pct]),
    "1w", AVERAGE('events_detail'[return_1w_pct]),
    "1m", AVERAGE('events_detail'[return_1m_pct])
)

Win Rate % =
VAR H = SELECTEDVALUE('Horizon'[Horizon], "1w")
VAR T = SELECTEDVALUE('events_detail'[topic])
VAR Filtered =
    FILTER(
        'events_detail',
        'events_detail'[topic] = T &&
        NOT ISBLANK(
            SWITCH(H, "1d", [return_1d_pct], "1w", [return_1w_pct], "1m", [return_1m_pct])
        )
    )
RETURN
DIVIDE(COUNTROWS(FILTER(Filtered, [Selected Return Value] > 0)), COUNTROWS(Filtered))

Avg Ending Value =
VAR Amt = SELECTEDVALUE('Investment Amount'[Amount], 100000)
VAR Ret = [Selected Return %] / 100
RETURN Amt * (1 + Ret)

Event Count =
COUNTROWS('events_detail')
```

*(You will need a small `Horizon` lookup table with rows: 1d, 1w, 1m.)*

**What-if parameter for investment:**
- Modeling → New parameter → `$ Investment` → min 1000, max 1000000, default 100000

---

## Making it look "very very good" in Power BI

### Theme & layout
- **Background:** Dark navy `#0B1020` (matches our analysis aesthetic)
- **Accent:** Gold `#C9A227` for headlines, blue `#4F8CFF` for charts
- **Font:** Segoe UI Semibold for titles, regular for body
- **Page size:** 16:9
- **Margins:** Large padding; never fill 100% of canvas

### Story navigation
- Use **buttons + bookmarks** — one button per chapter at the top of every page
- Each bookmark resets slicers to that chapter's defaults
- Optional: **Tooltip pages** — hover an event dot to see the post text

### Visual hierarchy (top → bottom on every page)
1. **Headline claim** (text box, 24pt)
2. **3 KPI cards** (the proof numbers)
3. **One hero chart** (the main evidence)
4. **Event table** (the receipts)
5. **Investor callout** (gold-bordered text box)
6. **Disclaimer** (small grey text: association ≠ causation)

### Interactivity that matters
- **Topic slicer** (synced across pages)
- **Date range slicer** on timeline charts
- **Sentiment slicer** (positive / negative / all) on investor page
- Click a row in the event table → **cross-filter** the price chart to that date

---

## Full catalog — one worksheet per stock (DONE)

All files live in **`powerbi/`** — see `powerbi/README.md`.

### Instruments (each gets its own Power BI page group)

| Instrument | Event-days | Topics rolled in |
|------------|------------|------------------|
| **S&P 500** | 1,773 | S&P, tariffs/China, Fed/rates, Israel/Mideast |
| **Oil** | 705 | Oil/energy, Iran/geopolitics |
| **Nasdaq** | 74 | Nasdaq / tech |
| **Gold** | 94 | Gold / safe haven |
| **Bitcoin** | 28 | Crypto / Bitcoin |
| **Dow** | 15 | Dow Jones |
| **VIX** | 29 | Fear / crash rhetoric |

### Topics (optional sub-worksheets within a stock dashboard)

| Topic | Events | Maps to |
|-------|--------|---------|
| Tariffs & China | 1,117 | S&P page (sub-tab) |
| Israel & Middle East | 448 | S&P page |
| Fed & Interest Rates | 389 | S&P page |
| Iran & Geopolitics | 381 | Oil page |
| Oil & Energy | 405 | Oil page |
| S&P 500 (direct) | 372 | S&P page |
| Nasdaq | 74 | Nasdaq page |
| Gold | 94 | Gold page |
| Bitcoin | 28 | Bitcoin page |

### Presidency comparison (on every instrument page)

Add a **clustered bar chart**: X = `in_office`, Y = avg `return_1w_pct`.

**Findings from the data (1-week hold, all events):**

| Instrument | In Office | Not In Office | Story angle |
|------------|-----------|---------------|-------------|
| **Nasdaq** | +0.16%, 56% win | −0.08%, 50% win | Better **1-month** in office (+3.8% vs +1.0%) |
| **S&P 500** | +0.37%, 64% win | +0.26%, 59% win | Slightly stronger when president |
| **Bitcoin** | −2.8% week | −0.9% week | **Not in office** better 1-month (+3.6% vs −1.5%) — pro-crypto pivot mostly 2024 |
| **Oil** | −2.1% week | −0.4% week | Geopolitical posts during 1st term often coincided with oil volatility |
| **Gold** | +0.54% week | +0.37% week | Modest safe-haven drift |
| **Tariffs** (topic) | +0.43% week | +0.23% week | Tariff talk slightly stronger market follow-through in office |

Use **4-way `presidency_era` slicer** when you want to split 1st term vs 2021–2024 vs 2nd term.

---

## What is next

| Step | Status |
|------|--------|
| Oil + gold + expanded market data | ✅ Done |
| Full `powerbi/` event catalog | ✅ Done |
| Presidency era columns | ✅ Done |
| **You:** build `.pbix` page per instrument | 🔲 Your turn |
| Curated headline episodes (optional polish) | 🔲 On request |
| Publish to web | 🔲 When dashboard looks good |

**We are NOT building the website until the Power BI story dashboard is done.**

---

## Honesty footer (put on every page)

> These results show **historical associations**, not proof that Trump's posts *caused* market moves. Other news, earnings, and macro trends also move markets. Past patterns may not repeat. This is an analytical case study, not financial advice.
