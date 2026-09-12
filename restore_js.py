# -*- coding: utf-8 -*-
"""Re-applies the session's js/gallery.js and js/contact.js changes."""
import io
import os

ROOT = r"C:\Users\santo\Downloads\equestrainMedia_website"

NEW_FILTERS = """export function initFilters() {
  const groups = document.querySelectorAll('[data-filter-group]');
  if (!groups.length) return;

  groups.forEach((group) => {
    const buttons = Array.from(group.querySelectorAll('.filter'));
    if (!buttons.length) return;

    const targetSelector = group.dataset.filterTarget;
    const grid = document.querySelector(targetSelector);
    const items = Array.from(document.querySelectorAll(`${targetSelector} [data-category]`));
    const empty = document.querySelector(group.dataset.filterEmpty || '__none__');
    const status = document.querySelector(group.dataset.filterStatus || '__none__');
    const keys = buttons.map((b) => b.dataset.filter);

    const label = (value) => {
      const button = buttons.find((b) => b.dataset.filter === value);
      if (!button) return value;
      const count = button.querySelector('.filter__count');
      return button.textContent.replace(count ? count.textContent : '', '').trim();
    };

    const apply = (value, { announce = true } = {}) => {
      let shown = 0;
      items.forEach((item) => {
        const match = value === 'all' || item.dataset.category.split(' ').includes(value);
        item.classList.toggle('is-hidden', !match);
        item.toggleAttribute('inert', !match);
        if (match) shown += 1;
      });

      buttons.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.filter === value)));
      if (empty) empty.hidden = shown > 0;
      if (status && announce) {
        status.textContent = value === 'all'
          ? `Showing all ${shown} projects`
          : `Showing ${shown} ${shown === 1 ? 'project' : 'projects'} in ${label(value)}`;
      }

      // The grid re-flows, so any scroll-driven animation needs new measurements.
      if (grid) {
        grid.classList.remove('is-filtering');
        // eslint-disable-next-line no-unused-expressions
        grid.offsetWidth;                       // restart the fade
        grid.classList.add('is-filtering');
      }
      if (window.ScrollTrigger) window.ScrollTrigger.refresh();
    };

    const fromUrl = () => {
      const value = new URLSearchParams(window.location.search).get('filter');
      return value && keys.includes(value) ? value : 'all';
    };

    buttons.forEach((button) => {
      button.addEventListener('click', () => {
        const value = button.dataset.filter;
        apply(value);

        const url = new URL(window.location.href);
        if (value === 'all') url.searchParams.delete('filter');
        else url.searchParams.set('filter', value);
        window.history.pushState({ filter: value }, '', url);
      });
    });

    // Deep link (work.html?filter=dooh) and browser back/forward.
    window.addEventListener('popstate', () => apply(fromUrl()));
    const initial = fromUrl();
    if (initial !== 'all') apply(initial);
  });
}"""

OLD_FILTERS = """export function initFilters() {
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
}"""

DOC = """/**
 * Portfolio / inventory category filter. Uses aria-pressed as the single source
 * of truth, hides non-matching cards from assistive tech too, announces the new
 * result count, and keeps the active category in the URL so a filtered view can
 * be linked to and survives a reload or a back/forward step.
 */
"""

PANEL_WIRING_OLD = """  const status = form.querySelector('.form-status');
  const submit = form.querySelector('[type="submit"]');
  const fields = Array.from(form.querySelectorAll('input, select, textarea'));"""

PANEL_WIRING_NEW = """  const status = form.querySelector('.form-status');
  const submit = form.querySelector('[type="submit"]');
  const fields = Array.from(form.querySelectorAll('input, select, textarea'));

  const panel = document.querySelector('[data-form-success]');
  const panelTitle = panel?.querySelector('[data-success-title]');
  const panelBody = panel?.querySelector('[data-success-body]');
  const resetBtn = panel?.querySelector('[data-form-reset]');

  // The label lives in a <span> so the button's red wipe cannot paint over it -
  // write through that span, never through the button's own textContent.
  const label = submit?.querySelector('span') || submit;
  const setLabel = (text) => { if (label) label.textContent = text; };

  /** Swaps the form out for the confirmation panel. */
  const showSuccess = (title, body) => {
    if (!panel) return false;
    if (panelTitle) panelTitle.textContent = title;
    if (panelBody) panelBody.textContent = body;
    form.hidden = true;
    panel.hidden = false;
    panel.focus();
    panel.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return true;
  };

  resetBtn?.addEventListener('click', () => {
    form.reset();
    fields.forEach((field) => setError(field, ''));
    if (status) { status.hidden = true; status.textContent = ''; }
    panel.hidden = true;
    form.hidden = false;
    form.querySelector('input, select, textarea')?.focus();
  });"""

LABEL_OLD = """    const originalLabel = submit?.textContent;

    if (submit) {
      submit.disabled = true;
      submit.textContent = 'Sending\u2026';
    }"""

LABEL_NEW = """    const originalLabel = label?.textContent;

    if (submit) {
      submit.disabled = true;
      setLabel('Sending\u2026');
    }"""

SUCCESS_OLD = """        form.reset();
        announce('Thank you \u2014 your brief has reached us. Our team will respond within one working day.');
      } else {
        // No endpoint configured yet: hand the enquiry to the visitor's mail client.
        window.location.href = buildMailto(form, data);
        announce('Opening your email app with the brief pre-filled. You can also call +91 81060 39919.');
      }"""

SUCCESS_NEW = """        form.reset();
        const sent = showSuccess(
          'Brief received',
          'Thank you \u2014 your brief has reached us. Our team will respond within one working day.'
        );
        if (!sent) {
          announce('Thank you \u2014 your brief has reached us. Our team will respond within one working day.');
        }
      } else {
        // No endpoint configured yet: hand the enquiry to the visitor's mail client.
        // The brief is prepared, not delivered - the panel must say so honestly.
        window.location.href = buildMailto(form, data);
        const shown = showSuccess(
          'Your brief is ready to send',
          'We have opened your email app with the brief filled in \u2014 press send there and it reaches '
          + 'us straight away. If nothing opened, email or call us directly.'
        );
        if (!shown) {
          announce('Opening your email app with the brief pre-filled. You can also call +91 81060 39919.');
        }
      }"""

RESTORE_OLD = """      if (submit) {
        submit.disabled = false;
        submit.textContent = originalLabel;
      }"""

RESTORE_NEW = """      if (submit) {
        submit.disabled = false;
        setLabel(originalLabel);
      }"""


def patch(rel, pairs, doc_swap=None):
    path = os.path.join(ROOT, rel)
    src = io.open(path, encoding="utf-8").read()
    if doc_swap:
        marker, replacement = doc_swap
        i = src.index(marker)
        j = src.index("export function initFilters() {")
        src = src[:i] + replacement + src[j:]
    for old, new, tag in pairs:
        assert src.count(old) == 1, f"{rel}: anchor problem for {tag} ({src.count(old)})"
        src = src.replace(old, new, 1)
    io.open(path, "w", encoding="utf-8", newline="\n").write(src)
    print(f"{rel}: {len(pairs)} patch(es) applied")


patch("js/gallery.js", [(OLD_FILTERS, NEW_FILTERS, "initFilters")],
      doc_swap=("/**\n * Portfolio / inventory category filter.", DOC))

patch("js/contact.js", [
    (PANEL_WIRING_OLD, PANEL_WIRING_NEW, "panel wiring"),
    (LABEL_OLD, LABEL_NEW, "label handling"),
    (SUCCESS_OLD, SUCCESS_NEW, "success paths"),
    (RESTORE_OLD, RESTORE_NEW, "label restore"),
])
