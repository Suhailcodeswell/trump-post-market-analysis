# Power BI — Step-by-step (no Microsoft account needed)

**Your situation:** Power BI Desktop works. Microsoft account does not. **That is fine.**

You can build the full dashboard locally, export screenshots/PDF, push everything to GitHub, and add a good-looking portfolio page later. Live Power BI embed is optional — only if you get a personal Outlook account someday.

**Time:** ~2–3 hours for a solid first version (Cover + 5 stock pages).

---

## What you will end up with

| Deliverable | Where | Who sees it |
|-------------|-------|-------------|
| Interactive report | `powerbi/reports/Trump_Markets.pbix` | Recruiters download & open in Power BI Desktop |
| Screenshot gallery | `powerbi/exports/*.png` | Portfolio website (static, looks professional) |
| PDF report | `powerbi/exports/Trump_Markets_Report.pdf` | GitHub + LinkedIn |
| Data + code | GitHub repo | Proves Python/SQL + BI pipeline |

---

## Before you start — files on your PC

All paths relative to: `C:\Users\ABDUL SATHAR\OneDrive\Desktop\Trump-Market\`

| File | Use |
|------|-----|
| `powerbi/Trump_Markets_Data.xlsx` | Load this in Power BI (easiest) |
| `powerbi/themes/TrumpMarkets-Portfolio.json` | Dark + gold theme |
| `powerbi/assets/trump_official_portrait.jpg` | Cover page photo |

---

# PHASE 1 — Open Power BI & load data (15 min)

### Step 1 — Open Power BI Desktop
- Start menu → **Power BI Desktop**

### Step 2 — Skip sign-in
- Login popup appears → click **X** or **Skip for now**
- You do **not** need an account to build or save

### Step 3 — Save your report immediately
- **File → Save As**
- Save to: `powerbi\reports\Trump_Markets.pbix`
- If `reports` folder doesn't exist, create it

### Step 4 — Load the Excel data
- **Home → Get data → Excel**
- Browse to `powerbi\Trump_Markets_Data.xlsx`
- In the Navigator window, **check every sheet**:
  - Bitcoin_Events, SP500_Events, Nasdaq_Events, Oil_Events, Gold_Events
  - Office_Compare, Instrument_Summary, Market_Prices, All_Events
- Click **Load** (not Transform, unless dates look wrong)

### Step 5 — Check the data loaded
- Right side panel → **Data** view (table icon)
- Click `Bitcoin_Events` — you should see ~28 rows
- Click `SP500_Events` — you should see ~1,773 rows

### Step 6 — Apply the theme
- **View → Themes → Browse for themes**
- Select `powerbi\themes\TrumpMarkets-Portfolio.json`
- Background turns dark navy, accents turn gold

### Step 7 — Set page size
- **View → Page view → Fit to page** (16:9)

### Step 8 — Save again
- **Ctrl + S**

---

# PHASE 2 — Cover page (20 min)

### Step 9 — Rename page
- Bottom tab **Page 1** → double-click → rename to **Cover**

### Step 10 — Add Trump photo
- **Insert → Image → Image**
- Browse: `powerbi\assets\trump_official_portrait.jpg`
- Drag to **right side** of page, height ~320px
- With image selected → **Format** (paint roller):
  - **Border** → On, color `#C9A227` (gold), radius 8

### Step 11 — Add title
- **Insert → Text box**
- Type:
  ```
  TRUMP POSTS & THE MARKETS
  Event-driven market study · 2009–2025
  ```
- Font: **Segoe UI Semibold**, 32pt, white
- Subtitle line: 14pt, gray

### Step 12 — Add gold line under title
- **Insert → Shapes → Line**
- Color gold, width 3px, place under title

### Step 13 — Add three KPI cards
- **Insert → Card** (do three times)
- Card 1: drag `All_Events` → field `event_id` → change to **Count** → title "Events studied"
- Card 2: type **5** manually in a text box, label "Markets tracked"
- Card 3: text box "VADER · SQL · Power BI"

### Step 14 — Add tagline
- Text box (italic, muted gray):
  *When Donald Trump posts about Bitcoin, the S&P 500, or oil — what does the market do next?*

### Step 15 — Add disclaimer (small, bottom)
- *Historical associations only. Not financial advice.*

**Save (Ctrl+S).**

---

# PHASE 3 — Bitcoin page (template for all stocks) (30 min)

### Step 16 — New page
- **Home → Insert → New page** (or + tab at bottom)
- Rename to **Bitcoin**

### Step 17 — Add claim box (top)
- Text box with gold left border feel:
  ```
  When Trump posts about Bitcoin, short-term dips are common.
  Standout pro-crypto posts saw up to +37% in one month.
  ```
- Format → Background `#1A2744`

### Step 18 — Three summary cards
- Table: `Instrument_Summary`
- Add **Filters on this visual** (not page): `instrument` = bitcoin, `horizon` = 1w
- Card 1: `mean_return_pct` — title "Avg 1-week return"
- Duplicate card → `win_rate_pct` — "Win rate (1 week)"
- Duplicate card → `n_events` — "Events"

### Step 19 — Bar chart: In office vs not
- **Clustered bar chart**
- Table: `Office_Compare`
- Visual filter: `instrument` = bitcoin, `horizon` = 1w
- Y-axis: `in_office`
- X-axis: `mean_return_pct`
- Title: "In Office vs Not In Office (1 week)"

### Step 20 — Line chart: Bitcoin price
- **Line chart**
- Table: `Market_Prices`
- Visual filter: `instrument` = bitcoin
- X-axis: `date_only`
- Y-axis: `close`
- Title: "Bitcoin price history"

### Step 21 — Event table (the proof)
- **Table** visual
- Table: `Bitcoin_Events`
- Columns: `event_date`, `presidency_era`, `in_office`, `sentiment_label`, `return_1w_pct`, `return_1m_pct`, `headline_text`
- Format → turn on **Word wrap** for headline
- **Conditional formatting** on `return_1w_pct`:
  - Format → Cell elements → Font color → Rules
  - If value ≥ 0 → green; if &lt; 0 → red

### Step 22 — Optional slicer
- **Slicer** → `presidency_era` from `Bitcoin_Events`

**Save.**

---

# PHASE 4 — Duplicate for other stocks (45 min)

For each stock, duplicate the Bitcoin page and swap the data:

### Step 23 — Duplicate page
- Right-click **Bitcoin** tab → **Duplicate page**
- Rename (e.g. **S&P 500**)

### Step 24 — Update every visual on the new page
For each visual, click it → **Fields** panel → change data source:

| Page | Events table | Instrument filter (summary/office charts) | Claim text |
|------|--------------|---------------------------------------------|------------|
| **S&P 500** | `SP500_Events` | sp500 | Tariffs, Fed, broad market moves |
| **Nasdaq** | `Nasdaq_Events` | nasdaq | Tech rallies, record highs |
| **Oil** | `Oil_Events` | oil | Iran, energy, Jun 2025 cluster |
| **Gold** | `Gold_Events` | gold | Safe-haven moves |

**Tip:** Easiest fix — delete old visuals, copy layout from Bitcoin, add new visuals wired to the correct table.

### Step 25 — Page navigator (navigation bar)
- On **Cover** page: **Insert → Buttons → Navigator → Page navigator**
- Resize to full width at top
- **Copy** the navigator (Ctrl+C)
- **Paste** on every other page (Ctrl+V)
- Format: selected tab gets gold border

**Save.**

---

# PHASE 5 — Export for portfolio (no account needed) (10 min)

### Step 26 — Create exports folder
```powershell
mkdir "powerbi\exports"
```

### Step 27 — Export full report as PDF
- **File → Export → Export to PDF**
- Save as: `powerbi\exports\Trump_Markets_Report.pdf`
- Check **Current values** if asked

### Step 28 — Export each page as PNG (for website)
- Go to **Cover** page
- **File → Export → Export current page as PNG**
- Save: `powerbi\exports\01_cover.png`
- Repeat for Bitcoin, S&P 500, Nasdaq, Oil, Gold
  - `02_bitcoin.png`, `03_sp500.png`, etc.

These PNGs are what you put on your portfolio website — they look exactly like Power BI.

---

# PHASE 6 — Push to GitHub (15 min)

### Step 29 — Initialize repo (once)
```powershell
cd "C:\Users\ABDUL SATHAR\OneDrive\Desktop\Trump-Market"
git init
git add powerbi/ scripts/ README.md PROJECT_JOURNAL.md POWERBI_STEP_BY_STEP.md
git add data/processed/
git commit -m "Trump market event study — Power BI report and data"
```

### Step 30 — Create GitHub repo & push
1. github.com → **New repository** → name: `Trump-Market`
2. Copy the remote URL
```powershell
git remote add origin https://github.com/YOUR_USERNAME/Trump-Market.git
git branch -M main
git push -u origin main
```

### Step 31 — What to include in README
Add a section like:

```markdown
## Power BI Dashboard
- Download [`powerbi/reports/Trump_Markets.pbix`](powerbi/reports/Trump_Markets.pbix) — open in Power BI Desktop
- [PDF export](powerbi/exports/Trump_Markets_Report.pdf)
- Preview: see `powerbi/exports/` screenshots
```

**Note:** If `.pbix` is over 100 MB, push CSV + PNG + PDF only (skip `.pbix` or use Git LFS).

---

# PHASE 7 — Portfolio website (later, no Power BI account needed)

When you're ready for the website, use **exported PNGs** in a simple gallery:

```
portfolio-site/
  images/trump-markets/
    01_cover.png
    02_bitcoin.png
    ...
  index.html   ← hero + image carousel + link to GitHub + PDF download
```

Visitors see polished dashboard screenshots. Recruiters who want interactivity download the `.pbix`.

**If you get a Microsoft account later:**
- **Home → Publish** → Publish to web → iframe on site (replaces static images)

---

# Quick reference — Power BI UI

| You want to… | Click… |
|--------------|--------|
| Load data | Home → Get data |
| Add chart | Home → bar/line/table icons, or **Visualizations** pane |
| Change colors | Select visual → Format (paint roller) |
| Filter one chart only | **Filters on this visual** (not "Filters on this page") |
| New page | + at bottom tabs |
| Save | Ctrl+S |

---

# Checklist — tick as you go

- [ ] Step 1–8: Data loaded, theme applied, file saved
- [ ] Step 9–15: Cover page with Trump photo
- [ ] Step 16–22: Bitcoin page complete
- [ ] Step 23–24: S&P, Nasdaq, Oil, Gold pages
- [ ] Step 25: Page navigator on all pages
- [ ] Step 26–28: PDF + PNG exports
- [ ] Step 29–31: GitHub push

---

# When you're stuck

| Problem | Fix |
|---------|-----|
| Login keeps popping up | Click X every time — doesn't block saving |
| Dates show as numbers | Get data → Transform → change column to Date |
| Wrong table on a page | Click visual → Fields → swap to correct `*_Events` table |
| Visual shows all stocks | Add filter: `instrument` = bitcoin (etc.) |
| File too big for GitHub | Push exports + CSV only; `.pbix` stays local or use Git LFS |

**Detailed visual layout:** see `POWERBI_VISUAL_GUIDE.md`  
**DAX / advanced:** see `POWERBI_BEGINNER_GUIDE.md`

---

**Start at Step 1.** When Cover + Bitcoin pages are done, we can refine claims and website layout together.
