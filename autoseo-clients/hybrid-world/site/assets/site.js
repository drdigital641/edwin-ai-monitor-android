// Small helpers only: all page content is already in the HTML.
(() => {
  const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Menu
  const btn = document.getElementById("menu-btn");
  const nav = document.getElementById("nav");
  if (btn && nav) {
    const set = (open) => { nav.classList.toggle("open", open); btn.setAttribute("aria-expanded", open ? "true" : "false"); };
    btn.addEventListener("click", () => set(!nav.classList.contains("open")));
    nav.addEventListener("click", (e) => { if (e.target.closest("a")) set(false); });
  }

  // Energy animations run only while on screen (CSS stops them fully under reduced motion).
  const moving = document.querySelectorAll(".anim");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      e.target.classList.toggle("paused", !e.isIntersecting);
      if (e.target.pauseAnimations) e.isIntersecting && !reduced ? e.target.unpauseAnimations() : e.target.pauseAnimations();
    }));
    moving.forEach((el) => io.observe(el));
  }
  if (reduced) document.querySelectorAll("svg.flowart").forEach((s) => s.pauseAnimations && s.pauseAnimations());

  // Self-hosted reels: the poster shows until a tap; the MP4 loads and plays only then. One plays at a time.
  const vids = [...document.querySelectorAll(".reel video")];
  vids.forEach((v) => v.addEventListener("play", () => vids.forEach((o) => { if (o !== v && !o.paused) o.pause(); })));
  document.querySelectorAll(".reel").forEach((r) => {
    const v = r.querySelector("video");
    r.querySelector(".reel-cover").addEventListener("click", () => {
      r.classList.add("playing");
      const p = v.play();
      if (p && p.catch) p.catch(() => {});
    });
  });

  // Map facade: the Google Maps iframe loads only on tap.
  document.querySelectorAll("[data-map]").forEach((m) => {
    const b = m.querySelector(".map-load");
    if (!b) return;
    b.addEventListener("click", () => {
      const f = document.createElement("iframe");
      f.src = m.dataset.map;
      f.title = m.dataset.title;
      f.loading = "lazy";
      f.referrerPolicy = "no-referrer-when-downgrade";
      f.allowFullscreen = true;
      m.replaceChildren(f);
      m.classList.add("loaded");
    });
  });

  // Photo carousel: auto-slide every 3 s, pause on touch/hover/focus or off-screen, none under reduced motion.
  document.querySelectorAll("[data-carousel]").forEach((c) => {
    const track = c.querySelector(".car-track");
    const slides = [...track.children];
    const dots = [...c.querySelectorAll(".car-dot")];
    const step = () => slides.length > 1 ? slides[1].offsetLeft - slides[0].offsetLeft : track.clientWidth;
    const index = () => Math.round(track.scrollLeft / step());
    const maxIndex = () => Math.max(0, Math.round((track.scrollWidth - track.clientWidth) / step()));
    const go = (i) => { const m = maxIndex(); if (i > m) i = 0; if (i < 0) i = m; track.scrollTo({ left: i * step(), behavior: reduced ? "auto" : "smooth" }); };
    const mark = () => { const i = index() >= maxIndex() && track.scrollLeft > 0 ? dots.length - 1 : Math.min(index(), dots.length - 1); dots.forEach((d, n) => d.setAttribute("aria-current", n === i ? "true" : "false")); };
    c.querySelector(".car-prev").addEventListener("click", () => go(index() - 1));
    c.querySelector(".car-next").addEventListener("click", () => go(index() + 1));
    dots.forEach((d, n) => d.addEventListener("click", () => go(Math.min(n, maxIndex()))));
    track.addEventListener("scroll", () => requestAnimationFrame(mark), { passive: true });
    mark();
    if (reduced) return;
    let held = false, visible = false;
    const tick = () => { if (!held && visible && !document.hidden) go(index() + 1); };
    const hold = () => { held = true; };
    const release = () => { held = false; };
    c.addEventListener("mouseenter", hold); c.addEventListener("mouseleave", release);
    c.addEventListener("focusin", hold); c.addEventListener("focusout", release);
    c.addEventListener("touchstart", hold, { passive: true });
    c.addEventListener("touchend", () => setTimeout(release, 2000), { passive: true });
    if ("IntersectionObserver" in window) new IntersectionObserver((es) => { visible = es[0].isIntersecting; }).observe(c);
    else visible = true;
    setInterval(tick, 3000);
  });
})();
