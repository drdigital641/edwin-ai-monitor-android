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

  // Click-to-load reels: nothing from Facebook loads until the visitor taps.
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a.reel[data-embed]");
    if (!a) return;
    e.preventDefault();
    const box = document.createElement("div");
    box.className = "embed-frame";
    const f = document.createElement("iframe");
    f.src = a.dataset.embed;
    f.title = a.dataset.title;
    f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    f.allowFullscreen = true;
    box.appendChild(f);
    a.replaceWith(box);
  });
})();
