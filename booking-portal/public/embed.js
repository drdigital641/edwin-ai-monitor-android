/* Booking embed (one shared file for every client).
   <script src="https://<portal>/booking/embed.js" data-client="<slug>" defer></script>
   - [data-p1-book] (optional data-service="<slug>") opens the booking page in a modal (desktop) or full-screen sheet (phone).
   - iframe[data-p1-booking] auto-resizes from {type:'p1-booking-height', h} messages sent by the portal origin only.
   Clicks are handled in the bubble phase on document and never stopped, so the site's tap counter (capture phase) records them first. */
(function () {
  if (window.__p1book) return; window.__p1book = 1;
  var d = document, me = d.currentScript || d.querySelector('script[src*="/embed.js"][data-client]');
  if (!me) return;
  var src = new URL(me.src, location.href), ORIGIN = src.origin, BASE = src.href.replace(/\/embed\.js.*$/, ''), CLIENT = me.getAttribute('data-client') || '';
  var KEY = 'p1book_tab_' + CLIENT, dlg = null, frame = null, lastFocus = null, pushed = false;
  function url(service, embed) {
    var u = new URL(BASE + '/' + encodeURIComponent(CLIENT) + '/');
    if (service) u.searchParams.set('service', service);
    if (embed) u.searchParams.set('embed', '1');
    return u.toString();
  }
  function preferTab() { try { return sessionStorage.getItem(KEY) === '1'; } catch (e) { return false; } }
  function css() {
    if (d.getElementById('p1book-css')) return;
    var s = d.createElement('style'); s.id = 'p1book-css';
    s.textContent = '.p1b-dlg[open]{display:flex;flex-direction:column}.p1b-dlg{border:0;padding:0;width:min(560px,96vw);height:min(860px,92vh);max-width:none;max-height:none;border-radius:16px;overflow:hidden;background:#fff;box-shadow:0 20px 60px rgba(0,0,0,.35)}'
      + '.p1b-dlg::backdrop{background:rgba(0,0,0,.55)}.p1b-dlg iframe{width:100%;flex:1 1 auto;min-height:0;border:0;display:block}.p1b-bar{flex:none;display:flex;justify-content:flex-end;padding:4px;background:#111}'
      + '.p1b-x{width:44px;height:44px;border-radius:50%;border:0;background:transparent;color:#fff;font:28px/44px sans-serif;cursor:pointer}'
      + '.p1b-fb{flex:1 1 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:16px;padding:24px;font:16px/1.4 system-ui,sans-serif;text-align:center}'
      + '.p1b-fb a{display:inline-flex;min-height:48px;align-items:center;padding:0 22px;border-radius:12px;background:#111;color:#fff;text-decoration:none;font-weight:700}'
      + '@media (max-width:640px){.p1b-dlg{width:100vw;height:100dvh;height:100vh;border-radius:0;margin:0;max-height:100vh}}';
    d.head.appendChild(s);
  }
  function close(fromPop) {
    if (!dlg) return;
    var x = dlg; dlg = null; frame = null;
    try { x.close(); } catch (e) {} x.remove();
    d.documentElement.style.overflow = '';
    if (pushed && !fromPop) { pushed = false; try { history.back(); } catch (e) {} }
    pushed = false;
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  function fallback(service) {
    if (!dlg) return;
    var box = d.createElement('div'); box.className = 'p1b-fb';
    var a = d.createElement('a'); a.href = url(service, false); a.target = '_blank'; a.rel = 'noopener'; a.textContent = 'Open booking';
    a.addEventListener('click', function () { setTimeout(function () { close(); }, 50); });
    box.appendChild(a);
    if (frame) frame.replaceWith(box);
    a.focus();
  }
  function open(service, opener) {
    if (preferTab() || typeof HTMLDialogElement !== 'function') { window.open(url(service, false), '_blank', 'noopener'); return; }
    css(); lastFocus = opener || d.activeElement;
    dlg = d.createElement('dialog'); dlg.className = 'p1b-dlg'; dlg.setAttribute('aria-label', 'Booking');
    var x = d.createElement('button'); x.type = 'button'; x.className = 'p1b-x'; x.setAttribute('aria-label', 'Close'); x.textContent = '×';
    x.addEventListener('click', function () { close(); });
    frame = d.createElement('iframe'); frame.src = url(service, true); frame.title = 'Booking'; frame.setAttribute('allow', 'clipboard-write');
    frame.setAttribute('data-p1-service', service || '');
    var bar = d.createElement('div'); bar.className = 'p1b-bar'; bar.appendChild(x);
    dlg.appendChild(bar); dlg.appendChild(frame); d.body.appendChild(dlg);
    dlg.addEventListener('cancel', function (e) { e.preventDefault(); close(); });   // Esc
    dlg.addEventListener('click', function (e) { if (e.target === dlg) close(); });
    dlg.showModal(); x.focus();
    d.documentElement.style.overflow = 'hidden';
    try { history.pushState({ p1book: 1 }, ''); pushed = true; } catch (e) {}
  }
  window.addEventListener('popstate', function () { if (dlg) close(true); });   // back gesture closes the sheet
  d.addEventListener('click', function (e) {
    var el = e.target && e.target.closest ? e.target.closest('[data-p1-book]') : null;
    if (!el || e.defaultPrevented && !el.hasAttribute('data-cta')) return;
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey) return;   // new-tab clicks behave normally
    e.preventDefault();
    open(el.getAttribute('data-service') || '', el);
  }, false);
  window.addEventListener('message', function (e) {
    if (e.origin !== ORIGIN || !e.data || typeof e.data !== 'object') return;
    var t = e.data.type;
    if (t === 'p1-booking-height' && typeof e.data.h === 'number') {
      [].forEach.call(d.querySelectorAll('iframe[data-p1-booking]'), function (f) {
        if (f.contentWindow === e.source) f.style.height = Math.max(200, Math.min(20000, Math.round(e.data.h))) + 'px';
      });
    } else if (t === 'p1-booking-nocookie') {
      try { sessionStorage.setItem(KEY, '1'); } catch (x) {}
      if (frame && frame.contentWindow === e.source) fallback(frame.getAttribute('data-p1-service'));
    } else if (t === 'p1-booking-close') {
      if (frame && frame.contentWindow === e.source) close();
    } else if (t === 'p1-booking-confirmed') {
      try { d.dispatchEvent(new CustomEvent('p1-booking-confirmed', { detail: { client: CLIENT } })); } catch (x) {}
    }
  });
})();
