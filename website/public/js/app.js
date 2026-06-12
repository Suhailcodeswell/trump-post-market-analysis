/**
 * Trump Post Market Analysis: tab navigation, scroll reveals,
 * and the featured-event investment calculator.
 */

const MARKET_LABELS = {
  bitcoin: "Bitcoin",
  oil: "Oil",
  sp500: "S&P 500",
  nasdaq: "Nasdaq",
};

// Update these three values once; every link on the site reads from here.
const CONTACT = {
  linkedin: "https://www.linkedin.com/in/suhail-ahmed-b75301232",
  email: "mailto:suhailahmedprof@gmail.com",
  github: "https://github.com/Suhailcodeswell/trump-post-market-analysis",
};

const TRANSITION_OUT_MS = 220;

let events = [];
let summary = [];
let activeHorizon = "1w";
let switching = false;

async function init() {
  applyContactLinks();
  setupTabs();
  setupReveals();

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
  setupCalculator();
}

function applyContactLinks() {
  const map = {
    linkedin: ["hero-linkedin", "about-linkedin", "footer-linkedin"],
    email: ["hero-email", "about-email", "footer-email"],
    github: ["hero-github", "about-github", "footer-github", "repo-link"],
  };
  Object.entries(map).forEach(([key, ids]) => {
    ids.forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.href = CONTACT[key];
    });
  });
}

/* ── Tabs ── */

function setupTabs() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => switchTab(tab.dataset.tab));
  });

  document.querySelectorAll("[data-tab-link]").forEach((el) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      switchTab(el.dataset.tabLink);
    });
  });

  const initial = location.hash.replace("#", "");
  if (initial && document.getElementById(initial)) {
    showPanel(initial);
  }
}

function switchTab(id) {
  const next = document.getElementById(id);
  const current = document.querySelector(".panel.active");
  if (!next || switching || next === current) return;

  switching = true;
  const container = document.getElementById("panels");
  container.classList.add("leaving");

  setTimeout(() => {
    container.classList.remove("leaving");
    showPanel(id);
    switching = false;
  }, TRANSITION_OUT_MS);
}

function showPanel(id) {
  document.querySelectorAll(".panel").forEach((p) => {
    p.classList.toggle("active", p.id === id);
  });
  document.querySelectorAll(".nav-tab").forEach((t) => {
    const isActive = t.dataset.tab === id;
    t.classList.toggle("active", isActive);
    t.setAttribute("aria-selected", String(isActive));
  });
  history.replaceState(null, "", `#${id}`);
  window.scrollTo({ top: 0, behavior: "instant" });
  refreshReveals();
}

/* ── Scroll reveals ── */

let revealObserver;

function setupReveals() {
  revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
  );

  document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));
}

function refreshReveals() {
  // Elements near the top of a freshly opened panel should appear immediately.
  const active = document.querySelector(".panel.active");
  if (!active) return;
  active.querySelectorAll(".reveal:not(.in)").forEach((el) => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight * 0.92) {
      el.classList.add("in");
      revealObserver.unobserve(el);
    }
  });
}

/* ── Stats ── */

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

/* ── Calculator ── */

function setupCalculator() {
  const marketSelect = document.getElementById("calc-market");
  const eventSelect = document.getElementById("calc-event");
  const amountInput = document.getElementById("calc-amount");
  const horizonBtns = document.querySelectorAll(".horizon-btn");

  function populateEvents() {
    const market = marketSelect.value;
    const filtered = events.filter((e) => e.market === market);
    eventSelect.innerHTML = filtered
      .map((e) => `<option value="${e.id}">${e.date} · ${e.title}</option>`)
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

    resultEl.classList.remove("refresh");
    void resultEl.offsetWidth; // restart the entrance animation
    resultEl.classList.add("refresh");
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
