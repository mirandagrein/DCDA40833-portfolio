/**
 * Dark mode toggle
 * Persists user preference in localStorage and respects system preference on first visit
 */

//AI assisted dark mode toggle.

document.addEventListener('DOMContentLoaded', function () {
  const STORAGE_KEY = 'dcda-dark-mode';
  const body = document.body;
  const toggle = document.querySelector('.dark-toggle');

  if (!toggle) return; // no toggle on this page

  // Apply stored preference or system default
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored === 'dark') {
    body.classList.add('dark-mode');
    toggle.setAttribute('aria-pressed', 'true');    //reads storage preference to keep default
  } else if (stored === 'light') {
    body.classList.remove('dark-mode');
    toggle.setAttribute('aria-pressed', 'false');
  } else {
    // no stored value: respect prefers-color-scheme
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (prefersDark) {
      body.classList.add('dark-mode');
      toggle.setAttribute('aria-pressed', 'true');
    } else {
      toggle.setAttribute('aria-pressed', 'false');
    }
  }

  function setDark(dark) {
    if (dark) {
      body.classList.add('dark-mode');
      toggle.setAttribute('aria-pressed', 'true');
      localStorage.setItem(STORAGE_KEY, 'dark');
    } else {
      body.classList.remove('dark-mode');             
      toggle.setAttribute('aria-pressed', 'false');
      localStorage.setItem(STORAGE_KEY, 'light');
    }   
  }

  toggle.addEventListener('click', function () {
    const isDark = body.classList.contains('dark-mode');
    setDark(!isDark);
  });

  // Allow keyboard activation via Space/Enter
  toggle.addEventListener('keydown', function (e) {
    if (e.key === ' ' || e.key === 'Enter') {
      e.preventDefault();
      toggle.click();
    }
  });
});
