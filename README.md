# Presidential Posts and Financial Markets

Event study on whether presidential social media posts are associated with forward market returns. Cleaned 90,343 posts down to 73,380 (2009-2025), scored sentiment, tagged topics, and measured outcomes for Bitcoin, oil, the S&P 500, and Nasdaq.

**Live site:** [trump-post-market-analysis.vercel.app](https://trump-post-market-analysis.vercel.app)

## Question

When posts mention a market topic, what happens to that market over the next day, week, and month?

This is an association study, not proof of causation, and not financial advice.

## Pipeline

1. `scripts/01_clean_data.py`: clean posts
2. `scripts/02_sentiment_vader.py`: VADER sentiment before joining market data
3. `scripts/03_market_data.py`: daily prices and returns (Yahoo Finance)
4. `scripts/05_topic_tagging.py`: topic tags
5. `scripts/06_event_study.py`: forward returns and investment calculator
6. `scripts/07_build_sql_db.py`: PostgreSQL/DuckDB star schema
7. `scripts/08_build_dashboard.py`: dashboard build

## Selected results

Average outcome of $100,000 invested on each event:

| Topic | 1 week | 1 month | 1-month win rate | Events |
| --- | ---: | ---: | ---: | ---: |
| Bitcoin | -2.0% | +1.4% | 44% | 25 |
| S&P 500 | +0.3% | +1.1% | 71% | ~378 |
| Nasdaq | +0.3% | +2.7% | 79% | 68 |
| Tariffs / China | +0.3% | +1.5% | 71% | ~1,113 |

Equities often drifted up in the month after topic-tagged posts. Bitcoin tended to dip in the following week before recovering. Daily aggregate sentiment alone showed little correlation with returns.

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python scripts/01_clean_data.py
python scripts/02_sentiment_vader.py
python scripts/03_market_data.py
python scripts/05_topic_tagging.py
python scripts/06_event_study.py
python scripts/07_build_sql_db.py
python scripts/08_build_dashboard.py
```

## Structure

```
data/raw/          Original posts
data/processed/    Cleaned and scored outputs
scripts/           Pipeline (run in order)
sql_queries/       Star-schema SQL
output/            Charts and study outputs
dashboard/         Local dashboard
website/public/    Vercel site
```

## Stack

Python (pandas, vaderSentiment, yfinance, scipy, matplotlib), SQL (PostgreSQL / DuckDB), HTML/CSS/JS

## License

All Rights Reserved. See [LICENSE](LICENSE).
