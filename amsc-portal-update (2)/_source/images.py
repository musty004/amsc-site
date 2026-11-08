"""Image pipeline for the AMSC site.

Run once whenever you add or replace a photo:

    python3 images.py

Reads full-size originals from  _source/img-originals/
Writes web-ready files to       assets/img/
  - every photo and flyer as WebP at two or three widths (used by srcset)
  - clean logo files (transparent white mark, blue app icon, favicons)
  - og-image.jpg, the preview card shown when a link is shared on WhatsApp
  - _source/img-manifest.json, which build.py reads to write width/height/srcset

To add a new photo: drop the JPG into img-originals/, add a line to PHOTOS or
FLYERS below, run this script, then run build.py.
"""
import json, os, io
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "img-originals")
OUT = os.path.join(HERE, "..", "assets", "img")
FONTS = os.path.join(HERE, "fonts-src")

BLUE = (0, 86, 206)
YELLOW = (252, 186, 0)

# name: list of output widths (never upscaled)
PHOTOS = {
    "community-group":    [480, 800, 1200, 1600],
    "walimah-group":      [480, 800, 1080],   # FYB Sendforth Walimah group photos
    "orientation-2024-sisters":  [480, 800, 1200],   # Freshers' Orientation 2024/1446
    "orientation-2024-brothers": [480, 800, 1200],
    "orientation-2024-hall":     [480, 800, 1200],
    "orientation-2024-front":    [480, 800, 1200],
    "orientation-2025-sisters":  [480, 800, 1200],   # Freshers' Orientation 2025/1447
    "orientation-2025-brothers": [480, 800, 1200],
    "orientation-2025-hall":     [480, 800, 1200],
    "orientation-2025-speaker":  [480, 800],
    "musabaqah-finale":   [480, 800, 1200, 1600],     # 5th Annual Musabaqatul Qur'an
    "musabaqah-award":    [480, 800, 1200],
    "musabaqah-team":     [480, 800, 1200],
    "musabaqah-sisters":  [480, 800, 1200],
    "musabaqah-audience": [480, 800, 1200],
    "quiz-mosque":        [480, 800, 1200],
    "musabaqah-judges":   [480, 800, 1008],
    "football-team":      [480, 765],
}
FLYERS = [
    "flyer-aman", "flyer-askbox", "flyer-convocation", "flyer-freshers",
    "flyer-hijabday", "flyer-idit-graduation", "flyer-idit", "flyer-matriculation",
    "flyer-musabaqah", "flyer-pdfnest", "flyer-sendforth-agenda", "flyer-sendforth",
    "flyer-sisters-circle", "flyer-welfare-officers", "flyer-islamiyyah", "flyer-dues",
]
FLYER_WIDTHS = [480, 900]


def save_webp(im, path, q):
    im.save(path, "WEBP", quality=q, method=6)


def resize_set(name, widths, quality):
    src = Image.open(os.path.join(SRC, name + ".jpg")).convert("RGB")
    out = []
    for w in widths:
        w = min(w, src.width)
        h = round(src.height * w / src.width)
        im = src.resize((w, h), Image.LANCZOS)
        fn = f"{name}-{w}.webp"
        save_webp(im, os.path.join(OUT, fn), quality)
        out.append({"w": w, "h": h, "file": fn})
    # dedupe widths that collapsed to the source width
    seen, uniq = set(), []
    for o in out:
        if o["w"] not in seen:
            uniq.append(o); seen.add(o["w"])
    return {"ratio": src.height / src.width, "sizes": uniq}


def clean_mark():
    """The supplied logo files carry a dark strip and corners from a screenshot
    crop. Remove every dark opaque pixel, keep the white and gold mark."""
    im = Image.open(os.path.join(SRC, "logo-mark-white.png")).convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and max(r, g, b) < 90:
                px[x, y] = (255, 255, 255, 0)
            elif a and max(r, g, b) < 170 and abs(r - g) < 20 and abs(g - b) < 20:
                # grey anti-alias fringe against the old dark strip: fade it out
                px[x, y] = (255, 255, 255, int(a * (max(r, g, b) - 90) / 80))
    bbox = im.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
    im = im.crop(bbox)
    # square canvas with breathing room
    side = max(im.size)
    canvas = Image.new("RGBA", (side, side), (255, 255, 255, 0))
    canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2), im)
    return canvas


def rounded_icon(mark, size, radius_ratio=0.22, pad_ratio=0.16, bg=BLUE):
    scale = 4
    S = size * scale
    base = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * radius_ratio), fill=255)
    fill = Image.new("RGBA", (S, S), bg + (255,))
    base.paste(fill, (0, 0), mask)
    inner = int(S * (1 - 2 * pad_ratio))
    m = mark.resize((inner, inner), Image.LANCZOS)
    base.alpha_composite(m, ((S - inner) // 2, (S - inner) // 2))
    return base.resize((size, size), Image.LANCZOS)


def logos(manifest):
    mark = clean_mark()
    for s in (48, 96, 384):
        mark.resize((s, s), Image.LANCZOS).save(os.path.join(OUT, f"logo-mark-{s}.webp"), "WEBP", quality=90, method=6)
    for s in (40, 80):
        rounded_icon(mark, s).save(os.path.join(OUT, f"logo-icon-{s}.webp"), "WEBP", quality=90, method=6)
    rounded_icon(mark, 32, 0.2, 0.1).save(os.path.join(OUT, "favicon-32.png"), optimize=True)
    # full-bleed squares for home-screen icons (the OS applies its own mask)
    for s, name in ((180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")):
        rounded_icon(mark, s, 0, 0.18).save(os.path.join(OUT, name), optimize=True)
    manifest["logo-mark"] = {"ratio": 1}
    return mark


def woff2_to_ttf(path, weight=None):
    from fontTools.ttLib import TTFont
    f = TTFont(path)
    f.flavor = None
    if weight and "fvar" in f:
        from fontTools.varLib import instancer
        f = instancer.instantiateVariableFont(f, {"wght": weight})
    buf = io.BytesIO(); f.save(buf); buf.seek(0)
    return buf


def og_image(mark):
    """1200x630 preview card for link sharing."""
    W, H = 1200, 630
    photo = Image.open(os.path.join(SRC, "community-group.jpg")).convert("RGB")
    # cover-crop the photo into the right 46%
    pw = int(W * 0.38)
    ratio = max(pw / photo.width, H / photo.height)
    p = photo.resize((int(photo.width * ratio), int(photo.height * ratio)), Image.LANCZOS)
    left = max(0, (p.width - pw) // 2 - int(p.width * 0.07))
    left = min(left, p.width - pw)
    p = p.crop((left, (p.height - H) // 2, left + pw, (p.height - H) // 2 + H))
    card = Image.new("RGB", (W, H), BLUE)
    # arch-shaped window for the photo
    mask = Image.new("L", (pw, H), 0)
    d = ImageDraw.Draw(mask)
    top = 40
    d.rectangle([0, top + pw // 2, pw, H], fill=255)
    d.ellipse([0, top, pw, top + pw], fill=255)
    card.paste(p, (W - pw - 40, 0), mask)
    draw = ImageDraw.Draw(card)
    bold = ImageFont.truetype(woff2_to_ttf(os.path.join(FONTS, "dm-sans-latin-wght-normal.woff2"), 700), 56)
    reg = ImageFont.truetype(woff2_to_ttf(os.path.join(FONTS, "dm-sans-latin-wght-normal.woff2"), 500), 28)
    m = mark.resize((120, 120), Image.LANCZOS)
    card.paste(m, (64, 64), m)
    y = 220
    for line in ("AFIT Muslim", "Students’ Community"):
        draw.text((64, y), line, font=bold, fill="white"); y += 66
    draw.text((64, y + 22), "Together in Faith and Purpose", font=reg, fill=YELLOW)
    draw.text((64, H - 84), "Air Force Institute of Technology, Kaduna", font=reg, fill=(214, 228, 250))
    card.save(os.path.join(OUT, "og-image.jpg"), "JPEG", quality=84, optimize=True, progressive=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    for name, widths in PHOTOS.items():
        manifest[name] = resize_set(name, widths, 68)
    for name in FLYERS:
        manifest[name] = resize_set(name, FLYER_WIDTHS, 78)
    mark = logos(manifest)
    og_image(mark)
    with open(os.path.join(HERE, "img-manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    total = sum(os.path.getsize(os.path.join(OUT, x)) for x in os.listdir(OUT))
    print(f"wrote {len(os.listdir(OUT))} files, {total/1024:.0f} KB total -> {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
