/* ==========================================================================
   EQUESTRIAN MEDIA — media.js
   Media detail drawer. Every inventory card already carries its own
   specification list in the markup, so the modal is composed from the card
   itself — there is one source of truth for each site's data.
   ========================================================================== */

const FOCUSABLE =
  'a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])';

let modal;
let lastFocused = null;

/** Builds the single modal shell shared by every media card. */
function ensureModal() {
  if (modal) return modal;

  modal = document.createElement('div');
  modal.className = 'modal';
  modal.setAttribute('role', 'dialog');
  modal.setAttribute('aria-modal', 'true');
  modal.setAttribute('aria-labelledby', 'media-modal-title');
  modal.hidden = false;
  modal.innerHTML = `
    <div class="modal__backdrop" data-close></div>
    <div class="modal__panel">
      <button class="modal__close" type="button" data-close aria-label="Close media details">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path d="M18 6 6 18M6 6l12 12"/>
        </svg>
      </button>
      <div class="modal__grid">
        <figure class="modal__figure">
          <img alt="" data-modal-img>
        </figure>
        <div class="modal__body">
          <p class="media-card__kicker" data-modal-kicker></p>
          <h2 class="h3" id="media-modal-title" data-modal-title></h2>
          <p class="muted" data-modal-desc style="margin-top:.75rem"></p>
          <div data-modal-specs style="margin-top:1.25rem"></div>
          <div style="margin-top:auto;padding-top:1.75rem;display:flex;flex-wrap:wrap;gap:.75rem">
            <a class="btn" href="contact.html" data-cursor="EXPLORE">
              <span>Request a media plan</span>
            </a>
            <a class="btn btn--outline" href="mailto:sales.equestrian@gmail.com"><span>Email sales.equestrian@gmail.com</span></a>
          </div>
        </div>
      </div>
    </div>`;

  document.body.appendChild(modal);

  modal.addEventListener('click', (e) => {
    if (e.target.closest('[data-close]')) close();
  });

  document.addEventListener('keydown', (e) => {
    if (!modal.classList.contains('is-open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'Tab') trapFocus(e);
  });

  return modal;
}

/** Keeps keyboard focus inside the open dialog. */
function trapFocus(e) {
  const items = Array.from(modal.querySelectorAll(FOCUSABLE)).filter(
    (el) => el.offsetParent !== null
  );
  if (!items.length) return;

  const first = items[0];
  const last = items[items.length - 1];

  if (e.shiftKey && document.activeElement === first) {
    e.preventDefault();
    last.focus();
  } else if (!e.shiftKey && document.activeElement === last) {
    e.preventDefault();
    first.focus();
  }
}

function close() {
  if (!modal) return;
  modal.classList.remove('is-open');
  document.body.classList.remove('is-locked');
  window.__lenis?.start();
  lastFocused?.focus();
}

/** Reads a card and pours its content into the shared modal. */
function open(card) {
  ensureModal();
  lastFocused = card;

  const img = card.querySelector('.media-card__img');
  const modalImg = modal.querySelector('[data-modal-img]');
  modalImg.src = card.dataset.fullImage || img?.src || '';
  modalImg.alt = img?.alt || '';

  modal.querySelector('[data-modal-kicker]').textContent =
    card.querySelector('.media-card__kicker')?.textContent || 'Media inventory';
  modal.querySelector('[data-modal-title]').textContent =
    card.querySelector('.media-card__title')?.textContent || 'Media detail';

  const desc = modal.querySelector('[data-modal-desc]');
  desc.textContent = card.dataset.description || '';
  desc.hidden = !card.dataset.description;

  // Clone the card's own specification list — no duplicated data.
  const specs = modal.querySelector('[data-modal-specs]');
  specs.innerHTML = '';
  const source = card.querySelector('.spec-list');
  if (source) specs.appendChild(source.cloneNode(true));

  modal.classList.add('is-open');
  document.body.classList.add('is-locked');
  window.__lenis?.stop();
  modal.querySelector('.modal__close').focus();
}

/** Wires every media card on the page to the drawer. */
export function initMediaDrawer() {
  const cards = document.querySelectorAll('.media-card[data-media]');
  if (!cards.length) return;

  ensureModal();
  cards.forEach((card) => {
    card.addEventListener('click', (e) => {
      e.preventDefault();
      open(card);
    });
  });
}
