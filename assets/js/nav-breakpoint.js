/* Deterministic navigation: full bar on a laptop, hamburger on a phone.

   REPLACES greedy-nav's measurement, which cannot deliver that. Its algorithm
   evicts `.visible-links`' last child while the list overflows, recording the
   list width in a `breaks` stack; it only restores an item when available space
   exceeds that recorded width. Once the list is shorter, that condition can
   never be met -- a one-way ratchet. Measured at 1512px: 119px of headroom, two
   items still hidden, and twelve resize ticks did not recover a single one.

   It also means any transient narrow moment during load evicts permanently --
   the logo is an <img> that gains its width asynchronously, so the first
   measurement can happen while the bar is narrow.

   Here the rule is a width comparison, re-evaluated on resize, with no state
   carried between evaluations. Above the breakpoint every item is in the bar
   and the toggle is hidden; below, everything but the logo sits behind the
   toggle. Same DOM the theme already ships, so the toggle keeps working. */
(function () {
  var nav = document.querySelector('#site-nav');
  if (!nav) return;
  var visible = nav.querySelector('.visible-links');
  var hidden = nav.querySelector('.hidden-links');
  var btn = nav.querySelector('button');
  if (!visible || !hidden || !btn) return;

  /* greedy-nav moves items with prependTo(), so visible ++ hidden is always
     the original order -- capture it once, before anything else runs. */
  var order = [].slice.call(visible.children).concat([].slice.call(hidden.children));

  /* Below this the bar cannot hold the logo, seven links and an expanded
     programme slug, so it collapses. Measured, not guessed: see the responsive
     logo sizes in _research.scss, which this rides on. */
  var FULL_BAR = 1200;

  function apply() {
    var full = window.innerWidth >= FULL_BAR;
    var into = full ? visible : hidden;
    order.forEach(function (li, i) {
      // The logo always stays in the bar: it is site identity, not a link, and
      // letting it be hidden is what collapsed the masthead on phones before.
      var keep = full || i === 0;
      var dest = keep ? visible : hidden;
      if (li.parentNode !== dest) dest.appendChild(li);
    });
    btn.classList.toggle('hidden', full);
    btn.setAttribute('aria-expanded', 'false');
    hidden.classList.add('hidden');
  }

  apply();
  window.addEventListener('resize', apply);
  window.addEventListener('load', apply);   // after the logo image has sized
})();
