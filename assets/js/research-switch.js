/* Programme switcher. Hover is a desktop convenience only -- open/close is
   driven by real events so keyboard and touch work identically:
   Enter/Space toggles, Escape closes and returns focus, outside click closes.
   A CSS-only :hover menu would be unusable on both. */
(function () {
  var wrap = document.querySelector('.rps');
  if (!wrap) return;
  var toggle = wrap.querySelector('.rps__btn');
  var menu = wrap.querySelector('.rps__menu');
  if (!toggle || !menu) return;

  function open(state) {
    wrap.classList.toggle('is-open', state);
    toggle.setAttribute('aria-expanded', state ? 'true' : 'false');
  }
  function toggleOpen(e) {
    e.preventDefault();
    open(toggle.getAttribute('aria-expanded') !== 'true');
  }
  toggle.addEventListener('click', toggleOpen);
  // The toggle is a span, not a <button>, because minimal-mistakes' greedy-nav
  // claims `#site-nav button` as its overflow control and hides it. A span
  // avoids that collision but carries no native keyboard behaviour, so Enter
  // and Space are wired up by hand to keep it operable.
  toggle.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') toggleOpen(e);
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
