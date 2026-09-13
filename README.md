# Equestrian Media — Corporate Website

Premium, conversion-focused website for **Equestrian Media Private Limited**, a Hyderabad-based
BTL marketing, brand activation and outdoor advertising company.

**Strategize | Activate | Elevate**

---

## Stack

Static HTML5, CSS3 and vanilla ES6 modules — no framework, no build step required to deploy.

| Library | Purpose | Delivery |
| --- | --- | --- |
| GSAP 3.12.5 + ScrollTrigger | Scroll choreography, reveals, counters, parallax | CDN, deferred |
| Lenis 1.1.20 | Smooth scrolling | CDN, deferred |
| Swiper 11.1.14 | Media environment carousel (Media Solutions only) | CDN, deferred |
| Manrope + Space Grotesk | Body / display typefaces | Google Fonts |

Icons are **inlined Lucide glyphs** (`arrow-right`, `arrow-up-right`, `check`, `x`, `info`) rather
than the Lucide runtime, so no icon library is downloaded. `initChrome()` in `js/main.js` still
hydrates `[data-lucide]` placeholders if the library is ever added.

---

## Structure

```
index.html              Home
about.html              About the company
services.html           Service pillars + the four deck service groups + rate card
media-solutions.html    Full media inventory (façade, DOOH, atrium, kiosk, backlit, mobile, outdoor)
work.html               Execution showcase
contact.html            Lead capture
brand-activation.html   Service landing page — brand activation / experiential marketing
outdoor-advertising.html Service landing page — outdoor & billboard advertising
mall-activation.html    Service landing page — mall activation / mall branding (LuLu Mall)
btl-marketing.html      Service landing page — BTL marketing campaigns / BTL activation
robots.txt, sitemap.xml Crawl directives + XML sitemap (canonical host: https://equestrianmedia.in/)

css/
  main.css              Tokens, layout primitives, components, utilities
  animations.css        Reveal start states, micro-motion, reduced-motion fallbacks
  responsive.css        Laptop / tablet / mobile layouts, print

js/
  main.js               Entry point + custom cursor
  navigation.js         Sticky header, mobile drawer, anchor scroll-spy
  animations.js         GSAP + Lenis, reveals, counters, parallax, page transitions
  gallery.js            Pinned horizontal gallery, Swiper, category filters
  media.js              Media detail drawer (modal)
  contact.js            Form validation + submission

assets/
  images/               Deck photography as responsive WebP pairs
  logos/                Logo lockups + transparent horse mark
  favicon.*             Favicons derived from the square lockup

build/                  Optional generators (see below)
assests/                Original supplied logo files — source of truth, do not edit
```

### Responsive images

Every photograph ships as a pair: `name-sm.webp` (800w) and `name.webp` (1600w), wired up through
`srcset` + `sizes`. All below-the-fold images are `loading="lazy" decoding="async"`.

---

## Brand system

Three colours only, defined once as CSS custom properties in `css/main.css`:

```css
--red:   #D50A0E;
--black: #000000;
--white: #FFFFFF;
```

Greys are strictly black/white alpha mixes (`--ink-70`, `--line`, `--wash`) — no other hue appears
anywhere in the stylesheet.

**Logo rules honoured:** the supplied artwork is never recoloured, redrawn or distorted — only
resized and re-encoded. Because the logo may not be recoloured, the dark footer places the original
lockup on a **white plate** rather than using an inverted version.

**Hero visual.** The home-page hero uses the supplied media-environment composite
(`assets/images/hero-media-environment.webp` — mall façade, cinema, brand activation stand,
billboard, DOOH panel and LED van). The source file `assets/logos/her_section_img.png` shipped with
its transparency checkerboard *baked in as opaque pixels*, so `build/make_assets.py` restores real
transparency by detecting the checkerboard's 11px periodicity — a signature no photographic region
reproduces, which is why the artwork's own white billboard faces and greyscale screens survive the
cut. Replace that PNG and re-run the script to swap the visual.

Because the composite carries its own red light trails and ground plane, the hero no longer draws
the separate red speed-trail bars or ground streak that accompanied the horse.

**Horse mark.** The closing call-to-action on every page uses `assets/logos/horse-mark.webp`,
re-encoded from the supplied transparent artwork at `assets/logos/horse-mark.png` (1465 × 887, true
alpha); `make_assets.py` always prefers that file over cutting a mark from the horizontal lockup.
`horse-mark_1.png` is the superseded cut-out, unused, and can be deleted.

The logo's oblique italic cut is echoed throughout the UI as a repeating motif: `skewX(-14deg)` red
ticks, dividers, button wipes and separators.

---

## Data provenance

**Every figure, dimension, rate and availability status on this site comes from the supplied
Equestrian Media deck.** Nothing was invented — no founding year, employee count, revenue, campaign
count or campaign results appear anywhere.

Where the source records no result, work entries read *"Campaign execution showcase"*. Where a
specification is absent, the card reads *"Not specified in deck"*.

Pricing and availability are presented as **indicative deck figures**, never as live website
pricing, and each inventory section carries the deck's own caveat that *sites are subject to
availability at the time of final confirmation*.

### ⚠️ One figure to confirm

The brief listed *"90+ internal signages"* and *"20+ national & international brands"*. The deck's
Quick Facts slide (p. 8) reads the other way round:

- **90+** international & national brands
- **20+** internal signages

The site follows **the deck**. If the brief is correct, swap the two labels in
`build/build.py` → `mall_stats`, or edit the two `.stat` blocks in `index.html` directly.

### Brand showcase

The marquee lists brands and retail environments **visible in the deck photography**, under the
heading *"Brands & environments in our media portfolio"* with an explicit note that marks belong to
their owners and their appearance does not imply a client relationship. No third-party logo files
are used and no client relationship is claimed.

---

## Contact form

`contact.html` posts to whatever URL is set on the form's `action` attribute. It currently ships as
`action="#"`, which makes `js/contact.js` fall back to composing a pre-filled email to
`sales.equestrian@gmail.com` so no enquiry is lost.

**To connect a real inbox**, set the action to your endpoint (Formspree, Web3Forms, Netlify Forms,
or your own handler):

```html
<form class="form-grid" data-contact-form action="https://formspree.io/f/XXXXXXX" method="post" novalidate>
```

The script then POSTs `FormData` with `Accept: application/json` and shows a success or failure
message inline. Client-side validation runs on blur and on submit either way.

---

## Accessibility & performance

- Semantic landmarks, one `<h1>` per page, no heading-level skips
- Every image has `alt`; decorative artwork is `alt="" aria-hidden="true"`
- Every form control has an associated `<label>`; errors announced via `aria-live`
- Visible focus rings, skip link, keyboard-operable drawer and modal (focus trap + Escape)
- `prefers-reduced-motion` resolves every animation to its final visible state
- Motion start-states are applied only after JS confirms it can animate (`html.js-anim`), so a
  script failure can never leave content invisible
- All libraries are deferred; no render-blocking JavaScript; no video in the hero

---

## Regenerating (optional)

The header, footer and `<head>` are shared across all six pages. `build/` holds the generator that
emits them so nav changes don't have to be made six times.

```bash
# Rebuild the six HTML pages
python build/build.py

# Rebuild images from the deck (requires pypdf + Pillow)
python build/make_assets.py "path/to/Equestrian Media Deck combined.pdf"
```

Editing the HTML directly is perfectly fine — but re-running `build/build.py` will overwrite it, so
mirror shared-chrome changes into `build/components.py`.

---

## Local preview

```bash
python -m http.server 8899
# then open http://127.0.0.1:8899/
```

A server is required (ES modules will not load over `file://`).

---

## Deployment

Upload the repository root as-is to any static host (Netlify, Vercel, Cloudflare Pages, S3, cPanel).
There is no build step. Before going live, update the domain in each page's `<link rel="canonical">`,
`og:url` and `og:image` — they currently point at `https://www.equestrianmedia.in/`.

© Equestrian Media Private Limited. All Rights Reserved.
