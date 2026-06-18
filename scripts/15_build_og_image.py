"""Build the Open Graph preview image (1200x630) for LinkedIn and social shares."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "website" / "public" / "assets"
OUT = ASSETS / "social-preview.jpg"
HERO = ASSETS / "trump-hero.webp"

W, H = 1200, 627
BG = (250, 249, 247)
ACCENT = (45, 90, 135)
TEXT = (22, 24, 29)
MUTED = (91, 96, 104)


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = Path("C:/Windows/Fonts") / name
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def paste_hero_faded(base: Image.Image) -> None:
    hero = Image.open(HERO).convert("RGBA")
    target_h = int(H * 1.05)
    scale = target_h / hero.height
    target_w = int(hero.width * scale)
    hero = hero.resize((target_w, target_h), Image.Resampling.LANCZOS)

    x = W - int(target_w * 0.72)
    y = (H - target_h) // 2 + 20

    # Fade hero into background on the left (same idea as the live site).
    fade = Image.new("L", (target_w, target_h), 255)
    fade_draw = ImageDraw.Draw(fade)
    for col in range(target_w):
        if col < target_w * 0.42:
            alpha = int(255 * (col / (target_w * 0.42)) * 0.95)
        else:
            alpha = 255
        fade_draw.line([(col, 0), (col, target_h)], fill=alpha)

    hero.putalpha(fade)
    base.paste(hero, (x, y), hero)

    # Soft wash over the text side.
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wash_draw = ImageDraw.Draw(wash)
    wash_draw.rectangle([0, 0, int(W * 0.62), H], fill=(250, 249, 247, 210))
    base.paste(wash, (0, 0), wash)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join(current + [word])
        if draw.textlength(trial, font=font) <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def main() -> None:
    if not HERO.exists():
        raise FileNotFoundError(f"Missing hero image: {HERO}")

    img = Image.new("RGB", (W, H), BG)
    paste_hero_faded(img)
    draw = ImageDraw.Draw(img)

    eyebrow_font = load_font("segoeui.ttf", 22)
    title_font = load_font("georgia.ttf", 54)
    lead_font = load_font("segoeui.ttf", 24)
    brand_font = load_font("segoeui.ttf", 20)

    margin = 72
    max_text = int(W * 0.52)

    draw.text((margin, 88), "AN EVENT STUDY · 73,380 POSTS", fill=ACCENT, font=eyebrow_font)

    title = "Does what Trump says affect financial markets?"
    y = 140
    for line in wrap_text(draw, title, title_font, max_text):
        draw.text((margin, y), line, fill=TEXT, font=title_font)
        y += 62

    lead = (
        "Bitcoin, oil, the S&P 500, and the Nasdaq. Measured after "
        "73,380 posts from 2009 to 2025."
    )
    y += 8
    for line in wrap_text(draw, lead, lead_font, max_text):
        draw.text((margin, y), line, fill=MUTED, font=lead_font)
        y += 34

    draw.text((margin, H - 56), "Suhail Ahmed · trump-post-market-analysis.vercel.app", fill=MUTED, font=brand_font)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "JPEG", quality=92, optimize=True)
    print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
