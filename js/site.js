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
     that moves the page (the browser's saved spot, the contact form loading) is undone. Add ?scrolldebug to the address to see
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
      var diff = netList - netDirect, v = el('verdict'), s = el('verdict-sub'), off = price - offer;
      if (Math.abs(diff) < 500) {
        v.innerHTML = 'About the <span>same</span> either way.';
        s.textContent = 'When the money is this close, speed, certainty, and skipping showings and repairs may decide it.';
      } else if (diff > 0) {
        v.innerHTML = 'You\u2019d keep about <span>' + usd(diff) + '</span> more by listing.';
        s.textContent = 'Selling direct gives that up, but you close in 7 to 14 days with no repairs, showings, or months of house payments and bills. The offer is ' + usd(off) + ' below the list price, but the gap in your pocket is smaller once costs come out.';
      } else {
        v.innerHTML = 'You\u2019d keep about <span>' + usd(-diff) + '</span> more by selling direct.';
        s.textContent = 'Once the commission, closing costs, repairs, and the cost of waiting come out, the direct offer leaves you ahead, and you close in 7 to 14 days.';
      }
      // Break-even (Checkpoint 36): the cash offer that leaves the same in your pocket as listing. Listing keeps price - payoff - costs; a direct sale keeps offer - payoff;
      // the mortgage cancels, so they are equal when offer = price - commission - closing costs - repairs - cost of waiting.
      var be = price - commAmt - closeAmt - repairs - carryAmt, bx = el('breakeven');
      if (bx) {
        if (price > 0 && be > 0 && be <= price) { bx.innerHTML = 'On these numbers, a cash offer above <strong>' + usd(be) + '</strong> keeps more in your pocket than listing.'; bx.hidden = false; }
        else { bx.textContent = ''; bx.hidden = true; }
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
    $$('#calc input').forEach(function (inp) {
      inp.addEventListener('input', calc);
      inp.addEventListener('blur', function () {
        if (inp.parentElement.classList.contains('pct')) return;
        var v = num(inp.id); inp.value = Math.round(v).toLocaleString('en-US');
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
        calc();
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

  /* ---------- Contact form ----------
     The form is the company's own (a GoHighLevel embed in a frame). Their embed script parks the frame 10,000 px off to the left, invisible,
     until the form has reported its height. A frame marked loading="lazy" is only fetched once it is near the screen, so a lazy frame that
     gets parked off to the left is never fetched at all: a blank box, the "form never loads" bug (found in Checkpoint 35). So there is no lazy
     attribute. This script adds the frame itself, when the box comes within about two screens of the visitor (or at once if it is already
     there), parked the same way, and then makes sure the visitor never meets a blank box:
       1. the box shows a calm "loading" card until the form has spoken (it sends the page messages once it is up) and has been shown;
       2. if the form has spoken but the embed script has not shown it after 6 s, we show it ourselves, at the height the form reported;
       3. if the form has not spoken after 12 s, the box turns into a "call or text us" card (and turns back into the form if it
          comes up after all); "Try the form again" builds a fresh frame.
     Time is counted only while the tab is visible: a background tab pauses the embed script's timers. */
  (function () {
    var box = $('.ghl[data-form]');
    if (!box) return;
    var FORM = box.getAttribute('data-form'), HOST = 'https://links.voiseai.com';
    var frame = null, timer = null, watcher = null, vis = 0, heardAt = -1, lastH = 0, started = false, tries = 0, vendorBad = false;

    function set(state) { if (box.getAttribute('data-state') !== state) box.setAttribute('data-state', state); }
    function parked() { var s = frame.style; return s.visibility === 'hidden' || s.opacity === '0' || s.left === '-9999px'; }
    function guess() {   // how tall the form is at this width (measured on the real form; it is taller where its text wraps more)
      var w = box.clientWidth || 300, T = [[260, 1340], [300, 1175], [340, 1050], [380, 1010], [420, 950], [483, 890], [560, 850], [700, 830]];
      if (w <= T[0][0]) return T[0][1];
      for (var i = 1; i < T.length; i++) {
        if (w <= T[i][0]) return Math.round(T[i - 1][1] + (T[i][1] - T[i - 1][1]) * (w - T[i - 1][0]) / (T[i][0] - T[i - 1][0]));
      }
      return T[T.length - 1][1];
    }
    function show() {   // put the frame where the form belongs (what the embed script does when it works)
      var s = frame.style;
      s.opacity = '1'; s.visibility = 'visible'; s.pointerEvents = 'auto'; s.display = 'block'; s.position = 'relative'; s.left = '';
      if (lastH > 0) s.height = (lastH + 5) + 'px';
    }
    function check() {
      if (!frame) return;
      if (heardAt < 0) { set(vis >= 12000 ? 'slow' : 'loading'); return; }
      if (!parked()) { set('ready'); if (timer) { clearInterval(timer); timer = null; } return; }
      if (vis - heardAt >= (vendorBad ? 1000 : 6000)) { show(); set('ready'); return; }
      set('loading');
    }
    function ticking() {
      if (timer) return;
      timer = setInterval(function () {
        if (!doc.hidden) vis += 250;
        check();
        if (vis >= 60000 && heardAt < 0 && timer) { clearInterval(timer); timer = null; }   // nothing heard for a minute: stop checking ("Try the form again" starts it again)
      }, 250);
    }
    function loadEmbed() {
      if ($('script[data-ghl]')) return;
      var sc = doc.createElement('script');
      sc.src = HOST + '/js/form_embed.js'; sc.async = true; sc.setAttribute('data-ghl', '');
      sc.onerror = function () { vendorBad = true; };
      doc.body.appendChild(sc);
    }
    function make() {
      var id = 'inline-' + FORM + (tries ? '-' + tries : ''), f = doc.createElement('iframe');
      f.id = id; f.src = HOST + '/widget/form/' + FORM;
      f.title = 'Contact form: send GLP Home Options a few details about your home';
      f.setAttribute('style', 'width:100%;height:' + guess() + 'px;border:none;border-radius:10px;position:absolute;left:-9999px;opacity:0;visibility:hidden;pointer-events:none');
      f.setAttribute('data-layout', "{'id':'INLINE'}");
      f.setAttribute('data-trigger-type', 'alwaysShow'); f.setAttribute('data-trigger-value', '');
      f.setAttribute('data-activation-type', 'alwaysActivated'); f.setAttribute('data-activation-value', '');
      f.setAttribute('data-deactivation-type', 'neverDeactivate'); f.setAttribute('data-deactivation-value', '');
      f.setAttribute('data-form-name', 'GLP Home Options lead form'); f.setAttribute('data-height', '760');
      f.setAttribute('data-layout-iframe-id', id); f.setAttribute('data-form-id', FORM);
      frame = f; vis = 0; heardAt = -1; lastH = 0;
      box.appendChild(f);
      if (window.MutationObserver) { watcher = new MutationObserver(function () { if (!timer && frame && parked()) ticking(); check(); }); watcher.observe(f, { attributes: true, attributeFilter: ['style'] }); }
      ticking(); loadEmbed();
    }
    function begin() { if (started) return; started = true; set('loading'); make(); }
    function retry() {
      if (timer) { clearInterval(timer); timer = null; }
      if (watcher) { watcher.disconnect(); watcher = null; }
      if (frame && frame.parentNode) frame.parentNode.removeChild(frame);
      frame = null; tries++; set('loading'); make();
    }

    window.addEventListener('message', function (e) {   // the form sends the page messages (its height, "I'm loaded", ...) once it is up
      if (!frame || e.source !== frame.contentWindow) return;
      if (heardAt < 0) heardAt = vis;
      var m = typeof e.data === 'string' && /^\[iFrameSizer\][^:]*:(\d+):/.exec(e.data);
      if (m && +m[1] > 200) lastH = +m[1];
      if (!timer) ticking();   // the form came up after we had stopped watching (a minute with nothing): watch again, so it is shown within 6 s
      check();
    });
    box.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('[data-ghl-retry]')) retry(); });

    if ('IntersectionObserver' in window) {
      var near = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { near.disconnect(); begin(); } }, { rootMargin: '1800px 0px' });
      near.observe(box);
    } else begin();
  })();

  window.__glpReady = true;   // the page's own safety timer (in the head) checks this: if it is missing after 6 s, every section is shown
})();
