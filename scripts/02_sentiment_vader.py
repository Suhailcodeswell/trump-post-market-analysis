"""
STEP 2 — SENTIMENT SCORING (VADER)
======================================================================
What this script does, in plain English:
  1. Loads the cleaned posts from Step 1.
  2. Runs each post's text through VADER, a sentiment engine.
  3. Adds a 'sentiment_score' column from -1.0 (very negative) to
     +1.0 (very positive), plus a simple 'sentiment_label'.
  4. Saves the scored file to data/processed/posts_scored.csv
  5. Prints a summary (averages, distribution, a few examples).

Why VADER:
  VADER (Valence Aware Dictionary and sEntiment Reasoner) is a rule-based
  engine built for social media. It understands capitals ("GREAT"),
  punctuation ("!!!"), and negation ("not good"). It is fast and needs
  no large model download. The single most useful number it returns is
  the 'compound' score, already scaled to -1.0 .. +1.0 -> we use that
  directly as our sentiment_score.
======================================================================
"""

from pathlib import Path
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

PROJECT_ROOT = Path(__file__).resolve().parents[1]
IN_FILE = PROJECT_ROOT / "data" / "processed" / "posts_clean.csv"
OUT_FILE = PROJECT_ROOT / "data" / "processed" / "posts_scored.csv"


def label_from_score(score: float) -> str:
    """Standard VADER thresholds for turning a number into a word."""
    if score >= 0.05:
        return "positive"
    if score <= -0.05:
        return "negative"
    return "neutral"


def main() -> None:
    print("=" * 60)
    print("STEP 2: SCORING SENTIMENT WITH VADER")
    print("=" * 60)

    df = pd.read_csv(IN_FILE, low_memory=False)
    print(f"Loaded clean file: {len(df):,} posts")

    analyzer = SentimentIntensityAnalyzer()

    # The 'compound' score is VADER's overall -1..+1 sentiment for the text.
    print("Scoring posts... (this runs through every post's text)")
    scores = df["text"].astype(str).apply(lambda t: analyzer.polarity_scores(t)["compound"])
    df["sentiment_score"] = scores.round(4)
    df["sentiment_label"] = df["sentiment_score"].apply(label_from_score)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_FILE, index=False)

    # ---- Report -------------------------------------------------------
    print(f"\nAverage sentiment (all posts): {df['sentiment_score'].mean():+.4f}")
    print("\nSentiment label breakdown:")
    counts = df["sentiment_label"].value_counts()
    for label in ["positive", "neutral", "negative"]:
        n = int(counts.get(label, 0))
        print(f"  - {label:<9}: {n:,}  ({n / len(df) * 100:.1f}%)")

    print("\nAverage sentiment by platform:")
    print(df.groupby("platform")["sentiment_score"].mean().round(4).to_string())

    print("\nMost POSITIVE example:")
    top = df.loc[df["sentiment_score"].idxmax()]
    print(f"  score {top['sentiment_score']:+.3f} | {str(top['text'])[:120]}...")

    print("\nMost NEGATIVE example:")
    bot = df.loc[df["sentiment_score"].idxmin()]
    print(f"  score {bot['sentiment_score']:+.3f} | {str(bot['text'])[:120]}...")

    print(f"\nSaved scored file to: {OUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
