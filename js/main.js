/* ==========================================================================
   EQUESTRIAN MEDIA — main.js
   Entry point. Boots every module and owns the custom cursor.
   ========================================================================== */

import { initHeader, initMobileNav, initAnchorNav, markCurrentPage } from './navigation.js';
import {
  initMotion,
  initSmoothScroll,
  initHero,
  initReveals,
  initCounters,
  initParallax,
  initPageTransitions,
} from './animations.js';
import { initHorizontalGallery, initCarousels, initFilters } from './gallery.js';
import { initMediaDrawer } from './media.js';
import { initContactForm } from './contact.js';

/* --------------------------------------------------------------------------
   Custom cursor — desktop, fine pointer only.
   A small black dot that expands into a red disc with a contextual label.
   -------------------------------------------------------------------------- */
function initCursor() {
  const fine = window.matchMedia('(hover: hover) and (pointer: fine) and (min-width: 1025px)');
  if (!fine.matches) return;

  const dot = document.createElement('div');
  dot.className = 'cursor';
  dot.setAttribute('aria-hidden', 'true');

  const ring = document.createElement('div');
  ring.className = 'cursor-ring';
  ring.setAttribute('aria-hidden', 'true');
  ring.innerHTML = '<span class="cursor-ring__label"></span>';

  document.body.append(dot, ring);
  const label = ring.querySelector('.cursor-ring__label');

  let mouseX = window.innerWidth / 2;
  let mouseY = window.innerHeight / 2;
  let ringX = mouseX;
  let ringY = mouseY;

  document.addEventListener(
    'mousemove',
    (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      dot.style.transform = `translate3d(${mouseX}px, ${mouseY}px, 0) translate(-50%, -50%)`;
    },
    { passive: true }
  );

  // The ring trails the dot with a light lag.
  const render = () => {
    ringX += (mouseX - ringX) * 0.16;
    ringY += (mouseY - ringY) * 0.16;
    ring.style.transform = `translate3d(${ringX}px, ${ringY}px, 0) translate(-50%, -50%)`;
    requestAnimationFrame(render);
  };
  requestAnimationFrame(render);

  const INTERACTIVE = 'a, button, [data-cursor], input, select, textarea, .media-card';

  document.addEventListener('mouseover', (e) => {
    const target = e.target.closest(INTERACTIVE);
    if (!target) return;
    const text = target.dataset.cursor || '';
    label.textContent = text;
    // Plain interactive elements get the outline ring; only a labelled target
    // fills with red so the label has something to read against.
    document.body.classList.toggle('cursor-labeled', Boolean(text));
    document.body.classList.add('cursor-active');
  });

  document.addEventListener('mouseout', (e) => {
    if (e.target.closest(INTERACTIVE) && !e.relatedTarget?.closest(INTERACTIVE)) {
      document.body.classList.remove('cursor-active', 'cursor-labeled');
    }
  });

  document.addEventListener('mouseleave', () => document.body.classList.add('cursor-hidden'));
  document.addEventListener('mouseenter', () => document.body.classList.remove('cursor-hidden'));
}

/* --------------------------------------------------------------------------
   Page chrome
   -------------------------------------------------------------------------- */
function initChrome() {
  document.querySelectorAll('[data-year]').forEach((el) => {
    el.textContent = new Date().getFullYear();
  });

  // Icons are inlined Lucide glyphs (arrow-right, arrow-up-right, check, x,
  // info) so no icon library is downloaded. If the Lucide script is ever added
  // to the page, any [data-lucide] placeholders will still be hydrated here.
  if (window.lucide?.createIcons) window.lucide.createIcons();
}

/* --------------------------------------------------------------------------
   Boot
   -------------------------------------------------------------------------- */
function boot() {
  // Navigation first — it must work even if a motion library fails to load.
  markCurrentPage();
  initHeader();
  initMobileNav();
  initAnchorNav();

  initChrome();
  initMediaDrawer();
  initContactForm();
  initFilters();
  initCarousels();

  // Motion layer.
  initMotion();
  initSmoothScroll();
  initHero();
  initReveals();
  initCounters();
  initParallax();
  initHorizontalGallery();
  initPageTransitions();
  initCursor();

  // Recalculate scroll positions once webfonts have settled the layout.
  if (document.fonts?.ready) {
    document.fonts.ready.then(() => window.ScrollTrigger?.refresh());
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}
