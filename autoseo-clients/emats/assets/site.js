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
})();
