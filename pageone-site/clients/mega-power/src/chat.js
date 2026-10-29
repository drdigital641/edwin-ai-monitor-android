/* Mega Power mascot assistant (preview). Routes each enquiry to the right channel and searches the catalogue.
   Demo: runs on rules + the site's own catalogue data in the browser; the live version can call an AI model through a small server function. */
(function () {
  'use strict';
  var M = window.MP; if (!M || document.body.classList.contains('st')) return;
  var D = M.D, R = M.ROOT, esc = M.esc;
  var SS = { get: function (k, d) { try { var v = sessionStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }, set: function (k, v) { try { sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) {} } };
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function tel(t) { return 'tel:+65' + String(t).replace(/\s/g, ''); }

  var BOT = '<svg viewBox="0 0 120 120" aria-hidden="true"><ellipse cx="58" cy="113" rx="28" ry="4.5" fill="rgba(10,31,53,.18)"/>' +
    '<rect x="37" y="101" width="15" height="9" rx="4" fill="#12304F"/><rect x="64" y="101" width="15" height="9" rx="4" fill="#12304F"/>' +
    '<line x1="58" y1="30" x2="58" y2="17" stroke="#0A1F35" stroke-width="3.5" stroke-linecap="round"/><circle cx="58" cy="14" r="6.5" fill="#E2601A"/><path d="M58 9.5v9M54 12l8 4M62 12l-8 4" stroke="#fff" stroke-width="1.4" stroke-linecap="round"/>' +
    '<rect x="16" y="64" width="13" height="25" rx="6.5" fill="#12304F"/><circle cx="22.5" cy="91" r="7" fill="#E2601A"/>' +
    '<g class="m-arm"><rect x="88" y="40" width="13" height="30" rx="6.5" fill="#12304F"/><circle cx="94.5" cy="37" r="8" fill="#E2601A"/><path d="M90 31.5v-3M94.5 30v-3.5M99 31.5v-3" stroke="#C24E10" stroke-width="1.6" stroke-linecap="round"/></g>' +
    '<rect x="26" y="29" width="64" height="76" rx="24" fill="#0A1F35"/>' +
    '<rect x="34" y="39" width="48" height="33" rx="14" fill="#EAF6F6"/>' +
    '<ellipse class="m-eye" cx="49" cy="54" rx="4.6" ry="5.6" fill="#0A1F35"/><ellipse class="m-eye" cx="67" cy="54" rx="4.6" ry="5.6" fill="#0A1F35"/><circle cx="50.6" cy="52" r="1.5" fill="#fff"/><circle cx="68.6" cy="52" r="1.5" fill="#fff"/>' +
    '<circle cx="42.5" cy="63" r="3" fill="#FFB48A" opacity=".8"/><circle cx="73.5" cy="63" r="3" fill="#FFB48A" opacity=".8"/>' +
    '<path d="M52.5 62.5q5.5 5 11 0" fill="none" stroke="#0A1F35" stroke-width="2.4" stroke-linecap="round"/>' +
    '<rect x="38" y="79" width="40" height="17" rx="7" fill="#12304F"/><text x="58" y="91.5" text-anchor="middle" font-family="IBM Plex Sans,Arial,sans-serif" font-weight="700" font-size="10.5" fill="#FFB48A" letter-spacing="1">MP</text></svg>';

  var AREAS = [
    ['Soon Lee', /pioneer|soon lee|tuas|jurong west|boon lay|joo koon|gul\b/],
    ['Toh Guan', /toh guan|jurong|clementi|bukit batok|bukit timah|bukit panjang|choa chu kang|cck|west coast|\bwest\b/],
    ['Kaki Bukit', /kaki bukit|\bubi\b|eunos|bedok|tampines|pasir ris|paya lebar|macpherson|geylang|changi|kallang|aljunied|\beast\b/],
    ['Ang Mo Kio', /ang mo kio|\bamk\b|yishun|bishan|toa payoh|thomson|sembawang|woodlands|serangoon|hougang|sengkang|punggol|yio chu kang|admiralty|kranji|\bnorth\b|central/]
  ];
  var COUNTRY = /malaysia|indonesia|thailand|vietnam|philippines|myanmar|cambodia|brunei|india\b|sri lanka|bangladesh|australia|new zealand|\buae\b|dubai|saudi|qatar|oman|africa|nigeria|kenya|pakistan|china|hong kong|taiwan|japan|korea|maldives|fiji|mauritius|europe|usa|america|canada|mexico|brazil/;
  function intent(t) {
    if (/^(hi|hello|hey|yo|good (morning|afternoon|evening))\b[!. ]*$/.test(t)) return 'greet';
    if (/supplier|supply (you|to)|\b(i|we) supply\b|manufactur|factory|we (make|produce)|our (factory|brand)|become a supplier|sell to (you|mega)|offer (our|my) (products|range)|propose/.test(t)) return 'supplier';
    if (/\b(talk|speak) to|human|real person|salesperson|agent|call me|contact me/.test(t)) return 'human';
    if (/\bvin\b|chassis|frame (no|number)/.test(t)) return 'vin';
    if (/export|overseas|ship(ping)?\b|ship to|container|\bfob\b|\bcif\b|wholesale|bulk|distributor|import(er)?\b|international/.test(t) || COUNTRY.test(t)) return 'export';
    if (/hour|opening|open (on|today|now)|closing|close at|sunday|saturday|public holiday/.test(t)) return 'hours';
    if (/price|cost|how much|\bquote\b|quotation|cheap|discount/.test(t)) return 'price';
    if (/workshop|garage|mechanic|collect|pick ?up|walk.?in|branch|outlet|nearest|near me|today|urgent|singapore/.test(t) || AREAS.some(function (a) { return a[1].test(t); })) return 'local';
    if (/contact|phone|number|call|email|address|location|where are you|directions|fax/.test(t)) return 'contact';
    return 'part';
  }
  function branchFor(t) { for (var i = 0; i < AREAS.length; i++) if (AREAS[i][1].test(t)) return AREAS[i][0]; return null; }
  function branch(n) { return D.branches.filter(function (b) { return b.name === n; })[0]; }
  function callBtns(list) { return list.map(function (b) { return '<a class="btn btn-g" href="' + tel(b.tel) + '">☎ ' + esc(b.name) + ' ' + esc(b.tel) + '</a>'; }).join(''); }
  function resHTML(list) {
    var K = { exact: 'Exact reference match', match: 'Matches your search', possible: 'Possible match, please verify' };
    return list.map(function (x) { var p = x.p; return '<a class="c-res" href="' + M.purl(p) + '"><img src="' + esc(M.pimg(p)) + '" alt="" onerror="this.onerror=null;this.src=\'' + M.ph(p) + '\'"><span><b>' + esc(p.name) + '</b><small>' + (K[x.kind] || '') + ((p.refs || [])[0] ? ' · ' + esc(p.refs[0].n) : '') + '</small></span></a>'; }).join('');
  }
  var meaningful = function (t) { return t.replace(/\b(i|we|need|want|looking|for|a|an|the|do|you|have|any|got|is|there|please|pls|can|find|search|part|parts|aircon|car|my|me|in|stock|available|of|to|some|sell|price|how|much|quote|wholesale|bulk|export|ship|shipping|overseas|pcs|units|singapore|workshop|garage|shipped|deliver|delivery|send|sent|qty|quantity|we|are|am|urgently|urgent)\b/g, ' ').replace(/[^a-z0-9]+/g, ' ').trim(); };

  var st = SS.get('mp_chat', { msgs: [], ctx: '', greeted: false });
  function save() { st.msgs = st.msgs.slice(-40); SS.set('mp_chat', st); }

  /* ---------- UI ---------- */
  var wrap = document.createElement('div'); wrap.className = 'mascot';
  wrap.innerHTML = '<div class="m-bub" role="button" tabindex="0"><button class="x2" aria-label="Hide message">×</button>Hi! Need a part or the right contact? <b>Ask me.</b></div><button class="m-btn" aria-label="Open the Mega Power assistant">' + BOT + '</button>';
  document.body.appendChild(wrap);
  var chat = document.createElement('section'); chat.className = 'chat'; chat.hidden = true; chat.setAttribute('aria-label', 'Mega Power assistant');
  chat.innerHTML = '<div class="c-hd"><svg class="mini" viewBox="0 0 120 120">' + BOT.replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '') + '</svg><div><b>Mega Power assistant</b><small>Parts search · right team · branch contacts</small></div><button type="button" aria-label="Close chat">×</button></div>' +
    '<div class="c-body" aria-live="polite"></div><div class="c-chips"></div><form class="c-in"><label class="sr" for="c-q">Message</label><input class="in" id="c-q" autocomplete="off" placeholder="Ask, or type a part no. / car model"><button class="btn btn-o" aria-label="Send"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15M13 6l6 6-6 6"/></svg></button></form>' +
    '<div class="c-note">Preview assistant: answers come from this site\'s catalogue and contacts. Enquiries are demo only.</div>';
  document.body.appendChild(chat);
  var body = $('.c-body', chat), chips = $('.c-chips', chat), form = $('.c-in', chat), inp = $('#c-q', chat), bub = $('.m-bub', wrap);

  function add(who, html, save_) { var d = document.createElement('div'); d.className = 'c-m ' + who; d.innerHTML = html; body.appendChild(d); body.scrollTop = body.scrollHeight; if (save_ !== false) { st.msgs.push({ w: who, h: html }); save(); } return d; }
  function setChips(list) { chips.innerHTML = list.map(function (c) { return '<button type="button">' + esc(c) + '</button>'; }).join(''); }
  var DEF = ['Find a part', 'Singapore workshop', 'Overseas buyer', 'I supply parts', 'Branch phone numbers'];
  function greet() {
    var pd = document.querySelector('[data-product]'), p = pd && M.byId(pd.getAttribute('data-product'));
    add('bot', '<p>Hi, I\'m the Mega Power assistant. I can search the parts catalogue, or get you to the right team and branch.</p>' + (p ? '<p>You\'re looking at <b>' + esc(p.name) + '</b>. Want a quote for it?</p><div class="acts"><button class="btn btn-o" data-cadd="' + esc(p.id) + '">Add to enquiry list</button></div>' : '<p>Type a part number or car model, or tell me who you are.</p>'));
    setChips(DEF);
  }
  function open() {
    chat.hidden = false; wrap.style.display = 'none'; bub.classList.remove('on');
    if (!body.childNodes.length) { if (st.msgs.length) { st.msgs.forEach(function (m) { add(m.w, m.h, false); }); setChips(DEF); } else greet(); }
    M.track('chat_open', {}); if (window.innerWidth > 700) inp.focus();
  }
  function close() { chat.hidden = true; wrap.style.display = ''; }
  $('.m-btn', wrap).addEventListener('click', open);
  bub.addEventListener('click', function (e) { if (e.target.closest('.x2')) { e.stopPropagation(); bub.classList.remove('on'); SS.set('mp_bub', 1); return; } open(); });
  $('.c-hd button', chat).addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !chat.hidden) close(); });
  // Greeting bubble: once per session, never over the hero. Phones wait until the visitor has scrolled past the hero.
  function showBub() { if (SS.get('mp_bub', 0) || !chat.hidden) return; bub.classList.add('on'); SS.set('mp_bub', 1); setTimeout(function () { bub.classList.remove('on'); }, 5000); }
  var small = window.matchMedia('(max-width:700px)').matches, hx = document.querySelector('.hx');
  if (!SS.get('mp_bub', 0)) {
    if (small) {
      var lim = function () { return hx ? hx.offsetTop + hx.offsetHeight : 500; };
      var onS = function () { if (window.scrollY > lim()) { window.removeEventListener('scroll', onS); setTimeout(showBub, 600); } };
      window.addEventListener('scroll', onS, { passive: true });
    } else setTimeout(showBub, 4000);
  }
  chips.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) ask(b.textContent); });
  form.addEventListener('submit', function (e) { e.preventDefault(); var v = inp.value.trim(); if (!v) return; inp.value = ''; ask(v); });
  body.addEventListener('click', function (e) {
    var a = e.target.closest('[data-cadd]'); if (a) { M.addRfq(a.getAttribute('data-cadd'), 1); a.textContent = 'Added ✓'; a.disabled = true; }
    var h = e.target.closest('[data-hand]'); if (h) handoff(h.getAttribute('data-hand'));
  });

  /* ---------- answers ---------- */
  function ask(text) {
    add('me', esc(text));
    var t = add('bot', '<span class="c-typing"><i></i><i></i><i></i></span>', false);
    setTimeout(function () { t.remove(); answer(text); }, 450 + Math.random() * 300);
  }
  function searchBlock(q, intro) {
    var r = M.search(q), list = r.results.filter(function (x) { return x.kind !== 'all'; });
    if (!list.length) return null;
    M.track('chat_search', { q: q, n: list.length });
    return '<p>' + (intro || 'Here\'s what I found in the catalogue:') + '</p>' + resHTML(list.slice(0, 3)) +
      '<div class="acts">' + (list.length > 3 ? '<a class="btn btn-g" href="' + R + 'our-products.html?q=' + encodeURIComponent(q) + '">See all ' + list.length + '</a>' : '<a class="btn btn-g" href="' + R + 'our-products.html?q=' + encodeURIComponent(q) + '">Open in catalogue</a>') +
      (list[0].kind === 'exact' || list.length === 1 ? '<button class="btn btn-o" data-cadd="' + esc(list[0].p.id) + '">Add to enquiry list</button>' : '') + '</div>' +
      (list[0].kind !== 'exact' ? '<p class="note" style="margin-top:6px">Fitment is confirmed by our team before quoting.</p>' : '');
  }
  function answer(raw) {
    var t = raw.toLowerCase().trim(), it = intent(t), q = meaningful(t), sb = null;
    M.track('chat_message', { intent: it });
    if (it !== 'supplier' && it !== 'greet' && it !== 'hours' && q.length >= 2) sb = searchBlock(q.replace(new RegExp(COUNTRY.source, 'g'), ' ').replace(/\b\d{1,2}\b/g, ' ').trim() || raw);
    if (raw.toLowerCase() === 'find a part') { add('bot', '<p>Type the part number (spaces and dashes don\'t matter), or the car and part, for example <b>BMW F45 compressor</b> or <b>4M0 816 421B</b>.</p>'); setChips(['8730R', 'Mercedes W205 compressor', 'Audi Q7 condenser']); return; }
    if (it === 'greet') { add('bot', '<p>Hello! What can I help with? A part number, a car model, or which team to talk to.</p>'); setChips(DEF); return; }
    if (it === 'supplier') {
      st.ctx = 'SUPPLIER';
      add('bot', '<p>Thanks for your interest in supplying Mega Power. Our purchasing team reviews new ranges of automotive A/C and cooling parts.</p><p>Please send your company details, the categories you make, your catalogue or price list and MOQ. It takes about 3 minutes.</p><div class="acts"><a class="btn btn-o" href="' + R + 'become-a-supplier/">Open the supplier form</a><button class="btn btn-g" data-hand="SUPPLIER">Leave my contact instead</button></div>');
      setChips(['What ranges do you source?', 'Branch phone numbers']); save(); return;
    }
    if (/what ranges/.test(t)) { add('bot', '<p>Compressors, condensers, cooling coils, fans and blower motors, filters, valves, driers, compressor oil and refrigerant, for passenger cars, commercial vehicles, trucks and excavators.</p><div class="acts"><a class="btn btn-o" href="' + R + 'become-a-supplier/">Propose your products</a></div>'); return; }
    if (it === 'export') {
      st.ctx = 'EXPORT';
      add('bot', (sb ? sb + '<hr style="border:0;border-top:1px solid var(--line);margin:10px 0">' : '') + '<p>For overseas orders we quote by quantity and destination. Shipping and payment terms are agreed in the quotation.</p><p>Fastest: paste your parts list (part numbers with quantities) and we match it against the catalogue.</p><div class="acts"><a class="btn btn-o" href="' + R + 'export/#bulk">Check my parts list</a><a class="btn btn-g" href="' + R + 'export/">Export enquiry form</a><button class="btn btn-g" data-hand="EXPORT">Have sales contact me</button></div>');
      setChips(['How do I send a chassis number?', 'Do you show prices?', 'Find a part']); return;
    }
    if (it === 'vin') { add('bot', '<p>Send the VIN or chassis number with the part you need, and our team identifies the right part. We don\'t decode VINs automatically, and chassis numbers are only seen by Mega Power staff.</p><div class="acts"><a class="btn btn-o" href="' + R + 'rfq/#vin">Send a chassis number</a></div>'); setChips(DEF); return; }
    if (it === 'price') {
      add('bot', (sb ? sb + '<hr style="border:0;border-top:1px solid var(--line);margin:10px 0">' : '') + '<p>Prices aren\'t shown online, because they depend on the exact part, the quantity and, for export, the destination. Add the parts to your enquiry list and our team replies with a quotation.</p><div class="acts"><a class="btn btn-o" href="' + R + 'rfq/">Open my enquiry list</a></div>');
      setChips(['Singapore workshop', 'Overseas buyer', 'Find a part']); return;
    }
    if (it === 'hours') { add('bot', '<p>Opening hours are being confirmed for the new website. Please call the branch before you come down:</p><div class="acts">' + callBtns(D.branches) + '</div>'); setChips(['Which branch is nearest?', 'Find a part']); return; }
    if (it === 'local' || /nearest/.test(t)) {
      st.ctx = 'LOCAL';
      var bn = branchFor(t), b = bn && branch(bn);
      add('bot', (sb ? sb + '<hr style="border:0;border-top:1px solid var(--line);margin:10px 0">' : '') + (b ? '<p>Your nearest branch is likely <b>' + esc(b.name) + '</b>: ' + esc(b.address) + '.</p><div class="acts"><a class="btn btn-o" href="' + tel(b.tel) + '">☎ Call ' + esc(b.name) + ' ' + esc(b.tel) + '</a></div>' :
        '<p>We have four branches in Singapore. Tell me your area (for example Jurong or Bedok), or call one now:</p><div class="acts">' + callBtns(D.branches) + '</div>') +
        '<p style="margin-top:8px">Or send the car details and our team checks the part before you collect.</p><div class="acts"><a class="btn btn-g" href="' + R + 'singapore-workshops/">Workshop enquiry</a></div>');
      setChips(['Jurong', 'Ang Mo Kio', 'Bedok', 'Find a part']); return;
    }
    if (it === 'contact') { add('bot', '<p>Main line <a href="tel:+6568423389">+65 6842 3389</a>, email <a href="mailto:' + esc(D.email) + '">' + esc(D.email) + '</a>. Branches:</p><div class="acts">' + callBtns(D.branches) + '</div>'); setChips(['Which branch is nearest?', 'Overseas buyer', 'I supply parts']); return; }
    if (it === 'human') { add('bot', '<p>Sure. Leave your name and a phone number or email, and the right team contacts you.</p>'); handoff(st.ctx || ''); return; }
    // part search
    if (sb) { add('bot', sb); setChips(['Do you show prices?', 'Overseas buyer', 'Singapore workshop']); return; }
    if (q.length >= 2) {
      M.track('chat_no_match', { q: raw });
      add('bot', '<p>I couldn\'t find a verified match for “' + esc(raw) + '” in the catalogue, and I won\'t guess a fitment.</p><p>Our team can check whether we can source it, best with the chassis number.</p><div class="acts"><a class="btn btn-o" href="' + R + 'rfq/?need=' + encodeURIComponent(raw) + '">Request sourcing</a><a class="btn btn-g" href="' + R + 'rfq/#vin">Send chassis number</a><button class="btn btn-g" data-hand="' + (st.ctx || '') + '">Have someone call me</button></div>');
      setChips(DEF); return;
    }
    add('bot', '<p>I can help with part numbers, car models, branch contacts, export orders and supplier offers. Try one of these:</p>'); setChips(DEF);
  }

  /* ---------- hand-off to the right team (saved as an enquiry) ---------- */
  function handoff(ctx) {
    var d = add('bot', '<p>Who should we contact?</p><form class="c-form"><input class="in" name="name" placeholder="Your name" required><input class="in" name="contact" placeholder="Phone, WhatsApp or email" required><select class="in" name="type"><option value="LOCAL"' + (ctx === 'LOCAL' ? ' selected' : '') + '>I\'m a Singapore workshop</option><option value="EXPORT"' + (ctx === 'EXPORT' ? ' selected' : '') + '>I\'m an overseas buyer</option><option value="SUPPLIER"' + (ctx === 'SUPPLIER' ? ' selected' : '') + '>I supply parts</option></select><button class="btn btn-o">Send to the team</button></form>', false);
    var f = $('form', d);
    f.addEventListener('submit', function (e) {
      e.preventDefault(); var n = f.name.value.trim(), c = f.contact.value.trim(), ty = f.type.value;
      if (!n || !c) { (n ? f.contact : f.name).classList.add('bad'); return; }
      var transcript = st.msgs.map(function (m) { return (m.w === 'me' ? 'Visitor: ' : 'Assistant: ') + m.h.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim(); }).slice(-12).join('\n');
      var lead = { id: M.nextId(ty), type: ty, sub: 'CHAT', created: new Date().toISOString(), status: 'New', fields: { name: n, contact: c, message: 'From the website assistant:\n' + transcript }, files: [], items: [], source: { page: location.pathname, url: location.href, referrer: document.referrer || '', product: (document.querySelector('[data-product]') || { getAttribute: function () { return ''; } }).getAttribute('data-product') || '', utm: '', need: '' }, tag: 'CHAT_' + ty, notes: [] };
      M.saveLead(lead); M.track('chat_handoff', { type: ty });
      var team = { LOCAL: 'local sales', EXPORT: 'export sales', SUPPLIER: 'purchasing' }[ty];
      d.innerHTML = '<p>Sent to our <b>' + team + '</b> team as <b>' + esc(lead.id) + '</b>, with this chat attached.</p><p class="note">Demo only: saved to the staff inbox in this browser. Nobody is notified yet.</p><div class="acts"><a class="btn btn-g" href="' + R + 'staff/#lead/' + encodeURIComponent(lead.id) + '">See it in the staff inbox</a></div>';
      st.msgs.push({ w: 'bot', h: d.innerHTML }); save();
    });
  }
  document.addEventListener('focusin', function (e) { if (e.target.matches && e.target.matches('input,textarea,select') && !e.target.closest('.chat')) document.body.classList.add('typing'); });
  document.addEventListener('focusout', function () { document.body.classList.remove('typing'); });
})();
