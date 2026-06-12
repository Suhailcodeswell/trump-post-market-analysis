# Power BI visual build — premium portfolio look

**Goal:** A polished, story-driven Power BI report with Trump imagery, dark/gold theme, and one page per stock.

**You said the HTML dashboard isn't what you want — this guide is Power BI only.**

---

## Part A — Get a Power BI account (school account won't work)

Your **school tenant blocks Power BI**. Do this instead:

### Option 1 — New Outlook email (recommended, 10 minutes)

1. Go to https://outlook.com → **Create free account**
2. Pick something professional, e.g. `suhail.portfolio@outlook.com` (not your school email)
3. Go to https://app.powerbi.com → **Sign up free** with that **personal** Outlook
4. Open **Power BI Desktop** → Sign in → choose **Personal account** (NOT Work or school)
5. You should see your workspace at app.powerbi.com

### Option 2 — Build without signing in (for now)

- Close the login popup in Power BI Desktop
- Build the full report locally
- Sign up with Outlook later only when you want **Publish**

### If personal account still fails in Desktop

- Update Power BI Desktop (Microsoft Store or download latest)
- File → Options → Global → clear cache
- Try signing in only at **app.powerbi.com** in browser first, then Desktop

---

## Part B — Files already prepared for you

| File | Purpose |
|------|---------|
| `powerbi/Trump_Markets_Data.xlsx` | **Load this one file** — all sheets (Bitcoin, S&P, Oil, etc.) |
| `powerbi/themes/TrumpMarkets-Portfolio.json` | Dark + gold theme — import once |
| `powerbi/assets/trump_official_portrait.jpg` | Official U.S. portrait (public domain, Wikimedia) |
| `powerbi/assets/README.txt` | Image usage note |

---

## Part C — Setup (one time, ~20 min)

### C1. New report

1. Power BI Desktop → **File → Save As**  
   `powerbi/reports/Trump_Markets.pbix`

### C2. Load data (easy way)

1. **Home → Get data → Excel**
2. Select `powerbi/Trump_Markets_Data.xlsx`
3. In Navigator, **check every sheet** → **Load**

You now have tables: `Bitcoin_Events`, `SP500_Events`, `Nasdaq_Events`, `Oil_Events`, `Gold_Events`, `Office_Compare`, `Instrument_Summary`, `Market_Prices`, `All_Events`.

### C3. Apply the premium theme

1. **View → Themes → Browse for themes**
2. Select `powerbi/themes/TrumpMarkets-Portfolio.json`
3. Entire report gets dark navy background + gold accents

### C4. Canvas size

1. **View → Page view → 16:9** (Fit to page)

---

## Part D — COVER PAGE (make it look expensive)

This is what recruiters see first. Follow the layout:

```
┌──────────────────────────────────────────────────────────────────┐
│  [dark navy background #0B1426]                                  │
│                                                                  │
│   TRUMP POSTS & THE MARKETS          ┌─────────────────────┐    │
│   ─────────────────────────          │                     │    │
│   Event Study · 2009–2025            │   TRUMP PHOTO       │    │
│   73,380 posts · 5 markets           │   (Image visual)    │    │
│                                      │                     │    │
│   [Card: 3,352 events]               └─────────────────────┘    │
│   [Card: 5 instruments]                                          │
│   [Card: Python + SQL + Power BI]                                │
│                                                                  │
│   "When he posts about a market, what happens next?"             │
│                                                                  │
│   [Page navigator buttons → Bitcoin | S&P | Nasdaq | Oil | Gold] │
└──────────────────────────────────────────────────────────────────┘
```

### Step-by-step — Cover page

1. Rename Page 1 → **Cover**

2. **Page background** (optional subtle gradient):  
   Format page (paint roller, no visual selected) → **Canvas background** → Color `#0B1426`

3. **Trump photo:**  
   - **Insert → Image → Image**  
   - Browse to `powerbi/assets/trump_official_portrait.jpg`  
   - Resize: ~height 320px, right side of page  
   - Format image → **Border** → On, color `#C9A227` (gold), radius 8  
   - Optional: **Shadow** → subtle

4. **Title text box:**  
   - **Insert → Text box**  
   - Text:
     ```
     TRUMP POSTS & THE MARKETS
     Event-driven market study · 2009–2025
     ```
   - Font: **Segoe UI Semibold**, 32pt, color white  
   - Subtitle: 14pt, color `#8B9CC7`

5. **Gold accent line:**  
   - **Insert → Shape → Line**  
   - Color `#C9A227`, width 3px, under title

6. **Three KPI cards:**  
   - Card 1: type **3352** manually or use `All_Events` count → Title "Events studied"  
   - Card 2: **5** → "Markets tracked"  
   - Card 3: text card "VADER · SQL · Power BI"

7. **Tagline text box** (italic, muted):  
   *"When Donald Trump posts about Bitcoin, the S&P 500, or oil — what does the market do in the next week? This report answers with data, not opinions."*

8. **Disclaimer** (small, bottom):  
   *Historical associations only. Not financial advice.*

---

## Part E — BITCOIN PAGE (template for all stocks)

Duplicate this pattern for every stock.

### E1. New page → rename **Bitcoin**

### E2. Page filter

**Filters on this page** → drag nothing from Bitcoin table (we use Bitcoin_Events table only on this page — no filter needed if you only use `Bitcoin_Events` table in visuals)

**Important:** On each stock page, use **only that stock's table** (`Bitcoin_Events`, not `All_Events`) so you don't need filters.

### E3. Layout

```
┌─────────────────────────────────────────────────────────────┐
│ [Page navigator at top]                                      │
│                                                              │
│ CLAIM (text box, gold border)                                │
│ "When Trump posts about Bitcoin, short-term dips are       │
│  common; standout pro-crypto events reached +37% in 1 mo." │
│                                                              │
│ [Card: Avg 1wk return] [Card: Win rate] [Card: 28 events]  │
│                                                              │
│ [Bar chart: In Office vs Not]    [Line chart: BTC price]    │
│                                                              │
│ [Table: every Bitcoin event — date, post, sentiment, returns]│
│                                                              │
│ [Investor callout text box — gold left border]              │
└─────────────────────────────────────────────────────────────┘
```

### E4. Build visuals

**Claim box:** Text box with Format → **Background** `#1A2744`, **Border** gold

**Cards** (from `Instrument_Summary` or calculate on `Bitcoin_Events`):
- Filter visual: `instrument` = bitcoin, `horizon` = 1w → show `mean_return_pct`, `win_rate_pct`, `n_events`

**Bar chart — President comparison:**
- Table: `Office_Compare`
- Visual filter: `instrument` = bitcoin, `horizon` = 1w
- Axis: `in_office`, Values: `mean_return_pct`
- Title: "In Office vs Not In Office (1 week)"
- Colors: gold + blue (theme handles this)

**Line chart — Bitcoin price:**
- Table: `Market_Prices`, filter `instrument` = bitcoin
- X: `date_only`, Y: `close`
- Title: "Bitcoin price history"

**Event table (the proof):**
- Table: `Bitcoin_Events`
- Columns: `event_date`, `presidency_era`, `in_office`, `sentiment_label`, `return_1w_pct`, `return_1m_pct`, `value_1w`, `headline_text`
- Turn on **Word wrap** for headline
- Conditional formatting on `return_1w_pct`: green if > 0, red if < 0  
  (Format → Cell elements → Font color → Rules)

**Slicer (optional):** `presidency_era` on this page

### E5. Duplicate for other stocks

Right-click **Bitcoin** tab → **Duplicate page**

| New page | Use table | Change headline |
|----------|-----------|-----------------|
| S&P 500 | `SP500_Events` | Tariffs, Fed, broad market |
| Nasdaq | `Nasdaq_Events` | Tech / record highs |
| Oil | `Oil_Events` | Iran, energy, Jun 2025 |
| Gold | `Gold_Events` | Safe haven |

On each duplicate: **delete old visuals**, reconnect to the correct table (or replace data source in each visual's fields).

---

## Part F — Navigation (professional feel)

1. **Insert → Buttons → Navigator → Page navigator**
2. Place at top of every page (copy/paste)
3. Format navigator:
   - Fill: `#1A2744`
   - Selected: gold border `#C9A227`
   - Text: white

---

## Part G — Extra polish (what makes it "portfolio good")

| Technique | How |
|-----------|-----|
| **Consistent margins** | Leave 24px padding; don't stretch visuals edge-to-edge |
| **One hero chart per page** | Max 2 charts + 1 table |
| **Gold = claims & headers** | Blue = numbers |
| **Conditional formatting** | Returns green/red in tables |
| **Tooltips page** (advanced) | Hover event → show full post text |
| **Sync slicers** | `presidency_era` synced across stock pages |
| **Report logo** | Insert small text "Suhail Ahmed · Data Portfolio" footer |

---

## Part H — Publish (when account works)

1. **Home → Publish** → My workspace  
2. app.powerbi.com → report → **⋯ → Embed → Publish to web (public)**  
3. Copy iframe URL → portfolio site

Until then: export pages as **PDF** (File → Export → PDF) for portfolio screenshots + keep `.pbix` on GitHub.

---

## Part I — Your checklist

- [ ] Create Outlook portfolio email & Power BI free account  
- [ ] Load `Trump_Markets_Data.xlsx`  
- [ ] Import `TrumpMarkets-Portfolio.json` theme  
- [ ] Cover page with Trump photo + title + cards  
- [ ] Bitcoin page (full template)  
- [ ] Duplicate → S&P, Nasdaq, Oil, Gold  
- [ ] Page navigator on all pages  
- [ ] Save `Trump_Markets.pbix`  
- [ ] Publish OR export PDF for portfolio  

---

## START NOW — first 3 clicks

1. Open Power BI Desktop (skip login if blocked)  
2. Get Data → Excel → `Trump_Markets_Data.xlsx` → Load all sheets  
3. View → Themes → Browse → `TrumpMarkets-Portfolio.json`  

Then build **Cover** page with the Trump photo from `powerbi/assets/trump_official_portrait.jpg`.

Tell me when Cover page is done — we'll refine Bitcoin page together.
