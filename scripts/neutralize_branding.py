"""Neutralize public-facing Trump branding for bank-facing applications."""
from pathlib import Path

ROOT = Path(r"C:\Users\ABDUL SATHAR\OneDrive\Desktop\Trump-Market")
NEW_HOST = "https://political-sentiment-market-analysis.vercel.app"
OLD_HOST = "https://trump-post-market-analysis.vercel.app"
NEW_REPO = "https://github.com/Suhailcodeswell/political-sentiment-market-analysis"
OLD_REPO = "https://github.com/Suhailcodeswell/trump-post-market-analysis"

# Order matters for some replacements
REPLACEMENTS = [
    (OLD_HOST, NEW_HOST),
    (OLD_REPO, NEW_REPO),
    ("Trump Posts and Financial Markets", "Political Sentiment and Financial Markets"),
    ("Trump Posts &amp; Financial Markets", "Political Sentiment &amp; Financial Markets"),
    ("Trump Posts & Financial Markets", "Political Sentiment & Financial Markets"),
    ("Does what Trump says affect financial markets?", "Do political posts move financial markets?"),
    ("Do Donald Trump's social media posts move Bitcoin, oil, the S&P 500, and Nasdaq?", "Do high-profile political social posts move Bitcoin, oil, the S&P 500, and Nasdaq?"),
    ("Trump Posts &amp; Financial Markets: An Event Study", "Political Sentiment &amp; Financial Markets: An Event Study"),
    ("Trump &amp; Markets", "Sentiment &amp; Markets"),
    ("Trump Post Market Analysis", "Political Sentiment Market Analysis"),
    ('src="/assets/trump-hero.webp"', 'src="/assets/market-hero.png"'),
    ('data-photo="trump-portrait.jpg"', 'data-photo="charts/slide-10.png"'),
    ("Official presidential portrait of Donald Trump", "Nasdaq event-study chart from the Power BI report"),
    ("The subject. Official presidential portrait.", "A sample event-study chart from the analysis."),
    ("trump-post-market-analysis", "political-sentiment-market-analysis"),
]

# Longer narrative swaps (exact substrings from index.html)
NARRATIVE = [
    (
        """          One man, sixteen years of posts, and four markets that may or may not be
          listening. This project lines up 73,380 of Donald Trump's posts against Bitcoin,
          crude oil, the S&amp;P 500, and the Nasdaq, and measures what prices actually did
          in the day, week, and month after each one.""",
        """          Sixteen years of political communication, and four markets that may or may not
          be listening. This project lines up 73,380 cleaned political posts against Bitcoin,
          crude oil, the S&amp;P 500, and the Nasdaq, and measures what prices actually did
          in the day, week, and month after each one.""",
    ),
    (
        """                Traders set alerts for his posts. Newsrooms refresh his feed. For almost
                twenty years, Donald Trump has been able to type a sentence and watch
                markets twitch. Some of those sentences were about Bitcoin. Some threatened
                Iran. A few announced tariffs that knocked billions off the S&amp;P 500
                before lunch.""",
        """                Traders set alerts for market-moving political posts. Newsrooms refresh
                those feeds in real time. For almost twenty years, high-profile political
                communication has been able to move a sentence into a market reaction. Some
                posts were about Bitcoin. Some touched Iran and energy. A few announced
                tariffs that knocked billions off the S&amp;P 500 before lunch.""",
    ),
    (
        """                Bitcoin never met a quiet news cycle. The largest cryptocurrency trades around the
                clock, in every timezone, and it reacts to politics faster than any stock exchange
                can open. Trump's stance on it has flipped completely. In 2019 he said it was based
                on thin air. By 2024 he was promising a strategic crypto reserve and courting the
                Bitcoin conference vote.""",
        """                Bitcoin never met a quiet news cycle. The largest cryptocurrency trades around the
                clock, in every timezone, and it reacts to politics faster than any stock exchange
                can open. Public political messaging on crypto has flipped over time, from deep
                skepticism in 2019 to later pledges around strategic crypto reserves and industry
                outreach.""",
    ),
    (
        """                The dataset holds <strong>28 posting events</strong> where Trump talked about
                Bitcoin or crypto. The honest summary: he is a small factor. Halving cycles, ETF
                flows, and macro conditions set the direction. But a handful of individual posts
                sat right next to violent moves, and those deserve a close look.""",
        """                The dataset holds <strong>28 posting events</strong> tagged to Bitcoin or crypto.
                The honest summary: political messaging is a small factor. Halving cycles, ETF
                flows, and macro conditions set the direction. But a handful of individual posts
                sat right next to violent moves, and those deserve a close look.""",
    ),
    (
        """                <strong>October 31, 2024.</strong> Trump wished "our great Bitcoiners" a happy
                anniversary of the Satoshi white paper and promised to end the war on crypto. One
                month later, a $100k position was worth $137k. He posted into a rally that was
                already running, so take the credit assignment with a grain of salt. Still, +37%
                is +37%.""",
        """                <strong>October 31, 2024.</strong> A high-profile political post celebrated the
                Satoshi white paper anniversary and promised to end the war on crypto. One
                month later, a $100k position was worth $137k. The post landed into a rally that was
                already running, so take the credit assignment with a grain of salt. Still, +37%
                is +37%.""",
    ),
    (
        """                <strong>July 12, 2019.</strong> "I am not a fan of Bitcoin..." The price gave up
                almost 11% in a week. People still point at this tweet as proof that he moves
                crypto. Maybe. That summer was also full of regulatory bad news that had nothing
                to do with him.""",
        """                <strong>July 12, 2019.</strong> A sharply bearish political post on Bitcoin.
                The price gave up almost 11% in a week. People still point at this moment as proof
                that political messaging moves crypto. Maybe. That summer was also full of
                regulatory bad news that had nothing to do with any single post.""",
    ),
    (
        """                <strong>March 2, 2025.</strong> He announced a U.S. Crypto Reserve, which is about
                as bullish as presidential news gets. Bitcoin fell 14.5% over the following week
                anyway. The market had priced the policy long before the post landed. Good news on
                the timeline is not the same thing as good news to a trader.""",
        """                <strong>March 2, 2025.</strong> A U.S. Crypto Reserve announcement, about
                as bullish as presidential news gets. Bitcoin fell 14.5% over the following week
                anyway. The market had priced the policy long before the post landed. Good news on
                the timeline is not the same thing as good news to a trader.""",
    ),
    (
        """                Same 28 events, split by whether he held office at the time. The bars say the
                presidency is not a multiplier. What he says, and into what kind of market he says
                it, matters more than the title under the handle.""",
        """                Same 28 events, split by whether the poster held office at the time. The bars say
                the office alone is not a multiplier. What gets said, and into what kind of market
                it is said, matters more than the title under the handle.""",
    ),
    (
        """                Trump appears <strong>705 times</strong> in the Iran-and-energy slice of the
                dataset, and the average week after those posts is slightly negative. As a single
                factor he barely registers here. The June 2025 Iran standoff is the exception that
                makes this tab worth reading.""",
        """                Political posts appear <strong>705 times</strong> in the Iran-and-energy slice of the
                dataset, and the average week after those posts is slightly negative. As a single
                factor, messaging barely registers here. The June 2025 Iran standoff is the exception that
                makes this tab worth reading.""",
    ),
    (
        """                The S&amp;P 500 is the scoreboard for American business. Roughly 500 companies,
                most of the country's retirement money, and the number presidents point at when
                they want credit for the economy. Trump posts about it constantly. Tariffs, China,
                the Fed, his own stock-market scorekeeping: <strong>1,772 posting days</strong>
                in the study touch this index.""",
        """                The S&amp;P 500 is the scoreboard for American business. Roughly 500 companies,
                most of the country's retirement money, and the number political leaders point at when
                they want credit for the economy. Political posts reference it constantly. Tariffs, China,
                the Fed, market scorekeeping: <strong>1,772 posting days</strong>
                in the study touch this index.""",
    ),
    (
        """                The week after he posts, the index averages +0.3%. The month after, +1.5%. That
                sounds like a signal until you remember the index spent most of 2009 to 2025 going
                up no matter who was typing.""",
        """                The week after tagged posts, the index averages +0.3%. The month after, +1.5%. That
                sounds like a signal until you remember the index spent most of 2009 to 2025 going
                up no matter who was typing.""",
    ),
    (
        """                <strong>April 8, 2025.</strong> He shared an article about auto tariffs steering
                jobs back to the U.S., and the index rallied 8.3% over the next week. Did the post
                cause it, or did it just land at the bottom of a selloff that was due for a relief
                rally? The chart shows price on both sides of the date. Decide for yourself.""",
        """                <strong>April 8, 2025.</strong> A political post shared coverage of auto tariffs steering
                jobs back to the U.S., and the index rallied 8.3% over the next week. Did the post
                cause it, or did it just land at the bottom of a selloff that was due for a relief
                rally? The chart shows price on both sides of the date. Decide for yourself.""",
    ),
    (
        """                The Nasdaq is where the tech giants live, which makes it the natural target for
                Trump's posts about Big Tech, censorship, and Silicon Valley money. When he goes
                after Google or accuses platforms of rigging elections, this is the index that
                should flinch.""",
        """                The Nasdaq is where the tech giants live, which makes it the natural target for
                political posts about Big Tech, censorship, and Silicon Valley money. When public
                messaging targets platforms or election integrity debates, this is the index that
                should flinch.""",
    ),
    (
        """                <strong>74 tagged events.</strong> A 79% one-month win rate, the best of any
                market in the study, averaging +3.0%. Before anyone builds a strategy on that
                number: tech beat nearly everything for fifteen straight years. He was posting
                into the strongest tailwind in modern markets.""",
        """                <strong>74 tagged events.</strong> A 79% one-month win rate, the best of any
                market in the study, averaging +3.0%. Before anyone builds a strategy on that
                number: tech beat nearly everything for fifteen straight years. Many of these posts
                landed into the strongest tailwind in modern markets.""",
    ),
    (
        """              <li><strong>Posts:</strong> 90,343 raw records cleaned down to 73,380 (2009 to 2025). Deleted posts, pure reposts, and empty text were removed so the analysis covers only what Trump actually wrote.</li>""",
        """              <li><strong>Posts:</strong> 90,343 raw records cleaned down to 73,380 (2009 to 2025). Deleted posts, pure reposts, and empty text were removed so the analysis covers only substantive political communication.</li>""",
    ),
]

ARIA = [
    ("Bitcoin chart around October 31 2024 Trump post", "Bitcoin chart around October 31 2024 political post"),
    ("Bitcoin chart around July 12 2019 anti-crypto Trump post", "Bitcoin chart around July 12 2019 bearish crypto post"),
    ("Bar chart comparing Bitcoin returns when Trump was in office versus not", "Bar chart comparing Bitcoin returns in-office versus not"),
    ("Column chart of oil one-week returns after Trump posts in June 2025", "Column chart of oil one-week returns after political posts in June 2025"),
    ("Nasdaq chart around November 2 2020 election eve Trump post", "Nasdaq chart around November 2 2020 election-eve political post"),
]


def process(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    original = text
    for a, b in NARRATIVE:
        text = text.replace(a, b)
    for a, b in REPLACEMENTS:
        text = text.replace(a, b)
    for a, b in ARIA:
        text = text.replace(a, b)
    # catch remaining common forms
    text = text.replace("Donald Trump", "a high-profile political figure")
    text = text.replace("Trump's", "political")
    text = text.replace("Trump ", "political messaging ")
    text = text.replace(" Trump", " political messaging")
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"updated: {path}")
    else:
        print(f"unchanged: {path}")


def main() -> None:
    targets = [
        ROOT / "website/public/index.html",
        ROOT / "website/public/linkedin-share.html",
        ROOT / "website/public/js/app.js",
        ROOT / "README.md",
    ]
    for t in targets:
        if t.exists():
            process(t)

    # Final sweep for leftover Trump tokens in public HTML/JS
    for path in [ROOT / "website/public/index.html", ROOT / "website/public/js/app.js", ROOT / "website/public/linkedin-share.html"]:
        text = path.read_text(encoding="utf-8")
        leftovers = []
        for token in ["Trump", "trump-hero", "trump-portrait", "Donald"]:
            if token in text:
                leftovers.append(token)
        print(f"{path.name} leftovers: {leftovers or 'none'}")


if __name__ == "__main__":
    main()
