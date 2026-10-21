/* GLP Home Options: hero PROTOTYPES only (Session 3). Cool/Warm surface toggle. Delete with css/proto.css in Session 6. */
(function () {
  'use strict';
  var root = document.documentElement;
  var buttons = document.querySelectorAll('.proto-bar [data-surface]');
  var links = document.querySelectorAll('.proto-bar a[data-base]');

  function apply(surface, remember) {
    var warm = surface === 'warm';
    if (warm) root.setAttribute('data-surface', 'warm'); else root.removeAttribute('data-surface');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].setAttribute('aria-pressed', String(buttons[i].getAttribute('data-surface') === (warm ? 'warm' : 'cool')));
    }
    /* the A/B links carry the choice along, so both prototypes can be compared in the same state */
    for (var j = 0; j < links.length; j++) {
      var base = links[j].getAttribute('data-base');
      links[j].setAttribute('href', warm ? base + '?surface=warm' : base);
    }
    if (remember) {
      try { history.replaceState(null, '', location.pathname + (warm ? '?surface=warm' : '') + location.hash); } catch (e) { /* ignore */ }
    }
  }

  for (var k = 0; k < buttons.length; k++) {
    buttons[k].addEventListener('click', function () { apply(this.getAttribute('data-surface'), true); });
  }
  apply(root.getAttribute('data-surface') === 'warm' ? 'warm' : 'cool', false);
})();
