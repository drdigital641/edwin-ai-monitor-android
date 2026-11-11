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

  // Hero video: muted autoplay loop, unless the visitor prefers reduced motion (then poster + play button).
  const v = document.getElementById("hero-video");
  if (v) {
    const toggle = document.querySelector("[data-toggle]");
    const sound = document.querySelector("[data-sound]");
    const sync = () => {
      const playing = !v.paused;
      toggle.firstElementChild.textContent = playing ? "❚❚" : "▶";
      toggle.setAttribute("aria-label", playing ? toggle.dataset.pause : toggle.dataset.play);
    };
    v.addEventListener("play", sync);
    v.addEventListener("pause", sync);
    toggle.addEventListener("click", () => (v.paused ? v.play() : v.pause()));
    sound.addEventListener("click", () => {
      v.muted = !v.muted;
      if (!v.muted && v.paused) v.play();
      sound.setAttribute("aria-pressed", v.muted ? "false" : "true");
      sound.querySelector(".lbl").textContent = v.muted ? sound.dataset.on : sound.dataset.off;
    });
    const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!reduced) { const p = v.play(); if (p && p.catch) p.catch(() => {}); }
  }

  // Click-to-load clips: nothing from the video platform loads until the visitor taps.
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a.facade[data-embed]");
    if (!a) return;
    e.preventDefault();
    const box = document.createElement("div");
    box.className = "embed-frame";
    const f = document.createElement("iframe");
    f.src = a.dataset.embed;
    f.title = a.dataset.title;
    f.loading = "lazy";
    f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    f.allowFullscreen = true;
    box.appendChild(f);
    a.replaceWith(box);
  });
})();
