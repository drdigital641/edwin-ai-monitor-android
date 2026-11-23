/* Booking portal page script: iframe height + confirmed signal to the parent (no PII), cookie fallback signal. */
(function () {
  var inFrame = window.parent !== window, d = document;
  function post(msg) { try { window.parent.postMessage(msg, '*'); } catch (e) {} }
  if (inFrame) {
    var last = 0;
    var send = function () { var h = Math.ceil(d.documentElement.scrollHeight); if (Math.abs(h - last) > 2) { last = h; post({ type: 'p1-booking-height', h: h }); } };
    window.addEventListener('load', send);
    if ('ResizeObserver' in window) new ResizeObserver(send).observe(d.body || d.documentElement); else setInterval(send, 800);
    d.addEventListener('DOMContentLoaded', function () {
      send();
      var ok = d.querySelector('[data-confirmed]');
      if (ok) post({ type: 'p1-booking-confirmed', client: ok.getAttribute('data-confirmed') });
      var nc = d.querySelector('[data-nocookie]');
      if (nc) post({ type: 'p1-booking-nocookie', client: nc.getAttribute('data-nocookie') });
    });
  }
  if (inFrame) d.addEventListener('keydown', function (e) { if (e.key === 'Escape') post({ type: 'p1-booking-close' }); });
  /* copy buttons for embed codes (super-admin) */
  d.addEventListener('focusin', function (e) { if (e.target.classList && e.target.classList.contains('code')) e.target.select(); });
})();
