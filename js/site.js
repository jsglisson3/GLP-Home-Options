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

  /* ---------- Scroll: header state, progress bar, ridge parallax ---------- */
  var hdr = $('#hdr'), hero = $('.hero, .phero'), ridge = $('.ridge');
  var ticking = false;
  function update() {
    ticking = false;
    var y = window.pageYOffset || doc.documentElement.scrollTop || 0;
    var vh = window.innerHeight || 800;
    if (hdr) {
      hdr.classList.toggle('scrolled', y > 8);
      var max = Math.max(1, doc.documentElement.scrollHeight - vh);
      hdr.style.setProperty('--sp', clamp(y / max, 0, 1).toFixed(4));
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

  /* ---------- Count-up on the stats strip ---------- */
  var counters = $$('[data-count]');
  function countUp(el) {
    var to = parseFloat(el.getAttribute('data-count')), from = parseFloat(el.getAttribute('data-from') || '0');
    var dur = 1200, t0 = null;
    function step(t) {
      if (t0 === null) t0 = t;
      var p = clamp((t - t0) / dur, 0, 1), e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(from + (to - from) * e);
      if (p < 1) window.requestAnimationFrame(step);
    }
    window.requestAnimationFrame(step);
  }
  if (counters.length && !reduce && 'IntersectionObserver' in window) {
    counters.forEach(function (el) { el.textContent = el.getAttribute('data-from') || '0'; });
    var stats = $('.stats'), fired = false;
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { fired = true; counters.forEach(countUp); cio.disconnect(); }
      });
    }, { threshold: 0.25 });
    if (stats) cio.observe(stats);
    /* failsafe: never leave a placeholder number on screen if the strip is never scrolled into view */
    setTimeout(function () {
      if (!fired) counters.forEach(function (el) { el.textContent = el.getAttribute('data-count'); });
    }, 8000);
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
    window.addEventListener('resize', function () { if (window.innerWidth > 1160 && !mnav.hidden) setMenu(false); });
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
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(map).forEach(function (id) { var s = doc.getElementById(id); if (s) sio.observe(s); });
  }

  /* ---------- "What matters most?" picker ---------- */
  var picker = $('.picker');
  if (picker) {
    var btns = $$('.picker-opts button', picker), out = $('#picker-out'), cards = $$('.path, .opt-sec');
    var linkBase = picker.getAttribute('data-href') || '#path-';
    var idle = out ? out.textContent : '';
    var msgs = {
      direct: 'If speed matters most, selling directly can close in 7–14 days, as-is, with no repairs, showings, or commission.',
      list: 'If you want the highest price and aren’t in a rush, listing with an agent usually nets the most, especially for a move-in ready home.',
      keep: 'If you’d rather stay, we can look at refinancing, renting the home out, or other ways to get past a rough patch.'
    };
    var setPick = function (p) {
      var same = btns.some(function (b) { return b.getAttribute('data-path') === p && b.getAttribute('aria-pressed') === 'true'; });
      var next = same ? null : p;
      btns.forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-path') === next)); });
      cards.forEach(function (c) { c.classList.toggle('on', c.getAttribute('data-path') === next); });
      if (!out) return;
      if (next) {
        out.textContent = msgs[next] + ' ';
        var a = doc.createElement('a');
        a.href = linkBase + next; a.textContent = 'See the details';
        a.style.cssText = 'font-weight:700;color:var(--green-700);text-underline-offset:3px';
        out.appendChild(a);
      } else { out.textContent = idle; }
    };
    btns.forEach(function (b) { b.addEventListener('click', function () { setPick(b.getAttribute('data-path')); }); });
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
      var max = Math.max(netList, netDirect, 1);
      el('b-list').style.width = Math.max(0, netList / max * 100) + '%';
      el('b-direct').style.width = Math.max(0, netDirect / max * 100) + '%';
      el('bv-list').textContent = usd(netList);
      el('bv-direct').textContent = usd(netDirect);
      var diff = netList - netDirect, v = el('verdict'), s = el('verdict-sub'), off = price - offer;
      if (Math.abs(diff) < 500) {
        v.innerHTML = 'About the <span>same</span> either way.';
        s.textContent = 'When the money is this close, speed, certainty, and skipping showings and repairs may decide it.';
      } else if (diff > 0) {
        v.innerHTML = 'Listing nets about <span>' + usd(diff) + '</span> more.';
        s.textContent = 'Selling direct trades that for closing in 7 to 14 days with no repairs, showings, or months of carrying costs. The offer is ' + usd(off) + ' below list price, but the gap in your pocket is smaller once costs come out.';
      } else {
        v.innerHTML = 'Selling direct nets about <span>' + usd(-diff) + '</span> more.';
        s.textContent = 'Once commission, closing costs, repairs, and carrying costs come out, the direct offer leaves you ahead, and you close in 7 to 14 days.';
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

  /* ---------- Contact form: hide the "loading" note once the embed is in ---------- */
  var gf = $('.ghl iframe');
  if (gf) {
    var box = gf.parentElement, done = function () { box.classList.add('loaded'); };
    gf.addEventListener('load', done); setTimeout(done, 7000);
  }
})();
