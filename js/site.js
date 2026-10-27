/* GLP Home Options: shared behavior. Everything degrades gracefully: with no JS the page is fully readable. */
(function () {
  'use strict';
  var doc = document;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };

  /* ---------- Year ---------- */
  var yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();

  /* ---------- Open at the very top ----------
     Rule: a page opens at the top. Two exceptions only: the Back button (the browser's own memory is right there), and a link
     from another page of this site that points at a section (index.html#numbers). A link from a text, an email or a bookmark,
     and a reload, all start at the top, even when the address carries a "#section" (that gets copied from the address bar after
     tapping a menu link, and used to land the visitor mid-page). Until the visitor drags, scrolls, types or taps a link, anything
     that moves the page (the browser's saved spot, something loading late) is undone. Add ?scrolldebug to the address to see
     what happened on a phone. */
  try { (function () {
    var t0 = Date.now(), nav = null;
    try { nav = performance.getEntriesByType('navigation')[0] || null; } catch (e) {}
    var type = (nav && nav.type) || 'navigate';
    var sameSite = false;
    try { sameSite = !!document.referrer && new URL(document.referrer).origin === location.origin; } catch (e) {}
    var hash0 = location.hash, y0 = window.pageYOffset || doc.documentElement.scrollTop || 0;
    var restore0 = 'scrollRestoration' in history ? history.scrollRestoration : 'n/a';
    var keep = type === 'back_forward' || (!!hash0 && type === 'navigate' && sameSite);

    var dbg = null, lines = [];
    function note(s) {
      if (!dbg) return;
      lines.push(((Date.now() - t0) / 1000).toFixed(1) + 's ' + s);
      dbg.textContent = lines.slice(-10).join('\n');
    }
    if (/[?&]scrolldebug\b/.test(location.search)) {
      dbg = doc.createElement('pre');
      dbg.style.cssText = 'position:fixed;left:0;right:0;top:0;z-index:99999;margin:0;padding:8px 10px;background:rgba(0,0,0,.82);color:#9f9;font:11px/1.35 monospace;white-space:pre-wrap;pointer-events:none';
      doc.body.appendChild(dbg);
    }
    note('type=' + type + ' hash=' + (hash0 || 'none') + ' ref=' + (document.referrer ? (sameSite ? 'same-site' : 'other') : 'none') + ' y0=' + Math.round(y0) + ' restore=' + restore0 + ' -> ' + (keep ? 'LEAVE ALONE' : 'GO TO TOP'));
    if (keep) return;

    if (hash0) { try { history.replaceState(history.state, '', location.pathname + location.search); } catch (e) {} }
    var guarding = true, canRestore = 'scrollRestoration' in history, fixes = 0, lastFix = 0, loaded = doc.readyState === 'complete';
    function topNow(why) {
      if (!guarding) return;
      var y = window.pageYOffset || doc.documentElement.scrollTop || 0;
      if (y > 0) {
        window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
        fixes++; lastFix = Date.now();
        note('moved to top from y=' + Math.round(y) + ' (' + why + ')');
        if (fixes >= 4) stop('moved 4 times, so someone is scrolling (touch, scrollbar or screen reader)');
      }
    }
    var intent = ['wheel', 'keydown', 'mousedown', 'touchmove'], tap = ['touchstart', 'pointerdown'];
    function onScroll() { topNow('scroll'); }
    function stop(why) {
      if (!guarding) return;
      guarding = false;
      clearInterval(timer);
      intent.forEach(function (ev) { window.removeEventListener(ev, onIntent); });
      tap.forEach(function (ev) { window.removeEventListener(ev, onTap); });
      window.removeEventListener('scroll', onScroll);
      if (canRestore) history.scrollRestoration = 'auto';   // give Back its normal memory again
      note('guard off (' + why + '), fixes=' + fixes);
    }
    function onIntent(e) { stop(e.type); }
    function onTap(e) {   // a tap on a link or button counts; a tap on bare page does not
      var t = e.target;
      if (t && t.closest && t.closest('a,button,summary,label,input,select,textarea,[role="button"]')) stop(e.type + ' on a control');
    }
    if (canRestore) history.scrollRestoration = 'manual';
    intent.forEach(function (ev) { window.addEventListener(ev, onIntent, { passive: true }); });
    tap.forEach(function (ev) { window.addEventListener(ev, onTap, { passive: true }); });
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('load', function () { loaded = true; topNow('load'); });
    window.addEventListener('pageshow', function () { topNow('pageshow'); });
    doc.addEventListener('visibilitychange', function () { if (!doc.hidden) topNow('visible'); });
    var timer = setInterval(function () {   // quiet for 3 s after the first 8 s, or 30 s at most
      var now = Date.now();
      if (now - t0 > 30000) stop('30 s');
      else if (loaded && now - t0 > 8000 && now - lastFix > 3000) stop('quiet');
    }, 500);
    topNow('start');
  })(); } catch (e) {}   // if anything in the guard ever fails, the rest of the script (menu, reveal, bars) must still run

  /* ---------- Scroll: header state, ridge parallax ---------- */
  var hdr = $('#hdr'), hero = $('.hero, .phero'), ridge = $('.ridge');
  var ticking = false;
  function update() {
    ticking = false;
    var y = window.pageYOffset || doc.documentElement.scrollTop || 0;
    var vh = window.innerHeight || 800;
    if (hdr) {
      hdr.classList.toggle('scrolled', y > 8);
    }
    if (reduce) return;
    if (hero && ridge) {
      var hh = hero.offsetHeight || 1;
      ridge.style.setProperty('--p', clamp(y / hh, 0, 1).toFixed(3));
    }
  }
  function onScroll() { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();

  /* ---------- Reveal on scroll (content stays visible if JS or IntersectionObserver is missing) ---------- */
  $$('[data-stagger]').forEach(function (g) {
    $$(':scope > .rv', g).forEach(function (el, i) { el.style.setProperty('--d', i); });
  });
  $$('.rv[data-d]').forEach(function (el) { el.style.setProperty('--d', el.getAttribute('data-d')); });
  var rvs = $$('.rv');
  if (!('IntersectionObserver' in window) || reduce) {
    rvs.forEach(function (el) { el.classList.add('in'); });
  } else {
    var rio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); rio.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.1 });
    rvs.forEach(function (el) { rio.observe(el); });
  }

  /* ---------- Phone action bar: slides in after the hero buttons scroll away, steps aside at the form ---------- */
  var mbar = $('.mobile-bar');
  if (mbar && 'IntersectionObserver' in window) {
    var heroCta = $('.hero .cta-row, .phero .cta-row'), formSec = $('#contact'), pastHero = !heroCta, atForm = false;
    var syncBar = function () { mbar.classList.toggle('on', pastHero && !atForm); };
    mbar.classList.add('auto');
    if (heroCta) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { pastHero = !e.isIntersecting && e.boundingClientRect.top < 0; syncBar(); });
      }).observe(heroCta);
    }
    if (formSec) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { atForm = e.isIntersecting; syncBar(); });
      }, { rootMargin: '0px 0px -30% 0px' }).observe(formSec);
    }
    syncBar();
  } else if (mbar) {
    /* very old browser without IntersectionObserver: the stylesheet hides the bar until it is told it may show, so show it for good */
    mbar.classList.add('auto'); mbar.classList.add('on');
  }

  /* ---------- Mobile menu ---------- */
  var mbtn = $('.menu-btn'), mnav = $('#mnav');
  function setMenu(open) {
    if (!mbtn || !mnav) return;
    mnav.hidden = !open;
    mbtn.setAttribute('aria-expanded', String(open));
    var label = $('span', mbtn); if (label) label.textContent = open ? 'Close' : 'Menu';
    var use = $('use', mbtn); if (use) use.setAttribute('href', open ? '#i-close' : '#i-menu');
  }
  if (mbtn && mnav) {
    mbtn.addEventListener('click', function () { setMenu(mnav.hidden); });
    mnav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !mnav.hidden) { setMenu(false); mbtn.focus(); } });
    window.addEventListener('resize', function () { if (window.matchMedia('(min-width:77.5625em)').matches && !mnav.hidden) setMenu(false); });
  }

  /* ---------- Scroll-spy for the desktop nav ---------- */
  var navLinks = $$('.nav a[href^="#"]');
  if (navLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    navLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var a = map[e.target.id]; if (!a) return;
        if (e.isIntersecting) {
          navLinks.forEach(function (n) { n.classList.remove('active'); n.removeAttribute('aria-current'); });
          a.classList.add('active'); a.setAttribute('aria-current', 'true');
        } else if (a.classList.contains('active')) {   // scrolled away again: no highlight when no section is in view
          a.classList.remove('active'); a.removeAttribute('aria-current');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(map).forEach(function (id) { var s = doc.getElementById(id); if (s) sio.observe(s); });
  }

  /* ---------- Seller net sheet ---------- */
  var calcForm = $('#calc');
  if (calcForm) {
    var el = function (id) { return doc.getElementById(id); };
    var num = function (id) { var v = parseFloat(String(el(id).value).replace(/[^0-9.\-]/g, '')); return isFinite(v) ? v : 0; };
    var usd = function (v) { return (v < 0 ? '−$' : '$') + Math.round(Math.abs(v)).toLocaleString('en-US'); };
    var neg = function (v) { return v === 0 ? '$0' : '−' + usd(v).replace('−', ''); };
    var calc = function () {
      var payoff = num('payoff'), price = num('price'), comm = num('comm') / 100, close = num('close') / 100;
      var repairs = num('repairs'), carry = num('carry'), months = num('months'), offer = num('offer');
      var commAmt = price * comm, closeAmt = price * close, carryAmt = carry * months;
      var netList = price - payoff - commAmt - closeAmt - repairs - carryAmt;
      var netDirect = offer - payoff;
      el('r-price').textContent = usd(price);
      el('r-payoff1').textContent = neg(payoff);
      el('r-comm').textContent = neg(commAmt);
      el('r-close').textContent = neg(closeAmt);
      el('r-repairs').textContent = neg(repairs);
      el('r-carry').textContent = neg(carryAmt);
      el('r-netlist').textContent = usd(netList);
      el('r-offer').textContent = usd(offer);
      el('r-payoff2').textContent = neg(payoff);
      el('r-netdirect').textContent = usd(netDirect);
      el('t-list').textContent = '~' + (Math.round(months * 10) / 10) + ' mo';
      var mo = (Math.round(months * 10) / 10) + (Math.round(months * 10) === 10 ? ' month' : ' months'), wl = el('when-list');
      if (wl) wl.textContent = 'If it sells for ' + usd(price) + ', in about ' + mo;
      var diff = netList - netDirect, v = el('verdict'), s = el('verdict-sub'), off = price - offer;
      // Checkpoint 50: the answer leads with what selling to us gives, then says plainly what listing might add and what it depends on. Same sums, same verdict.
      if (Math.abs(diff) < 500) {
        v.innerHTML = 'About the <span>same</span> money, and selling to us is done in 7 to 14 days.';
        s.textContent = 'When the money is this close, speed, certainty, and skipping showings and repairs may decide it.';
      } else if (diff > 0) {
        var wipe = carry > 0 ? Math.max(0.5, Math.round(diff / carry * 2) / 2) : 0;   // to the nearest half month
        v.innerHTML = 'On these numbers, selling to us puts <span>' + usd(netDirect) + '</span> in your pocket in 7 to 14 days.';
        s.textContent = 'You might keep about ' + usd(diff) + ' more by listing, but only if it sells for ' + usd(price) + (repairs > 0 ? ', needs no more than ' + usd(repairs) + ' of work' : '') + ' and closes in about ' + mo + '.' + (wipe > 0 ? ' About ' + wipe + ' more month' + (wipe === 1 ? '' : 's') + ' on the market would wipe that out.' : '') + ' Selling to us, there are no repairs, no showings and no buyer\u2019s loan to wait on.';
      } else {
        v.innerHTML = 'On these numbers, selling to us puts <span>' + usd(-diff) + ' more</span> in your pocket, in 7 to 14 days.';
        s.textContent = 'Once the commission, closing costs, repairs, and the cost of waiting come out, selling direct leaves you ahead, and you close in 7 to 14 days.';
      }
      // What can shrink the listing number (Checkpoint 50): one more month of the bills typed in, and 1% off the price after commission and closing costs
      var pm = el('r-permonth'), pp = el('r-perpct');
      if (pm) pm.textContent = neg(carry);
      if (pp) pp.textContent = neg(price * 0.01 * (1 - comm - close));
      // Break-even (Checkpoint 36): the cash offer that leaves the same in your pocket as listing. Listing keeps price - payoff - costs; a direct sale keeps offer - payoff;
      // the mortgage cancels, so they are equal when offer = price - commission - closing costs - repairs - cost of waiting.
      var be = price - commAmt - closeAmt - repairs - carryAmt, bx = el('breakeven');
      if (bx) {
        if (price > 0 && be > 0 && be <= price) { bx.innerHTML = 'On these numbers, a cash offer above <strong>' + usd(be) + '</strong> keeps more in your pocket than listing.'; bx.hidden = false; }
        else { bx.textContent = ''; bx.hidden = true; }
      }
      // The other side of the same line (Checkpoint 49): the sale price listing needs to beat this offer, with the costs as typed.
      // Listing keeps price x (1 - commission - closing) - repairs - cost of waiting - payoff; the offer keeps offer - payoff; equal at the price below.
      var keepShare = 1 - comm - close, se = keepShare > 0 ? (offer + repairs + carryAmt) / keepShare : 0, sx = el('sell-even');
      if (sx) {
        if (price > 0 && offer > 0 && se > 0) { sx.innerHTML = 'Listing comes out ahead only if it sells for more than <strong>' + usd(se) + '</strong>' + (se < price ? ', ' + usd(price - se) + ' under your price.' : '.'); sx.hidden = false; }
        else { sx.textContent = ''; sx.hidden = true; }
      }
      // The list of numbers that prints at the top of the printed page (the form itself does not print)
      var pin = el('p-inputs');
      if (pin) {
        var rows = [['Still owed on the mortgage', usd(payoff)], ['What it might sell for if listed', usd(price)], ['Cash offer compared', usd(offer)],
                    ['Agent commission', num('comm') + '%'], ['Seller closing costs', num('close') + '%'], ['Repairs and prep', usd(repairs)],
                    ['Monthly cost while listed', usd(carry)], ['Months to sell', String(num('months'))]];
        pin.textContent = '';
        rows.forEach(function (r) {
          var d = doc.createElement('div'), t = doc.createElement('dt'), v = doc.createElement('dd');
          t.textContent = r[0]; v.textContent = r[1]; d.appendChild(t); d.appendChild(v); pin.appendChild(d);
        });
      }
    };
    /* Worth a second look (Checkpoint 42): a calm note above the answer when the numbers look like a typo (an extra or missing digit).
       It only adds a line. It never changes a number or the verdict. It waits for a pause in the typing (a second) or for the person to leave
       the field (a third of a second, so a tap on a button that is already under the finger is never lost to the page moving), and it clears
       the moment the numbers look sensible again. A blank price or offer is only mentioned once the person leaves the field. */
    var checkBox = el('check-note'), checkText = el('check-text'), checkTimer = 0;
    var lookAgain = function (done) {
      var payoff = num('payoff'), price = num('price'), offer = num('offer');
      var costs = price * num('comm') / 100 + price * num('close') / 100 + num('repairs') + num('carry') * num('months');
      if (price <= 0 || offer <= 0) return done ? 'Add a sale price and a cash offer, and the comparison below will make sense.' : '';
      if (offer > price * 1.5 || offer < price * 0.25) return 'The cash offer (' + usd(offer) + ') and the sale price (' + usd(price) + ') are very far apart. Check for an extra or missing digit. If they\u2019re right, ignore this note.';
      if (payoff > price * 1.5) return 'The mortgage owed (' + usd(payoff) + ') is far above the sale price (' + usd(price) + '). Check for an extra or missing digit. If they\u2019re right, ignore this note.';
      if (costs > price * 0.5) return 'The costs of listing add up to ' + usd(costs) + ', more than half the sale price. Check the amounts under \u201cChange the costs we assumed.\u201d If they\u2019re right, ignore this note.';
      return '';
    };
    var showCheck = function (done) {
      clearTimeout(checkTimer);
      if (!checkBox || !checkText) return;
      var m = lookAgain(done);
      if (m) { checkText.textContent = m; checkBox.hidden = false; } else { checkText.textContent = ''; checkBox.hidden = true; }
    };
    var checkSoon = function () {
      if (!checkBox) return;
      clearTimeout(checkTimer);
      if (!lookAgain(false)) { checkText.textContent = ''; checkBox.hidden = true; return; }
      checkTimer = setTimeout(function () { showCheck(false); }, 1000);
    };
    $$('#calc input').forEach(function (inp) {
      inp.addEventListener('input', calc);
      inp.addEventListener('input', checkSoon);
      inp.addEventListener('blur', function () {
        if (inp.parentElement.classList.contains('pct')) return;
        var v = num(inp.id); inp.value = Math.round(v).toLocaleString('en-US');
      });
      inp.addEventListener('blur', function () {   // a moment's wait: if the person is tapping a button, the note must not slide it out from under the tap
        clearTimeout(checkTimer);
        checkTimer = setTimeout(function () { showCheck(true); }, 300);
      });
    });
    calc();

    /* Print my numbers (Checkpoint 36): the page prints only the net sheet (the print rules in the stylesheet key on html.print-sheet). */
    var pbtn = el('print-sheet');
    if (pbtn) {
      if (typeof window.print !== 'function') { pbtn.hidden = true; }
      var rootEl = doc.documentElement, undo = function () { rootEl.classList.remove('print-sheet'); };
      window.addEventListener('afterprint', undo);
      pbtn.addEventListener('click', function () {
        calc(); showCheck(true);
        var pd = el('p-date'); if (pd) pd.textContent = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
        rootEl.classList.add('print-sheet');
        try { window.print(); } finally { setTimeout(undo, 60000); }   // afterprint cleans up as usual; the timer covers a phone that never sends it
      });
    }
  }

  /* ---------- Faint topographic contours (the ridges around Chattanooga) ---------- */
  var topos = $$('canvas.topo');
  function drawTopo(cv) {
    var r = cv.getBoundingClientRect(); if (!r.width || !r.height) return;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.height * dpr);
    var ctx = cv.getContext('2d'); if (!ctx) return;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, r.width, r.height);
    var light = cv.getAttribute('data-tone') === 'light';
    ctx.strokeStyle = light ? 'rgba(255,255,255,.10)' : 'rgba(45,72,85,.075)';
    ctx.lineWidth = 1.2;
    var peaks = light
      ? [{ x: r.width * 0.9, y: r.height * 0.12, s: 1.0, seed: 2.1 }, { x: r.width * 0.05, y: r.height * 0.96, s: 0.9, seed: 5.3 }]
      : [{ x: r.width * 0.84, y: r.height * 0.2, s: 1.0, seed: 1.7 }, { x: r.width * 0.06, y: r.height * 0.9, s: 0.85, seed: 4.2 }];
    peaks.forEach(function (pk) {
      for (var i = 1; i <= 16; i++) {
        var base = i * 34 * pk.s;
        ctx.beginPath();
        for (var a = 0; a <= Math.PI * 2 + 0.01; a += Math.PI / 90) {
          var wob = 1 + 0.16 * Math.sin(a * 3 + pk.seed + i * 0.22) + 0.08 * Math.sin(a * 5 - pk.seed * 2 + i * 0.13) + 0.05 * Math.cos(a * 7 + i * 0.4);
          var x = pk.x + Math.cos(a) * base * 1.35 * wob, y = pk.y + Math.sin(a) * base * 0.85 * wob;
          if (a === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.closePath(); ctx.stroke();
      }
    });
  }
  if (topos.length) {
    var redraw = function () { topos.forEach(drawTopo); };
    redraw();
    var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(redraw, 150); });
  }

  /* ---------- Photo strip (Home, Checkpoint 47): swipe on a phone; Previous/Next or the arrow keys on a computer. It never moves by itself. ----------
     Without this script the strip still scrolls sideways (with its own scrollbar) and the count and buttons stay hidden. A button at the end of the
     strip is marked aria-disabled (not disabled), so keyboard focus never jumps away from it. Checkpoint 49: Previous/Next move one photo at a time,
     and the count ("3 of 8") and the thin progress line follow the strip however it is moved. */
  $$('[data-carousel]').forEach(function (car) {
    var track = $('.car-track', car), ctrl = $('.car-ctrl', car), prev = $('.car-prev', car), next = $('.car-next', car);
    var now = $('.car-now', car), bar = $('.car-bar span', car), slides = $$('.car-slide', car);
    if (!track || !ctrl || !prev || !next || !slides.length) return;
    ctrl.hidden = false;
    car.classList.add('car-on');
    var atStart = function () { return track.scrollLeft <= 2; };
    var atEnd = function () { return track.scrollLeft >= track.scrollWidth - track.clientWidth - 2; };
    var pad = function () { return parseFloat(getComputedStyle(track).scrollPaddingLeft) || 0; };
    // the photo whose left edge is nearest the strip's starting line (at the very end, the last photo)
    var current = function () {
      if (atEnd()) return slides.length - 1;
      var line = track.getBoundingClientRect().left + pad(), best = 0, dist = Infinity;
      slides.forEach(function (s, i) { var d = Math.abs(s.getBoundingClientRect().left - line); if (d < dist) { dist = d; best = i; } });
      return best;
    };
    var sync = function () {
      prev.setAttribute('aria-disabled', atStart() ? 'true' : 'false');
      next.setAttribute('aria-disabled', atEnd() ? 'true' : 'false');
      if (now) now.textContent = current() + 1;
      if (bar) {
        var sw = track.scrollWidth || 1, w = Math.min(1, track.clientWidth / sw);
        bar.style.setProperty('--car-w', (w * 100) + '%');
        bar.style.setProperty('--car-x', (w < 1 ? (track.scrollLeft / (sw - track.clientWidth)) * ((1 - w) / w) * 100 : 0) + '%');
      }
    };
    var step = function (dir) {
      if (dir < 0 ? atStart() : atEnd()) return;
      var i = Math.max(0, Math.min(slides.length - 1, current() + dir));
      var left = slides[i].getBoundingClientRect().left - track.getBoundingClientRect().left - pad();
      track.scrollBy({ left: left, behavior: reduce ? 'auto' : 'smooth' });
    };
    prev.addEventListener('click', function () { step(-1); });
    next.addEventListener('click', function () { step(1); });
    var raf = 0;
    track.addEventListener('scroll', function () { cancelAnimationFrame(raf); raf = requestAnimationFrame(sync); }, { passive: true });
    window.addEventListener('resize', sync);
    window.addEventListener('load', sync);
    sync();
  });

  /* The contact form is its own file, js/form.js (Checkpoint 46); only Home and Contact load it. */

  window.__glpReady = true;   // the page's own safety timer (in the head) checks this: if it is missing after 6 s, every section is shown
})();
