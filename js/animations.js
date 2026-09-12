/* ==========================================================================
   EQUESTRIAN MEDIA — animations.js
   GSAP + ScrollTrigger choreography and Lenis smooth scrolling.
   Every effect degrades to "content simply visible" without JS or when the
   visitor prefers reduced motion.
   ========================================================================== */

const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const hasGSAP = typeof window.gsap !== 'undefined';

export const motionEnabled = hasGSAP && !reduced;

/** Registers plugins and flags the document so the CSS start states apply. */
export function initMotion() {
  if (!motionEnabled) return false;
  window.gsap.registerPlugin(window.ScrollTrigger);
  document.documentElement.classList.add('js-anim');
  return true;
}

/* --------------------------------------------------------------------------
   Smooth scrolling
   -------------------------------------------------------------------------- */
export function initSmoothScroll() {
  if (!motionEnabled || typeof window.Lenis === 'undefined') return null;

  const lenis = new window.Lenis({
    duration: 1.05,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
    touchMultiplier: 1.6,
  });

  lenis.on('scroll', window.ScrollTrigger.update);
  window.gsap.ticker.add((time) => lenis.raf(time * 1000));
  window.gsap.ticker.lagSmoothing(0);

  // Route in-page anchors through Lenis so the sticky header is cleared.
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (e) => {
      const id = link.getAttribute('href');
      if (!id || id === '#') return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const offset = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--header-h'), 10) || 90;
      lenis.scrollTo(target, { offset: -(offset + 20) });
    });
  });

  window.__lenis = lenis;
  return lenis;
}

/* --------------------------------------------------------------------------
   Hero — clip-path line reveal and media composite entrance
   -------------------------------------------------------------------------- */
export function initHero() {
  const hero = document.querySelector('[data-hero]');
  if (!hero) return;

  if (!motionEnabled) return;

  const { gsap } = window;
  const lines = hero.querySelectorAll('[data-reveal-lines] .line > span');
  const tl = gsap.timeline({ defaults: { ease: 'power4.out' } });

  // fromTo, not to: the CSS start state is translateY(105%), but computed style
  // reports it as a pixel matrix, so GSAP would read yPercent as already 0 and
  // the tween would do nothing. GSAP must own both ends of this one.
  tl.fromTo(lines, { yPercent: 105 }, { yPercent: 0, duration: 1.05, stagger: 0.09 }, 0.15)
    .from(
      hero.querySelector('.hero__visual-wrap'),
      { xPercent: -8, opacity: 0, duration: 1.4, ease: 'power3.out' },
      0.1
    )
    .from(
      hero.querySelectorAll('.hero__sub, .actions, .hero__foot'),
      { y: 24, opacity: 0, duration: 0.8, stagger: 0.1 },
      0.6
    );

  // Very subtle parallax as the hero leaves the viewport. This drives the
  // wrapper, never the <img>, so nothing competes for the same transform.
  gsap.to(hero.querySelector('.hero__visual-wrap'), {
    yPercent: 10,
    ease: 'none',
    scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: 0.6 },
  });
}

/* --------------------------------------------------------------------------
   Generic scroll reveals
   -------------------------------------------------------------------------- */
export function initReveals() {
  if (!motionEnabled) return;
  const { gsap } = window;

  gsap.utils.toArray('[data-reveal]').forEach((el) => {
    const delay = parseFloat(el.dataset.revealDelay || 0);
    gsap.to(el, {
      opacity: 1,
      x: 0,
      y: 0,
      scale: 1,
      duration: 0.9,
      delay,
      ease: 'power3.out',
      scrollTrigger: { trigger: el, start: 'top 88%', once: true },
    });
  });

  // Staggered groups — children animate in sequence.
  gsap.utils.toArray('[data-reveal-group]').forEach((group) => {
    const kids = group.children;
    gsap.set(kids, { opacity: 0, y: 26 });
    gsap.to(kids, {
      opacity: 1,
      y: 0,
      duration: 0.75,
      stagger: 0.075,
      ease: 'power3.out',
      scrollTrigger: { trigger: group, start: 'top 85%', once: true },
    });
  });

  // Heading lines outside the hero.
  gsap.utils.toArray('[data-reveal-lines]:not([data-hero-title])').forEach((el) => {
    gsap.fromTo(
      el.querySelectorAll('.line > span'),
      { yPercent: 105 },
      {
        yPercent: 0,
        duration: 1,
        stagger: 0.08,
        ease: 'power4.out',
        scrollTrigger: { trigger: el, start: 'top 86%', once: true },
      }
    );
  });

  // Red curtain wipes off each image. The curtain is a pseudo-element, so it is
  // driven through the --wipe-scale custom property the stylesheet consumes.
  gsap.utils.toArray('.reveal-img').forEach((wrap) => {
    gsap
      .timeline({ scrollTrigger: { trigger: wrap, start: 'top 85%', once: true } })
      .to(wrap, { '--wipe-scale': 0, duration: 0.85, ease: 'power3.inOut' })
      .to(wrap.querySelector('img'), { scale: 1, duration: 1.3, ease: 'power3.out' }, 0.15);
  });

  // Process steps + red rules.
  gsap.utils.toArray('.step, .rule-red').forEach((el) => {
    window.ScrollTrigger.create({
      trigger: el,
      start: 'top 85%',
      once: true,
      onEnter: () => el.classList.add('is-inview'),
    });
  });
}

/* --------------------------------------------------------------------------
   Animated counters
   -------------------------------------------------------------------------- */
export function initCounters() {
  const nodes = document.querySelectorAll('[data-count]');
  if (!nodes.length) return;

  const render = (el, value) => {
    const decimals = parseInt(el.dataset.decimals || 0, 10);
    el.textContent = Number(value).toLocaleString('en-IN', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    });
  };

  if (!motionEnabled) {
    nodes.forEach((el) => render(el, parseFloat(el.dataset.count)));
    return;
  }

  const { gsap } = window;
  nodes.forEach((el) => {
    const target = parseFloat(el.dataset.count);
    const counter = { value: 0 };
    render(el, 0);
    gsap.to(counter, {
      value: target,
      duration: 2.1,
      ease: 'power2.out',
      onUpdate: () => render(el, counter.value),
      scrollTrigger: { trigger: el, start: 'top 90%', once: true },
    });
  });
}

/* --------------------------------------------------------------------------
   Parallax on full-bleed image bands
   -------------------------------------------------------------------------- */
export function initParallax() {
  if (!motionEnabled) return;
  const { gsap } = window;

  gsap.utils.toArray('[data-parallax]').forEach((img) => {
    const amount = parseFloat(img.dataset.parallax) || 12;
    gsap.fromTo(
      img,
      { yPercent: -amount / 2, scale: 1.12 },
      {
        yPercent: amount / 2,
        ease: 'none',
        scrollTrigger: {
          trigger: img.closest('section, .band') || img,
          start: 'top bottom',
          end: 'bottom top',
          scrub: true,
        },
      }
    );
  });
}

/* --------------------------------------------------------------------------
   Page transition curtain
   -------------------------------------------------------------------------- */
export function initPageTransitions() {
  return;
}
