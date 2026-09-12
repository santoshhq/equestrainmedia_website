/* ==========================================================================
   EQUESTRIAN MEDIA — gallery.js
   Horizontal scrolling media rails, Swiper carousels and portfolio filtering.
   ========================================================================== */

import { motionEnabled } from './animations.js';

/**
 * Pins a section and drives its track sideways as the visitor scrolls down.
 * Falls back to a native horizontal swipe rail when motion is unavailable.
 */
export function initHorizontalGallery() {
  const sections = document.querySelectorAll('[data-hscroll]');
  if (!sections.length) return;

  if (!motionEnabled || window.innerWidth < 1025) {
    sections.forEach((section) => {
      const track = section.querySelector('.hscroll__track');
      if (!track) return;
      track.style.overflowX = 'auto';
      track.style.scrollSnapType = 'x mandatory';
      track.style.paddingBottom = '1rem';
      Array.from(track.children).forEach((child) => {
        child.style.scrollSnapAlign = 'start';
      });
    });
    return;
  }

  const { gsap } = window;

  sections.forEach((section) => {
    const track = section.querySelector('.hscroll__track');
    if (!track) return;

    const distance = () => Math.max(0, track.scrollWidth - section.offsetWidth + 80);

    gsap.to(track, {
      x: () => -distance(),
      ease: 'none',
      scrollTrigger: {
        trigger: section,
        start: 'top top',
        end: () => `+=${distance()}`,
        pin: true,
        scrub: 0.8,
        anticipatePin: 1,
        invalidateOnRefresh: true,
      },
    });
  });
}

/**
 * Swiper carousels. Each `[data-swiper]` element reads its own options from
 * data attributes so markup stays declarative.
 */
export function initCarousels() {
  if (typeof window.Swiper === 'undefined') return;

  document.querySelectorAll('[data-swiper]').forEach((el) => {
    const perView = parseFloat(el.dataset.perView || 3);

    new window.Swiper(el, {
      slidesPerView: 1.1,
      spaceBetween: 16,
      grabCursor: true,
      speed: 650,
      a11y: {
        prevSlideMessage: 'Previous media',
        nextSlideMessage: 'Next media',
      },
      keyboard: { enabled: true },
      navigation: {
        prevEl: el.parentElement.querySelector('[data-swiper-prev]'),
        nextEl: el.parentElement.querySelector('[data-swiper-next]'),
      },
      breakpoints: {
        768:  { slidesPerView: Math.min(2, perView), spaceBetween: 20 },
        1024: { slidesPerView: perView, spaceBetween: 24 },
      },
    });
  });
}

/**
 * Portfolio / inventory category filter. Uses aria-pressed as the single source
 * of truth and hides non-matching cards from assistive tech too.
 */
export function initFilters() {
  const groups = document.querySelectorAll('[data-filter-group]');
  if (!groups.length) return;

  groups.forEach((group) => {
    const buttons = group.querySelectorAll('.filter');
    const targetSelector = group.dataset.filterTarget;
    const items = document.querySelectorAll(`${targetSelector} [data-category]`);
    const empty = document.querySelector(group.dataset.filterEmpty || '__none__');

    const apply = (value) => {
      let shown = 0;
      items.forEach((item) => {
        const match = value === 'all' || item.dataset.category.split(' ').includes(value);
        item.classList.toggle('is-hidden', !match);
        item.toggleAttribute('inert', !match);
        if (match) shown += 1;
      });
      if (empty) empty.hidden = shown > 0;
      if (window.ScrollTrigger) window.ScrollTrigger.refresh();
    };

    buttons.forEach((button) => {
      button.addEventListener('click', () => {
        buttons.forEach((b) => b.setAttribute('aria-pressed', String(b === button)));
        apply(button.dataset.filter);
      });
    });
  });
}
