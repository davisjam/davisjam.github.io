/* Programme switcher. Hover is a desktop convenience only -- open/close is
   driven by real events so keyboard and touch work identically:
   Enter/Space toggles, Escape closes and returns focus, outside click closes.
   A CSS-only :hover menu would be unusable on both. */
(function () {
  var wrap = document.querySelector('.research-switch');
  if (!wrap) return;
  var toggle = wrap.querySelector('.research-switch__toggle');
  var menu = wrap.querySelector('.research-switch__menu');
  if (!toggle || !menu) return;

  function open(state) {
    wrap.classList.toggle('is-open', state);
    toggle.setAttribute('aria-expanded', state ? 'true' : 'false');
  }
  toggle.addEventListener('click', function (e) {
    e.preventDefault();
    open(toggle.getAttribute('aria-expanded') !== 'true');
  });
  wrap.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && wrap.classList.contains('is-open')) {
      open(false); toggle.focus();
    }
  });
  document.addEventListener('click', function (e) {
    if (!wrap.contains(e.target)) open(false);
  });
  // Pointer convenience, only where hover is a real input mode.
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    wrap.addEventListener('mouseenter', function () { open(true); });
    wrap.addEventListener('mouseleave', function () { open(false); });
  }
})();
