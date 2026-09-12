# -*- coding: utf-8 -*-
"""
Rebuilds assets/images and assets/logos from the source material.

Photography is extracted from the supplied Equestrian Media deck (PDF), cropped
where a GPS Map Camera overlay would otherwise appear, and written as responsive
WebP pairs (`<name>-sm.webp` at 800w and `<name>.webp` at 1600w).

Usage:
    python build/make_assets.py "path/to/Equestrian Media Deck combined.pdf"

Requires: pypdf, Pillow
"""
import io
import os
import sys

from PIL import Image
from pypdf import PdfReader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "images")
LOGO = os.path.join(ROOT, "assets", "logos")
SRC_LOGOS = os.path.join(ROOT, "assests")  # original supplied logo files

WIDE, SMALL = 1600, 800

# (deck page, image index on that page, output name, fraction to crop off the
#  bottom to remove the GPS Map Camera overlay)
MAP = [
    # LuLu Mall / environment
    (6, 0, "lulu-facade-night", 0.00),
    (5, 0, "lulu-aerial", 0.00),
    (8, 0, "lulu-aerial-night", 0.00),
    (4, 1, "lulu-facade-day", 0.00),
    (14, 0, "lulu-exterior-wide", 0.00),
    (45, 0, "lulu-happiness", 0.00),
    (18, 0, "lulu-logo", 0.00),
    (7, 4, "hyderabad-corridor", 0.00),
    # Mall façade inventory
    (13, 0, "facade-h1-h2-h3", 0.00),
    (14, 0, "facade-h6-h7", 0.00),
    # DOOH / LED
    (15, 0, "atrium-led-main", 0.00),
    (16, 0, "floor-led-first", 0.00),
    (16, 1, "floor-led-second", 0.00),
    (16, 2, "floor-led-third", 0.00),
    # Backlit / lift lobby / billboards
    (17, 0, "backlit-b1-lobby", 0.00),
    (18, 1, "backlit-ug-entry", 0.00),
    (19, 0, "lift-south-lg-01", 0.00),
    (19, 1, "lift-south-lg-02", 0.00),
    (20, 0, "ramp-b1", 0.00),
    (21, 0, "backlit-lg", 0.00),
    (22, 0, "lift-south-ff", 0.00),
    (23, 0, "lift-south-sf", 0.00),
    (24, 0, "lift-south-tf", 0.00),
    (25, 0, "lift-south-fof", 0.00),
    (26, 0, "lift-north-lg", 0.00),
    (27, 0, "lift-north-ug", 0.00),
    (28, 0, "lift-north-ff", 0.00),
    (29, 0, "lift-north-sf", 0.00),
    (30, 0, "lift-north-tf", 0.00),
    (31, 0, "lift-north-fof", 0.00),
    (32, 0, "travelator-billboards", 0.00),
    (33, 0, "billboard-lg", 0.00),
    (34, 0, "easel-standees", 0.00),
    (35, 0, "periphery-poles", 0.00),
    # Atrium activations & kiosks
    (10, 0, "atrium-kiosk-brand", 0.00),
    (10, 1, "atrium-crowd", 0.00),
    (10, 2, "atrium-mercedes", 0.00),
    (10, 3, "atrium-mg-hector", 0.00),
    (10, 4, "atrium-tvs-display", 0.00),
    (36, 0, "atrium-two-wheeler", 0.00),
    (37, 0, "atrium-bikes-row", 0.00),
    (38, 0, "atrium-tata-curvv", 0.00),
    (40, 0, "atrium-car-display", 0.00),
    (41, 0, "atrium-stage-emcee", 0.00),
    (42, 0, "kiosk-first-floor", 0.00),
    (43, 0, "kiosk-second-floor", 0.00),
    # Cinema & entertainment
    (11, 0, "cinepolis-lulu", 0.00),
    (12, 0, "funtura-gaming", 0.00),
    # Mobile advertising — GPS overlay cropped off the bottom
    (47, 1, "led-van-street", 0.14),
    (47, 0, "led-van-residential", 0.22),
    (47, 2, "led-van-night", 0.00),
    (48, 0, "tata-ace-arc", 0.00),
    (48, 1, "tata-ace-road", 0.00),
    (49, 1, "round-flex-campaign", 0.00),
    (49, 0, "pole-kiosk-campaign", 0.20),
    (50, 0, "look-walkers", 0.18),
    (50, 1, "look-walkers-street", 0.18),
    (51, 0, "tricycle-fleet", 0.18),
    (51, 1, "tricycle-street", 0.18),
    (51, 2, "tricycle-college", 0.00),
    (52, 0, "wall-poster-campaign", 0.18),
    (52, 1, "wall-poster-wall", 0.18),
    (53, 0, "no-parking-boards", 0.18),
    (53, 1, "no-parking-gate", 0.18),
    (54, 0, "auto-top-branding", 0.18),
    (54, 2, "auto-top-fleet", 0.18),
    (55, 0, "auto-sticker-branding", 0.18),
    (55, 1, "auto-sticker-campaign", 0.18),
]


def page_images(reader, page_no):
    """
    Usable images on a deck page, keyed by their position in the page's full
    image list. Tiny decorations are filtered out but the surviving images keep
    their original index, which is what MAP refers to.
    """
    out = {}
    for index, im in enumerate(reader.pages[page_no - 1].images):
        if len(im.data) < 25000:
            continue
        try:
            img = Image.open(io.BytesIO(im.data))
            img.load()
        except Exception:
            continue
        if img.width < 300 or img.height < 200:
            continue
        out[index] = img
    return out


def write_pair(img, name):
    for width, suffix in ((WIDE, ""), (SMALL, "-sm")):
        out = img.copy()
        if out.width > width:
            out = out.resize((width, round(out.height * width / out.width)), Image.LANCZOS)
        out.save(os.path.join(IMG, f"{name}{suffix}.webp"), "WEBP", quality=82, method=6)


def matte_to_alpha(img):
    """Turns the artwork's white background transparent without altering its colours."""
    img = img.convert("RGB")
    px = img.load()
    out = Image.new("RGBA", img.size)
    op = out.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y]
            op[x, y] = (r, g, b, 255 - min(r, g, b))
    return out


def build_photos(pdf_path):
    reader = PdfReader(pdf_path)
    cache = {}
    written = 0
    for page_no, index, name, crop in MAP:
        if page_no not in cache:
            cache[page_no] = page_images(reader, page_no)
        images = cache[page_no]
        if index not in images:
            print(f"  ! skipped {name}: page {page_no} has no usable image at index {index}")
            continue
        img = images[index].convert("RGB")
        if crop:
            img = img.crop((0, 0, img.width, int(img.height * (1 - crop))))
        write_pair(img, name)
        written += 1
    print(f"photographs written: {written}")


def build_logos():
    """The logo artwork is never recoloured or redrawn — only resized and matted."""
    horizontal = Image.open(os.path.join(SRC_LOGOS, "horizontal_logo_eqestrain.png")).convert("RGB")
    square = Image.open(os.path.join(SRC_LOGOS, "square_logo (3).png")).convert("RGB")

    h = horizontal.copy()
    h.thumbnail((1200, 1200), Image.LANCZOS)
    h.save(os.path.join(LOGO, "equestrian-horizontal.png"), optimize=True)
    h.save(os.path.join(LOGO, "equestrian-horizontal.webp"), "WEBP", quality=92, method=6)

    s = square.copy()
    s.thumbnail((900, 900), Image.LANCZOS)
    s.save(os.path.join(LOGO, "equestrian-square.png"), optimize=True)
    s.save(os.path.join(LOGO, "equestrian-square.webp"), "WEBP", quality=92, method=6)

    # Horse mark. A supplied transparent artwork at assets/logos/horse-mark.png
    # always wins; it is only re-encoded to WebP, never redrawn. If none exists,
    # the mark is cut from the left third of the horizontal lockup instead.
    horse_png = os.path.join(LOGO, "horse-mark.png")
    if os.path.exists(horse_png):
        horse = Image.open(horse_png).convert("RGBA")
    else:
        horse = matte_to_alpha(horizontal.crop((0, 0, int(horizontal.width * 0.325), horizontal.height)))
        horse = horse.crop(horse.getbbox())
        horse.save(horse_png, optimize=True)
    horse.thumbnail((1100, 1100), Image.LANCZOS)
    horse.save(os.path.join(LOGO, "horse-mark.webp"), "WEBP", quality=82, method=6)
    print(f"horse mark: {horse.size}")

    # Favicons from the square lockup.
    icon = square.crop((int(square.width * 0.06), int(square.height * 0.06),
                        int(square.width * 0.94), int(square.height * 0.52)))
    icon.thumbnail((512, 512), Image.LANCZOS)
    pad = Image.new("RGB", (max(icon.size),) * 2, "white")
    pad.paste(icon, ((pad.width - icon.width) // 2, (pad.height - icon.height) // 2))
    assets = os.path.join(ROOT, "assets")
    pad.resize((512, 512), Image.LANCZOS).save(os.path.join(assets, "favicon.png"))
    pad.resize((180, 180), Image.LANCZOS).save(os.path.join(assets, "apple-touch-icon.png"))
    pad.resize((64, 64), Image.LANCZOS).save(os.path.join(assets, "favicon.ico"),
                                             sizes=[(64, 64), (32, 32), (16, 16)])
    print("logos and favicons written")


if __name__ == "__main__":
    os.makedirs(IMG, exist_ok=True)
    os.makedirs(LOGO, exist_ok=True)

    if len(sys.argv) > 1:
        pdf = sys.argv[1]
        if not os.path.exists(pdf):
            sys.exit(f"Deck not found: {pdf}")
        build_photos(pdf)
    else:
        print("No deck path given — rebuilding logos only.")
        print('Pass the deck to rebuild photography: python build/make_assets.py "…/Equestrian Media Deck combined.pdf"')

    build_logos()
    build_hero_composite()


# ---------------------------------------------------------------------------
# Hero composite
# ---------------------------------------------------------------------------
def build_hero_composite():
    """
    The supplied hero composite ships with its transparency checkerboard baked
    in as opaque pixels. This detects the checkerboard by its 11px periodicity
    (a signature no photographic region reproduces, so the artwork's own white
    panels and greyscale screens survive) and restores real transparency.
    """
    import numpy as np
    from scipy import ndimage
    from PIL import ImageFilter

    src_path = next(
        (q for q in (os.path.join(LOGO, "hero_section_img.png"),
                     os.path.join(LOGO, "her_section_img.png"))
         if os.path.exists(q)), None)
    if not src_path:
        print("hero composite: source not found, skipped")
        return

    raw = Image.open(src_path)

    # A source that already carries a real alpha channel needs no keying — only
    # trimming and re-encoding. Forcing it to RGB here would throw the alpha away.
    if raw.mode in ("RGBA", "LA") or "transparency" in raw.info:
        rgba = raw.convert("RGBA")
        alpha_ch = rgba.getchannel("A")
        lo, hi = alpha_ch.getextrema()
        transparent = sum(1 for v in alpha_ch.getdata() if v < 16) / (rgba.width * rgba.height)
        if lo < 250 and transparent > 0.02:
            out = rgba.crop(rgba.getbbox())
            _write_hero(out)
            print(f"hero composite: {out.size}, true alpha preserved "
                  f"({transparent*100:.0f}% transparent)")
            return
        print("hero composite: alpha channel present but effectively opaque — keying instead")

    src = raw.convert("RGB")
    a = np.asarray(src).astype(np.float32)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    spread = np.maximum(np.maximum(np.abs(R - G), np.abs(G - B)), np.abs(R - B))
    I = (R + G + B) / 3.0
    light = (spread <= 10) & (I >= 200) & (I <= 258)

    def sh(x, dy, dx):
        return np.roll(np.roll(x, -dy, axis=0), -dx, axis=1)

    # Cell size varies by whoever rendered the checkerboard, so measure it:
    # score each candidate by how much of the image shows the signature
    # "opposite tone one cell away, same tone two cells away".
    def signature(cell):
        return (((np.abs(I - sh(I, 0, cell)) > 25) & (np.abs(I - sh(I, 0, 2 * cell)) < 12)) |
                ((np.abs(I - sh(I, cell, 0)) > 25) & (np.abs(I - sh(I, 2 * cell, 0)) < 12)))

    CELL = max(range(6, 21), key=lambda c: (signature(c) & light).mean())
    sig = signature(CELL)
    print(f"hero composite: checkerboard cell measured at {CELL}px")
    sig_frac = ndimage.uniform_filter((sig & light).astype(np.float32), 25)
    frac_light = ndimage.uniform_filter(light.astype(np.float32), 25)

    core = ndimage.binary_opening(
        light & (sig_frac >= 0.40) & (frac_light >= 0.95), np.ones((7, 7)))
    # Growth is bounded and masked by `light`, so it stops at every dark edge.
    bg = ndimage.binary_dilation(core, np.ones((3, 3)), iterations=20, mask=light)

    # Enclosed pockets have no core of their own; score each leftover region by
    # its checker signature instead. Flat artwork panels score ~0.
    rem = light & ~bg
    lbl, n = ndimage.label(rem)
    if n:
        idx = np.arange(1, n + 1)
        means = ndimage.mean(sig_frac, lbl, idx)
        areas = ndimage.sum(np.ones_like(sig_frac), lbl, idx)
        # Enclosed pockets, anywhere in the frame.
        bg |= np.isin(lbl, idx[(means >= 0.22) & (areas >= 60)])

        # Cells stranded against the silhouette are what produce the stair-stepped
        # fringe. They are small, they touch the background, and they still carry
        # some checker signature — an interior artwork panel meets none of that.
        touching = np.unique(lbl[ndimage.binary_dilation(bg, np.ones((3, 3))) & (lbl > 0)])
        stranded = idx[(means >= 0.10) & (areas <= 4000) & np.isin(idx, touching)]
        bg |= np.isin(lbl, stranded)

    # Smooth the silhouette: close the remaining notches, but only into pixels
    # that still look like checker residue, never into dark artwork. Cells that
    # overlapped the red trails' glow read as light *pink*, not neutral grey, so
    # the test allows a warm blend (R >= G == B) as well as pure grey.
    residue = (np.abs(G - B) <= 16) & (R >= G - 4) & (I >= 165)
    bg |= ndimage.binary_closing(bg, np.ones((13, 13))) & residue


    # Feather to a genuine anti-aliased edge instead of a hard binary cut.
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    alpha = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(0.9))
    out = src.convert("RGBA")
    out.putalpha(alpha)
    out = out.crop(out.getbbox())
    _write_hero(out)
    print(f"hero composite: {out.size}, checkerboard keyed out")


def _write_hero(out):
    """Responsive WebP pair. 1140w covers a 2x screen at the 570px display cap."""
    for width, suffix in ((1140, ""), (640, "-sm")):
        o = out.copy()
        if o.width > width:
            o = o.resize((width, round(o.height * width / o.width)), Image.LANCZOS)
        o.save(os.path.join(IMG, f"hero-media-environment{suffix}.webp"),
               "WEBP", quality=86, method=6)
