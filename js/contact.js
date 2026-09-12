/* ==========================================================================
   EQUESTRIAN MEDIA — contact.js
   Campaign enquiry form: inline validation and submission handling.

   The form posts to whatever endpoint is set on the <form action> attribute.
   Until a backend/inbox endpoint is configured, it falls back to composing a
   pre-filled email to ravi.chander@equestrianmedia.in so no enquiry is lost.
   ========================================================================== */

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const PHONE_RE = /^[+]?[\d\s()-]{8,18}$/;

/** Shows or clears the inline error under a field. */
function setError(field, message) {
  const wrap = field.closest('.field');
  if (!wrap) return;
  const slot = wrap.querySelector('.field__error');
  wrap.classList.toggle('has-error', Boolean(message));
  field.setAttribute('aria-invalid', message ? 'true' : 'false');
  if (slot) slot.textContent = message || '';
}

/** Validates one control and returns true when it passes. */
function validateField(field) {
  const value = field.value.trim();
  const label = field.dataset.label || field.name;

  if (field.required && !value) {
    setError(field, `${label} is required`);
    return false;
  }
  if (value && field.type === 'email' && !EMAIL_RE.test(value)) {
    setError(field, 'Enter a valid email address');
    return false;
  }
  if (value && field.type === 'tel' && !PHONE_RE.test(value)) {
    setError(field, 'Enter a valid phone number');
    return false;
  }
  setError(field, '');
  return true;
}

/** Builds the mailto fallback body from the submitted values. */
function buildMailto(form, data) {
  const lines = [];
  form.querySelectorAll('[name]').forEach((field) => {
    const label = field.dataset.label || field.name;
    const value = (data.get(field.name) || '').toString().trim();
    if (value) lines.push(`${label}: ${value}`);
  });

  const subject = `Campaign enquiry — ${data.get('company') || data.get('name') || 'New enquiry'}`;
  return (
    `mailto:ravi.chander@equestrianmedia.in?subject=${encodeURIComponent(subject)}` +
    `&body=${encodeURIComponent(lines.join('\n'))}`
  );
}

export function initContactForm() {
  const form = document.querySelector('[data-contact-form]');
  if (!form) return;

  const status = form.querySelector('.form-status');
  const submit = form.querySelector('[type="submit"]');
  const fields = Array.from(form.querySelectorAll('input, select, textarea'));

  // Validate on blur, and clear the error as soon as the visitor corrects it.
  fields.forEach((field) => {
    field.addEventListener('blur', () => validateField(field));
    field.addEventListener('input', () => {
      if (field.closest('.field')?.classList.contains('has-error')) validateField(field);
    });
  });

  const announce = (message) => {
    if (!status) return;
    status.hidden = false;
    status.textContent = message;
  };

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const valid = fields.map(validateField).every(Boolean);
    if (!valid) {
      announce('Please correct the highlighted fields and try again.');
      form.querySelector('.has-error input, .has-error select, .has-error textarea')?.focus();
      return;
    }

    const data = new FormData(form);
    const endpoint = form.getAttribute('action');
    const originalLabel = submit?.textContent;

    if (submit) {
      submit.disabled = true;
      submit.textContent = 'Sending…';
    }

    try {
      if (endpoint && endpoint !== '#') {
        const response = await fetch(endpoint, {
          method: 'POST',
          body: data,
          headers: { Accept: 'application/json' },
        });
        if (!response.ok) throw new Error(`Request failed: ${response.status}`);

        form.reset();
        announce('Thank you — your brief has reached us. Our team will respond within one working day.');
      } else {
        // No endpoint configured yet: hand the enquiry to the visitor's mail client.
        window.location.href = buildMailto(form, data);
        announce('Opening your email app with the brief pre-filled. You can also call +91 81060 39919.');
      }
    } catch (error) {
      announce(
        'We could not send the form just now. Please email ravi.chander@equestrianmedia.in or call +91 81060 39919.'
      );
    } finally {
      if (submit) {
        submit.disabled = false;
        submit.textContent = originalLabel;
      }
    }
  });
}
