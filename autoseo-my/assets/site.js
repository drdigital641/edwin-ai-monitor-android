// Small helpers only: the page content is already in the HTML.
(() => {
  const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduced) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    els.forEach((el) => io.observe(el));
  } else {
    els.forEach((el) => el.classList.add("in"));
  }
  const btn = document.getElementById("menu-btn");
  const nav = document.getElementById("nav");
  if (btn && nav) {
    btn.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.textContent = open ? "✕" : "☰";
    });
  }
})();
// Hide the floating WhatsApp button while another WhatsApp button is on screen,
// so it never sits on top of the hero or the call-to-action band.
(() => {
  const fab = document.getElementById("wa-float");
  const spots = document.querySelectorAll(".hero-ctas, .page-hero .cta-row, .cta-band, .site-footer");
  if (!fab || !spots.length || !("IntersectionObserver" in window)) return;
  const seen = new Set();
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) e.isIntersecting ? seen.add(e.target) : seen.delete(e.target);
    fab.classList.toggle("wa-hide", seen.size > 0);
  });
  spots.forEach((s) => io.observe(s));
})();
