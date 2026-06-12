"""
STEP 11 — LIVE WEB DASHBOARD (GitHub Pages / portfolio embed)
======================================================================
Generates a self-contained interactive dashboard — NO Power BI cloud needed.

Outputs:
  docs/index.html          ← GitHub Pages serves this as your LIVE URL
  dashboard/index.html     ← copy for local preview

Data: powerbi/ catalog (all instruments, presidency eras, full events)
======================================================================
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PBI = ROOT / "powerbi"
DOCS = ROOT / "docs"
DASH = ROOT / "dashboard"

INSTRUMENTS = [
    {
        "id": "bitcoin",
        "label": "Bitcoin",
        "emoji": "₿",
        "claim": (
            "When Trump posts about Bitcoin, markets often show short-term "
            "\"sell the news\" pressure (~−1.8% avg over 1 week) — but standout "
            "pro-crypto events like Oct 2024 reached +37% in a month."
        ),
        "investor": (
            "Pattern: don't FOMO on announcement day. Historically, waiting 1–2 weeks "
            "or targeting 30-day holds on major policy posts captured stronger returns."
        ),
    },
    {
        "id": "sp500",
        "label": "S&P 500",
        "emoji": "📈",
        "claim": (
            "When Trump posts about the broad market, tariffs, the Fed, or the Middle East, "
            "the S&P 500 rose +0.31% on average within one week and +1.46% within one month "
            "(72% win rate over 1 month, 1,755 events)."
        ),
        "investor": (
            "Tariff-headline days often spike fear first, then equities drift up over ~30 days. "
            "SPY 1-month holds after tariff/China post-days won ~62% of the time historically."
        ),
    },
    {
        "id": "nasdaq",
        "label": "Nasdaq",
        "emoji": "💻",
        "claim": (
            "Nasdaq-related posts correlate with tech strength: +0.10% avg in 1 week, "
            "+3.0% over 1 month, with an 80% win rate on the monthly horizon."
        ),
        "investor": (
            "When Trump celebrates Nasdaq record highs, a 30-day QQQ hold historically "
            "outperformed 1-week trades — especially during in-office periods (+3.8% avg 1mo)."
        ),
    },
    {
        "id": "oil",
        "label": "Oil",
        "emoji": "🛢",
        "claim": (
            "Oil & energy posts (including Iran geopolitics) show high volatility. "
            "June 2025 Iran crisis: VIX spiked, then markets rallied on the ceasefire."
        ),
        "investor": (
            "Geopolitical clusters move oil sharply. June 2025: oil and equities recovered "
            "after ceasefire headlines — crisis phase vs resolution phase behave differently."
        ),
    },
    {
        "id": "gold",
        "label": "Gold",
        "emoji": "🥇",
        "claim": (
            "Gold posts align with modest safe-haven drift: +0.41% avg 1-week, +1.12% avg 1-month "
            "across 94 event-days."
        ),
        "investor": (
            "Gold historically showed steadier (smaller) moves than equities after Trump posts — "
            "a diversifier rather than a momentum trade."
        ),
    },
]


def clean_records(df: pd.DataFrame) -> list[dict]:
    out = df.to_dict(orient="records")
    for r in out:
        for k, v in list(r.items()):
            if isinstance(v, float) and math.isnan(v):
                r[k] = None
            elif hasattr(v, "isoformat"):
                r[k] = str(v)[:10]
    return out


def load_data() -> dict:
    events = pd.read_csv(PBI / "all_events.csv")
    events["headline_text"] = events["headline_text"].astype(str).str.slice(0, 280)

    by_inst = {}
    for inst in [i["id"] for i in INSTRUMENTS]:
        p = PBI / "by_instrument" / f"{inst}_events.csv"
        if p.exists():
            df = pd.read_csv(p)
            df["headline_text"] = df["headline_text"].astype(str).str.slice(0, 280)
            by_inst[inst] = clean_records(df)

    market = pd.read_csv(ROOT / "data" / "processed" / "market_data.csv")
    market["date_only"] = pd.to_datetime(market["date_only"])
    market["month"] = market["date_only"].dt.to_period("M").dt.to_timestamp()
    monthly = (
        market.groupby(["instrument", "month"])["close"]
        .mean()
        .reset_index()
    )
    monthly["month"] = monthly["month"].dt.strftime("%Y-%m-%d")
    prices = {}
    for inst in [i["id"] for i in INSTRUMENTS]:
        sub = monthly[monthly["instrument"] == inst]
        prices[inst] = clean_records(sub)

    office = pd.read_csv(PBI / "in_office_comparison_by_instrument.csv")
    summary = pd.read_csv(PBI / "instrument_summary.csv")

    return {
        "instruments": INSTRUMENTS,
        "eventsByInstrument": by_inst,
        "pricesMonthly": prices,
        "officeCompare": clean_records(office),
        "summary": clean_records(summary),
        "meta": {
            "totalPosts": 73380,
            "totalEvents": int(len(events)),
        },
    }


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Trump Posts &amp; The Markets — Live Dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,600;0,9..40,700;1,9..40,400&display=swap" rel="stylesheet"/>
<style>
:root{
  --bg:#080c18;--panel:#111827;--panel2:#1a2235;--border:#243049;
  --text:#eef2ff;--muted:#8b9cc7;--accent:#5b8cff;--gold:#e8c547;
  --green:#3dd68c;--red:#ff6b6b;--nav-h:56px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'DM Sans',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.55}
nav{position:fixed;top:0;left:0;right:0;height:var(--nav-h);background:rgba(8,12,24,.92);
  backdrop-filter:blur(12px);border-bottom:1px solid var(--border);z-index:100;
  display:flex;align-items:center;padding:0 16px;gap:8px;overflow-x:auto}
nav .brand{font-weight:700;font-size:14px;white-space:nowrap;margin-right:12px;color:var(--gold)}
nav button{background:transparent;border:1px solid transparent;color:var(--muted);
  padding:8px 14px;border-radius:8px;cursor:pointer;font:inherit;font-size:13px;white-space:nowrap}
nav button:hover{color:var(--text);background:var(--panel2)}
nav button.active{color:var(--text);border-color:var(--accent);background:rgba(91,140,255,.12)}
main{padding-top:calc(var(--nav-h) + 24px);padding-bottom:60px;max-width:1200px;margin:0 auto;padding-left:20px;padding-right:20px}
.section{display:none;animation:fade .35s ease}
.section.active{display:block}
@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1}}
.hero{text-align:center;padding:48px 20px 32px}
.hero h1{font-size:clamp(1.6rem,4vw,2.4rem);font-weight:700;margin-bottom:12px}
.hero p{color:var(--muted);max-width:640px;margin:0 auto;font-size:1.05rem}
.claim{background:linear-gradient(135deg,rgba(232,197,71,.08),rgba(91,140,255,.06));
  border:1px solid rgba(232,197,71,.25);border-radius:14px;padding:20px 24px;margin:24px 0;
  font-size:1.05rem;line-height:1.65}
.claim strong{color:var(--gold);font-weight:600;display:block;margin-bottom:6px;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:20px 0}
.kpi{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center}
.kpi .n{font-size:1.5rem;font-weight:700;color:var(--accent)}
.kpi .l{font-size:.75rem;color:var(--muted);margin-top:4px;text-transform:uppercase;letter-spacing:.04em}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:20px 0}
@media(max-width:800px){.grid2{grid-template-columns:1fr}}
.card{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:16px;margin:16px 0}
.card h3{font-size:.85rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px}
.chart{min-height:320px}
.investor{background:var(--panel2);border-left:3px solid var(--gold);padding:16px 20px;border-radius:0 10px 10px 0;margin:20px 0;font-size:.95rem;color:var(--muted)}
.investor b{color:var(--gold)}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{padding:10px 8px;border-bottom:1px solid var(--border);text-align:left;vertical-align:top}
th{color:var(--muted);font-weight:600;cursor:pointer;user-select:none;position:sticky;top:0;background:var(--panel)}
td.num{text-align:right;font-variant-numeric:tabular-nums}
.pos{color:var(--green)}.neg{color:var(--red)}
.tag{display:inline-block;font-size:11px;padding:2px 8px;border-radius:20px;background:var(--panel2);color:var(--muted)}
.table-wrap{max-height:420px;overflow:auto;border-radius:10px;border:1px solid var(--border)}
.filters{display:flex;flex-wrap:wrap;gap:12px;margin:16px 0;align-items:center}
.filters label{font-size:12px;color:var(--muted)}
select,input{background:var(--panel2);border:1px solid var(--border);color:var(--text);
  padding:8px 12px;border-radius:8px;font:inherit}
.disclaimer{font-size:12px;color:var(--muted);border-top:1px solid var(--border);padding-top:20px;margin-top:40px}
footer{text-align:center;color:var(--muted);font-size:12px;padding:24px}
</style>
</head>
<body>
<nav id="nav"></nav>
<main id="main"></main>
<footer>Trump Market Event Study · Suhail Ahmed · Not financial advice</footer>
<script>
const DATA = /*DATA_JSON*/;

const fmtPct = v => v==null?'—':((v>=0?'+':'')+v.toFixed(2)+'%');
const fmtMoney = v => v==null?'—':('$'+Math.round(v).toLocaleString());
const cls = v => v==null?'':(v>=0?'pos':'neg');

function sumRow(inst, horizon){
  return DATA.summary.find(r=>r.instrument===inst && r.horizon===horizon)||{};
}

function officeRows(inst, horizon){
  return DATA.officeCompare.filter(r=>r.instrument===inst && r.horizon===horizon);
}

function renderNav(){
  const tabs = [{id:'cover',label:'Overview'}, ...DATA.instruments.map(i=>({id:i.id,label:i.emoji+' '+i.label})), {id:'calc',label:'💵 Calculator'}];
  document.getElementById('nav').innerHTML = '<span class="brand">Trump × Markets</span>' +
    tabs.map(t=>`<button data-tab="${t.id}" class="${t.id==='cover'?'active':''}">${t.label}</button>`).join('');
  document.querySelectorAll('nav button').forEach(b=>{
    b.onclick=()=>showTab(b.dataset.tab);
  });
}

function showTab(id){
  document.querySelectorAll('nav button').forEach(b=>b.classList.toggle('active', b.dataset.tab===id));
  document.querySelectorAll('.section').forEach(s=>s.classList.toggle('active', s.id===id));
  if(id!=='cover' && id!=='calc') setTimeout(()=>drawStockCharts(id), 50);
  if(id==='calc') setTimeout(renderCalc, 50);
}

function renderMain(){
  let html = `<section id="cover" class="section active">
    <div class="hero">
      <h1>When Trump Posts, Does The Market Move?</h1>
      <p>Live interactive event study · ${DATA.meta.totalPosts.toLocaleString()} posts · ${DATA.meta.totalEvents.toLocaleString()} market events · 2009–2025</p>
    </div>
    <div class="kpis">
      <div class="kpi"><div class="n">${DATA.meta.totalPosts.toLocaleString()}</div><div class="l">Posts analysed</div></div>
      <div class="kpi"><div class="n">${DATA.instruments.length}</div><div class="l">Markets tracked</div></div>
      <div class="kpi"><div class="n">5</div><div class="l">Story dashboards</div></div>
      <div class="kpi"><div class="n">Live</div><div class="l">No login required</div></div>
    </div>
    <div class="card"><h3>Pick a market in the nav bar</h3>
    <p style="color:var(--muted)">Each tab is a story: a plain-English claim, proof charts, every historical event, and president vs not-president comparison.</p></div>
    <p class="disclaimer">Historical associations only — not proof of causation. Not financial advice. Built with Python + event-study methodology.</p>
  </section>`;

  DATA.instruments.forEach(inst=>{
    const s1w = sumRow(inst.id,'1w');
    const s1m = sumRow(inst.id,'1m');
    html += `<section id="${inst.id}" class="section">
      <div class="claim"><strong>Claim — ${inst.label}</strong>${inst.claim}</div>
      <div class="kpis">
        <div class="kpi"><div class="n">${s1w.n_events||0}</div><div class="l">Events</div></div>
        <div class="kpi"><div class="n ${cls(s1w.mean_return_pct)}">${fmtPct(s1w.mean_return_pct)}</div><div class="l">Avg 1-week return</div></div>
        <div class="kpi"><div class="n ${cls(s1m.mean_return_pct)}">${fmtPct(s1m.mean_return_pct)}</div><div class="l">Avg 1-month return</div></div>
        <div class="kpi"><div class="n">${s1m.win_rate_pct||0}%</div><div class="l">1-month win rate</div></div>
      </div>
      <div class="grid2">
        <div class="card"><h3>In Office vs Not In Office (1 week)</h3><div id="chart-office-${inst.id}" class="chart"></div></div>
        <div class="card"><h3>${inst.label} price over time</h3><div id="chart-price-${inst.id}" class="chart"></div></div>
      </div>
      <div class="card"><h3>Every event — click column headers to sort</h3>
        <div class="filters">
          <label>Filter era <select id="era-${inst.id}"><option value="">All</option>
            <option>President — 1st Term (2017–2021)</option>
            <option>Not President (2021–2024)</option>
            <option>President — 2nd Term (2025+)</option>
            <option>Not President (Pre-2017)</option></select></label>
          <label>Office <select id="office-${inst.id}"><option value="">All</option><option>In Office</option><option>Not In Office</option></select></label>
        </div>
        <div class="table-wrap"><table id="tbl-${inst.id}"><thead><tr>
          <th data-k="event_date">Date</th><th data-k="presidency_era">Era</th><th data-k="in_office">Office</th>
          <th data-k="sentiment_label">Mood</th><th class="num" data-k="return_1w_pct">1wk</th><th class="num" data-k="return_1m_pct">1mo</th>
          <th class="num" data-k="value_1w">$100k→1wk</th><th data-k="headline_text">Post</th>
        </tr></thead><tbody></tbody></table></div>
      </div>
      <div class="investor"><b>Investor note:</b> ${inst.investor}</div>
    </section>`;
  });

  html += `<section id="calc" class="section">
    <div class="claim"><strong>Investor Calculator</strong>If you invested on every day Trump posted about a topic, then sold after the chosen period — what happened on average? (All events, no cherry-picking.)</div>
    <div class="filters">
      <label>Market <select id="c-inst">${DATA.instruments.map(i=>`<option value="${i.id}">${i.label}</option>`).join('')}</select></label>
      <label>Amount $<input id="c-amt" type="number" value="100000" min="1000" step="1000" style="width:120px"/></label>
      <label>Hold <select id="c-hor"><option value="1d">1 day</option><option value="1w" selected>1 week</option><option value="1m">1 month</option></select></label>
      <label>Office <select id="c-off"><option value="">All</option><option>In Office</option><option>Not In Office</option></select></label>
    </div>
    <div class="kpis">
      <div class="kpi"><div class="n" id="c-val">$0</div><div class="l">Avg ending value</div></div>
      <div class="kpi"><div class="n" id="c-ret">0%</div><div class="l">Avg return</div></div>
      <div class="kpi"><div class="n" id="c-win">0%</div><div class="l">Win rate</div></div>
      <div class="kpi"><div class="n" id="c-n">0</div><div class="l">Events</div></div>
    </div>
    <div class="card"><div id="chart-hist" class="chart"></div></div>
  </section>`;

  document.getElementById('main').innerHTML = html;

  DATA.instruments.forEach(inst=>{
    setupTable(inst.id);
    document.getElementById('era-'+inst.id).onchange = ()=>renderTable(inst.id);
    document.getElementById('office-'+inst.id).onchange = ()=>renderTable(inst.id);
  });
  ['c-inst','c-amt','c-hor','c-off'].forEach(id=>document.getElementById(id).oninput=renderCalc);
}

const sortState = {};
function setupTable(inst){
  sortState[inst] = {k:'event_date',d:-1};
  document.querySelectorAll('#tbl-'+inst+' th').forEach(th=>{
    th.onclick=()=>{
      const k=th.dataset.k;
      if(sortState[inst].k===k) sortState[inst].d*=-1; else {sortState[inst].k=k; sortState[inst].d=-1;}
      renderTable(inst);
    };
  });
  renderTable(inst);
}

function renderTable(inst){
  let rows = (DATA.eventsByInstrument[inst]||[]).slice();
  const era = document.getElementById('era-'+inst).value;
  const off = document.getElementById('office-'+inst).value;
  if(era) rows = rows.filter(r=>r.presidency_era===era);
  if(off) rows = rows.filter(r=>r.in_office===off);
  const {k,d} = sortState[inst];
  rows.sort((a,b)=>{
    let x=a[k], y=b[k];
    if(x==null) return 1; if(y==null) return -1;
    if(typeof x==='string') return d*x.localeCompare(y);
    return d*(x-y);
  });
  const tb = document.querySelector('#tbl-'+inst+' tbody');
  tb.innerHTML = rows.map(r=>{
    const c = (v)=>`<td class="num ${cls(v)}">${fmtPct(v)}</td>`;
    return `<tr><td>${r.event_date}</td><td style="font-size:11px;color:var(--muted)">${(r.presidency_era||'').replace('President — ','').slice(0,20)}</td>
      <td><span class="tag">${r.in_office||''}</span></td><td><span class="tag">${r.sentiment_label||''}</span></td>
      ${c(r.return_1w_pct)}${c(r.return_1m_pct)}<td class="num">${fmtMoney(r.value_1w)}</td>
      <td style="max-width:360px;font-size:12px;color:var(--muted)">${(r.headline_text||'').replace(/</g,'')}</td></tr>`;
  }).join('');
}

function drawStockCharts(inst){
  const off = officeRows(inst,'1w');
  const layout = {paper_bgcolor:'transparent',plot_bgcolor:'transparent',font:{color:'#8b9cc7',family:'DM Sans'},margin:{t:24,r:16,b:40,l:50},height:300};
  Plotly.newPlot('chart-office-'+inst, [{
    x: off.map(r=>r.in_office), y: off.map(r=>r.mean_return_pct), type:'bar',
    marker:{color:['#5b8cff','#e8c547']}, text: off.map(r=>fmtPct(r.mean_return_pct)), textposition:'outside'
  }], {...layout, yaxis:{title:'Avg 1-week return %', zeroline:true, zerolinecolor:'#243049'}}, {displayModeBar:false,responsive:true});

  const px = DATA.pricesMonthly[inst]||[];
  Plotly.newPlot('chart-price-'+inst, [{
    x: px.map(p=>p.month), y: px.map(p=>p.close), type:'scatter', mode:'lines', line:{color:'#5b8cff',width:2}
  }], {...layout, yaxis:{title:'Price (monthly avg)'}}, {displayModeBar:false,responsive:true});
}

function renderCalc(){
  const inst = document.getElementById('c-inst').value;
  const amt = +document.getElementById('c-amt').value||0;
  const hor = document.getElementById('c-hor').value;
  const off = document.getElementById('c-off').value;
  const rk = 'return_'+hor+'_pct';
  let rows = (DATA.eventsByInstrument[inst]||[]).filter(r=>r[rk]!=null);
  if(off) rows = rows.filter(r=>r.in_office===off);
  const rets = rows.map(r=>r[rk]);
  const n = rets.length;
  const mean = n?rets.reduce((a,b)=>a+b,0)/n:0;
  const win = n?rets.filter(r=>r>0).length/n*100:0;
  const valEl = document.getElementById('c-val');
  valEl.textContent = fmtMoney(amt*(1+mean/100));
  valEl.className = 'n '+cls(mean);
  const retEl = document.getElementById('c-ret');
  retEl.textContent = fmtPct(mean);
  retEl.className = 'n '+cls(mean);
  document.getElementById('c-win').textContent = win.toFixed(0)+'%';
  document.getElementById('c-n').textContent = n;
  Plotly.newPlot('chart-hist', [{x:rets,type:'histogram',marker:{color:'#5b8cff'},nbinsx:25}],
    {paper_bgcolor:'transparent',plot_bgcolor:'transparent',font:{color:'#8b9cc7'},margin:{t:10,r:10,b:40,l:40},height:280,
     xaxis:{title:'Return %'},yaxis:{title:'# events'}} , {displayModeBar:false,responsive:true});
}

renderNav();
renderMain();
</script>
</body>
</html>"""


def main() -> None:
    print("=" * 60)
    print("STEP 11: BUILDING LIVE WEB DASHBOARD")
    print("=" * 60)
    data = load_data()
    blob = json.dumps(data, ensure_ascii=False)
    html = HTML.replace("/*DATA_JSON*/", blob)

    DOCS.mkdir(parents=True, exist_ok=True)
    DASH.mkdir(parents=True, exist_ok=True)
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    (DASH / "index.html").write_text(html, encoding="utf-8")

    size_mb = len(html.encode("utf-8")) / 1024 / 1024
    print(f"Written docs/index.html ({size_mb:.1f} MB)")
    print(f"Written dashboard/index.html")
    print("\nLIVE URL (after GitHub Pages setup):")
    print("  https://YOUR_USERNAME.github.io/Trump-Market/")
    print("\nLocal preview: open docs/index.html in your browser")
    print("=" * 60)


if __name__ == "__main__":
    main()
