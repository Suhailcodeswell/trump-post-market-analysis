/**
 * Trump Post Market Analysis.
 * Two-screen layout: hero, then a horizontal tab deck.
 * Tabs slide left/right; swipe, arrow keys, and edge arrows all work.
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

const TAB_ORDER = ["story", "bitcoin", "oil", "sp500", "nasdaq", "invest", "about"];
const TRANSITION_OUT_MS = 220;

let events = [];
let summary = [];
let activeHorizon = "1w";
let switching = false;

async function init() {
  applyContactLinks();
  setupTabs();
  setupReveals();
  setupSnap();
  setupSwipe();
  setupKeyboard();
  updateArrows();

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
    github: ["hero-github", "about-github", "footer-github"],
  };
  Object.entries(map).forEach(([key, ids]) => {
    ids.forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.href = CONTACT[key];
    });
  });
}

/* ── Snap scroll between hero and deck ── */

let autoScrolling = false;

function animateScrollTo(targetY, duration = 1200) {
  const wrap = document.getElementById("snap-wrap");
  const startY = wrap.scrollTop;
  const delta = targetY - startY;
  if (Math.abs(delta) < 2) return;

  autoScrolling = true;
  // Snap would correct intermediate positions mid-animation; pause it.
  wrap.style.scrollSnapType = "none";
  const startTime = performance.now();
  const easeInOutCubic = (t) =>
    t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

  function frame(now) {
    const progress = Math.min(1, (now - startTime) / duration);
    wrap.scrollTop = startY + delta * easeInOutCubic(progress);
    if (progress < 1) {
      requestAnimationFrame(frame);
    } else {
      wrap.style.scrollSnapType = "";
      autoScrolling = false;
    }
  }
  requestAnimationFrame(frame);
}

function isMobileSnap() {
  return window.matchMedia("(max-width: 768px)").matches;
}

function scrollToDeck() {
  const duration = isMobileSnap() ? 1400 : 1200;
  animateScrollTo(document.getElementById("deck").offsetTop, duration);
}

function scrollToTop() {
  const duration = isMobileSnap() ? 1400 : 1200;
  animateScrollTo(0, duration);
}

function setupSnap() {
  const wrap = document.getElementById("snap-wrap");
  const deck = document.getElementById("deck");

  document.getElementById("scroll-cue").addEventListener("click", scrollToDeck);
  document.getElementById("brand-link").addEventListener("click", (e) => {
    e.preventDefault();
    scrollToTop();
  });

  // Laptop: eased transition on wheel between hero and deck.
  wrap.addEventListener(
    "wheel",
    (e) => {
      if (autoScrolling) {
        e.preventDefault();
        return;
      }
      const onHero = wrap.scrollTop < deck.offsetTop * 0.5;
      if (onHero && e.deltaY > 8) {
        e.preventDefault();
        scrollToDeck();
      } else if (!onHero && e.deltaY < -8) {
        const panel = document.querySelector(".panel.active");
        if (panel && panel.scrollTop <= 0) {
          e.preventDefault();
          scrollToTop();
        }
      }
    },
    { passive: false }
  );

  // Phone: native snap feels instant — intercept vertical swipes on the outer wrap.
  let touchStartY = 0;
  let touchStartX = 0;
  let touchActive = false;

  wrap.addEventListener(
    "touchstart",
    (e) => {
      if (!isMobileSnap() || e.touches.length !== 1) return;
      touchStartY = e.touches[0].clientY;
      touchStartX = e.touches[0].clientX;
      touchActive = true;
    },
    { passive: true }
  );

  wrap.addEventListener(
    "touchmove",
    (e) => {
      if (!isMobileSnap() || !touchActive || autoScrolling) return;
      const dy = e.touches[0].clientY - touchStartY;
      const dx = e.touches[0].clientX - touchStartX;
      if (Math.abs(dx) > Math.abs(dy)) return;

      const onHero = wrap.scrollTop < deck.offsetTop * 0.5;
      if (onHero && dy < -8) {
        e.preventDefault();
      } else if (!onHero && dy > 8) {
        const panel = document.querySelector(".panel.active");
        if (panel && panel.scrollTop <= 0) {
          e.preventDefault();
        }
      }
    },
    { passive: false }
  );

  wrap.addEventListener(
    "touchend",
    (e) => {
      if (!isMobileSnap() || !touchActive || autoScrolling) return;
      touchActive = false;

      const dy = e.changedTouches[0].clientY - touchStartY;
      const dx = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(dy) < 50 || Math.abs(dx) > Math.abs(dy) * 1.2) return;

      const onHero = wrap.scrollTop < deck.offsetTop * 0.5;
      if (onHero && dy < 0) {
        scrollToDeck();
      } else if (!onHero && dy > 0) {
        const panel = document.querySelector(".panel.active");
        if (panel && panel.scrollTop <= 0) {
          scrollToTop();
        }
      }
    },
    { passive: true }
  );

  // At the top of a tab, pull down to return to the hero (phone only).
  document.querySelectorAll(".panel").forEach((panel) => {
    let panelTouchY = 0;

    panel.addEventListener(
      "touchstart",
      (e) => {
        if (!isMobileSnap() || e.touches.length !== 1) return;
        panelTouchY = e.touches[0].clientY;
      },
      { passive: true }
    );

    panel.addEventListener(
      "touchend",
      (e) => {
        if (!isMobileSnap() || autoScrolling) return;
        const dy = e.changedTouches[0].clientY - panelTouchY;
        if (dy > 55 && panel.scrollTop <= 8) {
          scrollToTop();
        }
      },
      { passive: true }
    );
  });
}

/* ── Tabs with directional slides ── */

function currentTabId() {
  const active = document.querySelector(".panel.active");
  return active ? active.id : TAB_ORDER[0];
}

function setupTabs() {
  document.querySelectorAll(".nav-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      scrollToDeck();
      switchTab(tab.dataset.tab);
    });
  });

  document.querySelectorAll("[data-tab-link]").forEach((el) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      scrollToDeck();
      switchTab(el.dataset.tabLink);
    });
  });

  document.getElementById("deck-prev").addEventListener("click", () => step(-1));
  document.getElementById("deck-next").addEventListener("click", () => step(1));

  const initial = location.hash.replace("#", "");
  if (initial && TAB_ORDER.includes(initial)) {
    showPanel(initial, null);
    requestAnimationFrame(() => {
      const wrap = document.getElementById("snap-wrap");
      wrap.scrollTop = document.getElementById("deck").offsetTop;
    });
  }
}

function step(direction) {
  const idx = TAB_ORDER.indexOf(currentTabId());
  const next = TAB_ORDER[idx + direction];
  if (next) switchTab(next);
}

function switchTab(id) {
  const current = currentTabId();
  if (switching || id === current || !TAB_ORDER.includes(id)) return;

  const goingRight = TAB_ORDER.indexOf(id) > TAB_ORDER.indexOf(current);
  switching = true;

  const container = document.getElementById("panels");
  container.classList.add(goingRight ? "leaving-left" : "leaving-right");

  setTimeout(() => {
    container.classList.remove("leaving-left", "leaving-right");
    showPanel(id, goingRight ? "from-right" : "from-left");
    switching = false;
  }, TRANSITION_OUT_MS);
}

function showPanel(id, slideClass) {
  document.querySelectorAll(".panel").forEach((p) => {
    p.classList.remove("active", "from-right", "from-left");
    if (p.id === id) {
      p.classList.add("active");
      if (slideClass) p.classList.add(slideClass);
      p.scrollTop = 0;
    }
  });
  document.querySelectorAll(".nav-tab").forEach((t) => {
    const isActive = t.dataset.tab === id;
    t.classList.toggle("active", isActive);
    t.setAttribute("aria-selected", String(isActive));
  });
  history.replaceState(null, "", `#${id}`);
  updateArrows();
  refreshReveals();
}

function updateArrows() {
  const idx = TAB_ORDER.indexOf(currentTabId());
  document.getElementById("deck-prev").toggleAttribute("disabled", idx <= 0);
  document
    .getElementById("deck-next")
    .toggleAttribute("disabled", idx >= TAB_ORDER.length - 1);
}

/* ── Swipe gestures ── */

function setupSwipe() {
  const panels = document.getElementById("panels");
  let startX = 0;
  let startY = 0;
  let tracking = false;

  panels.addEventListener(
    "touchstart",
    (e) => {
      if (e.touches.length !== 1) return;
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
      tracking = true;
    },
    { passive: true }
  );

  panels.addEventListener(
    "touchend",
    (e) => {
      if (!tracking) return;
      tracking = false;
      const dx = e.changedTouches[0].clientX - startX;
      const dy = e.changedTouches[0].clientY - startY;
      if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) {
        step(dx < 0 ? 1 : -1);
      }
    },
    { passive: true }
  );
}

/* ── Keyboard navigation ── */

function setupKeyboard() {
  document.addEventListener("keydown", (e) => {
    if (e.target.matches("input, select, textarea")) return;
    if (e.key === "ArrowRight") step(1);
    if (e.key === "ArrowLeft") step(-1);
  });
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
  const active = document.querySelector(".panel.active");
  if (!active) return;
  active.querySelectorAll(".reveal:not(.in)").forEach((el) => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight * 0.95) {
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
    void resultEl.offsetWidth;
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
