/* Programme switcher.

   Open/close is driven by real events so keyboard and touch work identically:
   Enter/Space toggles, Escape closes and returns focus, outside click closes.
   A CSS-only :hover menu would be unusable on both.

   HOVER AND CLICK MUST NOT FIGHT (260905). An earlier version opened on
   mouseenter AND toggled on click. On a mouse, those run in sequence: hovering
   opened the menu, and the click that followed toggled it straight back shut,
   so clicking the control appeared to do nothing. Where hover is a real input
   mode, hover owns opening and click is inert; where it is not (touch), click
   toggles. Keyboard is unaffected either way.

   The toggle is a <span role="button">, not a <button>, because
   minimal-mistakes' greedy-nav claims `#site-nav button` as its overflow
   control and hides it. That costs us native keyboard behaviour, so Enter and
   Space are wired up by hand below. */
(function () {
  var wrap = document.querySelector('.rps');
  if (!wrap) return;
  var toggle = wrap.querySelector('.rps__btn');
  var menu = wrap.querySelector('.rps__menu');
  if (!toggle || !menu) return;

  var hoverable = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  function open(state) {
    wrap.classList.toggle('is-open', state);
    toggle.setAttribute('aria-expanded', state ? 'true' : 'false');
  }
  function toggleOpen(e) {
    e.preventDefault();
    open(toggle.getAttribute('aria-expanded') !== 'true');
  }

  toggle.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') toggleOpen(e);
  });
  toggle.addEventListener('click', function (e) {
    e.preventDefault();
    if (!hoverable) toggleOpen(e);   // see HOVER AND CLICK MUST NOT FIGHT
  });

  wrap.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && wrap.classList.contains('is-open')) {
      cancelClose(); open(false); toggle.focus(); return;
    }
    if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
    var items = [].slice.call(menu.querySelectorAll('a'));
    if (!items.length) return;
    e.preventDefault();
    if (!wrap.classList.contains('is-open')) open(true);
    var at = items.indexOf(document.activeElement);
    var next = e.key === 'ArrowDown'
      ? (at < 0 ? 0 : (at + 1) % items.length)
      : (at < 0 ? items.length - 1 : (at - 1 + items.length) % items.length);
    items[next].focus();
  });
  document.addEventListener('click', function (e) {
    if (!wrap.contains(e.target)) open(false);
  });
  wrap.addEventListener('focusout', function (e) {
    if (!wrap.contains(e.relatedTarget)) scheduleClose();
  });
  /* FORGIVING DISMISSAL. Opening is immediate; closing waits, so a pointer
     travelling slowly or diagonally from "Research" down to the last item does
     not lose the menu on the way. Re-entering cancels the pending close.
     mouseleave does not fire when moving onto a descendant, so the menu itself
     counts as still-inside; the only real gap was the geometric one above,
     which the CSS now closes. */
  var closeAfter = 320, pending = null;
  function cancelClose() { if (pending) { clearTimeout(pending); pending = null; } }
  function scheduleClose() {
    cancelClose();
    pending = setTimeout(function () { pending = null; open(false); }, closeAfter);
  }
  if (hoverable) {
    wrap.addEventListener('mouseenter', function () { cancelClose(); open(true); });
    wrap.addEventListener('mouseleave', scheduleClose);
  }
  /* Keyboard parity: focus anywhere inside holds it open, leaving schedules the
     same delayed close, and Escape (above) closes at once. */
  wrap.addEventListener('focusin', function () { cancelClose(); open(true); });
})();
