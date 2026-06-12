# Power BI Beginner Guide — Stock-by-Stock Dashboards

> **You have never used Power BI?** Follow this document top to bottom.  
> Do **not** skip ahead. Each stock is one **page** inside **one master report** (recommended).

**Last updated:** 2026-06-10

---

## ⚠️ School or work account blocked? (READ THIS IF LOGIN FAILS)

If you see *"Your administrator doesn't allow this"* or *"Personal account can't be used"* — **you are not stuck.** You have three paths:

### Path A — Don't sign in at all (build locally) ✅ **Start here**

Power BI Desktop **does not require sign-in** to build dashboards.

1. When the login popup appears → click **X** or **Skip for now** / **Continue without signing in**  
2. Build your report normally (load CSV, charts, pages)  
3. **File → Save** → `powerbi/reports/Trump_Markets.pbix`  
4. Push `.pbix` + CSVs to **GitHub**

**What works without publishing:**

| Works | Doesn't work |
|-------|----------------|
| Build full multi-page report | Live iframe on website from Power BI cloud |
| Save `.pbix` to GitHub | Viewers clicking `.pbix` in browser (GitHub can't render it) |
| Export pages as **PDF** or **PNG** for portfolio | "Publish to web" button |
| Recruiters with PBI Desktop open your file | Interactive embed without cloud |

**For your portfolio:** GitHub link *"Download `.pbix` to explore"* + **PDF screenshots** of each stock page + (optional) our **HTML dashboard** for live interactivity without Microsoft cloud.

### Path B — New free Outlook email (only if you want live embed later)

School tenants block Power BI Service. A **personal @outlook.com** used only for this project often works:

1. Create https://outlook.com account (e.g. `suhail.portfolio@outlook.com`) — **not** your school email  
2. In Power BI Desktop → Sign in → choose **Personal account** (not Work/school)  
3. Sign up at https://app.powerbi.com with same Outlook  
4. Then **Publish → Publish to web** works

If Desktop still rejects personal account, stay on **Path A** — your project is still valid.

### Path C — Live website without Power BI cloud

We already built `dashboard/index.html` — interactive charts, no Microsoft login. For portfolio:

- **Power BI `.pbix` on GitHub** = proves BI / DAX / modeling skills  
- **HTML dashboard on GitHub Pages** = live demo visitors can click  

Both in one repo is a strong portfolio combo.

### Bottom line

| Question | Answer |
|----------|--------|
| Must I publish to build the dashboard? | **No** — build and save locally |
| Can I push `.pbix` to GitHub only? | **Yes** — recommended minimum |
| Will `.pbix` work on GitHub in the browser? | **No** — needs download or PDF exports |
| Is the project still portfolio-worthy without publish? | **Yes** — `.pbix` + README + PDF exports + HTML dashboard |

---

## Part 0 — How this all fits together (read once)

```
YOUR COMPUTER                         MICROSOFT CLOUD              YOUR PORTFOLIO SITE
─────────────────                     ───────────────              ───────────────────

Power BI Desktop                      Power BI Service             Next.js / HTML page
  │                                     (free account)                 │
  │  You build visuals                  │                              │
  │  from our CSV files                 │  "Publish to web"            │
  ▼                                     ▼                              ▼
Trump_Markets.pbix  ──Publish──►  Live interactive report  ──embed──►  iframe on your site
       │                                                                 (later step)
       │
       └── Save to GitHub ──►  powerbi/reports/Trump_Markets.pbix
                               (backup + portfolio proof you built it)
```

**Three separate things:**

| Thing | What it is | Where it lives |
|-------|------------|----------------|
| **Data (CSV)** | The numbers we calculated | `powerbi/by_instrument/*.csv` — already done |
| **Report (.pbix)** | The dashboard you design | `powerbi/reports/Trump_Markets.pbix` — you create this |
| **Live embed** | What visitors click on | Power BI cloud URL → iframe on website — last step |

**GitHub:** Yes — put `.pbix` file(s) in **`powerbi/reports/`** in the same repo. One repo, one folder for reports.

**One file or many?**

| Approach | Pros | Cons | Recommendation |
|----------|------|------|----------------|
| **ONE `.pbix`, one page per stock** | One publish link, easy navigation, cleaner portfolio | File gets larger | ✅ **Do this** |
| **Many `.pbix` (one per stock)** | Smaller files, work on one stock at a time | Many publish links, messy portfolio | Only if file is huge |

We use **one master report** with these **pages** (think of pages as "sheets"):

1. Cover — The Question  
2. Bitcoin  
3. S&P 500  
4. Nasdaq  
5. Oil  
6. Gold  
7. Investor Playbook (calculator page)

---

## Part 1 — Install Power BI Desktop (15 minutes)

### Step 1.1 — Download (free)

1. Open: https://www.microsoft.com/en-us/download/details.aspx?id=58494  
2. Click **Download** → choose **PBIDesktopSetup_x64.exe** (64-bit Windows).  
3. Run the installer → Next → Next → Finish.

### Step 1.2 — Sign in (OPTIONAL — skip if school account is blocked)

1. Open **Power BI Desktop** from Start menu.  
2. If a login popup appears:
   - **School/work blocked?** → Click **X** or **Skip for now**. You can build everything without signing in.  
   - **Want live embed later?** → Use a **new @outlook.com** (not school email) → Sign in as **Personal account**.  
3. You do **not** need Power BI Pro to build locally.

### Step 1.3 — Turn off distractions (optional)

File → Options → Global → Privacy → allow data collection (default is fine).

---

## Part 2 — Create the master report file (10 minutes)

### Step 2.1 — New file

1. Open Power BI Desktop.  
2. You see a blank canvas.  
3. **File → Save As**  
4. Navigate to:  
   `C:\Users\ABDUL SATHAR\OneDrive\Desktop\Trump-Market\powerbi\reports\`  
5. Save as: **`Trump_Markets.pbix`**

> Create the `reports` folder if it doesn't exist.

### Step 2.2 — Load ALL data (one time)

We load 3 types of files:

**A) All instrument events (main table)**

1. **Home → Get data → Text/CSV**  
2. Browse to: `Trump-Market\powerbi\all_events.csv`  
3. Click **Load** (not Transform — data is already clean).

**B) Market prices (for line charts)**

1. **Home → Get data → Text/CSV**  
2. Load: `Trump-Market\data\processed\market_data.csv`

**C) Presidency comparison summary (for bar charts)**

1. **Home → Get data → Text/CSV**  
2. Load: `Trump-Market\powerbi\in_office_comparison_by_instrument.csv`

You should see 3 tables in the **Data** pane on the right:
- `all_events`
- `market_data`
- `in_office_comparison_by_instrument`

### Step 2.3 — Fix dates (important)

Power BI sometimes reads dates wrong.

1. Click **Transform data** (top ribbon) — opens Power Query.  
2. Click `all_events` table → click `event_date` column → **Data type → Date**  
3. Same for `buy_date`.  
4. Click `market_data` → `date_only` → **Date**  
5. **Home → Close & Apply**

### Step 2.4 — Rename your first page

1. At the bottom, double-click **Page 1**  
2. Rename to: **Cover**

---

## Part 3 — Build the COVER page (10 minutes)

This is your title slide.

1. **Insert → Text box** — type:
   ```
   When Trump Posts, Does The Market Move?
   Event study · 2009–2025 · 73,380 posts
   ```
2. Format: large font (24pt), bold, dark background optional.  
3. **Insert → Card** visual → drag `event_date` from `all_events` → change to **Count (Distinct)**  
   - This shows total events. Rename visual title to "Market events studied".  
4. **Insert → Text box** (small, bottom):
   ```
   Historical associations only — not financial advice.
   ```

**Save:** Ctrl+S

---

## Part 4 — Build BITCOIN page (first stock — 45 minutes)

> Bitcoin has only **28 events** — perfect to learn before S&P (1,773 events).

### Step 4.1 — New page

1. **Insert → New page**  
2. Rename bottom tab to: **Bitcoin**

### Step 4.2 — Headline claim (text box at top)

```
CLAIM: When Trump posts about Bitcoin, the market often dips short-term
then recovers — averaging −2.8% in 1 week while IN office vs stronger
long-term gains when NOT in office (+3.6% over 1 month).
```

(You can edit wording after you see the numbers in your visuals.)

### Step 4.3 — Filter this page to Bitcoin only

We use a **page-level filter** so every visual on this page shows Bitcoin only.

1. In **Filters** pane (right side), find **Filters on this page**.  
2. Drag `instrument` from `all_events` into **Filters on this page**.  
3. Check only **bitcoin**.  
4. Do the same for `market_data` → filter `instrument` = **bitcoin**.

Now everything you add on this page is Bitcoin-only.

### Step 4.4 — KPI cards (3 proof numbers)

**Card 1 — Average 1-week return**

1. **Insert → Card**  
2. Drag `return_1w_pct` → ensure it says **Average** (not Sum).  
   - If it says Sum: click the field in the visual → **Average**.  
3. Title: "Avg 1-week return %"

**Card 2 — Win rate**

1. **Insert → Card**  
2. Drag `return_1w_pct` again.  
3. Click dropdown on the field → **Count** won't work — instead we'll use a simple approach:  
   - For beginners: use **Table** visual with `return_1w_pct`, add a **Conditional formatting** green/red, and eyeball — OR skip win rate until DAX (Part 8).  
   - **Easier shortcut:** Load `powerbi/in_office_comparison_by_instrument.csv`, filter instrument=bitcoin, horizon=1w, show `win_rate_pct` in a Card.

**Card 3 — Event count**

1. **Insert → Card**  
2. Drag `event_date` → **Count (Distinct)**  
3. Title: "Bitcoin post-days"

### Step 4.5 — President vs Not President (bar chart)

1. Use table `in_office_comparison_by_instrument`  
2. **Insert → Clustered bar chart**  
3. **Axis:** `in_office`  
4. **Values:** `mean_return_pct`  
5. **Filters on this visual:** `instrument` = bitcoin, `horizon` = 1w  
6. Title: "Avg 1-week return: In Office vs Not In Office"

### Step 4.6 — Event table (the receipts)

1. **Insert → Table**  
2. Columns (drag in order):
   - `event_date`
   - `presidency_era`
   - `sentiment_label`
   - `return_1w_pct`
   - `value_1w`
   - `headline_text`
3. Sort by `event_date` descending (newest first).  
4. Format `headline_text` column wide enough to read.

### Step 4.7 — Price line chart

1. **Insert → Line chart**  
2. **X-axis:** `date_only` from `market_data` (bitcoin filtered)  
3. **Y-axis:** `close`  
4. Title: "Bitcoin price (2009–2025)"

*(Advanced later: add event dots on the line — skip for first pass.)*

### Step 4.8 — Investor callout (text box)

```
INVESTOR NOTE: Historical pattern shows short-term "sell the news"
after pro-Bitcoin posts. Best single event: Oct 31 2024 — $100k →
$137k in 30 days. Not financial advice.
```

**Save:** Ctrl+S

---

## Part 5 — Repeat for each stock (same template)

For each new page, **duplicate the Bitcoin page** and change the filter:

| Page name | Filter `instrument` to | Also load topic sub-page? |
|-----------|------------------------|---------------------------|
| **S&P 500** | sp500 | Add bookmark for Tariffs (filter topic) |
| **Nasdaq** | nasdaq | — |
| **Oil** | oil | Filter `iran_geopolitics` topic for Jun 2025 |
| **Gold** | gold | — |
| **Dow** | dow | — (only 15 events) |
| **VIX** | vix | — |

### How to duplicate a page (fast)

1. Right-click **Bitcoin** page tab → **Duplicate page**  
2. Rename tab (e.g. **S&P 500**)  
3. Change **Filters on this page**: `instrument` → **sp500**  
4. Update headline text box with S&P claim  
5. Update investor callout  

### S&P 500 sub-worksheets (optional, looks professional)

Instead of separate `.pbix` files, use **bookmarks** on the S&P page:

1. Build S&P page with all sp500 events.  
2. **View → Bookmarks pane → Add** bookmark "All S&P events".  
3. Add filter `topic` = tariffs_china → **Add** bookmark "Tariffs".  
4. **Insert → Buttons → Navigator** to switch bookmarks.

Viewer clicks **Tariffs | Fed | Israel | All** on the same page.

---

## Part 6 — Navigation between stocks (make it feel like one app)

### Option A — Page navigator (easiest)

1. **Insert → Buttons → Navigator → Page navigator**  
2. Power BI auto-lists all pages (Cover, Bitcoin, S&P…).  
3. Place at top of every page.  
4. Format → turn on **Show only selected page** if you want tabs.

### Option B — Buttons + Bookmarks

More control, more work — use Option A first.

---

## Part 7 — Save to GitHub (when first stock page looks good)

### Folder structure in your repo

```
Trump-Market/
├── powerbi/
│   ├── by_instrument/          ← data (already there)
│   ├── by_topic/
│   ├── all_events.csv
│   └── reports/
│       └── Trump_Markets.pbix    ← YOU save here
├── data/
├── scripts/
└── README.md
```

### Git commands (when ready)

```powershell
cd "C:\Users\ABDUL SATHAR\OneDrive\Desktop\Trump-Market"
git init
git add powerbi/ data/processed/market_data.csv scripts/ README.md
git add powerbi/reports/Trump_Markets.pbix
git commit -m "Add Power BI market event study report"
git remote add origin YOUR_GITHUB_URL
git push -u origin main
```

**Note:** `.pbix` files can be 20–100 MB if data is imported. GitHub allows up to 100 MB per file. If too large:
- Use Git LFS, OR  
- Don't commit `.pbix` — commit CSV + screenshots + publish link only.

Add to `.gitignore` only if file is too big — otherwise **commit the `.pbix`** so recruiters see you built it.

---

## Part 8 — Publish live (for portfolio website — LATER)

Do this **after all pages look good**.

### Step 8.1 — Publish to Power BI Service

1. In Power BI Desktop: **Home → Publish**  
2. Choose **My workspace**  
3. Wait for "Success"

### Step 8.2 — Publish to web (public embed — free)

1. Go to https://app.powerbi.com  
2. Find your report **Trump_Markets**  
3. Click **⋯** (More options) → **Embed report → Publish to web (public)**  
4. Confirm (data is public — fine for portfolio)  
5. Copy the **iframe HTML** snippet

### Step 8.3 — Put on portfolio site (when we build the site)

```html
<iframe 
  title="Trump Markets Study"
  width="100%" 
  height="600"
  src="YOUR_EMBED_URL_FROM_POWER_BI"
  frameborder="0" 
  allowFullScreen="true">
</iframe>
```

Save embed URL in: `powerbi/publish_url.txt` in the repo.

**Important:** The website does **not** read `.pbix` files directly. Visitors need the **published embed link**.

---

## Part 9 — Simple DAX for win rate (optional, when ready)

**Modeling → New measure:**

```dax
Win Rate 1W = 
DIVIDE(
    COUNTROWS(FILTER(all_events, all_events[return_1w_pct] > 0)),
    COUNTROWS(FILTER(all_events, NOT ISBLANK(all_events[return_1w_pct])))
)
```

Format as **Percentage**. Use in a Card on each page (respects page filter).

---

## Part 10 — Your checklist (do in order)

- [ ] Install Power BI Desktop  
- [ ] Save `Trump_Markets.pbix` in `powerbi/reports/`  
- [ ] Load 3 CSV files (all_events, market_data, in_office_comparison)  
- [ ] Fix date types in Power Query  
- [ ] Build **Cover** page  
- [ ] Build **Bitcoin** page (full template)  
- [ ] Duplicate → **S&P 500** page  
- [ ] Duplicate → **Nasdaq**, **Oil**, **Gold**  
- [ ] Add **Page navigator** at top  
- [ ] Publish → Publish to web → save embed URL  
- [ ] Commit to GitHub  

---

## START HERE — Do these 5 actions right now

1. **Install** Power BI Desktop (Part 1).  
2. **Save** empty report as `powerbi/reports/Trump_Markets.pbix`.  
3. **Load** `powerbi/all_events.csv` via Get Data → CSV → Load.  
4. **Rename** Page 1 to **Cover**, add title text box.  
5. **Add** new page **Bitcoin**, set page filter `instrument = bitcoin`, add **Table** with columns: date, headline, return_1w_pct.

When Bitcoin table shows 28 rows — **stop and tell me**. We'll do the charts together on the next step.

---

## Quick answers

**Q: Multiple pbix in one GitHub repo?**  
A: Yes. Folder `powerbi/reports/`. One master file is cleaner than seven files.

**Q: Can portfolio website read pbix from a folder?**  
A: No. Website needs **Publish to web** iframe URL. The `.pbix` in GitHub is for source/backup.

**Q: Do I need Power BI Pro?**  
A: No for public embed. Pro needed for private sharing only.

**Q: Sheets vs pages?**  
A: Power BI uses **Pages** (tabs at bottom). Same idea as Excel sheets.

**Q: What if I mess up?**  
A: Ctrl+Z. Or delete visual and re-add. Data is in CSV — reload anytime.
