# -*- coding: utf-8 -*-
"""
Generates the Equestrian Media static site.

Header, footer and <head> are shared here so the six emitted HTML files stay
consistent. All inventory figures come from the supplied Equestrian Media deck.
"""
import os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PHONE_RAW = "+918106039919"
PHONE = "+91 81060 39919"
EMAIL = "ravi.chander@equestrianmedia.in"
CONTACT = "Ravi Chander"

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Services"),
    ("media-solutions.html", "Media Solutions"),
    ("work.html", "Work"),
    ("contact.html", "Contact"),
]

DECK_NOTE = ("Figures, specifications and rates shown are taken from the Equestrian Media media deck "
             "and are indicative. All sites are subject to availability at the time of final confirmation.")


# ---------------------------------------------------------------- helpers
def img(name, alt, cls="", sizes="(max-width: 767px) 92vw, (max-width: 1024px) 48vw, 34vw",
        lazy=True, extra=""):
    """Responsive <picture>-free img using the -sm / full WebP pair."""
    loading = 'loading="lazy" decoding="async"' if lazy else 'decoding="async" fetchpriority="high"'
    klass = f' class="{cls}"' if cls else ""
    return (f'<img{klass} src="assets/images/{name}-sm.webp" '
            f'srcset="assets/images/{name}-sm.webp 800w, assets/images/{name}.webp 1600w" '
            f'sizes="{sizes}" alt="{alt}" {loading} {extra}>')


def arrow(size=16):
    return (f'<svg class="btn__arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def icon_arrow_ur():
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg>')


def icon_check():
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" '
            'aria-hidden="true"><path d="m5 13 4 4L19 7"/></svg>')


def icon_info():
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>')


def note(text):
    return f'<p class="note">{icon_info()}<span>{text}</span></p>'


def lines(*rows):
    """Wraps each row for the clip-path line reveal."""
    return "".join(f'<span class="line"><span>{r}</span></span>' for r in rows)


# ---------------------------------------------------------------- chrome
def head(title, desc, page, keywords="", extra=""):
    nav_json = ""
    if page == "index.html":
        nav_json = """
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "AdvertisingAgency",
    "name": "Equestrian Media Private Limited",
    "slogan": "Strategize | Activate | Elevate",
    "description": "Hyderabad-based BTL marketing, brand activation and outdoor advertising company delivering on-ground campaigns, mall branding, DOOH, cinema advertising and mobile advertising.",
    "url": "https://www.equestrianmedia.in/",
    "logo": "https://www.equestrianmedia.in/assets/logos/equestrian-horizontal.png",
    "email": "ravi.chander@equestrianmedia.in",
    "telephone": "+91-81060-39919",
    "address": { "@type": "PostalAddress", "addressLocality": "Hyderabad", "addressRegion": "Telangana", "addressCountry": "IN" },
    "areaServed": [
      { "@type": "State", "name": "Telangana" },
      { "@type": "State", "name": "Andhra Pradesh" }
    ],
    "contactPoint": {
      "@type": "ContactPoint",
      "contactType": "sales",
      "name": "Ravi Chander",
      "telephone": "+91-81060-39919",
      "email": "ravi.chander@equestrianmedia.in"
    },
    "knowsAbout": ["BTL Marketing", "Brand Activation", "Outdoor Advertising", "Mall Branding", "DOOH Advertising", "Cinema Advertising", "Mobile Advertising"]
  }
  </script>"""

    kw = f'\n  <meta name="keywords" content="{keywords}">' if keywords else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">{kw}
  <link rel="canonical" href="https://www.equestrianmedia.in/{'' if page == 'index.html' else page}">
  <meta name="theme-color" content="#000000">
  <meta name="robots" content="index, follow">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Equestrian Media">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://www.equestrianmedia.in/assets/logos/equestrian-square.png">
  <meta property="og:url" content="https://www.equestrianmedia.in/{'' if page == 'index.html' else page}">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" href="assets/favicon.ico" sizes="any">
  <link rel="icon" href="assets/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style"
        href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&family=Space+Grotesk:wght@500;700&display=swap">
  <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&family=Space+Grotesk:wght@500;700&display=swap">

  <!-- Styles -->
  <link rel="stylesheet" href="css/main.css">
  <link rel="stylesheet" href="css/animations.css">
  <link rel="stylesheet" href="css/responsive.css">{extra}{nav_json}
</head>
<body>
  <div class="page-curtain" aria-hidden="true"></div>
  <a class="skip-link" href="#main">Skip to content</a>
"""


def header(page):
    desktop = "".join(
        f'<li><a class="nav__link" href="{href}"'
        f'{" aria-current=\"page\"" if href == page else ""}>{label}</a></li>'
        for href, label in NAV
    )
    mobile = "".join(
        f'<li class="mobile-nav__item"><a class="mobile-nav__link" href="{href}"'
        f'{" aria-current=\"page\"" if href == page else ""}>'
        f'<span>{label}</span><span class="idx">{i:02d}</span></a></li>'
        for i, (href, label) in enumerate(NAV, start=1)
    )

    return f"""  <header class="site-header">
    <div class="wrap header__inner">
      <a class="brand" href="index.html" aria-label="Equestrian Media — home">
        <img class="brand__logo" src="assets/logos/equestrian-horizontal.webp"
             alt="Equestrian Media — Strategize, Activate, Elevate" width="1200" height="299">
      </a>

      <nav class="nav" aria-label="Primary">
        <ul class="nav__list">{desktop}</ul>
      </nav>

      <div class="header__actions">
        <a class="btn header__cta" href="contact.html" data-cursor="EXPLORE"><span>Plan your campaign</span></a>
        <button class="burger" type="button" aria-expanded="false" aria-controls="mobile-nav"
                aria-label="Open menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <nav class="mobile-nav" id="mobile-nav" aria-label="Mobile" aria-hidden="true">
    <ul class="mobile-nav__list">{mobile}</ul>
    <div class="mobile-nav__foot">
      <a class="btn btn--block" href="contact.html"><span>Plan your campaign</span></a>
      <p class="mobile-nav__meta">
        {CONTACT} · <a href="tel:{PHONE_RAW}">{PHONE}</a><br>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
      </p>
    </div>
  </nav>

  <div class="header-spacer" aria-hidden="true"></div>
"""


def footer():
    nav_links = "".join(f'<li><a href="{href}">{label}</a></li>' for href, label in NAV)
    services = "".join(
        f'<li><a href="{href}">{label}</a></li>' for href, label in [
            ("services.html#brand-activation", "Brand Activation"),
            ("services.html#mobile-advertising", "Mobile Advertising"),
            ("services.html#outdoor-advertising", "Outdoor Advertising"),
            ("services.html#promotional-campaigns", "Promotional Campaigns"),
            ("media-solutions.html#mall-media", "Mall Branding"),
            ("media-solutions.html#dooh", "DOOH / LED Media"),
            ("media-solutions.html#cinema", "Cinema Advertising"),
        ]
    )

    return f"""  <footer class="site-footer">
    <div class="wrap">
      <div class="footer__top">
        <div class="footer__brand">
          <span class="footer__logo-plate">
            <img src="assets/logos/equestrian-horizontal.webp"
                 alt="Equestrian Media" width="1200" height="299" loading="lazy">
          </span>
          <p class="footer__blurb">
            Hyderabad-based BTL marketing, brand activation and outdoor advertising company.
            On-ground campaigns, mall branding, DOOH, cinema and mobile media across Telangana
            and Andhra Pradesh.
          </p>
        </div>

        <div class="footer__col">
          <h3>Navigate</h3>
          <ul>{nav_links}</ul>
        </div>

        <div class="footer__col">
          <h3>Media &amp; Services</h3>
          <ul>{services}</ul>
        </div>

        <div class="footer__col">
          <h3>Contact</h3>
          <ul>
            <li><span>{CONTACT}</span></li>
            <li><a href="tel:{PHONE_RAW}">{PHONE}</a></li>
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><span>Hyderabad, Telangana, India</span></li>
          </ul>
        </div>
      </div>

      <p class="footer__tagline">
        <span>Strategize</span><i aria-hidden="true"></i>
        <span>Activate</span><i aria-hidden="true"></i>
        <span>Elevate</span>
      </p>

      <div class="footer__bottom">
        <p>&copy; <span data-year>2026</span> Equestrian Media Private Limited. All Rights Reserved.</p>
        <p>BTL Marketing · Brand Activation · Outdoor Advertising · Hyderabad</p>
      </div>
    </div>
  </footer>

  <!-- Libraries (deferred, non-blocking) -->
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/lenis@1.1.20/dist/lenis.min.js"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/Swiper/11.1.14/swiper-bundle.min.js"></script>
  <script defer src="js/bundle.js"></script>
</body>
</html>
"""


def cta_final():
    return f"""  <!-- ==================== FINAL CTA ==================== -->
  <section class="section cta-final">
    <img class="cta-final__horse" src="assets/logos/horse-mark.webp" alt="" aria-hidden="true"
         width="1100" height="666" loading="lazy">
    <div class="wrap cta-final__inner">
      <h2 class="cta-final__title" data-reveal-lines>
        {lines('Your brand deserves', '<span class="red">to be seen.</span>')}
      </h2>
      <p class="cta-final__tag" data-reveal>
        <span>Strategize</span><i aria-hidden="true"></i>
        <span>Activate</span><i aria-hidden="true"></i>
        <span>Elevate</span>
      </p>
      <div class="actions" data-reveal data-reveal-delay="0.1">
        <a class="btn btn--lg" href="contact.html" data-cursor="EXPLORE">
          <span>Plan your campaign</span>{arrow()}
        </a>
        <a class="btn btn--outline btn--lg" href="tel:{PHONE_RAW}"><span>{PHONE}</span></a>
      </div>
    </div>
  </section>
"""


def page_hero(eyebrow, title_rows, lead, crumb):
    crumbs = ('<a href="index.html">Home</a><span aria-hidden="true">/</span>'
              f'<span aria-current="page">{crumb}</span>')
    return f"""  <section class="page-hero">
    <div class="wrap">
      <nav class="breadcrumb" aria-label="Breadcrumb">{crumbs}</nav>
      <p class="eyebrow">{eyebrow}</p>
      <h1 class="page-hero__title" data-reveal-lines>{lines(*title_rows)}</h1>
      <p class="lead measure u-mt-1" data-reveal>{lead}</p>
    </div>
  </section>
"""


# ---------------------------------------------------------------- data
SERVICE_PILLARS = [
    ("01", "Corporate Marketing", "corporate-marketing",
     "Brand-led marketing programmes built for corporate audiences, employee engagement and B2B visibility.",
     ["Corporate Events", "Brand Programmes", "Custom BTL"], "atrium-crowd"),
    ("02", "BTL Activations", "btl-activations",
     "On-ground activations that put your product in the customer's hands — malls, retail and high-footfall environments.",
     ["Mall Activations", "Retail Promotions", "Sampling"], "atrium-tvs-display"),
    ("03", "Mall Branding", "mall-branding",
     "Facade hoardings, atriums, kiosks, lift lobbies and backlit media inside Hyderabad's premium mall environment.",
     ["Facade", "Atrium", "Kiosks", "Backlit"], "lulu-facade-day"),
    ("04", "Cinema Advertising", "cinema-advertising",
     "On-screen and in-cinema brand presence in a premium multiplex environment with a captive audience.",
     ["On-screen", "Foyer", "Standees"], "cinepolis-lulu"),
    ("05", "DOOH", "dooh",
     "Digital out-of-home: main atrium LED and floor-level digital screens running scheduled ad rotations.",
     ["Atrium LED", "Floor LED", "JPG / MP4"], "atrium-led-main"),
]

WHY = [
    "Complete BTL Marketing Solutions",
    "Experienced &amp; Professional Team",
    "Innovative Advertising Platforms",
    "Fast Campaign Execution",
    "Competitive Pricing",
    "Customized Brand Promotions",
    "Reliable Service &amp; Support",
    "Strong Local Market Presence",
    "High Visibility &amp; Maximum Reach",
]

PROCESS = [
    ("01", "Understand", "Understand the brand objective, the category and the target audience before a single site is proposed."),
    ("02", "Strategize", "Select the appropriate activation and media solution — mall, DOOH, cinema, mobile or on-ground."),
    ("03", "Plan", "Finalise locations, formats, artwork specifications and execution requirements against your dates."),
    ("04", "Activate", "Execute the campaign on-ground — installation, manpower, permissions and day-to-day supervision."),
    ("05", "Elevate", "Maximise visibility and audience engagement across the campaign window, with execution reporting."),
]

# Brands and environments visible inside the supplied deck photography.
BRANDS = ["Cinépolis", "LuLu Hypermarket", "Starbucks", "Funtura", "Mercedes-Benz", "MG Motor",
          "TVS", "Tata Motors", "vivo", "Bombay Dyeing", "Trident", "KFC", "Tissot", "HP World",
          "Market 99", "Centre for Sight", "Kapil Properties", "AlBaik"]


def media_card(cid, kicker, title, image, alt, specs, availability, description="",
               note_text="", badge="", cursor="VIEW MEDIA"):
    # <button> may only contain phrasing content, so the spec rows are spans.
    spec_html = "".join(
        f'<span class="spec"><span class="spec__k">{k}</span><span class="spec__v">{v}</span></span>'
        for k, v in specs
    )
    badge_html = f'<span class="badge {badge[1]}">{badge[0]}</span>' if badge else ""
    desc_attr = f' data-description="{description}"' if description else ""
    note_attr = f' data-note="{note_text}"' if note_text else ""

    return f"""            <button class="media-card" type="button" data-media="{cid}" data-cursor="{cursor}"
                    data-full-image="assets/images/{image}.webp"{desc_attr}{note_attr}>
              <span class="media-card__figure">{badge_html}
                {img(image, alt, cls="media-card__img", sizes="(max-width:767px) 92vw, (max-width:1024px) 46vw, 30vw")}
              </span>
              <span class="media-card__body">
                <span class="media-card__kicker">{kicker}</span>
                <span class="media-card__title h4">{title}</span>
                <span class="spec-list">{spec_html}</span>
                <span class="media-card__foot">
                  <span class="availability">{availability}</span>
                  <span class="media-card__cta">Request media plan
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
                  </span>
                </span>
              </span>
            </button>"""


AVAIL_NOTE = "Availability subject to confirmation. The deck states that all sites are subject to availability at the time of final confirmation."

# ---- Mall facade (deck pp. 13–14)
FACADE = [
    ("facade-h1", "H1 · Mall Façade", "facade-h1-h2-h3", "LuLu Mall Hyderabad façade hoardings H1, H2 and H3",
     [("Site", "Mall façade hoarding"), ("Approx. size", "8.50 × 5.10 m"), ("Type", "Front lit"),
      ("Material", "Flex"), ("Installation", "11 PM – 6 AM"), ("Indicative charge", "₹2,25,000 / month")],
     "Deck status: not available"),
    ("facade-h2", "H2 · Mall Façade", "facade-h1-h2-h3", "LuLu Mall Hyderabad façade hoarding H2",
     [("Site", "Mall façade hoarding"), ("Approx. size", "8.50 × 5.10 m"), ("Type", "Front lit"),
      ("Material", "Flex"), ("Installation", "11 PM – 6 AM"), ("Indicative charge", "₹2,25,000 / month")],
     "Deck status: available"),
    ("facade-h3", "H3 · Mall Façade", "facade-h1-h2-h3", "LuLu Mall Hyderabad façade hoarding H3",
     [("Site", "Mall façade hoarding"), ("Approx. size", "9.50 × 5.50 m"), ("Type", "Front lit"),
      ("Material", "Flex"), ("Installation", "11 PM – 6 AM"), ("Indicative charge", "₹2,50,000 / month")],
     "Deck status: available"),
    ("facade-h6", "H6 · Mall Façade", "facade-h6-h7", "LuLu Mall Hyderabad façade hoardings H6 and H7",
     [("Site", "Mall façade hoarding"), ("Approx. size", "11.90 × 8.50 m"), ("Type", "Front lit"),
      ("Material", "Flex"), ("Installation", "11 PM – 6 AM"), ("Indicative charge", "₹2,50,000 / month")],
     "Deck status: available"),
    ("facade-h7", "H7 · Mall Façade", "facade-h6-h7", "LuLu Mall Hyderabad façade hoarding H7",
     [("Site", "Mall façade hoarding"), ("Approx. size", "11.90 × 8.25 m"), ("Type", "Front lit"),
      ("Material", "Flex"), ("Installation", "11 PM – 6 AM"), ("Indicative charge", "₹2,50,000 / month")],
     "Deck status: available"),
]

# ---- Backlit / lift lobby / billboards (deck pp. 17–35)
BACKLIT = [
    ("b1-lobby", "Basement Lobby B1", "backlit-b1-lobby", "Backlit board in the basement lobby B1",
     [("Site", "Basement lobby B1"), ("Approx. size", "165.4 × 90.6 in"), ("Type", "Back lit"),
      ("Material", "Fabric / Flex"), ("Indicative charge", "₹1,00,000")], "Deck status: not available"),
    ("ug-entry", "UG Entrance Backlit", "backlit-ug-entry", "Backlit board at the upper ground entrance",
     [("Site", "Backlit board – UG entrance"), ("Approx. size", "11 × 11.48 in"), ("Type", "Back lit"),
      ("Material", "Fabric / Flex"), ("Indicative charge", "₹1,00,000 per pole")], "Deck status: ready to occupy"),
    ("lift-south-lg", "Lift Lobby South · LG", "lift-south-lg-01", "Backlit lift lobby boards, south side lower ground",
     [("Site", "South side elevator LG 01 &amp; 02"), ("Approx. size", "47.2 × 66.9 in"), ("Type", "Back lit"),
      ("Material", "Fabric / Flex"), ("Indicative charge", "₹50,000 per board")], "Deck status: ready to occupy"),
    ("lift-south-ff", "Lift Lobby South · FF", "lift-south-ff", "Backlit lift lobby boards, south side first floor",
     [("Site", "South side elevator FF 01 &amp; 02"), ("Approx. size", "47.2 × 66.9 in"), ("Type", "Back lit"),
      ("Material", "Fabric"), ("Indicative charge", "₹50,000 per board")], "Deck status: ready to occupy"),
    ("lift-south-sf", "Lift Lobby South · SF", "lift-south-sf", "Backlit lift lobby boards, south side second floor",
     [("Site", "South side elevator SF 01 &amp; 02"), ("Approx. size", "47.2 × 60.9 in"), ("Type", "Back lit"),
      ("Material", "Fabric"), ("Indicative charge", "₹50,000 per board")], "Deck status: ready to occupy"),
    ("lift-south-tf", "Lift Lobby South · TF", "lift-south-tf", "Backlit lift lobby boards, south side third floor",
     [("Site", "South side elevator TF 01 &amp; 02"), ("Approx. size", "47.2 × 66.9 in"), ("Type", "Back lit"),
      ("Material", "Fabric"), ("Indicative charge", "₹50,000 per board")], "Deck status: 01 not available · 02 available"),
    ("lift-south-fof", "Lift Lobby South · FOF", "lift-south-fof", "Backlit lift lobby boards, south side fourth floor",
     [("Site", "South side elevator FOF 01 &amp; 02"), ("Approx. size", "47.2 × 66.9 in"), ("Type", "Back lit"),
      ("Material", "Fabric"), ("Indicative charge", "₹50,000 per board")], "Deck status: ready to occupy"),
    ("lift-north-lg", "Lift Lobby North · LG", "lift-north-lg", "Backlit lift lobby boards, north side lower ground",
     [("Site", "North side elevator LG 01 &amp; 02"), ("Approx. size", "47.2 × 66.9 in"), ("Type", "Back lit"),
      ("Material", "Fabric"), ("Indicative charge", "₹50,000 per board")], "Deck status: ready to occupy"),
    ("lift-north-ug", "Lift Lobby North · UG", "lift-north-ug", "Backlit lift lobby boards, north side upper ground",
     [("Site", "North side elevator UG 01 &amp; 02"), ("Approx. size", "39 × 78 in"), ("Type", "Back lit"),
      ("Material", "Fabric"), ("Indicative charge", "₹50,000 per board")], "Deck status: not available"),
    ("lift-north-ff", "Lift Lobby North · FF", "lift-north-ff", "Backlit lift lobby boards, north side first floor",
     [("Site", "North side elevator FF 01 &amp; 02"), ("Approx. size", "47.2 × 66.9 in"), ("Type", "Back lit"),
      ("Material", "Fabric"), ("Indicative charge", "₹50,000 per board")], "Deck status: ready to occupy"),
    ("lift-north-sf", "Lift Lobby North · SF", "lift-north-sf", "Backlit lift lobby boards, north side second floor",
     [("Site", "North side elevator SF 01 &amp; 02"), ("Approx. size", "47.2 × 66.9 in"), ("Type", "Back lit"),
      ("Material", "Fabric"), ("Indicative charge", "₹50,000 per board")], "Deck status: ready to occupy"),
    ("lift-north-tf", "Lift Lobby North · TF", "lift-north-tf", "Backlit lift lobby boards, north side third floor",
     [("Site", "North side elevator TF 01 &amp; 02"), ("Approx. size", "47.2 × 66.9 in"), ("Type", "Back lit"),
      ("Material", "Fabric"), ("Indicative charge", "₹50,000 per board")], "Deck status: not available"),
    ("lift-north-fof", "Lift Lobby North · FOF", "lift-north-fof", "Backlit lift lobby boards, north side fourth floor",
     [("Site", "North side elevator FOF 01 &amp; 02"), ("Approx. size", "47.2 × 66.9 in"), ("Type", "Back lit"),
      ("Material", "Fabric"), ("Indicative charge", "₹50,000 per board")], "Deck status: ready to occupy"),
    ("ramp-b1", "B1 Ramp · C1 / C2 / C3", "ramp-b1", "Backlit ramp boards in basement B1",
     [("Site", "Basement lobby B1 ramp"), ("Approx. size", "137.7 × 59 in"), ("Type", "Back lit"),
      ("Material", "Fabric / Flex"), ("Indicative charge", "₹50,000 per board")],
     "Deck status: C1 available · C2 not available · C3 available"),
    ("lg-backlit", "LG Backlit", "backlit-lg", "Backlit board on the lower ground level",
     [("Site", "LG backlit"), ("Approx. size", "Not specified in deck"), ("Type", "Back lit"),
      ("Material", "Fabric"), ("Indicative charge", "₹60,000 per board")], "Deck status: not available"),
    ("travelator", "Travelator Billboards", "travelator-billboards", "Billboards next to the travelator on the lower ground",
     [("Site", "Next to travelator LG 01–03"), ("Approx. size", "78.7 × 161.4 in"), ("Type", "Front lit"),
      ("Material", "Fabric"), ("Indicative charge", "₹1,00,000 per board")], "Deck status: 1 available"),
    ("lg-billboard", "LG Billboards", "billboard-lg", "Billboard opposite the hypermarket entry on the lower ground",
     [("Site", "Opposite hypermarket entry, LG"), ("Approx. size", "108.3 × 118.1 in"), ("Type", "Front lit"),
      ("Material", "Fabric / Flex"), ("Indicative charge", "₹1,00,000")], "Deck status: available"),
    ("easel", "Easel Standees", "easel-standees", "Easel standee boards inside the mall",
     [("Site", "Easel boards"), ("Approx. size", "2 ft W × 3 ft H"), ("Material", "5 mm foam sheet"),
      ("Installation", "11 PM – 6 AM"), ("Indicative charge", "₹50,000 per standee")], "Deck status: 2 available"),
    ("periphery", "Periphery Poles", "periphery-poles", "Front-lit periphery pole kiosks outside the mall",
     [("Site", "Periphery poles"), ("Approx. size", "36 × 72 in"), ("Type", "Front lit"),
      ("Material", "Fabric / Flex"), ("Indicative charge", "₹40,000 per pole")], "Deck status: available"),
]

# ---- Atrium activations (deck pp. 36–41)
ATRIUM = [
    ("atrium-10x10", "Central Atrium · up to 10 × 10 ft", "atrium-two-wheeler",
     "Two-wheeler brand display in the central atrium",
     [("Site", "Central atrium"), ("Approx. size", "Up to 10 × 10 ft"), ("Branding", "Pylons"),
      ("Installation", "11 PM – 6 AM"), ("Indicative charge", "₹1,75,000 + taxes per day")],
     "Deck status: ready to occupy"),
    ("atrium-8x8", "Central Atrium · 8 × 8 to 10 × 10 ft", "atrium-bikes-row",
     "Motorcycle line-up activation in the central atrium",
     [("Site", "Central atrium"), ("Approx. size", "8 × 8 ft to 10 × 10 ft"), ("Branding", "Pylons"),
      ("Installation", "11 PM – 6 AM"), ("Indicative charge", "₹2,50,000 + taxes for 2 days")],
     "Deck status: available"),
    ("atrium-12x16", "Central Atrium · 12 × 16 ft + car", "atrium-tata-curvv",
     "Car display activation with backdrop in the central atrium",
     [("Site", "Central atrium"), ("Approx. size", "12 × 16 ft"), ("Display", "1 car display"),
      ("Branding", "Pylons 3 × 8 ft"), ("Indicative charge", "₹1,50,000 + GST per day")],
     "Deck status: available"),
    ("atrium-display", "Central Atrium · Display 8 × 8 to 10 × 10 ft", "atrium-mg-hector",
     "Car display in the mall atrium with promotional standees",
     [("Site", "Central atrium (display)"), ("Approx. size", "8 × 8 ft to 10 × 10 ft"), ("Branding", "Pylons"),
      ("Installation", "11 PM – 6 AM"), ("Indicative charge", "₹1,50,000 + tax per day")],
     "Deck status: ready to occupy"),
    ("atrium-10x12", "Central Atrium · 10 × 12 ft + car", "atrium-car-display",
     "Premium car display activation in the central atrium",
     [("Site", "Central atrium"), ("Approx. size", "10 × 12 ft"), ("Display", "1 car display"),
      ("Branding", "Pylons 3 × 8 ft"), ("Indicative charge", "₹6,00,000 for 2 days")],
     "Deck status: available"),
    ("atrium-20x20", "Central Atrium · 20 × 20 ft with emcee", "atrium-stage-emcee",
     "Stage activation with emcee and sound in the central atrium",
     [("Site", "Central atrium"), ("Approx. size", "20 × 20 ft"), ("Format", "With emcee &amp; sound"),
      ("Installation", "11 PM – 6 AM"), ("Indicative charge", "₹1,50,000 + taxes per day")],
     "Deck status: available"),
]

KIOSKS = [
    ("kiosk-ff", "Kiosk · First Floor, beside Fashion", "kiosk-first-floor",
     "Branded promotional kiosk on the first floor beside the fashion zone",
     [("Site", "First floor, beside Fashion"), ("Approx. size", "4 × 4 ft or 6 × 6 ft"),
      ("Backdrop", "3 × 6 ft"), ("Installation", "11 PM – 6 AM"),
      ("Indicative charge", "₹3,00,000 + taxes per month")], "Deck status: ready to occupy"),
    ("kiosk-sf", "Kiosk · Second Floor, beside Connect", "kiosk-second-floor",
     "Branded promotional kiosk on the second floor beside Connect",
     [("Site", "Second floor, beside Connect"), ("Approx. size", "4 × 4 ft or 6 × 6 ft"),
      ("Backdrop", "3 × 6 ft"), ("Installation", "11 PM – 6 AM"),
      ("Indicative charge", "₹2,50,000 + tax")], "Deck status: ready to occupy"),
]

# ---- Mobile advertising (deck pp. 47–56)
MOBILE = [
    ("led-van", "LED Van", "led-van-street", "LED advertising van on a Hyderabad street",
     [("Coverage", "70 km per day"), ("Operating", "8 hours per day"), ("Format", "Digital LED screen"),
      ("Indicative rate", "₹2,50,000 / month")], "Own medium"),
    ("tata-ace", "Tata Ace", "tata-ace-road", "Tata Ace mobile branding vehicle on a city road",
     [("Coverage", "70 km per day"), ("Operating", "8 hours per day"), ("Format", "Panel branding"),
      ("Indicative rate", "₹75,000 / month")], "Indicative rate"),
    ("t-shape", "T-Shape Auto", "led-van-night", "T-shape auto branding running at night",
     [("Coverage", "70 km per day"), ("Operating", "8 hours per day"), ("Format", "T-shape panel"),
      ("Indicative rate", "₹75,000 / month")], "Indicative rate"),
    ("tricycle", "Tricycle Campaign", "tricycle-fleet", "Tricycle branding fleet deployed on a street",
     [("Coverage", "5 km"), ("Operating", "7 hours"), ("Format", "Twin-panel tricycle"),
      ("Indicative rate", "₹1,500 / day")], "Indicative rate"),
    ("look-walker", "Look Walkers", "look-walkers", "Look walkers carrying brand panels in a market area",
     [("Coverage", "5 km"), ("Operating", "7 hours"), ("Format", "Walker-mounted panel"),
      ("Indicative rate", "₹1,500 / day")], "Indicative rate"),
    ("auto-top", "Auto Tops", "auto-top-branding", "Auto rickshaw top branding in rexene",
     [("Format", "Rexene auto top, incl. pasting"), ("Minimum", "500 autos"), ("Area", "One area"),
      ("Indicative rate", "₹650 per auto")], "Indicative rate"),
    ("auto-sticker", "Auto Stickers", "auto-sticker-branding", "Auto rickshaw rear sticker branding",
     [("Format", "Rear sticker, incl. pasting"), ("Minimum", "500 autos"), ("Area", "One area"),
      ("Indicative rate", "₹120 per auto")], "Indicative rate"),
]

OUTDOOR = [
    ("wall-poster", "Digital Wall Posters", "wall-poster-campaign", "Digital wall poster campaign on a city wall",
     [("Format", "Digital wall poster"), ("Indicative rate", "₹25 per sq. ft"),
      ("Use", "High-density residential &amp; market walls")], "Indicative rate"),
    ("pole-kiosk", "Pole Kiosks", "pole-kiosk-campaign", "Pole kiosk branding along a road",
     [("Format", "Pole kiosk"), ("Use", "Arterial roads and colony entries"),
      ("Note", "Rate on requirement")], "On request"),
    ("round-flex", "Round Flex", "round-flex-campaign", "Round flex hoarding installed on a road divider",
     [("Format", "Round flex"), ("Size", "15 × 15"), ("Indicative rate", "₹9,000")], "Indicative rate"),
    ("no-parking", "No Parking Boards", "no-parking-boards", "No parking boards with brand advertising on a gate",
     [("Format", "No parking board"), ("Size", "18 in × 12 in"), ("Minimum", "500 boards"),
      ("Indicative rate", "₹29 per board")], "Indicative rate"),
]

WORK = [
    ("atrium-mercedes", "Mercedes-Benz atrium display", "mall-activation", "Mall Activation",
     "LuLu Mall, Hyderabad", "Central atrium · car display"),
    ("atrium-tata-curvv", "Tata Curvv.ev atrium launch display", "mall-activation", "Mall Activation",
     "LuLu Mall, Hyderabad", "Central atrium 12 × 16 ft"),
    ("atrium-mg-hector", "MG Hector mall display", "mall-activation", "Mall Activation",
     "LuLu Mall, Hyderabad", "Atrium display + standees"),
    ("atrium-bikes-row", "Two-wheeler line-up activation", "mall-activation", "Mall Activation",
     "LuLu Mall, Hyderabad", "Atrium 8 × 8 to 10 × 10 ft"),
    ("atrium-stage-emcee", "Stage activation with emcee and sound", "promotional", "Promotional Campaign",
     "LuLu Mall, Hyderabad", "Atrium 20 × 20 ft"),
    ("kiosk-first-floor", "Brand kiosk, first floor", "mall-activation", "Mall Activation",
     "LuLu Mall, Hyderabad", "Kiosk 4 × 4 / 6 × 6 ft"),
    ("atrium-kiosk-brand", "In-mall brand engagement counter", "mall-activation", "Mall Activation",
     "LuLu Mall, Hyderabad", "Kiosk + backdrop"),
    ("facade-h1-h2-h3", "Mall façade hoardings H1 / H2 / H3", "outdoor", "Outdoor",
     "LuLu Mall, Hyderabad", "Front lit flex · 8.50 × 5.10 m"),
    ("facade-h6-h7", "Mall façade hoardings H6 / H7", "outdoor", "Outdoor",
     "LuLu Mall, Hyderabad", "Front lit flex · 11.90 × 8.50 m"),
    ("atrium-led-main", "Main atrium LED screen", "dooh", "DOOH",
     "LuLu Mall, Hyderabad", "2048 × 1152 · 20 sec spot"),
    ("floor-led-first", "Floor-level digital LED tower", "dooh", "DOOH",
     "LuLu Mall, Hyderabad", "360 × 960 · 10 sec spot"),
    ("lift-south-ff", "Lift lobby backlit media", "outdoor", "Outdoor",
     "LuLu Mall, Hyderabad", "Backlit fabric · 47.2 × 66.9 in"),
    ("cinepolis-lulu", "Cinema environment", "cinema", "Cinema",
     "Cinépolis, LuLu Mall Hyderabad", "5 screens · 1,427 seats"),
    ("led-van-street", "LED van campaign", "mobile", "Mobile Media",
     "Hyderabad", "70 km / day · 8 hours"),
    ("tata-ace-road", "Tata Ace real-estate campaign", "mobile", "Mobile Media",
     "Hyderabad", "70 km / day · 8 hours"),
    ("tricycle-fleet", "Tricycle campaign fleet", "promotional", "Promotional Campaign",
     "Telangana", "5 km · 7 hours"),
    ("look-walkers", "Look walker deployment", "promotional", "Promotional Campaign",
     "Hyderabad", "5 km · 7 hours"),
    ("auto-top-branding", "Auto top branding", "mobile", "Mobile Media",
     "Hyderabad", "Rexene · min. 500 autos"),
    ("wall-poster-campaign", "Digital wall poster campaign", "outdoor", "Outdoor",
     "Hyderabad", "₹25 per sq. ft"),
    ("no-parking-boards", "No parking board branding", "outdoor", "Outdoor",
     "Hyderabad", "18 × 12 in · min. 500"),
]
