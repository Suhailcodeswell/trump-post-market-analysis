# Deploy the live dashboard (no Power BI account needed)

Your **live interactive dashboard** is a single HTML file in the `docs/` folder.  
GitHub Pages hosts it for **free** with a public URL.

---

## What you get

- **URL format:** `https://YOUR_GITHUB_USERNAME.github.io/Trump-Market/`
- **Fully interactive:** tabs per stock, sortable tables, charts, investor calculator
- **No Microsoft login** required for you or visitors

---

## Step 1 — Preview locally (right now)

1. Open folder: `Trump-Market\docs\`
2. Double-click **`index.html`**
3. Or run: `start docs\index.html` in PowerShell

You should see tabs: Overview | Bitcoin | S&P 500 | Nasdaq | Oil | Gold | Calculator

---

## Step 2 — Rebuild after data changes

```powershell
cd "C:\Users\ABDUL SATHAR\OneDrive\Desktop\Trump-Market"
.\.venv\Scripts\python.exe scripts\11_build_live_dashboard.py
```

This updates both `docs/index.html` and `dashboard/index.html`.

---

## Step 3 — Push to GitHub

```powershell
cd "C:\Users\ABDUL SATHAR\OneDrive\Desktop\Trump-Market"
git init
git add docs/ powerbi/ scripts/ data/processed/market_data.csv README.md PROJECT_JOURNAL.md
git commit -m "Add live interactive market event study dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Trump-Market.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## Step 4 — Turn on GitHub Pages (one time)

1. Go to your repo on GitHub  
2. **Settings → Pages**  
3. **Source:** Deploy from a branch  
4. **Branch:** `main`  
5. **Folder:** `/docs`  
6. Click **Save**  
7. Wait 1–3 minutes — your live URL appears at the top of the Pages settings

---

## Step 5 — Add to portfolio

Link the GitHub Pages URL on your portfolio site:

```html
<a href="https://YOUR_USERNAME.github.io/Trump-Market/" target="_blank">
  Trump Posts &amp; Market Event Study (Live Dashboard)
</a>
```

Or embed full-screen:

```html
<iframe src="https://YOUR_USERNAME.github.io/Trump-Market/" 
        width="100%" height="800" style="border:none;border-radius:12px"></iframe>
```

---

## Power BI `.pbix` vs live dashboard

| | Live HTML (`docs/`) | Power BI `.pbix` |
|--|---------------------|------------------|
| Works without Microsoft cloud | ✅ Yes | Build only (no publish) |
| Visitors click & filter in browser | ✅ Yes | Needs publish OR download file |
| Shows on portfolio | ✅ GitHub Pages URL | PDF screenshots or file download |
| Proves Power BI skill | — | ✅ Commit `.pbix` to repo |

**Best portfolio combo:** Live HTML dashboard **+** `.pbix` on GitHub **+** link to both.
