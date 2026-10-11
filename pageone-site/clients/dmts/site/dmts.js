(function () {
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('mnav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  var money = function (n) { return 'S$' + n.toLocaleString('en-SG'); };
  var wa = function (text) { return 'https://wa.me/' + (window.DMTS_WA || '6584309665') + '?text=' + encodeURIComponent(text); };

  // Cost estimator
  var P = window.DMTS_PRICES, cats = document.getElementById('cats');
  if (P && cats) {
    var brand = document.getElementById('brand'), syms = document.getElementById('syms'),
        sum = document.getElementById('sum'), picked = document.getElementById('picked'),
        sendWa = document.getElementById('send-wa'), sendMail = document.getElementById('send-mail'), cur = 0;
    var esc = function (s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; };

    var summary = function () {
      var c = P[cur], lines = [], total = 0;
      syms.querySelectorAll('input:checked').forEach(function (i) {
        var s = c.symptoms[+i.dataset.s], o = s.options[+i.dataset.o];
        total += o.price_sgd; lines.push(s.symptom + ': ' + o.repair + ' (' + (o.price_sgd ? money(o.price_sgd) : 'free') + ')');
      });
      return { lines: lines, total: total, car: (brand.value || c.category) };
    };
    var update = function () {
      var r = summary();
      sum.textContent = money(r.total);
      picked.innerHTML = r.lines.length ? r.lines.map(function (l) { return '<li>' + esc(l) + '</li>'; }).join('') : '<li>Tick a repair to add it.</li>';
      var msg = 'Hi Dynamic Motoring, I used your cost estimator.\nCar: ' + r.car + '\n' +
        (r.lines.length ? r.lines.join('\n') + '\nEstimated total: ' + money(r.total) : 'Symptoms: ') + '\nPlease advise on a quote.';
      sendWa.href = wa(msg);
      sendMail.href = 'mailto:' + window.DMTS_EMAIL + '?subject=' + encodeURIComponent('Gearbox repair estimate: ' + r.car) + '&body=' + encodeURIComponent(msg);
    };
    var render = function () {
      var c = P[cur];
      cats.querySelectorAll('button').forEach(function (b, i) { b.setAttribute('aria-selected', i === cur ? 'true' : 'false'); });
      brand.innerHTML = '<option value="">Select your ' + esc(c.category.replace(/s$/, '').toLowerCase()) + ' brand</option>' +
        c.brands.map(function (b) { return '<option>' + esc(b) + '</option>'; }).join('') + '<option>Other</option>';
      syms.innerHTML = c.symptoms.map(function (s, si) {
        return '<div class="symrow"><h3>' + esc(s.symptom) + '</h3><div class="d">' + s.description.map(esc).join('<br>') + '</div>' +
          s.options.map(function (o, oi) {
            return '<label class="opt"><input type="checkbox" data-s="' + si + '" data-o="' + oi + '"><span>' + esc(o.repair) +
              '</span><b>' + (o.price_sgd ? money(o.price_sgd) : 'Free') + '</b></label>';
          }).join('') + '</div>';
      }).join('');
      update();
    };
    P.forEach(function (c, i) {
      var b = document.createElement('button');
      b.type = 'button'; b.setAttribute('role', 'tab'); b.textContent = c.category;
      b.addEventListener('click', function () { cur = i; render(); });
      cats.appendChild(b);
    });
    syms.addEventListener('change', function (ev) {
      var t = ev.target; if (t.type !== 'checkbox') return;
      // Options under one symptom are alternatives: ticking one clears the other.
      if (t.checked) syms.querySelectorAll('input[data-s="' + t.dataset.s + '"]').forEach(function (o) { if (o !== t) o.checked = false; });
      update();
    });
    brand.addEventListener('change', update);
    render();
  }

  // Contact form -> WhatsApp / email
  var f = document.getElementById('qform');
  if (f) {
    var msg = function () {
      var v = function (id) { return document.getElementById(id).value.trim(); };
      return 'Hi Dynamic Motoring, I would like a gearbox quote.\nName: ' + v('q-name') + '\nContact: ' + v('q-phone') +
        (v('q-car') ? '\nCar: ' + v('q-car') : '') + (v('q-msg') ? '\nProblem: ' + v('q-msg') : '');
    };
    f.addEventListener('submit', function (ev) { ev.preventDefault(); window.open(wa(msg()), '_blank', 'noopener'); });
    document.getElementById('q-mail').addEventListener('click', function () {
      if (!f.reportValidity()) return;
      location.href = 'mailto:sales@dmts.com.sg?subject=' + encodeURIComponent('Gearbox quote request') + '&body=' + encodeURIComponent(msg());
    });
  }
})();
