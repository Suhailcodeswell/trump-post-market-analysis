"""
STEP 8 — BUILD THE INTERACTIVE WEB DASHBOARD
======================================================================
What this script does, in plain English:
  Reads our analysis outputs (events_detail.csv, event_study_summary.csv,
  daily_merged.csv) and generates a single self-contained web page,
  dashboard/index.html, that includes:
    * KPI cards (posts analysed, events, topics)
    * THE INVESTOR CALCULATOR: pick a topic, an amount, and a holding
      period, and see the average outcome + a distribution chart.
    * An event-study overview chart (avg return by topic & horizon).
    * A sentiment-vs-S&P 500 timeline.
    * A recent-events table per topic.

  The page uses Plotly (via CDN) for charts and plain JavaScript for the
  calculator. The data is embedded directly in the file, so it works as
  a static page - perfect for GitHub Pages or Vercel, no server needed.

Output: dashboard/index.html
======================================================================
"""

from pathlib import Path
import json
import math
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "dashboard"
EVENTS = PROJECT_ROOT / "output" / "events_detail.csv"
SUMMARY = PROJECT_ROOT / "output" / "event_study_summary.csv"
DAILY = PROJECT_ROOT / "data" / "processed" / "daily_merged.csv"

TOPIC_LABELS = {
    "bitcoin": "Bitcoin",
    "sp500": "S&P 500",
    "nasdaq": "Nasdaq",
    "tariffs_china": "Tariffs / China",
}


def clean_records(df: pd.DataFrame) -> list[dict]:
    """Convert a dataframe to JSON-safe records (NaN -> None)."""
    records = df.to_dict(orient="records")
    for r in records:
        for k, v in r.items():
            if isinstance(v, float) and math.isnan(v):
                r[k] = None
    return records


def main() -> None:
    print("=" * 60)
    print("STEP 8: BUILDING THE INTERACTIVE WEB DASHBOARD")
    print("=" * 60)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    events = pd.read_csv(EVENTS)
    events["headline_text"] = events["headline_text"].astype(str).str.slice(0, 160)
    keep = [
        "topic", "instrument", "event_date", "avg_sentiment", "sentiment_label",
        "return_1d_pct", "return_1w_pct", "return_1m_pct",
        "value_1d", "value_1w", "value_1m", "headline_text",
    ]
    events = events[keep]

    summary = pd.read_csv(SUMMARY)

    # Monthly sentiment vs S&P for the timeline chart
    daily = pd.read_csv(DAILY)
    daily["date_only"] = pd.to_datetime(daily["date_only"])
    daily["month"] = daily["date_only"].dt.to_period("M").dt.to_timestamp()
    monthly = (
        daily.groupby("month")
        .agg(avg_sentiment=("avg_sentiment", "mean"), close=("close", "mean"))
        .reset_index()
    )
    monthly["month"] = monthly["month"].dt.strftime("%Y-%m-%d")

    data_blob = {
        "events": clean_records(events),
        "summary": clean_records(summary),
        "monthly": clean_records(monthly),
        "topicLabels": TOPIC_LABELS,
        "totalPosts": 73380,
        "totalEvents": int(len(events)),
    }

    html = HTML_TEMPLATE.replace("/*DATA_PLACEHOLDER*/", json.dumps(data_blob))
    (OUT_DIR / "index.html").write_text(html, encoding="utf-8")

    print(f"Embedded {len(events):,} events and {len(summary)} summary rows.")
    print(f"Saved dashboard to: {OUT_DIR / 'index.html'}")
    print("Open it in a browser, or deploy the 'dashboard/' folder to GitHub Pages / Vercel.")
    print("=" * 60)


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Trump Posts &amp; The Markets — Event Study</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
  :root {
    --bg:#0b1020; --panel:#141b32; --panel2:#1b2444; --text:#e8ecf5;
    --muted:#94a0bd; --accent:#4f8cff; --green:#2ecc71; --red:#ff5a5a;
    --border:#26304f;
  }
  *{box-sizing:border-box}
  body{margin:0;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;
       background:var(--bg);color:var(--text);line-height:1.5}
  header{padding:48px 24px 28px;text-align:center;
         background:radial-gradient(900px 300px at 50% -50%,#1d2c5a 0,transparent 70%)}
  header h1{margin:0;font-size:34px;letter-spacing:.3px}
  header p{margin:10px auto 0;max-width:760px;color:var(--muted);font-size:16px}
  .wrap{max-width:1100px;margin:0 auto;padding:0 20px 60px}
  .kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:26px 0}
  .kpi{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:18px;text-align:center}
  .kpi .num{font-size:26px;font-weight:700;color:var(--accent)}
  .kpi .lbl{color:var(--muted);font-size:13px;margin-top:4px}
  .card{background:var(--panel);border:1px solid var(--border);border-radius:16px;
        padding:24px;margin:22px 0}
  .card h2{margin:0 0 6px;font-size:21px}
  .card .sub{color:var(--muted);font-size:14px;margin-bottom:18px}
  .controls{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end;margin-bottom:18px}
  .control{display:flex;flex-direction:column;gap:6px}
  .control label{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px}
  select,input{background:var(--panel2);color:var(--text);border:1px solid var(--border);
        border-radius:10px;padding:10px 12px;font-size:15px;min-width:150px}
  .result{display:grid;grid-template-columns:1.1fr 1fr;gap:20px;align-items:center}
  .bigval{font-size:44px;font-weight:800;margin:4px 0}
  .pos{color:var(--green)} .neg{color:var(--red)}
  .metarow{display:flex;gap:26px;flex-wrap:wrap;margin-top:10px;color:var(--muted);font-size:14px}
  .metarow b{color:var(--text)}
  table{width:100%;border-collapse:collapse;font-size:13.5px}
  th,td{padding:9px 10px;border-bottom:1px solid var(--border);text-align:left}
  th{color:var(--muted);font-weight:600;cursor:pointer;user-select:none}
  td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
  .tag{font-size:11px;padding:2px 8px;border-radius:20px;background:var(--panel2);color:var(--muted)}
  .disclaimer{color:var(--muted);font-size:13px;border-left:3px solid var(--accent);padding:8px 14px;background:#0f1730;border-radius:6px}
  footer{text-align:center;color:var(--muted);font-size:13px;padding:30px}
  @media(max-width:760px){.kpis{grid-template-columns:repeat(2,1fr)}.result{grid-template-columns:1fr}}
</style>
</head>
<body>
<header>
  <h1>When Trump Posts, Does The Market Move?</h1>
  <p>An event study of 16 years of Donald Trump's social media posts (2009&ndash;2025),
     measuring what the market did <em>after</em> he posted about Bitcoin, the S&amp;P 500,
     Nasdaq, and tariffs/China &mdash; plus an interactive "what if I'd invested" calculator.</p>
</header>

<div class="wrap">
  <div class="kpis" id="kpis"></div>

  <!-- INVESTOR CALCULATOR -->
  <div class="card">
    <h2>💵 Investor Calculator</h2>
    <div class="sub">If you had invested on <em>every</em> day Trump posted about a topic, then sold after the chosen period &mdash; what happened on average? (All events, no cherry-picking.)</div>
    <div class="controls">
      <div class="control">
        <label>Topic</label>
        <select id="c_topic"></select>
      </div>
      <div class="control">
        <label>Amount invested ($)</label>
        <input id="c_amount" type="number" value="100000" min="1" step="1000" />
      </div>
      <div class="control">
        <label>Hold for</label>
        <select id="c_horizon">
          <option value="1d">1 day</option>
          <option value="1w" selected>1 week</option>
          <option value="1m">1 month</option>
        </select>
      </div>
      <div class="control">
        <label>Only posts that were</label>
        <select id="c_sentiment">
          <option value="all" selected>Any sentiment</option>
          <option value="positive">Positive</option>
          <option value="negative">Negative</option>
        </select>
      </div>
    </div>
    <div class="result">
      <div>
        <div style="color:var(--muted);font-size:14px">Average ending value</div>
        <div class="bigval" id="c_value">$0</div>
        <div class="metarow">
          <span>Avg return: <b id="c_return">0%</b></span>
          <span>Win rate: <b id="c_winrate">0%</b></span>
          <span>Events: <b id="c_n">0</b></span>
          <span>Best: <b id="c_best">0%</b></span>
          <span>Worst: <b id="c_worst">0%</b></span>
        </div>
      </div>
      <div id="c_hist" style="height:260px"></div>
    </div>
  </div>

  <!-- EVENT STUDY OVERVIEW -->
  <div class="card">
    <h2>📊 Average Market Return After a Post</h2>
    <div class="sub">Mean forward return by topic and holding period.</div>
    <div id="overviewChart" style="height:420px"></div>
  </div>

  <!-- TIMELINE -->
  <div class="card">
    <h2>📈 Sentiment vs S&amp;P 500 Over Time</h2>
    <div class="sub">Monthly average post sentiment (red) against the S&amp;P 500 price (blue).</div>
    <div id="timelineChart" style="height:420px"></div>
  </div>

  <!-- EVENTS TABLE -->
  <div class="card">
    <h2>🗓️ Event Explorer</h2>
    <div class="sub">Individual posting-day events for the selected topic. Click a column header to sort.</div>
    <div class="controls">
      <div class="control">
        <label>Topic</label>
        <select id="t_topic"></select>
      </div>
    </div>
    <div style="max-height:420px;overflow:auto">
      <table id="eventsTable">
        <thead><tr>
          <th data-k="event_date">Date</th>
          <th data-k="sentiment_label">Mood</th>
          <th class="num" data-k="avg_sentiment">Sentiment</th>
          <th class="num" data-k="return_1w_pct">1wk %</th>
          <th class="num" data-k="return_1m_pct">1mo %</th>
          <th data-k="headline_text">Headline post</th>
        </tr></thead>
        <tbody></tbody>
      </table>
    </div>
  </div>

  <div class="card">
    <h2>🔍 Methodology &amp; Honesty Note</h2>
    <p class="disclaimer">
      A market move after a post is an <b>association, not proof of causation</b> &mdash; other
      news, earnings, and macro events also move markets. Results use <b>all</b> matching events
      (no cherry-picking) and reflect the general market uptrend over 2009&ndash;2025. Sentiment is
      scored by VADER from the post text alone, <em>before</em> any market data is examined, to
      avoid bias. "Investing on every event" is an illustrative back-test, not financial advice.
    </p>
  </div>
</div>

<footer>Built by Suhail Ahmed · Data: 73,380 cleaned posts (2009&ndash;2025) · Markets via Yahoo Finance</footer>

<script>
const DATA = /*DATA_PLACEHOLDER*/;
const fmtMoney = v => '$' + Math.round(v).toLocaleString();
const cls = v => v >= 0 ? 'pos' : 'neg';

// ---- KPI cards ----
document.getElementById('kpis').innerHTML = [
  ['num', DATA.totalPosts.toLocaleString(), 'Posts analysed'],
  ['num', DATA.totalEvents.toLocaleString(), 'Market events'],
  ['num', Object.keys(DATA.topicLabels).length, 'Topics tracked'],
  ['num', '16 yrs', '2009 – 2025'],
].map(([c,n,l]) => `<div class="kpi"><div class="num">${n}</div><div class="lbl">${l}</div></div>`).join('');

// ---- Populate topic dropdowns ----
const topicOpts = Object.entries(DATA.topicLabels)
  .map(([k,v]) => `<option value="${k}">${v}</option>`).join('');
['c_topic','t_topic'].forEach(id => document.getElementById(id).innerHTML = topicOpts);

// ---- Investor calculator ----
function calc() {
  const topic = document.getElementById('c_topic').value;
  const amount = parseFloat(document.getElementById('c_amount').value) || 0;
  const horizon = document.getElementById('c_horizon').value;
  const sent = document.getElementById('c_sentiment').value;
  const retKey = 'return_' + horizon + '_pct';

  let rows = DATA.events.filter(e => e.topic === topic && e[retKey] !== null);
  if (sent !== 'all') rows = rows.filter(e => e.sentiment_label === sent);

  const returns = rows.map(e => e[retKey]);
  const n = returns.length;
  const mean = n ? returns.reduce((a,b)=>a+b,0)/n : 0;
  const win = n ? returns.filter(r=>r>0).length/n*100 : 0;
  const best = n ? Math.max(...returns) : 0;
  const worst = n ? Math.min(...returns) : 0;
  const endVal = amount * (1 + mean/100);

  const valEl = document.getElementById('c_value');
  valEl.textContent = fmtMoney(endVal);
  valEl.className = 'bigval ' + cls(mean);
  const setRet = (id,v,suffix='%') => {
    const el = document.getElementById(id);
    el.textContent = (v>=0?'+':'') + v.toFixed(2) + suffix;
    el.className = cls(v);
  };
  setRet('c_return', mean);
  document.getElementById('c_winrate').textContent = win.toFixed(0)+'%';
  document.getElementById('c_n').textContent = n;
  setRet('c_best', best);
  setRet('c_worst', worst);

  Plotly.newPlot('c_hist', [{
    x: returns, type:'histogram', marker:{color:'#4f8cff'}, nbinsx:25
  }], {
    margin:{t:10,r:10,b:36,l:40}, paper_bgcolor:'transparent', plot_bgcolor:'transparent',
    font:{color:'#94a0bd'}, xaxis:{title:'Return (%)',zeroline:true,zerolinecolor:'#26304f'},
    yaxis:{title:'# events'}, bargap:0.05
  }, {displayModeBar:false, responsive:true});
}
['c_topic','c_amount','c_horizon','c_sentiment'].forEach(id =>
  document.getElementById(id).addEventListener('input', calc));

// ---- Overview chart ----
function overviewChart() {
  const horizons = ['1d','1w','1m'];
  const colors = {'1d':'#4f8cff','1w':'#f5a623','1m':'#2ecc71'};
  const topics = Object.keys(DATA.topicLabels);
  const traces = horizons.map(h => ({
    x: topics.map(t => DATA.topicLabels[t]),
    y: topics.map(t => {
      const row = DATA.summary.find(s => s.topic===t && s.horizon===h);
      return row ? row.mean_return_pct : null;
    }),
    name: h==='1d'?'1 day':h==='1w'?'1 week':'1 month',
    type:'bar', marker:{color:colors[h]}
  }));
  Plotly.newPlot('overviewChart', traces, {
    barmode:'group', margin:{t:10,r:10,b:40,l:50}, paper_bgcolor:'transparent',
    plot_bgcolor:'transparent', font:{color:'#94a0bd'},
    yaxis:{title:'Avg forward return (%)', zeroline:true, zerolinecolor:'#26304f'},
    legend:{orientation:'h', y:1.12}
  }, {displayModeBar:false, responsive:true});
}

// ---- Timeline chart ----
function timelineChart() {
  const x = DATA.monthly.map(m => m.month);
  Plotly.newPlot('timelineChart', [
    {x, y:DATA.monthly.map(m=>m.close), name:'S&P 500', yaxis:'y', line:{color:'#4f8cff'}},
    {x, y:DATA.monthly.map(m=>m.avg_sentiment), name:'Sentiment', yaxis:'y2', line:{color:'#ff5a5a'}}
  ], {
    margin:{t:10,r:50,b:40,l:50}, paper_bgcolor:'transparent', plot_bgcolor:'transparent',
    font:{color:'#94a0bd'},
    yaxis:{title:'S&P 500'}, yaxis2:{title:'Sentiment', overlaying:'y', side:'right', zeroline:true},
    legend:{orientation:'h', y:1.12}
  }, {displayModeBar:false, responsive:true});
}

// ---- Events table ----
let sortKey='event_date', sortDir=-1;
function renderTable() {
  const topic = document.getElementById('t_topic').value;
  let rows = DATA.events.filter(e => e.topic===topic);
  rows.sort((a,b)=>{
    let x=a[sortKey], y=b[sortKey];
    if(x===null) return 1; if(y===null) return -1;
    if(typeof x==='string') return sortDir*x.localeCompare(y);
    return sortDir*(x-y);
  });
  const body = rows.slice(0,200).map(e=>{
    const r1w = e.return_1w_pct, r1m = e.return_1m_pct;
    const c = v => v===null?'<td class="num">—</td>':`<td class="num ${cls(v)}">${(v>=0?'+':'')+v.toFixed(2)}</td>`;
    return `<tr>
      <td>${e.event_date}</td>
      <td><span class="tag">${e.sentiment_label}</span></td>
      <td class="num">${e.avg_sentiment===null?'—':e.avg_sentiment.toFixed(2)}</td>
      ${c(r1w)}${c(r1m)}
      <td>${(e.headline_text||'').replace(/</g,'&lt;')}</td></tr>`;
  }).join('');
  document.querySelector('#eventsTable tbody').innerHTML = body;
}
document.querySelectorAll('#eventsTable th').forEach(th=>{
  th.addEventListener('click', ()=>{
    const k=th.dataset.k;
    if(k===sortKey) sortDir*=-1; else {sortKey=k; sortDir=-1;}
    renderTable();
  });
});
document.getElementById('t_topic').addEventListener('change', renderTable);

// ---- init ----
calc(); overviewChart(); timelineChart(); renderTable();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
