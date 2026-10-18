// Home page motion, presentation style: charts draw in, tiles and steps appear in turn. Figures never change.
// The HTML already holds the final text and sizes; this only animates to them (transform/opacity, no layout change).
// It does nothing when the visitor prefers reduced motion, so the page stays in its final state.
(() => {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches || !("IntersectionObserver" in window)) return;
  // Crawlers and AI readers (Google, Bing, ChatGPT and other fetchers, headless browsers) get the page as written.
  if (navigator.webdriver || /bot|crawl|spider|slurp|headless|lighthouse|gpt|openai|claude|anthropic|perplexity|bing|google|preview/i.test(navigator.userAgent)) return;
  document.documentElement.classList.add("pm");

  const later = (fn, ms) => fn && setTimeout(fn, ms);
  const watch = (els, onIn, threshold) => {
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (e.isIntersecting) { io.unobserve(e.target); onIn(e.target); }
    }), { threshold: threshold || 0.35 });
    els.forEach((n) => io.observe(n));
  };

  // Figures are never rewritten (MASTER-RULES 4.12, 19 Oct 2026): the numbers in the HTML stay exactly as published,
  // for every visitor, crawler and page reader. Only the card, bars and tiles move.
  // Hero proof card: the card arrives and the bars grow.
  document.querySelectorAll(".proof-card").forEach((card) => {
    watch([card], (c) => c.classList.add("on"), 0.25);
  });

  // KPI tiles: one after another, then the mini chart and note.
  const tiles = [...document.querySelectorAll(".proof .kpi")];
  watch(tiles.length ? [tiles[0].parentNode] : [], () => tiles.forEach((t, i) => later(() => t.classList.add("on"), i * 180)), 0.2);

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
