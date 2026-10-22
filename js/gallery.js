/* GLP Home Options: Our work photo viewer.
   Every photo on the page is a plain link to the larger picture, so it all works with no JavaScript. This adds a viewer
   on top: Esc or the Close button leaves it, the arrow keys (or the buttons) move between photos, and focus goes back
   to the photo you opened. */
(function () {
  'use strict';
  var tiles = Array.prototype.slice.call(document.querySelectorAll('.work-grid a'));
  if (!tiles.length || typeof HTMLDialogElement === 'undefined') return;

  var root = document.documentElement;
  var dlg, img, cap, count, closeBtn, now = 0, opener = null;

  function build() {
    dlg = document.createElement('dialog');
    dlg.className = 'lb';
    dlg.setAttribute('aria-label', 'Photo viewer');
    dlg.innerHTML =
      '<div class="lb-bar"><p class="lb-count" aria-live="polite"></p>' +
      '<button class="lb-close" type="button" aria-label="Close photo viewer"><svg class="i" aria-hidden="true"><use href="#i-close"/></svg></button></div>' +
      '<button class="lb-nav lb-prev" type="button" aria-label="Previous photo"><svg class="i" aria-hidden="true"><use href="#i-arrow"/></svg></button>' +
      '<figure class="lb-fig"><img class="lb-img" alt=""><figcaption class="lb-cap"></figcaption></figure>' +
      '<button class="lb-nav lb-next" type="button" aria-label="Next photo"><svg class="i" aria-hidden="true"><use href="#i-arrow"/></svg></button>';
    document.body.appendChild(dlg);
    img = dlg.querySelector('.lb-img');
    cap = dlg.querySelector('.lb-cap');
    count = dlg.querySelector('.lb-count');
    closeBtn = dlg.querySelector('.lb-close');
    closeBtn.addEventListener('click', function () { dlg.close(); });
    dlg.querySelector('.lb-prev').addEventListener('click', function () { show(now - 1); });
    dlg.querySelector('.lb-next').addEventListener('click', function () { show(now + 1); });
    dlg.addEventListener('click', function (e) {
      if (e.target === dlg || e.target.classList.contains('lb-fig')) dlg.close();
    });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); show(now - 1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); show(now + 1); }
    });
    dlg.addEventListener('close', function () {
      root.classList.remove('lb-open');
      if (opener) opener.focus();
    });
  }

  function show(i) {
    var n = tiles.length;
    now = (i + n) % n;
    var t = tiles[now];
    var thumb = t.querySelector('img');
    var label = t.parentNode.querySelector('figcaption');
    img.src = t.href;
    img.alt = thumb ? thumb.alt : '';
    cap.textContent = label ? label.textContent : '';
    count.textContent = (now + 1) + ' of ' + n;
    // warm up the neighbours so the arrows feel instant
    [now + 1, now - 1].forEach(function (k) { new Image().src = tiles[(k + n) % n].href; });
  }

  tiles.forEach(function (t, i) {
    t.addEventListener('click', function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button) return;   // let "open in new tab" work
      e.preventDefault();
      if (!dlg) build();
      opener = t;
      show(i);
      root.classList.add('lb-open');
      dlg.showModal();
      closeBtn.focus();
    });
  });
})();
