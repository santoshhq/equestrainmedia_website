/* ==========================================================================
   EQUESTRIAN MEDIA — navigation.js
   Sticky header state, mobile drawer, in-page anchor nav.
   ========================================================================== */

/**
 * Adds `.is-stuck` to the header once the page has scrolled past the fold edge,
 * which shrinks the bar and reveals its border/shadow.
 */
export function initHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  const THRESHOLD = 24;
  let ticking = false;

  const update = () => {
    header.classList.toggle('is-stuck', window.scrollY > THRESHOLD);
    ticking = false;
  };

  window.addEventListener(
    'scroll',
    () => {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(update);
      }
    },
    { passive: true }
  );

  update();
}

/**
 * Mobile drawer: slides down from under the header, traps nothing but closes on
 * Escape, on outbound navigation and when the viewport grows past the breakpoint.
 */
export function initMobileNav() {
  const burger = document.querySelector('.burger');
  const drawer = document.querySelector('.mobile-nav');
  if (!burger || !drawer) return;

  const links = drawer.querySelectorAll('.mobile-nav__link');

  const setState = (open) => {
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    drawer.classList.toggle('is-open', open);
    drawer.setAttribute('aria-hidden', String(!open));
    document.body.classList.toggle('is-locked', open);

    // Stagger the link entrance each time the drawer opens.
    links.forEach((link, i) => {
      link.style.animationDelay = open ? `${0.06 * i + 0.05}s` : '0s';
    });
  };

  burger.addEventListener('click', () => {
    setState(burger.getAttribute('aria-expanded') !== 'true');
  });

  drawer.addEventListener('click', (e) => {
    if (e.target.closest('a')) setState(false);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') {
      setState(false);
      burger.focus();
    }
  });

  const mq = window.matchMedia('(min-width: 1025px)');
  mq.addEventListener('change', (e) => {
    if (e.matches) setState(false);
  });

  setState(false);
}

/**
 * Scroll-spy for the in-page section nav used on Media Solutions.
 */
export function initAnchorNav() {
  const nav = document.querySelector('.anchor-nav');
  if (!nav) return;

  const links = Array.from(nav.querySelectorAll('a[href^="#"]'));
  const sections = links
    .map((link) => document.querySelector(link.getAttribute('href')))
    .filter(Boolean);
  if (!sections.length) return;

  const setActive = (id) => {
    links.forEach((link) => {
      const on = link.getAttribute('href') === `#${id}`;
      link.classList.toggle('is-active', on);
      if (on) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });
  };

  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (visible) setActive(visible.target.id);
    },
    { rootMargin: '-45% 0px -50% 0px', threshold: [0, 0.25, 0.5] }
  );

  sections.forEach((section) => observer.observe(section));

  // Keep the active chip in view on narrow screens.
  nav.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (link) link.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
  });
}

/**
 * Marks the nav item matching the current document as the current page.
 */
export function markCurrentPage() {
  const file = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav__link, .mobile-nav__link').forEach((link) => {
    const href = link.getAttribute('href');
    if (!href) return;
    if (href === file || (file === '' && href === 'index.html')) {
      link.setAttribute('aria-current', 'page');
    }
  });
}
