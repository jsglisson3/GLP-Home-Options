/* GLP Home Options: the contact form (Checkpoint 46). Loaded only on the pages that have the form (Home and Contact). ES5, no libraries.

   What it does, in the order a visitor meets it:
     1. opens with the right choice ticked when a button said what the visitor wants (a button's data-topic, or ?for=sell in the address);
     2. formats the phone number as it is typed, never fighting the finger (it leaves deleting, a leading 1 or +, and edits in the middle alone);
     3. checks the name, phone and email when the visitor presses Send (and again, gently, when they leave a field that has something in it), says what is
        wrong in plain words next to the field AND in one box at the top (which follows the boxes below it, so a line goes when its problem is fixed), and moves the focus there;
     4. sends. Two ways, chosen by data-endpoint on the form (set once, in tools/build-pages.py FORM_ENDPOINT):
          empty (today)   nothing is sent from here. The details become a ready-made text and email; the visitor's own phone or mail app sends it, and the
                          page says plainly that nothing has been sent until they do. A "Copy my message" button and the phone number are always there too.
          an https address  the details are posted there (as JSON, or as an ordinary web form: data-format, FORM_FORMAT in the builder); "Thank you" shows when
                          it says yes; if it fails or times out the visitor gets the text/email hand-off instead, so a lead is never lost to a dead end.
   Nothing here is ever sent anywhere except by the visitor's own app (today) or to FORM_ENDPOINT (later). Nothing is stored in the browser.
   A hidden "website" box is for robots. The page never judges it (a person's password manager can fill it by mistake, and a person must never be told "thank you" for a request that
   went nowhere): when it has something in it, it is posted along with how many seconds the form was open, and the receiving end decides (research/form-wiring.md).
   The two text-message boxes are never touched by this file except to read them. tools/form-test.py plays all of this. */
(function () {
  'use strict';
  var doc = document;
  var form = doc.getElementById('lf');
  if (!form) return;

  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var coarse = !!(window.matchMedia && window.matchMedia('(pointer: coarse)').matches);   // a phone or tablet
  var smallScreen = !window.screen || Math.min(screen.width || 0, screen.height || 0) < 500;   // ...and only a phone-sized one can be counted on to send a text (an iPad with no iPhone beside it cannot; a computer cannot)
  var phoneLike = coarse && smallScreen;
  var card = form.closest ? form.closest('.form-card') : null;

  var f = { name: $('#lf-name'), phone: $('#lf-phone'), email: $('#lf-email'), address: $('#lf-address'), message: $('#lf-message') };
  var sum = $('#lf-sum'), more = $('#lf-more'), send = $('.lf-send', form), sendT = $('.lf-send-t', form), status = $('#lf-status');
  var hand = $('#lf-hand'), done = $('#lf-done'), live = $('#lf-live');
  var SMS = form.getAttribute('data-sms') || '', MAIL = form.getAttribute('data-mail') || '', ENDPOINT = form.getAttribute('data-endpoint') || '';
  var FORMAT = form.getAttribute('data-format') === 'form' ? 'form' : 'json', CONSENT_V = form.getAttribute('data-consent-version') || '';   // how the details are posted, and which wording of the two text-message boxes was on screen
  var opened = Date.now();   // when the form appeared: how long people spent on it is sent along, so a robot that fills it in at once can be told from a person
  var sendLabel = sendT ? sendT.textContent : '', working = false, launched = false, lastBody = '';

  /* ---------- small helpers ---------- */
  function clean(s) { return s.replace(/([\uD800-\uDBFF][\uDC00-\uDFFF])|[\uD800-\uDFFF]/g, function (m, pair) { return pair ? m : '\uFFFD'; }); }   // half an emoji (a broken paste) would make the link-building throw: a whole emoji is kept, any other half is swapped for the usual replacement mark
  function val(el) { return clean(String(el && el.value || '')).replace(/^\s+|\s+$/g, ''); }
  function digits(s) { return String(s).replace(/\D/g, ''); }
  function usDigits(s) { var d = digits(s); return d.length === 11 && d.charAt(0) === '1' ? d.slice(1) : d; }   // a leading country code 1 is not part of the number
  function isIntl(s) { return /^\s*\+/.test(s) && digits(s).charAt(0) !== '1'; }   // +44 20 7946 0958: another country's number (a homeowner who lives abroad, say). Kept exactly as typed; only its length is checked
  function pretty(d) {   // (423) 451-5707, built up as the digits arrive
    if (d.length > 6) return '(' + d.slice(0, 3) + ') ' + d.slice(3, 6) + '-' + d.slice(6, 10);
    if (d.length > 3) return '(' + d.slice(0, 3) + ') ' + d.slice(3);
    return d.length ? '(' + d : '';
  }
  function greet(name) {   // "Pat" from "pat jones"; nothing from "Mrs. Smith", "J.R." or a lone initial, so the thank-you never reads "Thank you, Mrs.."
    var w = String(name || '').split(' ')[0];
    if (!/^[A-Za-z\u00C0-\u024F][A-Za-z\u00C0-\u024F'\u2019-]+$/.test(w) || /^(mr|mrs|ms|miss|dr)$/i.test(w)) return '';
    return w.charAt(0).toUpperCase() + w.slice(1);
  }
  function checked(name) { var r = $('input[name="' + name + '"]:checked', form); return r ? r.value : ''; }
  function labelOf(name, value) { var r = value ? $('input[name="' + name + '"][value="' + value + '"]', form) : null; var s = r ? $('span', r.parentNode) : null; return s ? s.textContent : ''; }
  function ascii(s) { return String(s).replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/[–—]/g, '-').replace(/\u2026/g, '...').replace(/ /g, ' '); }   // a curly quote makes a text message cost double
  function bring(el, box) {   // move the keyboard and screen-reader focus to el, and the screen to box (the whole card unless told otherwise) if it is out of sight
    try { el.focus({ preventScroll: true }); } catch (e) { el.focus(); }
    box = box || card || el;
    var top = box.getBoundingClientRect().top;
    if (top < 70 || top > (window.innerHeight || 800) * 0.55) box.scrollIntoView({ block: 'start', behavior: reduce ? 'auto' : 'smooth' });
  }

  /* ---------- 1. a button said what the visitor wants ---------- */
  function setTopic(v) {
    var r = v ? $('input[name="topic"][value="' + v + '"]', form) : null;
    if (r) r.checked = true;
    return !!r;
  }
  var asked = /[?&]for=([a-z]+)/.exec(location.search);
  if (asked) setTopic(asked[1]);
  doc.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[data-topic]') : null;
    if (a) setTopic(a.getAttribute('data-topic'));
  });

  /* ---------- 2. the phone number, formatted as it is typed ---------- */
  f.phone.addEventListener('input', function (e) {
    if (e && e.isComposing) return;   // a keyboard that is still building a word (some Android ones): wait until it has finished
    if (((e && e.inputType) || '').indexOf('delete') === 0) return;   // never fight someone who is deleting
    var v = f.phone.value, d = digits(v), atEnd = true;
    if (!d || /^\s*\+/.test(v) || d.charAt(0) === '1' || d.charAt(0) === '0' || d.length > 10) return;   // a country code or an odd start: leave it as typed (it is tidied when they leave the field)
    try { atEnd = f.phone.selectionStart === v.length; } catch (x) {}
    if (!atEnd) return;   // an edit in the middle: leave it alone, so the cursor never jumps
    var p = pretty(d);
    if (p !== v) f.phone.value = p;
  });
  function tidyPhone() {   // on leaving the field, on autofill, and after a composing keyboard: any way of writing a US number becomes (423) 451-5707
    if (isIntl(f.phone.value)) return;
    var d = usDigits(f.phone.value);
    if (d.length === 10) f.phone.value = pretty(d);
  }
  f.phone.addEventListener('blur', tidyPhone);
  f.phone.addEventListener('change', tidyPhone);
  f.phone.addEventListener('compositionend', tidyPhone);

  /* ---------- 3. checking, in plain words ---------- */
  var CHECK = {
    name: function () { return val(f.name).replace(/\s+/g, ' ').length < 2 ? 'Please tell us your name.' : ''; },
    phone: function () {
      var raw = val(f.phone), d = usDigits(raw), n = digits(raw).length;
      if (!n) return 'Please add a phone number so we can reach you.';
      if (isIntl(raw)) return n < 8 || n > 15 ? 'That phone number doesn\u2019t look right. Please include the country code and the whole number.' : '';
      if (d.length < 10) return 'That phone number looks too short. Please include the area code, like (423) 555-0123.';
      if (d.length > 10) return 'That phone number has too many digits. Please check it. (An extension can go in the note.)';
      if (!/^[2-9]\d\d[2-9]\d{6}$/.test(d)) return 'That phone number doesn\u2019t look right. Please check the area code and the first three digits.';   // no US number starts an area code or the next three digits with 0 or 1
      return '';
    },
    email: function () {
      var v = val(f.email);
      if (!v) return '';   // optional
      return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? '' : "That email address doesn\u2019t look right. It should look like name@example.com.";
    }
  };
  var KEYS = ['name', 'phone', 'email'];
  var SUM_ONE = 'Almost there. One thing to check:', SUM_MANY = 'Almost there. A few things to check:';

  function setErr(key, msg) {
    var wrap = $('[data-f="' + key + '"]', form), inp = f[key], out = $('#lf-' + key + '-err');
    if (!wrap || !inp || !out) return;
    if (msg) {
      out.textContent = '';
      out.innerHTML = '<svg class="i" aria-hidden="true"><use href="#i-alert"/></svg><span class="vh">Error: </span><span></span>';
      out.lastChild.textContent = msg;
      out.hidden = false; wrap.classList.add('err'); inp.setAttribute('aria-invalid', 'true');
    } else {
      out.hidden = true; out.textContent = ''; wrap.classList.remove('err'); inp.removeAttribute('aria-invalid');
    }
    syncSummary(key, msg);
  }
  KEYS.forEach(function (k) {
    f[k].addEventListener('input', function () { if (f[k].getAttribute('aria-invalid')) setErr(k, CHECK[k]()); });   // an error clears the moment it is fixed
    f[k].addEventListener('blur', function () { if (val(f[k]) || f[k].getAttribute('aria-invalid')) setErr(k, CHECK[k]()); });   // a field left empty is not scolded; one with something wrong in it is told
  });

  function showSummary(list) {
    sum.textContent = '';
    var box = doc.createElement('div'), h = doc.createElement('p'), ul = doc.createElement('ul');
    box.setAttribute('role', 'alert');   // on an inner box, not on the one that takes focus: some screen readers skip the text when both are the same element
    h.className = 'lf-sum-h'; h.textContent = list.length === 1 ? SUM_ONE : SUM_MANY;
    list.forEach(function (it) {
      var li = doc.createElement('li'), a = doc.createElement('a');
      a.href = '#lf-' + it[0]; a.setAttribute('data-for', it[0]); a.textContent = it[1];
      li.appendChild(a); ul.appendChild(li);
    });
    box.appendChild(h); box.appendChild(ul); sum.appendChild(box);
    sum.hidden = false;
    if (list.some(function (it) { return it[0] === 'email'; }) && more) more.open = true;   // the email field lives in the extras: open them so the problem is in plain sight
    bring(sum, sum);   // the box itself comes to the top of the screen (its CSS leaves room for the header), with the name and phone boxes just under it
  }
  function hideSummary() { sum.hidden = true; sum.textContent = ''; }
  function syncSummary(key, msg) {   // the box at the top follows the boxes below it: a line changes with its message and goes the moment its problem is fixed, and the box goes with the last line
    if (sum.hidden) return;
    var a = $('a[data-for="' + key + '"]', sum), box = $('[role="alert"]', sum), li, h, left;
    if (!a) return;
    if (msg && a.textContent === msg) return;   // nothing changed (leaving the box the summary has just pulled focus away from says the same thing again): the alert on the box must stay, or the first announcement is lost
    if (box) box.removeAttribute('role');   // it was announced when it appeared; what changes while someone is typing must not interrupt them
    if (msg) { if (a.textContent !== msg) a.textContent = msg; return; }
    li = a.parentNode; li.parentNode.removeChild(li);
    left = $$('li', sum).length;
    if (!left) { hideSummary(); return; }
    h = $('.lf-sum-h', sum);
    if (h) h.textContent = left === 1 ? SUM_ONE : SUM_MANY;
  }
  sum.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[data-for]') : null;
    if (!a) return;
    e.preventDefault();
    var el = f[a.getAttribute('data-for')];
    if (a.getAttribute('data-for') === 'email' && more) more.open = true;   // the extras may have been closed again since the box appeared
    if (el) el.focus();
  });

  /* the keyboard's "next" key. An iPhone's "next" still sends Enter, and Enter in a text box sends the whole form: make the key do what its label says */
  var NEXT = { 'lf-name': 'phone', 'lf-email': 'address', 'lf-address': 'message' };
  form.addEventListener('keydown', function (e) {
    var t = e.target, to = t && NEXT[t.id];
    if (e.key !== 'Enter' || e.isComposing || e.keyCode === 229 || !t) return;
    if (t.type === 'radio' || t.type === 'checkbox') { e.preventDefault(); return; }   // Space ticks a choice; Enter on one must not send a half-finished form
    if (e.repeat && t.tagName === 'INPUT') { e.preventDefault(); return; }   // a key held a moment too long: the first press moved on, the repeats must not send the form from the next box
    if (!to) return;
    e.preventDefault();
    try { f[to].focus(); } catch (x) {}
  });

  /* ---------- the message the visitor's own app will send ---------- */
  function collect() {
    var topic = checked('topic'), channel = checked('channel');
    return {
      name: val(f.name).replace(/\s+/g, ' '),
      phone: isIntl(f.phone.value) ? val(f.phone).replace(/\s+/g, ' ') : pretty(usDigits(f.phone.value)),
      email: val(f.email),
      topic: topic, topic_label: labelOf('topic', topic),
      channel: channel,
      address: val(f.address),
      message: val(f.message),
      consent_service: !!$('input[name="consent_service"]:checked', form),
      consent_marketing: !!$('input[name="consent_marketing"]:checked', form),
      consent_version: CONSENT_V,
      page: location.origin + location.pathname,
      sent_at: new Date().toISOString(),
      seconds_on_form: Math.round((Date.now() - opened) / 1000),
      website: val($('#lf-web'))   // the hidden trap field: people never see it, so anything in it is a robot
    };
  }
  function compose(d) {
    var L = ["Hi Joey and Ethan, this is " + d.name + ". I'm reaching out from your website.", ''];
    if (d.topic_label) L.push('Interested in: ' + d.topic_label);
    L.push('Best number: ' + d.phone);
    if (d.email) L.push('Email: ' + d.email);
    if (d.channel) L.push('Best way to reach me: ' + labelOf('channel', d.channel));
    if (d.consent_service) L.push('Text messages OK (non-marketing): yes');   // a box they ticked is not lost: until a receiving end records it, this line in their own message is the record
    if (d.consent_marketing) L.push('Text messages OK (marketing): yes');
    if (d.address) L.push('Home address or ZIP: ' + d.address);
    if (d.message) L.push('', d.message);
    return ascii(L.join('\n'));
  }
  function smsHref(body) { return SMS + '?&body=' + encodeURIComponent(body); }   // "?&body=" is read the same way by iPhone and Android
  function mailHref(d, body) {   // the subject is what Joey scans in his inbox: who, and what they want
    var subject = 'Website request from ' + d.name + (d.topic_label ? ' - ' + d.topic_label : '');
    return 'mailto:' + MAIL + '?subject=' + encodeURIComponent(ascii(subject)) + '&body=' + encodeURIComponent(body.replace(/\n/g, '\r\n'));
  }

  /* ---------- what shows: the form, the ready-made message, or the thank-you ---------- */
  var shownAt = 0;
  doc.addEventListener('click', function (e) {   // a double-click on Send: its second click would land on whatever the new panel put under the pointer (Change my details, the Call link, or, on a phone where the panel is shorter than the form, the tiles below it). A panel ignores clicks, anywhere, for its first moments.
    var dt = Date.now() - shownAt;   // a clock set back by the phone must not leave the buttons dead (dt below 0)
    if (shownAt && dt >= 0 && dt < 450 && !form.contains(e.target)) { e.preventDefault(); e.stopPropagation(); }
  }, true);
  function showPanel(p) {
    form.hidden = !!p;
    hand.hidden = p !== hand;
    done.hidden = p !== done;
    shownAt = p ? Date.now() : 0;
    if (p) bring(p);
  }
  function showForm(focusName) {
    showPanel(null);
    if (live) live.textContent = '';
    launched = false;
    if (focusName) { try { f.name.focus(); } catch (e) {} }
  }
  function say(variant) {   // one of the three lines under the heading of the message panel, which a screen reader hears with the panel's name
    $$('[data-v]', hand).forEach(function (p) { p.hidden = p.getAttribute('data-v') !== variant; });
    hand.setAttribute('aria-describedby', 'lf-lede-' + variant);
  }
  function words(smsFirst) {   // the first button is the main one: its words say so, and the other says "or"
    var st = $('#lf-sms-t'), mt = $('#lf-mail-t');
    if (st) st.textContent = smsFirst ? 'Text it to Joey & Ethan' : 'Or text it instead';
    if (mt) mt.textContent = smsFirst ? 'Or email it instead' : 'Email it to Joey & Ethan';
  }
  function showHand(d, failed) {
    var body = compose(d), actions = $('.lf-actions', hand), sms = $('#lf-sms'), mail = $('#lf-mail');
    lastBody = body;
    $('#lf-msg').textContent = body;
    sms.href = smsHref(body); mail.href = mailHref(d, body);
    var mailFirst = !phoneLike || d.channel === 'email';   // a phone: text first, unless they said they prefer email. A computer or tablet: email first (what they prefer for the REPLY is not what this device can send)
    var first = mailFirst ? mail : sms, second = mailFirst ? sms : mail;
    actions.insertBefore(first, actions.firstChild);
    first.className = 'btn btn-primary btn-lg'; second.className = 'btn btn-ghost btn-lg';
    words(!mailFirst);
    $('#lf-hand-h').textContent = failed ? "We couldn\u2019t confirm that was sent" : 'Your message is ready to send';
    say(failed ? 'fail' : (mailFirst ? 'mail' : 'sms'));
    if (live) live.textContent = '';
    launched = false;
    showPanel(hand);
  }
  function showDone(d) {
    var first = greet(d.name);
    $('#lf-first').textContent = first ? ', ' + first : '';
    showPanel(done);
  }

  hand.addEventListener('click', function (e) {
    var t = e.target && e.target.closest ? e.target.closest('a,button') : null;
    if (!t) return;
    if (t.id === 'lf-sms' || t.id === 'lf-mail') { launched = true; return; }   // let the phone's own app open
    if (t.id === 'lf-edit') { showForm(true); return; }
    if (t.id === 'lf-copy') {
      copyText(lastBody, function () { if (live) live.textContent = 'Copied. You can paste it into any message or email.'; },
                         function () { if (live) live.textContent = "Couldn\u2019t copy it from here. Select the message above to copy it."; });
    }
  });
  done.addEventListener('click', function (e) {
    var t = e.target && e.target.closest ? e.target.closest('button') : null;
    if (t && t.id === 'lf-again') {
      form.reset(); KEYS.forEach(function (k) { setErr(k, ''); }); hideSummary(); if (more) more.open = false; opened = Date.now();
      showForm(true);
    }
  });
  doc.addEventListener('visibilitychange', function () {   // back from the messages or mail app: say what to do next, without pretending to know whether they pressed Send
    if (doc.hidden || !launched || hand.hidden || !live) return;
    live.textContent = 'Back already? If your message went through, Joey and Ethan have it. If not, try the button again, or call us.';
  });
  function copyText(text, ok, bad) {
    function legacy() {
      var ta = doc.createElement('textarea'), good = false, prev = doc.activeElement;
      ta.value = text; ta.setAttribute('readonly', ''); ta.style.cssText = 'position:fixed;left:-9999px;top:0;opacity:0';
      doc.body.appendChild(ta); ta.select();
      try { ta.setSelectionRange(0, text.length); good = doc.execCommand('copy'); } catch (e) {}
      doc.body.removeChild(ta);
      if (prev && prev.focus) { try { prev.focus({ preventScroll: true }); } catch (e) {} }   // selecting took the keyboard's place: give it back to the Copy button
      (good ? ok : bad)();
    }
    if (navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext) navigator.clipboard.writeText(text).then(ok, legacy); else legacy();
  }

  /* ---------- 4. sending ---------- */
  function busy(on) {
    working = on;
    if (!send) return;
    if (on) {
      send.setAttribute('aria-busy', 'true');
      if (sendT) sendT.textContent = 'Sending';
      var sp = doc.createElement('span'); sp.className = 'spin'; sp.setAttribute('aria-hidden', 'true'); send.insertBefore(sp, send.firstChild);
      if (status) status.textContent = 'Sending your details.';
    } else {
      send.removeAttribute('aria-busy');
      if (sendT) sendT.textContent = sendLabel;
      var s = $('.spin', send); if (s) s.parentNode.removeChild(s);
      if (status) status.textContent = '';
    }
  }
  function encode(o) {   // name=value&name=value, the way an ordinary web form is sent (true and false become yes and no)
    var out = [], k, x;
    for (k in o) { if (!o.hasOwnProperty(k)) continue; x = o[k]; if (x === true) x = 'yes'; else if (x === false) x = 'no'; out.push(encodeURIComponent(k) + '=' + encodeURIComponent(String(x))); }
    return out.join('&');
  }
  function post(d) {
    if (!window.fetch || !window.Promise) { showHand(d, true); return; }
    var finished = false, ctl = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctl) ctl.abort(); fail(); }, 15000);
    function good() { if (finished) return; finished = true; clearTimeout(timer); busy(false); showDone(d); }
    function fail() {   // collect() again: the visitor may have fixed a typo while it waited. But not if they emptied or broke a box meanwhile: then the details that passed the check are used, so the message never reads "this is ."
      if (finished) return; finished = true; clearTimeout(timer); busy(false);
      showHand(KEYS.some(function (k) { return CHECK[k](); }) ? d : collect(), true);
    }
    busy(true);
    var payload = {}, k;
    for (k in d) { if (d.hasOwnProperty(k) && (k !== 'website' || d.website)) payload[k] = d[k]; }   // the trap field goes along only when it has something in it (a slow robot: the receiving end can drop it)
    var asForm = FORMAT === 'form';   // both ways are "simple" requests: the browser sends them at once, with no permission check first
    fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': asForm ? 'application/x-www-form-urlencoded;charset=UTF-8' : 'text/plain;charset=UTF-8' }, body: asForm ? encode(payload) : JSON.stringify(payload), mode: 'cors', credentials: 'omit', keepalive: true, signal: ctl ? ctl.signal : undefined })
      .then(function (r) { if (r && r.ok) good(); else fail(); }, fail);
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (working) return;
    try {
      var bad = [];
      KEYS.forEach(function (k) { var m = CHECK[k](); setErr(k, m); if (m) bad.push([k, m]); });
      if (bad.length) { showSummary(bad); return; }
      hideSummary();
      var d = collect();
      // The hidden trap field is NOT judged here. A robot fills it in; so, now and then, does a person's password manager, and a person must never be shown a
      // thank-you for a request that went nowhere. So it is posted (with the seconds the form was open) and the receiving end decides what to do with it.
      // Nothing is posted in the hand-off, so there the trap field is simply ignored.
      if (ENDPOINT) post(d); else showHand(d, false);
    } catch (err) {   // something unforeseen: never leave a button that does nothing. Give the visitor the call, text and email card instead.
      busy(false);
      doc.documentElement.classList.remove('js');
    }
  });
  if (window.__glpReady && !doc.documentElement.classList.contains('js')) doc.documentElement.classList.add('js');   // a very slow connection: the page's 6-second timer (in the head) may already have swapped the form for the call, text and email card. Both scripts have now run, so the form comes back.
  window.__glpForm = true;   // the page's own safety timer (in the head) checks this: if it is missing after 6 s, the form gives way to the call, text and email card
})();
