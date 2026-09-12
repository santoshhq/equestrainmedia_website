# -*- coding: utf-8 -*-
"""Page bodies for the Equestrian Media site. Run this file to emit the HTML."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from components import *  # noqa

SWIPER_CSS = chr(10) + '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Swiper/11.1.14/swiper-bundle.min.css">'


def in_group(n):
    """Indian-grouped digits, matching the counter's en-IN toLocaleString output."""
    s = str(int(n))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts + [tail])

# ============================================================== shared blocks
def why_section():
    items = "".join(
        f'<li class="why"><span class="why__mark">{icon_check()}</span>'
        f'<span class="why__text">{w}</span></li>' for w in WHY
    )
    return f"""  <!-- ==================== WHY EQUESTRIAN MEDIA ==================== -->
  <section class="section section--dark" id="why">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">Why brands choose us</p>
          <h2 class="section-head__title" data-reveal-lines>
            {lines('Built around', '<span class="red">real-world impact.</span>')}
          </h2>
        </div>
        <div class="section-head__aside">
          <p class="lead">Nine reasons brands hand us the ground. Every one of them is something
          you can hold us to on the day of execution.</p>
        </div>
      </div>
      <ul class="why-list" data-reveal-group>{items}</ul>
      <p class="source-note u-mt-1">Source: Equestrian Media deck.</p>
    </div>
  </section>
"""


def process_section(dark=False):
    steps = "".join(
        f"""        <li class="step">
          <span class="step__num">{n}</span>
          <h3 class="step__title">{t}</h3>
          <p class="step__body">{b}</p>
        </li>""" for n, t, b in PROCESS
    )
    cls = " section--dark" if dark else ""
    return f"""  <!-- ==================== CAMPAIGN PROCESS ==================== -->
  <section class="section{cls}" id="process">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">Campaign process</p>
          <h2 class="section-head__title" data-reveal-lines>
            {lines('From brief', 'to visibility.')}
          </h2>
        </div>
        <div class="section-head__aside">
          <p class="lead">Our process is our tagline, in order:
          <strong>Strategize</strong>, <strong>Activate</strong>, <strong>Elevate</strong>.</p>
        </div>
      </div>
      <ol class="process">{steps}</ol>
    </div>
  </section>
"""


def brands_marquee():
    row = "".join(
        f'<li class="marquee__item">{b}</li><li class="marquee__sep" aria-hidden="true"></li>'
        for b in BRANDS
    )
    return f"""  <!-- ==================== BRANDS & ENVIRONMENTS ==================== -->
  <section class="section section--tight">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">Portfolio environment</p>
          <h2 class="section-head__title" data-reveal-lines>
            {lines('Brands &amp; environments', 'in our media portfolio.')}
          </h2>
        </div>
        <div class="section-head__aside">
          <p class="muted text-sm">Brands and retail environments appearing within the
          media and activation portfolio documented in our deck. Names and marks belong to their
          respective owners; their appearance does not imply a client relationship.</p>
        </div>
      </div>
    </div>
    <div class="marquee" aria-label="Brands and environments featured in our media portfolio">
      <ul class="marquee__track">{row}{row}</ul>
    </div>
  </section>
"""


def cinema_section():
    strip = '<div class="filmstrip"><div class="filmstrip__row">' + ('<i></i>' * 40) + '</div></div>'
    return f"""  <!-- ==================== CINEMA ADVERTISING ==================== -->
  <section class="section section--dark section--flush-bottom" id="cinema">
    <div class="wrap">
      <div class="split split--center">
        <div>
          <p class="eyebrow">Cinema advertising</p>
          <h2 class="split__title" data-reveal-lines>
            {lines('Your brand.', 'Before the movie', '<span class="red">even begins.</span>')}
          </h2>
          <p class="lead u-mt-1" data-reveal>
            Cinema puts your brand in front of a seated, undistracted audience in a premium
            environment. The Cinépolis multiplex documented in our deck features five screens
            and 1,427 seats, with Dolby Atmos and RealD 3D.
          </p>
          <ul class="pill-row u-mt-2" data-reveal>
            <li class="pill">5 Screens</li>
            <li class="pill">1,427 Seats</li>
            <li class="pill">Dolby Atmos</li>
            <li class="pill">RealD 3D</li>
            <li class="pill">Premium South India market</li>
          </ul>
          <div class="actions" data-reveal>
            <a class="btn btn--on-dark" href="contact.html" data-cursor="EXPLORE">
              <span>Discuss cinema advertising</span>{arrow()}
            </a>
          </div>
          <p class="source-note u-mt-1">Source: Equestrian Media deck.</p>
        </div>
        <figure class="reveal-img u-flush">
          {img('cinepolis-lulu', 'Cinépolis multiplex entrance at LuLu Mall, Hyderabad', sizes='(max-width:1024px) 92vw, 46vw')}
        </figure>
      </div>
    </div>
    <div class="u-mt-5">{strip}</div>
  </section>
"""


def contact_block(dark=False):
    """Lead capture form + direct contact details."""
    services = ["Mall Branding", "Atrium Activation", "Kiosk Promotion", "DOOH / LED Media",
                "Cinema Advertising", "Mobile Advertising (LED Van / Tata Ace / T-Shape)",
                "Auto Branding", "Tricycle / Look Walkers", "Outdoor Advertising (Hoardings / Poles)",
                "Digital Wall Posters / No Parking Boards", "Corporate Marketing", "Not sure yet"]
    options = "".join(f'<option value="{s}">{s}</option>' for s in services)
    durations = ["1 day", "2–7 days", "15 days", "1 month", "3 months", "6 months+", "To be decided"]
    dur_options = "".join(f'<option value="{d}">{d}</option>' for d in durations)

    return f"""      <div class="split">
        <div>
          <p class="eyebrow">Request a media plan</p>
          <h2 class="split__title" data-reveal-lines>
            {lines('Ready to make', 'your brand', '<span class="red">visible?</span>')}
          </h2>
          <p class="lead u-mt-1">
            Tell us what you're planning. We'll help you identify the right media and
            activation opportunity.
          </p>

          <dl class="contact-lines u-mt-3">
            <div class="contact-line"><dt>Contact</dt><dd>{CONTACT}</dd></div>
            <div class="contact-line"><dt>Company</dt><dd>Equestrian Media Pvt. Ltd.</dd></div>
            <div class="contact-line"><dt>Phone</dt><dd><a href="tel:{PHONE_RAW}">{PHONE}</a></dd></div>
            <div class="contact-line"><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
            <div class="contact-line"><dt>Markets</dt><dd>Hyderabad · Telangana · Andhra Pradesh</dd></div>
          </dl>
        </div>

        <div>
          <form class="form-grid" data-contact-form action="#" method="post" novalidate>
            <div class="field">
              <label for="f-name">Name <span class="req" aria-hidden="true">*</span></label>
              <input id="f-name" name="name" type="text" autocomplete="name" required data-label="Name"
                     placeholder="Your full name">
              <p class="field__error" aria-live="polite"></p>
            </div>
            <div class="field">
              <label for="f-company">Company <span class="req" aria-hidden="true">*</span></label>
              <input id="f-company" name="company" type="text" autocomplete="organization" required
                     data-label="Company" placeholder="Brand or company name">
              <p class="field__error" aria-live="polite"></p>
            </div>
            <div class="field">
              <label for="f-phone">Phone <span class="req" aria-hidden="true">*</span></label>
              <input id="f-phone" name="phone" type="tel" autocomplete="tel" required data-label="Phone"
                     placeholder="+91 00000 00000">
              <p class="field__error" aria-live="polite"></p>
            </div>
            <div class="field">
              <label for="f-email">Email <span class="req" aria-hidden="true">*</span></label>
              <input id="f-email" name="email" type="email" autocomplete="email" required data-label="Email"
                     placeholder="name@company.com">
              <p class="field__error" aria-live="polite"></p>
            </div>
            <div class="field field--full">
              <label for="f-objective">Campaign objective</label>
              <input id="f-objective" name="objective" type="text" data-label="Campaign objective"
                     placeholder="Product launch, footfall, awareness, offer promotion…">
              <p class="field__error" aria-live="polite"></p>
            </div>
            <div class="field">
              <label for="f-service">Required service</label>
              <span class="select-wrap">
                <select id="f-service" name="service" data-label="Required service">
                  <option value="">Select a service</option>{options}
                </select>
              </span>
              <p class="field__error" aria-live="polite"></p>
            </div>
            <div class="field">
              <label for="f-location">Preferred location</label>
              <input id="f-location" name="location" type="text" data-label="Preferred location"
                     placeholder="Hyderabad, LuLu Mall, Kukatpally…">
              <p class="field__error" aria-live="polite"></p>
            </div>
            <div class="field field--full">
              <label for="f-duration">Campaign duration</label>
              <span class="select-wrap">
                <select id="f-duration" name="duration" data-label="Campaign duration">
                  <option value="">Select a duration</option>{dur_options}
                </select>
              </span>
              <p class="field__error" aria-live="polite"></p>
            </div>
            <div class="field field--full">
              <label for="f-message">Message</label>
              <textarea id="f-message" name="message" data-label="Message"
                        placeholder="Tell us about the campaign, dates and any sites you already have in mind."></textarea>
              <p class="field__error" aria-live="polite"></p>
            </div>
            <div class="field field--full">
              <button class="btn btn--lg btn--block" type="submit" data-cursor="EXPLORE">Request a media plan</button>
              <p class="form-status" role="status" aria-live="polite" hidden></p>
              <p class="form-note">We reply to campaign briefs within one working day. Prefer to talk?
                Call <a href="tel:{PHONE_RAW}" class="link-red">{PHONE}</a>.</p>
            </div>
          </form>
        </div>
      </div>"""


# ============================================================== INDEX
def build_index():
    page = "index.html"

    services_rows = "".join(f"""        <a class="service" href="services.html#{slug}" data-cursor="EXPLORE">
          {img(image, '', cls='service__thumb', sizes='250px')}
          <span class="service__inner wrap">
            <span class="service__num">{num}</span>
            <span class="service__title h3">{title}</span>
            <span class="service__body">{desc}
              <span class="service__tags">{"".join(f'<span>{t}</span>' for t in tags)}</span>
            </span>
            <span class="service__arrow">{icon_arrow_ur()}</span>
          </span>
        </a>""" for num, title, slug, desc, tags, image in SERVICE_PILLARS)

    solutions = [
        ("Mall Media", "mall-media", "lulu-facade-day", "Façade hoardings, atriums, kiosks, lift lobbies and backlit boards."),
        ("DOOH", "dooh", "atrium-led-main", "Main atrium LED and floor-level digital screens on scheduled rotations."),
        ("Cinema", "cinema", "cinepolis-lulu", "On-screen and in-cinema presence in a premium multiplex environment."),
        ("Mobile Media", "mobile-media", "led-van-street", "LED vans, Tata Ace, T-shape autos, auto tops and stickers."),
        ("On-Ground Activation", "atrium-activations", "atrium-stage-emcee", "Atrium activations, kiosks, sampling, emcee-led engagement."),
        ("Outdoor Branding", "outdoor", "wall-poster-campaign", "Wall posters, pole kiosks, flex hoardings, no-parking boards."),
    ]
    solution_cards = "".join(f"""        <a class="work-card" href="media-solutions.html#{slug}" data-cursor="VIEW MEDIA">
          <span class="work-card__figure reveal-img">
            {img(image, alt, sizes='(max-width:767px) 92vw, (max-width:1024px) 46vw, 31vw')}
          </span>
          <span class="work-card__meta"><span class="cat">Media solution</span></span>
          <span class="work-card__title h4">{title}</span>
          <span class="work-card__desc">{alt}</span>
        </a>""" for title, slug, image, alt in solutions)

    hscroll_items = [
        ("lulu-facade-night", "Mall façade at night", "Façade"),
        ("atrium-led-main", "Main atrium LED screen", "DOOH"),
        ("atrium-mercedes", "Car display activation", "Atrium"),
        ("floor-led-second", "Floor-level LED tower", "DOOH"),
        ("lift-south-ff", "Lift lobby backlit boards", "Backlit"),
        ("travelator-billboards", "Travelator billboards", "Billboard"),
        ("kiosk-second-floor", "Promotional kiosk", "Kiosk"),
        ("atrium-bikes-row", "Two-wheeler activation", "Atrium"),
        ("periphery-poles", "Periphery pole kiosks", "Outdoor"),
    ]
    hscroll = "".join(f"""          <figure class="hscroll__item u-flush">
            {img(name, alt, sizes='(max-width:767px) 78vw, 30vw')}
            <figcaption class="hscroll__cap"><span>{alt}</span><span>{tag}</span></figcaption>
          </figure>""" for name, alt, tag in hscroll_items)

    mall_stats = [
        ("5", " Lakh", "Sq. ft. mall area"),
        ("1900", "+", "Parking capacity"),
        ("90", "+", "National &amp; international brands"),
        ("20", "+", "Internal signages"),
        ("5", "", "Façade locations"),
        ("30", "+", "Food court brands"),
    ]
    stats_html = "".join(f"""          <div class="stat">
            <p class="stat__num"><span data-count="{n}">{in_group(n)}</span><span class="suffix">{s}</span></p>
            <p class="stat__label">{label}</p>
          </div>""" for n, s, label in mall_stats)

    footfall = [("25000", "Average daily footfall"), ("40000", "Average weekend footfall"),
                ("70000", "Footfall during occasions (per day)")]
    footfall_html = "".join(f"""          <div class="stat">
            <p class="stat__num"><span data-count="{n}">{in_group(n)}</span><span class="suffix">+</span></p>
            <p class="stat__label">{label}</p>
          </div>""" for n, label in footfall)

    return head(
        "Equestrian Media | BTL Marketing, Brand Activation &amp; Outdoor Advertising",
        "Equestrian Media is a Hyderabad-based BTL marketing, brand activation and outdoor "
        "advertising company delivering on-ground campaigns, mall branding, DOOH, cinema "
        "advertising and mobile advertising solutions.",
        page,
        keywords="BTL Marketing Hyderabad, Brand Activation Hyderabad, Outdoor Advertising Hyderabad, "
                 "Mall Branding Hyderabad, DOOH Advertising Hyderabad, Cinema Advertising Hyderabad, "
                 "Mobile Advertising Hyderabad, BTL Activation Telangana, Outdoor Media Telangana, "
                 "Brand Promotion Hyderabad",
    ) + header(page) + f"""  <main id="main">

  <!-- ==================== HERO ==================== -->
  <section class="hero" data-hero>
    <div class="wrap hero__grid">
      <div>
        <p class="eyebrow">BTL Marketing · Brand Activation · Outdoor Advertising</p>
        <h1 class="hero__title" data-reveal-lines data-hero-title>
          {lines('On-ground', 'marketing.', 'Built for', '<span class="red">visibility.</span>')}
        </h1>
        <p class="hero__sub">
          Equestrian Media delivers BTL marketing, brand activations, outdoor advertising and
          high-impact media solutions that connect brands with audiences on the ground.
        </p>
        <div class="actions">
          <a class="btn btn--compact" href="contact.html" data-cursor="EXPLORE">
            <span>Plan your campaign</span>{arrow()}
          </a>
          <a class="btn btn--outline btn--compact" href="media-solutions.html" data-cursor="VIEW MEDIA">
            <span>Explore our media</span>
          </a>
        </div>
      </div>

      <div class="hero__stage">
        <span class="hero__visual-wrap">
          <img class="hero__visual" src="assets/images/hero-media-environment.webp"
               srcset="assets/images/hero-media-environment-sm.webp 640w,
                       assets/images/hero-media-environment.webp 1140w"
               sizes="(max-width: 767px) 92vw, (max-width: 1024px) 520px, 530px"
               width="1140" height="698"
               alt="Mall façade branding, cinema advertising, brand activation stand, billboard, DOOH screen and LED van mobile advertising"
               fetchpriority="high" decoding="async">
        </span>
      </div>
    </div>

    <div class="wrap">
      <ul class="hero__foot">
        <li>Hyderabad</li>
        <li>Telangana</li>
        <li>Andhra Pradesh</li>
        <li>Official advertising rights — LuLu Mall, Hyderabad</li>
      </ul>
    </div>
  </section>

  <!-- ==================== TAGLINE ==================== -->
  <section class="tagline" aria-label="Strategize, Activate, Elevate">
    <div class="wrap">
      <div class="tagline__inner" data-reveal-group>
        <p class="tagline__word"><span class="tagline__num">01</span>Strategize</p>
        <p class="tagline__word"><span class="tagline__num">02</span>Activate</p>
        <p class="tagline__word"><span class="tagline__num">03</span>Elevate</p>
      </div>
    </div>
  </section>

  <!-- ==================== ABOUT ==================== -->
  <section class="section" id="about">
    <div class="wrap split">
      <div>
        <p class="eyebrow">About Equestrian Media</p>
        <h2 class="split__title" data-reveal-lines>
          {lines('Built around', '<span class="red">real-world impact.</span>')}
        </h2>
        <div class="geo-line" data-reveal>
          <span class="geo-line__bar" aria-hidden="true"></span>
          <p class="geo-line__text">
            Hyderabad | Telangana | Andhra Pradesh
            <small>On-ground execution across the two-state market.</small>
          </p>
        </div>
      </div>
      <div data-reveal>
        <p class="lead">
          Equestrian Media Private Limited is a Hyderabad-based BTL Marketing, Brand Activation
          and Outdoor Advertising Company.
        </p>
        <p class="u-mt-1">
          We specialize in innovative on-ground marketing campaigns that connect brands directly
          with their target audience. Our customized BTL solutions help businesses increase brand
          visibility, customer engagement and market reach across Telangana and Andhra Pradesh.
        </p>
        <div class="actions">
          <a class="link-arrow" href="about.html">About the company {icon_arrow_ur()}</a>
        </div>
        <p class="source-note u-mt-3">Source: Equestrian Media deck.</p>
      </div>
    </div>
  </section>

  <!-- ==================== SERVICES ==================== -->
  <section class="section section--wash u-bleed" id="services">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">What we do</p>
          <h2 class="section-head__title" data-reveal-lines>
            {lines('Five ways we put', 'brands in front', 'of people.')}
          </h2>
        </div>
        <div class="section-head__aside">
          <p class="lead">Corporate marketing, BTL activations, mall branding, cinema advertising
          and DOOH — planned and executed by one team.</p>
        </div>
      </div>
    </div>
    <div class="service-list">{services_rows}
    </div>
  </section>

  <!-- ==================== MEDIA SOLUTIONS ==================== -->
  <section class="section" id="media-solutions">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">Media solutions</p>
          <h2 class="section-head__title" data-reveal-lines>
            {lines('Put your brand', '<span class="red">where people are.</span>')}
          </h2>
        </div>
        <div class="section-head__aside">
          <p class="lead">Physical media inventory across malls, digital screens, cinema,
          vehicles and street-level outdoor.</p>
          <a class="link-arrow u-mt-1" href="media-solutions.html">
            View full inventory {icon_arrow_ur()}
          </a>
        </div>
      </div>
      <div class="work-grid">{solution_cards}
      </div>
    </div>
  </section>

  <!-- ==================== MEDIA ENVIRONMENT (horizontal gallery) ==================== -->
  <section class="section section--dark u-clip" data-hscroll>
    <div class="wrap">
      <p class="eyebrow">Inside the environment</p>
      <h2 class="h2 u-mb-3" data-reveal-lines>
        {lines('Real sites.', 'Real execution.')}
      </h2>
    </div>
    <div class="wrap hscroll">
      <div class="hscroll__track">{hscroll}
      </div>
    </div>
  </section>

  <!-- ==================== LULU MALL FEATURE ==================== -->
  <section class="band" id="lulu">
    <img class="band__img" data-parallax="14" src="assets/images/lulu-aerial-night-sm.webp"
         srcset="assets/images/lulu-aerial-night-sm.webp 800w, assets/images/lulu-aerial-night.webp 1600w"
         sizes="100vw" alt="Aerial night view of LuLu Mall, Hyderabad" loading="lazy" decoding="async">
    <div class="wrap band__content">
      <p class="eyebrow">Official advertising rights</p>
      <h2 class="band__title" data-reveal-lines>{lines('LuLu Mall,', 'Hyderabad.')}</h2>
      <p class="lead measure--narrow u-mt-1" data-reveal>
        <span class="hl">Equestrian Media holds official advertising rights for LuLu Mall,
        Hyderabad — façade, atrium, DOOH, kiosk, lift lobby and backlit media inside one of the
        city's highest-footfall retail environments.</span>
      </p>
      <div class="actions" data-reveal>
        <a class="btn btn--on-dark" href="media-solutions.html#mall-media" data-cursor="VIEW MEDIA">
          <span>See the mall inventory</span>{arrow()}
        </a>
      </div>
    </div>
  </section>

  <section class="section section--dark section--tight">
    <div class="wrap">
      <div class="stats" data-reveal-group>{stats_html}
      </div>
      <p class="eyebrow u-mt-4">Footfall</p>
      <div class="stats" data-reveal-group>{footfall_html}
      </div>
      <p class="source-note u-mt-1">
        Quick facts and footfall figures as supplied in the Equestrian Media media deck. These are
        deck figures, not independently verified current statistics.
      </p>
    </div>
  </section>

{cinema_section()}
{why_section()}
{process_section()}
{brands_marquee()}
{cta_final()}
  </main>
""" + footer()


# ============================================================== ABOUT
def build_about():
    page = "about.html"
    return head(
        "About | Equestrian Media — BTL Marketing &amp; Brand Activation, Hyderabad",
        "Equestrian Media Private Limited is a Hyderabad-based BTL marketing, brand activation and "
        "outdoor advertising company delivering on-ground campaigns across Telangana and Andhra Pradesh.",
        page,
        keywords="BTL Marketing Hyderabad, Brand Activation Hyderabad, BTL Activation Telangana, "
                 "Outdoor Media Telangana, Brand Promotion Hyderabad",
    ) + header(page) + f"""  <main id="main">
{page_hero('About us', ['Built around', '<span class="red">real-world impact.</span>'],
           'A Hyderabad-based BTL marketing, brand activation and outdoor advertising company '
           'built for on-ground execution.', 'About')}

  <!-- ==================== COMPANY ==================== -->
  <section class="section">
    <div class="wrap split">
      <div>
        <h2 class="split__title" data-reveal-lines>
          {lines('We connect brands', 'directly with', '<span class="red">their audience.</span>')}
        </h2>
        <div class="geo-line" data-reveal>
          <span class="geo-line__bar" aria-hidden="true"></span>
          <p class="geo-line__text">
            Hyderabad | Telangana | Andhra Pradesh
            <small>On-ground execution across the two-state market.</small>
          </p>
        </div>
      </div>
      <div data-reveal>
        <p class="lead">
          Equestrian Media Private Limited is a Hyderabad-based BTL Marketing, Brand Activation
          and Outdoor Advertising Company.
        </p>
        <p class="u-mt-1">
          We specialize in innovative on-ground marketing campaigns that connect brands directly
          with their target audience. Our customized BTL solutions help businesses increase brand
          visibility, customer engagement and market reach across Telangana and Andhra Pradesh.
        </p>
        <p class="u-mt-1">
          Our work spans mall branding and atrium activations, digital out-of-home and cinema,
          mobile media across the city, and street-level outdoor advertising — planned, produced
          and executed by one team.
        </p>
        <p class="source-note u-mt-3">Source: Equestrian Media deck.</p>
      </div>
    </div>
  </section>

  <!-- ==================== ENVIRONMENT BAND ==================== -->
  <section class="band">
    <img class="band__img" data-parallax="12" src="assets/images/lulu-aerial-sm.webp"
         srcset="assets/images/lulu-aerial-sm.webp 800w, assets/images/lulu-aerial.webp 1600w"
         sizes="100vw" alt="Aerial view of the Hyderabad retail and growth corridor" loading="lazy" decoding="async">
    <div class="wrap band__content">
      <p class="eyebrow">Hyderabad market</p>
      <h2 class="band__title" data-reveal-lines>{lines('We know', 'the ground.')}</h2>
      <p class="lead measure--narrow u-mt-1" data-reveal>
        Strong local market presence, fast execution and access to premium media inventory in the
        environments where Hyderabad's audiences actually spend their time.
      </p>
    </div>
  </section>

{why_section()}
{process_section()}

  <!-- ==================== CTA BAND ==================== -->
  <section class="section section--tight">
    <div class="wrap">
      <div class="cta-band" data-reveal>
        <h2 class="cta-band__title">Looking for a media and activation partner in Hyderabad?</h2>
        <a class="btn btn--on-dark btn--lg" href="contact.html" data-cursor="EXPLORE">
          <span>Plan your campaign</span>{arrow()}
        </a>
      </div>
    </div>
  </section>

{cta_final()}
  </main>
""" + footer()


# ============================================================== SERVICES
def build_services():
    page = "services.html"

    # Each pillar is both an anchor target (linked from the home page) and a link
    # onward to the detail section that covers it.
    pillar_target = {
        "corporate-marketing": "#brand-activation",
        "btl-activations": "#brand-activation",
        "mall-branding": "media-solutions.html#mall-media",
        "cinema-advertising": "media-solutions.html#cinema",
        "dooh": "media-solutions.html#dooh",
    }
    pillars = "".join(f"""        <a class="service" id="{slug}" href="{pillar_target[slug]}" data-cursor="EXPLORE">
          {img(image, '', cls='service__thumb', sizes='250px')}
          <span class="service__inner wrap">
            <span class="service__num">{num}</span>
            <span class="service__title h3">{title}</span>
            <span class="service__body">{desc}
              <span class="service__tags">{"".join(f'<span>{t}</span>' for t in tags)}</span>
            </span>
            <span class="service__arrow">{icon_arrow_ur()}</span>
          </span>
        </a>""" for num, title, slug, desc, tags, image in SERVICE_PILLARS)

    detail = [
        ("01", "Brand Activation", "brand-activation",
         "Activations that place your product, your people and your message directly in front of "
         "customers in high-footfall environments.",
         ["Mall Activations", "Retail Promotions", "Corporate Events"],
         "atrium-stage-emcee", "Stage activation with emcee and sound in a mall atrium", False),
        ("02", "Mobile Advertising", "mobile-advertising",
         "Media that moves through the city — reaching audiences on routes, at junctions and in "
         "neighbourhoods that fixed media cannot cover.",
         ["Tata Ace LED Vans", "Bolero LED Vehicles", "Auto Hood Branding", "T-Shape Auto Branding",
          "Auto Boom Campaigns"],
         "led-van-street", "LED advertising van running a campaign on a Hyderabad street", True),
        ("03", "Outdoor Advertising", "outdoor-advertising",
         "Street-level visibility built at scale — the formats that make a brand unavoidable across "
         "a catchment.",
         ["Digital Wall Posters", "Pole Kiosks", "Flex Hoardings", "No Parking Boards", "Street Branding"],
         "pole-kiosk-campaign", "Pole kiosk and street branding campaign", False),
        ("04", "Promotional Campaigns", "promotional-campaigns",
         "Manpower-led campaigns that carry a message into markets, colonies and campuses — and put "
         "product into people's hands.",
         ["Tricycle Campaigns", "Walkers &amp; Look Walkers", "Sampling Activities"],
         "tricycle-fleet", "Tricycle campaign fleet deployed across a market area", True),
    ]

    detail_html = ""
    for num, title, slug, desc, items, image, alt, reverse in detail:
        li = "".join(f'<li class="pill">{i}</li>' for i in items)
        rev = " feature--reverse" if reverse else ""
        detail_html += f"""  <section class="section{' section--wash' if reverse else ''}" id="{slug}">
    <div class="wrap feature{rev}">
      <figure class="feature__media reveal-img u-flush">
        {img(image, alt, sizes='(max-width:1024px) 92vw, 46vw')}
        <figcaption class="feature__tag">Service {num}</figcaption>
      </figure>
      <div>
        <p class="eyebrow">Service {num}</p>
        <h2 class="h2 u-uc" data-reveal-lines>{lines(title)}</h2>
        <p class="lead u-mt-1" data-reveal>{desc}</p>
        <ul class="pill-row u-mt-2" data-reveal>{li}</ul>
        <div class="actions" data-reveal>
          <a class="btn" href="contact.html" data-cursor="EXPLORE"><span>Discuss this service</span>{arrow()}</a>
        </div>
      </div>
    </div>
  </section>
"""

    rate_rows = "".join(f"""            <tr>
              <th scope="row">{name}</th>
              <td>{rate}</td>
              <td>{cover}</td>
              <td>{hours}</td>
            </tr>""" for name, rate, cover, hours in [
        ("LED Van", "₹2,50,000 / month", "70 km", "8 hrs per day"),
        ("Tata Ace", "₹75,000 / month", "70 km", "8 hrs per day"),
        ("T-Shape Auto", "₹75,000 / month", "70 km", "8 hrs per day"),
        ("Tricycle", "₹1,500 / day", "5 km", "7 hrs"),
        ("Look Walkers", "₹1,500 / day", "5 km", "7 hrs"),
        ("Auto Tops", "₹650 per auto", "Min. 500 autos", "One area"),
        ("Auto Stickers", "₹120 per auto", "Min. 500 autos", "One area"),
    ])

    return head(
        "Services | BTL Activations, Mobile &amp; Outdoor Advertising — Equestrian Media",
        "Brand activation, mobile advertising, outdoor advertising and promotional campaigns from "
        "Equestrian Media — a Hyderabad BTL marketing and outdoor advertising company.",
        page,
        keywords="BTL Marketing Hyderabad, Brand Activation Hyderabad, Mobile Advertising Hyderabad, "
                 "Outdoor Advertising Hyderabad, Brand Promotion Hyderabad",
    ) + header(page) + f"""  <main id="main">
{page_hero('Services', ['What we do', '<span class="red">on the ground.</span>'],
           'Corporate marketing, BTL activations, mall branding, cinema advertising and DOOH — '
           'plus the mobile, outdoor and promotional formats that carry a campaign across a city.',
           'Services')}

  <!-- ==================== PILLARS ==================== -->
  <section class="section section--tight u-bleed">
    <div class="wrap">
      <p class="eyebrow">Core capabilities</p>
    </div>
    <div class="service-list">{pillars}
    </div>
  </section>

{detail_html}
  <!-- ==================== MOBILE MEDIA RATES ==================== -->
  <section class="section" id="rates">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">Mobile &amp; promotional media</p>
          <h2 class="section-head__title" data-reveal-lines>{lines('Indicative', 'rate card.')}</h2>
        </div>
        <div class="section-head__aside">
          <p class="lead">Deck figures for the mobile and promotional formats we operate.</p>
        </div>
      </div>

      <div class="u-scroll-x" data-reveal>
        <table class="rate-table">
          <caption class="visually-hidden">Indicative rates for mobile and promotional media formats</caption>
          <thead>
            <tr>
              <th scope="col">Format</th>
              <th scope="col">Indicative rate</th>
              <th scope="col">Coverage</th>
              <th scope="col">Operating</th>
            </tr>
          </thead>
          <tbody>{rate_rows}
          </tbody>
        </table>
      </div>

      <div class="u-mt-2">
        {note('<strong>Indicative rates from the supplied media deck.</strong> Contact us for current campaign pricing and availability. Rates exclude taxes unless stated and are subject to route, duration and artwork requirements.')}
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <div class="cta-band" data-reveal>
        <h2 class="cta-band__title">Not sure which format fits your objective?</h2>
        <a class="btn btn--on-dark btn--lg" href="contact.html" data-cursor="EXPLORE">
          <span>Request a media plan</span>{arrow()}
        </a>
      </div>
    </div>
  </section>

{cta_final()}
  </main>
""" + footer()


# ============================================================== MEDIA SOLUTIONS
def build_media():
    page = "media-solutions.html"

    anchors = [("mall-media", "Mall Media"), ("dooh", "DOOH / LED"), ("floor-led", "Floor LED"),
               ("atrium-activations", "Atrium"), ("kiosks", "Kiosks"), ("backlit", "Lift Lobby &amp; Backlit"),
               ("cinema", "Cinema"), ("mobile-media", "Mobile Media"), ("outdoor", "Outdoor")]
    anchor_html = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in anchors)

    def cards(dataset, kicker):
        return "".join(
            media_card(cid, kicker, title, image, alt, specs, avail, note_text=AVAIL_NOTE)
            for cid, title, image, alt, specs, avail in dataset
        )


    gallery_shots = [
        ("lulu-facade-night", "LuLu Mall façade lit at night", "Façade"),
        ("atrium-led-main", "Main atrium LED screen", "DOOH"),
        ("atrium-mercedes", "Car display activation in the atrium", "Atrium"),
        ("floor-led-third", "Floor-level digital LED tower", "Floor LED"),
        ("travelator-billboards", "Travelator billboards", "Billboard"),
        ("backlit-ug-entry", "Upper ground entrance backlit board", "Backlit"),
        ("kiosk-first-floor", "Promotional kiosk in the shopper flow", "Kiosk"),
        ("periphery-poles", "Front-lit periphery poles", "Outdoor"),
        ("atrium-crowd", "Shopper footfall inside the mall", "Environment"),
    ]
    gallery = "".join(f"""            <figure class="swiper-slide u-flush">
              {img(n, a, sizes='(max-width:767px) 88vw, (max-width:1024px) 46vw, 31vw')}
              <figcaption class="hscroll__cap"><span>{a}</span><span>{tag}</span></figcaption>
            </figure>""" for n, a, tag in gallery_shots)

    facade_cards = cards(FACADE, "Mall façade")
    backlit_cards = cards(BACKLIT, "Backlit &amp; billboards")
    atrium_cards = cards(ATRIUM, "Atrium activation")
    kiosk_cards = cards(KIOSKS, "Kiosk promotion")
    mobile_cards = cards(MOBILE, "Mobile media")
    outdoor_cards = cards(OUTDOOR, "Outdoor")

    dooh_specs = [("Site", "Main atrium"), ("Screen size", "2048 × 1152"), ("Ad duration", "20 seconds"),
                  ("Total slots", "9 slots"), ("Rotation", "3 minutes"), ("Rotations per day", "≈ 280"),
                  ("Mall hours", "9:00 – 23:00 (14 hrs)"), ("Formats", "JPG / MP4"),
                  ("Indicative charge", "₹2,50,000 / month")]
    floor_specs = [("Site", "1st, 2nd &amp; 3rd floor"), ("Resolution", "360 × 960"), ("Ad duration", "10 seconds"),
                   ("Total slots", "9 slots"), ("Rotation", "3 minutes"), ("Rotations per day", "≈ 780"),
                   ("Mall hours", "9:00 – 23:00 (14 hrs)"), ("Formats", "JPG / MP4"),
                   ("Indicative charge", "₹2,50,000 / month")]

    def spec_table(specs):
        return "".join(f'<div class="spec"><span class="spec__k">{k}</span>'
                       f'<span class="spec__v">{v}</span></div>' for k, v in specs)

    floor_cards = "".join(
        media_card(f"floor-led-{i}", "Floor LED", f"{label} Floor LED", image,
                   f"Digital LED tower on the {label.lower()} floor of the mall", floor_specs,
                   "Deck status: 3 slots available", note_text=AVAIL_NOTE)
        for i, (label, image) in enumerate([("First", "floor-led-first"), ("Second", "floor-led-second"),
                                            ("Third", "floor-led-third")], start=1)
    )

    return head(
        "Media Solutions | Mall Branding, DOOH, Cinema &amp; Mobile Media — Equestrian Media",
        "Mall branding, atrium activations, DOOH LED screens, kiosks, lift lobby backlit media, "
        "cinema and mobile advertising inventory in Hyderabad from Equestrian Media.",
        page,
        keywords="Mall Branding Hyderabad, DOOH Advertising Hyderabad, Cinema Advertising Hyderabad, "
                 "Mobile Advertising Hyderabad, Outdoor Advertising Hyderabad, Outdoor Media Telangana",
        extra=SWIPER_CSS,
    ) + header(page) + f"""  <main id="main">
{page_hero('Media solutions', ['Put your brand', '<span class="red">where people are.</span>'],
           'Physical media inventory across mall façade, atrium, DOOH, kiosks, lift lobbies, cinema, '
           'mobile media and street-level outdoor.', 'Media Solutions')}

  <nav class="anchor-nav" aria-label="Media sections">
    <div class="wrap"><ul class="anchor-nav__list">{anchor_html}</ul></div>
  </nav>

  <!-- ==================== MEDIA ENVIRONMENT CAROUSEL ==================== -->
  <section class="section section--tight">
    <div class="wrap">
      <p class="eyebrow">Media environment</p>
      <h2 class="h2 u-uc u-mb-3" data-reveal-lines>
        {lines('The sites,', 'as they stand.')}
      </h2>
      <div class="swiper" data-swiper data-per-view="3">
        <div class="swiper-wrapper">{gallery}
        </div>
      </div>
      <div class="swiper-nav">
        <button type="button" data-swiper-prev aria-label="Previous media">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>
        </button>
        <button type="button" data-swiper-next aria-label="Next media">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
        </button>
      </div>
    </div>
  </section>

  <!-- ==================== MALL MEDIA ==================== -->
  <section class="section" id="mall-media">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">Official advertising rights</p>
          <h2 class="section-head__title" data-reveal-lines>{lines('LuLu Mall,', 'Hyderabad.')}</h2>
        </div>
        <div class="section-head__aside">
          <p class="lead">Equestrian Media holds official advertising rights for LuLu Mall, Hyderabad.
          Façade, atrium, DOOH, kiosk and backlit media inside one retail environment.</p>
        </div>
      </div>

      <figure class="reveal-img figure-lead">
        {img('lulu-facade-day', 'LuLu Mall Hyderabad façade with brand hoardings', sizes='100vw')}
        <figcaption class="figure-caption">Mall façade — front-lit hoarding positions</figcaption>
      </figure>

      <h3 class="h3 u-uc u-mb-3">Mall façade inventory</h3>
      <div class="card-grid">{facade_cards}
      </div>
      <div class="u-mt-3">
        {note('<strong>Indicative media specifications</strong> — contact us for current availability and commercial confirmation. Artwork approval is by mall management; installation runs 11 PM – 6 AM.')}
      </div>
    </div>
  </section>

  <!-- ==================== DOOH ==================== -->
  <section class="section section--dark" id="dooh">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">DOOH · Digital out-of-home</p>
          <h2 class="section-head__title" data-reveal-lines>{lines('Main atrium', 'LED screen.')}</h2>
        </div>
        <div class="section-head__aside">
          <p class="lead">A 20-second spot in a nine-slot loop, running roughly 280 rotations a day
          across the mall's 14 operating hours.</p>
        </div>
      </div>

      <div class="feature">
        <figure class="feature__media reveal-img screen-mock u-flush">
          {img('atrium-led-main', 'Main atrium LED screen inside LuLu Mall, Hyderabad', sizes='(max-width:1024px) 92vw, 46vw')}
          <figcaption class="feature__tag">Main atrium LED</figcaption>
        </figure>
        <div>
          <div class="spec-list" data-reveal>{spec_table(dooh_specs)}</div>
          <p class="availability u-mt-1">Deck status: 3 slots available</p>
          <div class="actions">
            <a class="btn btn--on-dark" href="contact.html" data-cursor="EXPLORE">
              <span>Request media plan</span>{arrow()}
            </a>
          </div>
          <div class="u-mt-2">
            {note('<strong>Inventory shown from the media deck.</strong> Confirm current availability — sites are subject to availability at the time of final confirmation.')}
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ==================== FLOOR LED ==================== -->
  <section class="section" id="floor-led">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">Floor LED media</p>
          <h2 class="section-head__title" data-reveal-lines>{lines('Digital towers,', 'floor by floor.')}</h2>
        </div>
        <div class="section-head__aside">
          <p class="lead">Vertical 360 × 960 screens on the first, second and third floors —
          10-second spots, nine slots, roughly 780 rotations a day.</p>
        </div>
      </div>
      <div class="card-grid">{floor_cards}
      </div>
    </div>
  </section>

  <!-- ==================== ATRIUM ACTIVATIONS ==================== -->
  <section class="section section--wash" id="atrium-activations">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">On-ground activation</p>
          <h2 class="section-head__title" data-reveal-lines>{lines('Atrium', 'activations.')}</h2>
        </div>
        <div class="section-head__aside">
          <p class="lead">Central atrium footprints from 8 × 8 ft display spaces to a 20 × 20 ft
          stage with emcee and sound — including car and two-wheeler displays.</p>
        </div>
      </div>
      <div class="card-grid">{atrium_cards}
      </div>
      <div class="u-mt-3">
        {note('Examples are drawn from the media deck and are not fixed public packages. <strong>Request availability</strong> for your dates and format.')}
      </div>
    </div>
  </section>

  <!-- ==================== KIOSKS ==================== -->
  <section class="section" id="kiosks">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">Kiosk promotions</p>
          <h2 class="section-head__title" data-reveal-lines>{lines('Kiosks in the', 'shopper flow.')}</h2>
        </div>
        <div class="section-head__aside">
          <p class="lead">4 × 4 ft and 6 × 6 ft kiosk footprints with a 3 × 6 ft backdrop, positioned
          on the first and second floors.</p>
        </div>
      </div>
      <div class="card-grid card-grid--wide">{kiosk_cards}
      </div>
      <div class="actions">
        <a class="btn" href="contact.html" data-cursor="EXPLORE">
          <span>Check media availability</span>{arrow()}
        </a>
      </div>
    </div>
  </section>

  <!-- ==================== LIFT LOBBY / BACKLIT ==================== -->
  <section class="section section--wash" id="backlit">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">Lift lobby &amp; backlit media</p>
          <h2 class="section-head__title" data-reveal-lines>{lines('Backlit media,', 'floor to floor.')}</h2>
        </div>
        <div class="section-head__aside">
          <p class="lead">Backlit boards at every lift lobby north and south, ramp and travelator
          positions, billboards, easel standees and periphery poles.</p>
        </div>
      </div>
      <div class="card-grid">{backlit_cards}
      </div>
      <div class="u-mt-3">
        {note('Dimensions are reproduced as supplied. Where the deck does not state a specification, it is shown as <strong>not specified in deck</strong> rather than estimated.')}
      </div>
    </div>
  </section>

{cinema_section()}

  <!-- ==================== MOBILE MEDIA ==================== -->
  <section class="section" id="mobile-media">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">Mobile media</p>
          <h2 class="section-head__title" data-reveal-lines>{lines('Media that', 'moves.')}</h2>
        </div>
        <div class="section-head__aside">
          <p class="lead">LED vans, Tata Ace, T-shape autos, tricycles, look walkers, auto tops and
          auto stickers — covering routes fixed media cannot reach.</p>
        </div>
      </div>
      <div class="card-grid">{mobile_cards}
      </div>
      <div class="u-mt-3">
        {note('<strong>Indicative rates from the supplied media deck.</strong> Contact us for current campaign pricing and availability.')}
      </div>
    </div>
  </section>

  <!-- ==================== OUTDOOR ==================== -->
  <section class="section section--wash" id="outdoor">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">Outdoor branding</p>
          <h2 class="section-head__title" data-reveal-lines>{lines('Street-level', 'visibility.')}</h2>
        </div>
        <div class="section-head__aside">
          <p class="lead">Digital wall posters, pole kiosks, flex hoardings, round flex and no-parking
          boards deployed across a catchment.</p>
        </div>
      </div>
      <div class="card-grid">{outdoor_cards}
      </div>
    </div>
  </section>

  <!-- ==================== TERMS ==================== -->
  <section class="section section--tight">
    <div class="wrap">
      <h2 class="h3 u-uc u-mb-3">Branding &amp; promotions — terms</h2>
      <ul class="stack terms measure--wide">
        <li class="spec"><span class="spec__k">01</span><span class="spec__v">Blocked sites are held for 24 hours only, and released after that without prior intimation.</span></li>
        <li class="spec"><span class="spec__k">02</span><span class="spec__v">All sites are subject to availability at the time of final confirmation.</span></li>
        <li class="spec"><span class="spec__k">03</span><span class="spec__v">Faded or damaged creative must be replaced immediately; the same applies to clusters.</span></li>
        <li class="spec"><span class="spec__k">04</span><span class="spec__v">Printing is processed only after mail approval of creative and site.</span></li>
        <li class="spec"><span class="spec__k">05</span><span class="spec__v">100% advance payment applies to branding and promotional space; execution follows receipt of payment.</span></li>
        <li class="spec"><span class="spec__k">06</span><span class="spec__v">Campaign start and end dates are as per the invoice.</span></li>
      </ul>
      <p class="source-note u-mt-1">Source: Equestrian Media deck — Terms and Conditions, Branding &amp; Promotions.</p>
    </div>
  </section>

{cta_final()}
  </main>
""" + footer()


# ============================================================== WORK
def build_work():
    page = "work.html"

    cats = [("all", "All work"), ("mall-activation", "Mall Activation"), ("outdoor", "Outdoor"),
            ("dooh", "DOOH"), ("mobile", "Mobile Media"), ("cinema", "Cinema"),
            ("promotional", "Promotional Campaign")]
    filters = "".join(
        f'<button class="filter" type="button" data-filter="{key}" '
        f'aria-pressed="{"true" if key == "all" else "false"}">{label}</button>'
        for key, label in cats
    )

    cards = "".join(f"""        <article class="work-card" data-category="{cat}">
          <span class="work-card__figure reveal-img">
            {img(image, alt, sizes='(max-width:767px) 92vw, (max-width:1024px) 46vw, 31vw')}
          </span>
          <p class="work-card__meta">
            <span class="cat">{label}</span><span>{location}</span>
          </p>
          <h2 class="work-card__title">{alt}</h2>
          <p class="work-card__desc">{fmt} · Campaign execution showcase</p>
        </article>""" for image, alt, cat, label, location, fmt in WORK)

    return head(
        "Work | Campaign Execution Showcase — Equestrian Media Hyderabad",
        "Mall activations, outdoor, DOOH, cinema, mobile media and promotional campaign execution "
        "by Equestrian Media across Hyderabad, Telangana and Andhra Pradesh.",
        page,
        keywords="Brand Activation Hyderabad, Mall Branding Hyderabad, Outdoor Advertising Hyderabad, "
                 "Mobile Advertising Hyderabad, BTL Activation Telangana",
    ) + header(page) + f"""  <main id="main">
{page_hero('Work', ['Execution', '<span class="red">on the ground.</span>'],
           'A showcase of media and activation execution across mall, outdoor, DOOH, cinema, mobile '
           'and promotional formats.', 'Work')}

  <section class="section">
    <div class="wrap">
      <div class="filters" data-filter-group data-filter-target=".work-grid"
           data-filter-empty="#work-empty" role="group" aria-label="Filter work by category">{filters}
      </div>

      <div class="work-grid">{cards}
      </div>

      <p id="work-empty" class="lead" hidden>No work in this category yet.</p>

      <div class="u-mt-4">
        {note('Images are execution photography from the Equestrian Media media deck. Where the source does not record campaign results, entries are shown as <strong>campaign execution showcase</strong> rather than carrying invented metrics.')}
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <div class="cta-band" data-reveal>
        <h2 class="cta-band__title">Want execution like this for your brand?</h2>
        <a class="btn btn--on-dark btn--lg" href="contact.html" data-cursor="EXPLORE">
          <span>Plan your campaign</span>{arrow()}
        </a>
      </div>
    </div>
  </section>

{cta_final()}
  </main>
""" + footer()


# ============================================================== CONTACT
def build_contact():
    page = "contact.html"
    return head(
        "Contact | Request a Media Plan — Equestrian Media Hyderabad",
        "Contact Equestrian Media for BTL marketing, brand activation, mall branding, DOOH, cinema "
        "and mobile advertising in Hyderabad. Call +91 81060 39919.",
        page,
        keywords="BTL Marketing Hyderabad, Brand Activation Hyderabad, Outdoor Advertising Hyderabad, "
                 "Brand Promotion Hyderabad",
    ) + header(page) + f"""  <main id="main">
{page_hero('Contact', ['Ready to make', 'your brand', '<span class="red">visible?</span>'],
           "Tell us what you're planning. We'll help you identify the right media and activation "
           "opportunity.", 'Contact')}

  <section class="section">
    <div class="wrap">
{contact_block()}
    </div>
  </section>

  <section class="section section--dark section--tight">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="eyebrow">Where we work</p>
          <h2 class="section-head__title" data-reveal-lines>{lines('Hyderabad', 'and beyond.')}</h2>
        </div>
        <div class="section-head__aside">
          <p class="lead">On-ground execution across Telangana and Andhra Pradesh, with premium
          media inventory in Hyderabad's mall and cinema environments.</p>
        </div>
      </div>
      <ul class="pill-row">
        <li class="pill">Hyderabad</li><li class="pill">Telangana</li><li class="pill">Andhra Pradesh</li>
        <li class="pill">Mall Branding</li><li class="pill">DOOH</li><li class="pill">Cinema</li>
        <li class="pill">Mobile Media</li><li class="pill">Outdoor</li><li class="pill">BTL Activations</li>
      </ul>
    </div>
  </section>

{cta_final()}
  </main>
""" + footer()


# ============================================================== emit
if __name__ == "__main__":
    pages = {
        "index.html": build_index(),
        "about.html": build_about(),
        "services.html": build_services(),
        "media-solutions.html": build_media(),
        "work.html": build_work(),
        "contact.html": build_contact(),
    }
    for name, html in pages.items():
        with io.open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(html)
        print(f"{name:24} {len(html):>8,} bytes")
