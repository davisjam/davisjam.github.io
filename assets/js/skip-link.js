/* Make the skip link actually skip.

   minimal-mistakes runs `$("a").smoothScroll({offset: -20})`, which binds every
   anchor on the page -- including the skip link. It animates the scroll and
   never sets location.hash, so the browser's own "jump to fragment, move focus
   to the target" behaviour never runs. Measured: the page scrolled 161px, the
   hash stayed empty, focus stayed on the skip link, and the next Tab went
   straight back into the navigation. The link looked right and bypassed
   nothing, which is worse than not having one -- a keyboard user is told a
   shortcut exists and it silently does not work.

   Handled in the capture phase so this runs BEFORE smoothScroll's bubble-phase
   handler, and stopPropagation keeps it from animating afterwards. */
(function () {
  var link = document.querySelector('.skip-link');
  if (!link) return;
  link.addEventListener('click', function (e) {
    var target = document.querySelector(link.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    e.stopPropagation();
    target.focus({preventScroll: true});
    target.scrollIntoView();
  }, true);
})();
