// Small helpers only: all page content is already in the HTML.
(() => {
  // Menu
  const btn = document.getElementById("menu-btn");
  const nav = document.getElementById("nav");
  if (btn && nav) {
    const set = (open) => { nav.classList.toggle("open", open); btn.setAttribute("aria-expanded", open ? "true" : "false"); btn.firstElementChild.textContent = open ? "✕" : "☰"; };
    btn.addEventListener("click", () => set(!nav.classList.contains("open")));
    nav.addEventListener("click", (e) => { if (e.target.closest("a")) set(false); });
  }

  // Animations run only while on screen (CSS stops them fully under reduced motion).
  const moving = document.querySelectorAll(".anim, .hero, .phero");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((es) => es.forEach((e) => e.target.classList.toggle("paused", !e.isIntersecting)));
    moving.forEach((el) => io.observe(el));
  }

  // Facebook iframe (click-to-load): nothing from Facebook loads until the visitor taps.
  const fbFrame = (el) => {
    const box = document.createElement("div");
    box.className = "embed-frame";
    const f = document.createElement("iframe");
    f.src = el.dataset.embed;
    f.title = el.dataset.title;
    f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    f.allowFullscreen = true;
    box.appendChild(f);
    el.replaceWith(box);
  };

  // Self-hosted reels: the poster shows until a tap; the MP4 loads and plays only then.
  // A missing poster leaves the circuit background; a missing MP4 falls back to Facebook.
  document.querySelectorAll(".reel-mp4").forEach((r) => {
    const v = r.querySelector("video");
    const src = v.querySelector("source");
    src.addEventListener("error", () => { if (r.isConnected) fbFrame(r); });
    r.querySelector(".reel-cover").addEventListener("click", () => {
      r.classList.add("playing");
      const p = v.play();
      if (p && p.catch) p.catch(() => {});
    });
  });

  document.addEventListener("click", (e) => {
    const a = e.target.closest("a.reel[data-embed]");
    if (!a) return;
    e.preventDefault();
    fbFrame(a);
  });

  // Bench carousel: auto-slide every 3 s, pause on touch/hover/focus or off-screen, none under reduced motion.
  const reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.querySelectorAll("[data-carousel]").forEach((c) => {
    const track = c.querySelector(".car-track");
    const slides = [...track.children];
    const dots = [...c.querySelectorAll(".car-dot")];
    const step = () => slides.length > 1 ? slides[1].offsetLeft - slides[0].offsetLeft : track.clientWidth;
    const index = () => Math.round(track.scrollLeft / step());
    const maxIndex = () => Math.max(0, Math.round((track.scrollWidth - track.clientWidth) / step()));
    const go = (i) => { const m = maxIndex(); if (i > m) i = 0; if (i < 0) i = m; track.scrollTo({ left: i * step() }); };
    const mark = () => { const i = index() >= maxIndex() && track.scrollLeft > 0 ? dots.length - 1 : Math.min(index(), dots.length - 1); dots.forEach((d, n) => d.setAttribute("aria-current", n === i ? "true" : "false")); };
    c.querySelector(".car-prev").addEventListener("click", () => go(index() - 1));
    c.querySelector(".car-next").addEventListener("click", () => go(index() + 1));
    dots.forEach((d, n) => d.addEventListener("click", () => go(Math.min(n, maxIndex()))));
    track.addEventListener("scroll", () => requestAnimationFrame(mark), { passive: true });
    mark();
    if (reducedMotion) return;
    let held = false, visible = false, timer = null;
    const tick = () => { if (!held && visible && !document.hidden) go(index() + 1); };
    const start = () => { if (!timer) timer = setInterval(tick, 3000); };
    const hold = () => { held = true; };
    const release = () => { held = false; };
    c.addEventListener("mouseenter", hold); c.addEventListener("mouseleave", release);
    c.addEventListener("focusin", hold); c.addEventListener("focusout", release);
    c.addEventListener("touchstart", hold, { passive: true });
    c.addEventListener("touchend", () => setTimeout(release, 2000), { passive: true });
    if ("IntersectionObserver" in window) new IntersectionObserver((es) => { visible = es[0].isIntersecting; }).observe(c);
    else visible = true;
    start();
  });
})();
