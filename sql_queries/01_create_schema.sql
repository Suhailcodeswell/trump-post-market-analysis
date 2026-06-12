-- ======================================================================
-- STAR SCHEMA — PostgreSQL DDL
-- Project: Trump Social Media & Market Correlation
-- ----------------------------------------------------------------------
-- A "star schema" has one central FACT table (the measurements) linked
-- to descriptive DIMENSION tables. This layout is the industry standard
-- for analytics / BI because it is simple to query and fast to slice.
--
--                 Dim_Date
--                    |
--   Dim_Platform -- Fact_Posts        Fact_Market -- Dim_Date
--
-- Run order: this file first (creates structure), then load data, then
-- 02_analysis_queries.sql to analyse.
-- ======================================================================

DROP TABLE IF EXISTS Fact_Posts;
DROP TABLE IF EXISTS Fact_Market;
DROP TABLE IF EXISTS Dim_Platform;
DROP TABLE IF EXISTS Dim_Date;

-- ----------------------------------------------------------------------
-- DIMENSION: Date  (one row per calendar day, with time attributes)
-- ----------------------------------------------------------------------
CREATE TABLE Dim_Date (
    date_key     DATE PRIMARY KEY,
    year         INT  NOT NULL,
    quarter      INT  NOT NULL,
    month        INT  NOT NULL,
    month_name   TEXT NOT NULL,
    day          INT  NOT NULL,
    day_of_week  TEXT NOT NULL,
    is_weekend   BOOLEAN NOT NULL
);

-- ----------------------------------------------------------------------
-- DIMENSION: Platform  (Twitter vs Truth Social)
-- ----------------------------------------------------------------------
CREATE TABLE Dim_Platform (
    platform_key  SERIAL PRIMARY KEY,
    platform_name TEXT UNIQUE NOT NULL
);

-- ----------------------------------------------------------------------
-- FACT: Posts  (one row per Trump post, with its sentiment + engagement)
-- ----------------------------------------------------------------------
CREATE TABLE Fact_Posts (
    post_id          BIGINT PRIMARY KEY,
    date_key         DATE NOT NULL REFERENCES Dim_Date(date_key),
    platform_key     INT  NOT NULL REFERENCES Dim_Platform(platform_key),
    sentiment_score  NUMERIC(6,4) NOT NULL,   -- -1.0000 .. +1.0000
    sentiment_label  TEXT NOT NULL,           -- positive / neutral / negative
    favorite_count   INT NOT NULL,
    repost_count     INT NOT NULL,
    engagement       INT NOT NULL,            -- favorite + repost
    word_count       INT,
    topic_bitcoin    BOOLEAN,
    topic_sp500      BOOLEAN,
    topic_nasdaq     BOOLEAN,
    topic_tariffs    BOOLEAN
);

-- ----------------------------------------------------------------------
-- FACT: Market  (one row per instrument per trading day)
-- (Acts as the "Dim_Market" price source described in the roadmap.)
-- ----------------------------------------------------------------------
CREATE TABLE Fact_Market (
    date_key       DATE NOT NULL REFERENCES Dim_Date(date_key),
    instrument     TEXT NOT NULL,             -- sp500, nasdaq, dow, vix, bitcoin
    close_price    NUMERIC(18,4),
    daily_return   NUMERIC(10,4),             -- % change vs previous trading day
    volatility_7d  NUMERIC(10,4),             -- 7-day rolling std of returns
    PRIMARY KEY (date_key, instrument)
);

-- Helpful indexes for the analytical queries.
CREATE INDEX idx_factposts_date     ON Fact_Posts(date_key);
CREATE INDEX idx_factmarket_instr   ON Fact_Market(instrument);
