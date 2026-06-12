-- ======================================================================
-- ANALYTICAL QUERIES
-- Project: Trump Social Media & Market Correlation
-- ----------------------------------------------------------------------
-- These queries demonstrate the core SQL skills for a BI Analyst role:
--   * Common Table Expressions (CTEs)
--   * Window functions (rolling averages, LAG)
--   * LEFT JOINs to handle non-trading days (markets closed weekends)
--   * Aggregations, GROUP BY, and the CORR() statistical aggregate
--
-- They are written to run on BOTH PostgreSQL and DuckDB.
-- ======================================================================


-- Q1 ------------------------------------------------------------------
-- Daily average sentiment with a 7-DAY ROLLING AVERAGE (window function).
-- Smooths the noisy day-to-day sentiment into a trend line.
WITH daily AS (
    SELECT
        date_key,
        AVG(sentiment_score) AS avg_sentiment,
        COUNT(*)             AS post_count
    FROM Fact_Posts
    GROUP BY date_key
)
SELECT
    date_key,
    ROUND(avg_sentiment, 4)                                   AS avg_sentiment,
    post_count,
    ROUND(AVG(avg_sentiment) OVER (
        ORDER BY date_key
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 4)                                                     AS sentiment_7day_rolling
FROM daily
ORDER BY date_key;


-- Q2 ------------------------------------------------------------------
-- LEFT JOIN daily sentiment onto S&P 500 TRADING DAYS only.
-- The LEFT JOIN keeps every trading day even if Trump did not post,
-- which is how we correctly handle non-posting / non-trading mismatches.
WITH daily AS (
    SELECT date_key, AVG(sentiment_score) AS avg_sentiment, COUNT(*) AS post_count
    FROM Fact_Posts
    GROUP BY date_key
)
SELECT
    m.date_key,
    m.close_price,
    m.daily_return,
    m.volatility_7d,
    d.avg_sentiment,
    d.post_count
FROM Fact_Market m
LEFT JOIN daily d ON d.date_key = m.date_key
WHERE m.instrument = 'sp500'
ORDER BY m.date_key;


-- Q3 ------------------------------------------------------------------
-- CORRELATION between daily sentiment and same-day S&P 500 return,
-- using the built-in CORR() statistical aggregate.
WITH daily AS (
    SELECT date_key, AVG(sentiment_score) AS avg_sentiment
    FROM Fact_Posts
    GROUP BY date_key
)
SELECT
    ROUND(CORR(d.avg_sentiment, m.daily_return)::numeric, 4)  AS corr_sentiment_return,
    ROUND(CORR(d.avg_sentiment, m.volatility_7d)::numeric, 4) AS corr_sentiment_volatility,
    COUNT(*)                                                  AS n_days
FROM Fact_Market m
JOIN daily d ON d.date_key = m.date_key
WHERE m.instrument = 'sp500';


-- Q4 ------------------------------------------------------------------
-- Platform comparison: average sentiment + post volume, Twitter vs Truth Social.
SELECT
    p.platform_name,
    COUNT(*)                          AS total_posts,
    ROUND(AVG(f.sentiment_score), 4)  AS avg_sentiment,
    ROUND(AVG(f.engagement), 1)       AS avg_engagement
FROM Fact_Posts f
JOIN Dim_Platform p ON p.platform_key = f.platform_key
GROUP BY p.platform_name
ORDER BY total_posts DESC;


-- Q5 ------------------------------------------------------------------
-- EVENT STUDY in pure SQL: for each Bitcoin post-day, use LAG/lead-style
-- window logic to compare Bitcoin's price ~1 week later.
-- (Bitcoin trades every day, so a 7-row shift ~ 1 week.)
WITH btc AS (
    SELECT
        date_key,
        close_price,
        LEAD(close_price, 7) OVER (ORDER BY date_key) AS price_1w_later
    FROM Fact_Market
    WHERE instrument = 'bitcoin'
),
btc_events AS (
    SELECT DISTINCT date_key
    FROM Fact_Posts
    WHERE topic_bitcoin = TRUE
)
SELECT
    e.date_key                                              AS event_date,
    b.close_price                                           AS buy_price,
    b.price_1w_later                                        AS price_1w_later,
    ROUND(((b.price_1w_later / b.close_price) - 1) * 100, 2) AS return_1w_pct
FROM btc_events e
JOIN btc b ON b.date_key = e.date_key
WHERE b.price_1w_later IS NOT NULL
ORDER BY e.date_key;
