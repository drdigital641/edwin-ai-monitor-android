// Small helpers only: every word and link is already in the HTML.
(() => {
  const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isBot = navigator.webdriver || /bot|crawl|spider|slurp|gpt|claude|perplexity|bing|google/i.test(navigator.userAgent);
  const onScreen = (el, cb) => {
    if (!("IntersectionObserver" in window)) return cb(true);
    new IntersectionObserver((es) => es.forEach((e) => cb(e.isIntersecting))).observe(el);
  };

  // Floating WhatsApp + call buttons appear once the visitor scrolls past the first screen's own buttons.
  const fab = () => document.body.classList.toggle("hw-scrolled", window.scrollY > 320);
  window.addEventListener("scroll", fab, { passive: true }); fab();

  // Menu (phones): full-height drawer with a close button, scroll lock and focus kept inside.
  const menu = document.getElementById("hw-menu");
  const links = document.getElementById("hw-links");
  if (menu && links) {
    let x = links.querySelector(".hw-menu-x");
    if (!x) {
      const lang = (document.documentElement.lang || "en").slice(0, 2);
      x = document.createElement("button");
      x.type = "button";
      x.className = "hw-menu-x";
      x.setAttribute("aria-label", { ms: "Tutup menu", zh: "关闭菜单" }[lang] || "Close menu");
      x.innerHTML = '<span aria-hidden="true">x</span>';
      links.prepend(x);
    }
    const isOpen = () => links.classList.contains("is-open");
    const set = (open) => {
      if (open === isOpen()) return;
      links.classList.toggle("is-open", open);
      document.body.classList.toggle("hw-menu-open", open);
      menu.setAttribute("aria-expanded", open ? "true" : "false");
      (open ? x : menu).focus();
    };
    menu.addEventListener("click", () => set(!isOpen()));
    x.addEventListener("click", () => set(false));
    links.addEventListener("click", (e) => { if (e.target.closest("a")) set(false); });
    document.addEventListener("keydown", (e) => {
      if (!isOpen()) return;
      if (e.key === "Escape") { set(false); return; }
      if (e.key !== "Tab") return;
      const f = [...links.querySelectorAll("a[href], button")].filter((el) => el.offsetParent !== null);
      if (!f.length) return;
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      else if (!links.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
    });
  }

  // Animations run only while on screen (CSS stops them fully under reduced motion).
  document.querySelectorAll(".hw-anim, .hw-system-stage, .hw-plug, .hw-art-panel").forEach((el) => onScreen(el, (v) => el.classList.toggle("hw-still", !v)));

  // Battery charge meter: the HTML says 100%; the count 0 > 100% runs only on screen, never for bots or reduced motion, and always ends on 100%.
  document.querySelectorAll("[data-meter]").forEach((m) => {
    if (reduced || isBot) return;
    const num = m.querySelector("[data-meter-num]");
    let visible = false, t0 = 0;
    const frame = (t) => {
      if (!visible) { num.textContent = "100%"; m.style.setProperty("--fill", "100%"); return; }
      if (!t0) t0 = t;
      const k = ((t - t0) % 5000) / 3800;
      const p = Math.min(100, Math.round(k * 100));
      num.textContent = p + "%";
      m.style.setProperty("--fill", p + "%");
      requestAnimationFrame(frame);
    };
    onScreen(m, (v) => { const was = visible; visible = v; if (v && !was) { t0 = 0; requestAnimationFrame(frame); } });
  });

  // Hybrid system diagram: one part open at a time; buttons carry aria-expanded.
  document.querySelectorAll("[data-system]").forEach((sys) => {
    const nodes = [...sys.querySelectorAll(".hw-node")];
    const spots = [...sys.querySelectorAll(".hw-spot")];
    const open = (name, focus) => {
      nodes.forEach((n) => {
        const on = n.dataset.node === name;
        n.setAttribute("aria-expanded", on ? "true" : "false");
        document.getElementById(n.getAttribute("aria-controls")).classList.toggle("is-on", on);
        if (on && focus) n.focus();
      });
      spots.forEach((s) => s.classList.toggle("is-on", s.dataset.node === name));
    };
    nodes.forEach((n, i) => {
      n.addEventListener("click", () => open(n.dataset.node));
      n.addEventListener("keydown", (e) => {
        const d = e.key === "ArrowRight" || e.key === "ArrowDown" ? 1 : e.key === "ArrowLeft" || e.key === "ArrowUp" ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        open(nodes[(i + d + nodes.length) % nodes.length].dataset.node, true);
      });
    });
    spots.forEach((s) => s.addEventListener("click", () => open(s.dataset.node)));
    open(nodes[0].dataset.node);
  });

  // Reel stories: the self-hosted MP4 loads only when tapped, in one player (so only one plays at a time).
  const player = document.querySelector(".hw-player");
  if (player && player.showModal) {
    const box = player.querySelector(".hw-player-box");
    const cap = player.querySelector(".hw-player-cap");
    const close = () => { const v = box.querySelector("video"); if (v) v.pause(); box.replaceChildren(); if (player.open) player.close(); };
    document.querySelectorAll(".hw-story a[data-video]").forEach((a) => a.addEventListener("click", (e) => {
      e.preventDefault();
      const v = document.createElement("video");
      v.controls = true; v.playsInline = true; v.preload = "none"; v.poster = a.dataset.poster;
      v.setAttribute("playsinline", ""); v.title = a.dataset.title;
      const s = document.createElement("source"); s.src = a.dataset.video; s.type = "video/mp4"; v.appendChild(s);
      box.replaceChildren(v); cap.textContent = a.dataset.title;
      player.showModal();
      const p = v.play(); if (p && p.catch) p.catch(() => {});
    }));
    player.querySelector(".hw-player-x").addEventListener("click", close);
    player.addEventListener("click", (e) => { if (e.target === player) close(); });
    player.addEventListener("close", () => { const v = box.querySelector("video"); if (v) v.pause(); box.replaceChildren(); });
  }

  // Map facade: the Google Maps iframe loads only on tap.
  document.querySelectorAll("[data-map]").forEach((m) => {
    const b = m.querySelector(".hw-map-load");
    if (!b) return;
    b.addEventListener("click", () => {
      const f = document.createElement("iframe");
      f.src = m.dataset.map; f.title = m.dataset.title; f.loading = "lazy"; f.allowFullscreen = true;
      f.referrerPolicy = "no-referrer-when-downgrade";
      m.replaceChildren(f); m.classList.add("is-live");
    });
  });

  // Photo filmstrip: auto-advance every 3 s, pause on touch/hover/focus or off-screen, none under reduced motion.
  document.querySelectorAll("[data-film]").forEach((c) => {
    const rail = c.querySelector(".hw-film-rail");
    const frames = [...rail.children];
    const dots = [...c.querySelectorAll(".hw-dot")];
    const step = () => frames.length > 1 ? frames[1].offsetLeft - frames[0].offsetLeft : rail.clientWidth;
    const index = () => Math.round(rail.scrollLeft / step());
    const last = () => Math.max(0, Math.round((rail.scrollWidth - rail.clientWidth) / step()));
    const go = (i) => { const m = last(); if (i > m) i = 0; if (i < 0) i = m; rail.scrollTo({ left: i * step(), behavior: reduced ? "auto" : "smooth" }); };
    const mark = () => { const i = index() >= last() && rail.scrollLeft > 0 ? dots.length - 1 : Math.min(index(), dots.length - 1); dots.forEach((d, n) => d.setAttribute("aria-current", n === i ? "true" : "false")); };
    c.querySelector(".hw-film-prev").addEventListener("click", () => go(index() - 1));
    c.querySelector(".hw-film-next").addEventListener("click", () => go(index() + 1));
    dots.forEach((d, n) => d.addEventListener("click", () => go(Math.min(n, last()))));
    rail.addEventListener("scroll", () => requestAnimationFrame(mark), { passive: true });
    mark();
    if (reduced) return;
    let held = false, visible = false;
    const hold = () => { held = true; }, release = () => { held = false; };
    c.addEventListener("mouseenter", hold); c.addEventListener("mouseleave", release);
    c.addEventListener("focusin", hold); c.addEventListener("focusout", release);
    c.addEventListener("touchstart", hold, { passive: true });
    c.addEventListener("touchend", () => setTimeout(release, 2000), { passive: true });
    onScreen(c, (v) => { visible = v; });
    setInterval(() => { if (!held && visible && !document.hidden) go(index() + 1); }, 3000);
  });
})();
