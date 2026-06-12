# Deploy — GitHub + Vercel

## Local preview

Open `website/public/index.html` in a browser, or serve the folder:

```powershell
cd website\public
python -m http.server 8080
```

Visit http://localhost:8080

## GitHub (one-time)

1. Install [GitHub CLI](https://cli.github.com/) and sign in: `gh auth login`
2. From the project root:

```powershell
gh repo create trump-post-market-analysis --public --source=. --remote=origin --description "Event study: Do Trump's posts move Bitcoin, oil, S&P 500, and Nasdaq?"
git push -u origin master
```

If your default branch is `main`:

```powershell
git branch -M main
git push -u origin main
```

Or create the repo manually at https://github.com/new and:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/trump-post-market-analysis.git
git push -u origin master
```

## Vercel (one-time)

1. Sign up at https://vercel.com (use “Continue with GitHub”)
2. **Add New Project** → import `trump-post-market-analysis`
3. Vercel reads `vercel.json` at the repo root — **Output Directory** is `website/public`
4. Deploy — no build command needed (static site)

Your live URL will look like: `https://trump-post-market-analysis.vercel.app`

### Custom domain (optional)

In Vercel → Project → Settings → Domains, add your portfolio domain.

## Re-export charts after Power BI changes

```powershell
.venv\Scripts\activate
pip install pymupdf
python scripts/14_export_website_charts.py
```

Then commit and push — Vercel redeploys automatically if connected to GitHub.
