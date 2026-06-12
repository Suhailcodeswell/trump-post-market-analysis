/**
 * Trump Post Market Analysis — client-side interactivity
 */

const MARKET_LABELS = {
  bitcoin: "Bitcoin",
  oil: "Oil",
  sp500: "S&P 500",
  nasdaq: "Nasdaq",
};

let events = [];
let summary = [];
let activeHorizon = "1w";

async function init() {
  try {
    const [eventsRes, summaryRes] = await Promise.all([
      fetch("/data/events.json"),
      fetch("/data/summary.json"),
    ]);
    events = await eventsRes.json();
    summary = await summaryRes.json();
  } catch (e) {
    console.error("Failed to load data", e);
    return;
  }

  renderStats();
  setupNav();
  setupCalculator();
}

function renderStats() {
  const configs = [
    { id: "bitcoin-stats", instrument: "bitcoin", horizon: "1w" },
    { id: "oil-stats", instrument: "oil", horizon: "1w" },
    { id: "sp500-stats", instrument: "sp500", horizon: "1m" },
    { id: "nasdaq-stats", instrument: "nasdaq", horizon: "1m" },
  ];

  configs.forEach(({ id, instrument, horizon }) => {
    const el = document.getElementById(id);
    if (!el) return;
    const row = summary.find(
      (s) => s.instrument === instrument && s.horizon === horizon
    );
    if (!row) return;

    const sign = row.mean_return_pct >= 0 ? "+" : "";
    el.innerHTML = `
      <div class="stat-card">
        <div class="stat-value">${row.n_events}</div>
        <div class="stat-label">Events</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">${sign}${row.mean_return_pct.toFixed(1)}%</div>
        <div class="stat-label">Avg ${horizon === "1w" ? "1-week" : "1-month"} return</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">${row.win_rate_pct.toFixed(0)}%</div>
        <div class="stat-label">Win rate</div>
      </div>
    `;
  });
}

function setupNav() {
  const links = document.querySelectorAll(".nav-links a");
  const sections = [...links].map((a) =>
    document.querySelector(a.getAttribute("href"))
  );

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          links.forEach((link) => {
            link.classList.toggle(
              "active",
              link.getAttribute("href") === `#${entry.target.id}`
            );
          });
        }
      });
    },
    { rootMargin: "-40% 0px -55% 0px", threshold: 0 }
  );

  sections.forEach((sec) => sec && observer.observe(sec));
}

function setupCalculator() {
  const marketSelect = document.getElementById("calc-market");
  const eventSelect = document.getElementById("calc-event");
  const amountInput = document.getElementById("calc-amount");
  const horizonBtns = document.querySelectorAll(".horizon-btn");

  function populateEvents() {
    const market = marketSelect.value;
    const filtered = events.filter((e) => e.market === market);
    eventSelect.innerHTML = filtered
      .map(
        (e) =>
          `<option value="${e.id}">${e.date} — ${e.title}</option>`
      )
      .join("");
    if (filtered.length === 0) {
      eventSelect.innerHTML =
        '<option value="">No featured events for this market</option>';
    }
    updateResult();
  }

  function updateResult() {
    const resultEl = document.getElementById("calc-result");
    const market = marketSelect.value;
    const eventId = eventSelect.value;
    const amount = parseFloat(amountInput.value) || 100000;

    if (!eventId) {
      resultEl.innerHTML =
        '<p class="result-headline">No events available for this market</p>';
      return;
    }

    const ev = events.find((e) => e.id === eventId);
    if (!ev) return;

    const isWeek = activeHorizon === "1w";
    const returnPct = isWeek ? ev.return_1w_pct : ev.return_1m_pct;
    const baseValue = isWeek ? ev.value_1w : ev.value_1m;
    const finalValue = (amount / 100000) * baseValue;
    const profit = finalValue - amount;
    const sign = returnPct >= 0 ? "+" : "";
    const cls = returnPct >= 0 ? "positive" : "negative";

    resultEl.innerHTML = `
      <p class="result-headline">${MARKET_LABELS[market]} · ${ev.date}</p>
      <div class="result-numbers">
        <div>
          <div class="result-main ${cls}">${formatMoney(finalValue)}</div>
          <div class="result-detail">Portfolio value after ${isWeek ? "1 week" : "1 month"}</div>
        </div>
        <div>
          <div class="result-main ${cls}">${sign}${returnPct.toFixed(1)}%</div>
          <div class="result-detail">Return on ${formatMoney(amount)} invested on post day</div>
        </div>
        <div>
          <div class="result-main ${cls}">${profit >= 0 ? "+" : ""}${formatMoney(profit)}</div>
          <div class="result-detail">Gain / loss vs. entry</div>
        </div>
      </div>
      <blockquote class="event-quote">"${escapeHtml(ev.headline)}"</blockquote>
      <p class="result-detail" style="margin-top: 1rem;">
        Hypothetical back-test only. The post may not have caused this return.
        Other news and macro factors were active on ${ev.date}.
      </p>
    `;
  }

  marketSelect.addEventListener("change", populateEvents);
  eventSelect.addEventListener("change", updateResult);
  amountInput.addEventListener("input", updateResult);

  horizonBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      horizonBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      activeHorizon = btn.dataset.horizon;
      updateResult();
    });
  });

  populateEvents();
}

function formatMoney(n) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(n);
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

document.addEventListener("DOMContentLoaded", init);
