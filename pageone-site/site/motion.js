// Home page motion, presentation style: figures count up, charts draw in, tiles and steps appear in turn.
// The HTML already holds the final text and sizes; this only animates to them (transform/opacity, no layout change).
// It does nothing when the visitor prefers reduced motion, so the page stays in its final state.
(() => {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches || !("IntersectionObserver" in window)) return;
  document.documentElement.classList.add("pm");

  // Count a number in el from `from` to the number already written in it, keeping any prefix/suffix ("#", "+").
  const count = (el, d, from) => {
    const m = el.textContent.match(/^([^\d]*)([\d,.]+)(.*)$/);
    if (!m) return;
    const end = parseFloat(m[2].replace(/,/g, "")), dec = (m[2].split(".")[1] || "").length;
    const start = from == null ? 0 : from;
    const fmt = (v) => v.toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec });
    el.textContent = m[1] + fmt(start) + m[3];
    return () => {
      const t0 = performance.now();
      const step = (t) => {
        const k = Math.min(1, (t - t0) / d), e = 1 - Math.pow(1 - k, 3);
        el.textContent = m[1] + fmt(k < 1 ? start + (end - start) * e : end) + m[3];
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
  };
  const later = (fn, ms) => fn && setTimeout(fn, ms);
  const watch = (els, onIn, threshold) => {
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (e.isIntersecting) { io.unobserve(e.target); onIn(e.target); }
    }), { threshold: threshold || 0.35 });
    els.forEach((n) => io.observe(n));
  };

  // Hero proof card: headline numbers count, each bar's label counts while its bar grows.
  document.querySelectorAll(".proof-card").forEach((card) => {
    const heads = [...card.querySelectorAll(".proof-hero b")].map((b) =>
      count(b, 1400, b.dataset.from ? parseFloat(b.dataset.from) : null));
    const bars = [...card.querySelectorAll(".pb span")].map((s) => count(s, 1000));
    watch([card], (c) => {
      c.classList.add("on");
      heads.forEach((f) => later(f, 200));
      bars.forEach((f, i) => later(f, i * 250));
    }, 0.25);
  });

  // KPI tiles: one after another, number counts, then the mini chart and note.
  const tiles = [...document.querySelectorAll(".proof .kpi")];
  const runs = tiles.map((t) => count(t.querySelector(".value"), 1200));
  watch(tiles.length ? [tiles[0].parentNode] : [], () => tiles.forEach((t, i) => later(() => {
    t.classList.add("on");
    later(runs[i], 150);
  }, i * 180)), 0.2);

  // "How it works": the connector line draws and the steps arrive in order.
  document.querySelectorAll(".steps").forEach((s) => {
    s.querySelectorAll("li.reveal").forEach((li, i) => { li.style.transitionDelay = i * 0.2 + "s"; });
    watch([s], (n) => n.classList.add("on"), 0.3);
  });

  // Card grids: cards arrive one after another instead of all at once.
  document.querySelectorAll(".cards").forEach((g) => {
    [...g.children].filter((c) => c.classList.contains("reveal")).forEach((c, i) => {
      if (!i) return;
      c.style.transitionDelay = Math.min(i, 5) * 0.09 + "s";
      // Clear the delay once it has shown, so hover effects stay instant.
      c.addEventListener("transitionend", () => { c.style.transitionDelay = ""; }, { once: true });
    });
  });

  // Desktop only: client screenshots tilt slightly towards the pointer.
  if (matchMedia("(hover: hover) and (pointer: fine)").matches) {
    document.querySelectorAll(".story .browser").forEach((b) => {
      b.addEventListener("pointermove", (e) => {
        const r = b.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        b.style.setProperty("--ry", (x * 10).toFixed(2) + "deg");
        b.style.setProperty("--rx", (-y * 8).toFixed(2) + "deg");
      });
      b.addEventListener("pointerleave", () => { b.style.setProperty("--ry", "0deg"); b.style.setProperty("--rx", "0deg"); });
    });
  }
})();
