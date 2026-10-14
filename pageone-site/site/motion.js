// Home page motion: count-up on result figures and card tilt. Text is final in the HTML;
// nothing here changes layout, and it does nothing when the visitor prefers reduced motion.
(() => {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const run = (el) => {
    const m = el.textContent.match(/^([^\d]*)([\d,.]+)(.*)$/);
    if (!m) return;
    const end = parseFloat(m[2].replace(/,/g, "")), dec = (m[2].split(".")[1] || "").length, t0 = performance.now(), d = 1200;
    const fmt = (v) => v.toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec });
    const step = (t) => {
      const k = Math.min(1, (t - t0) / d), e = 1 - Math.pow(1 - k, 3);
      el.textContent = m[1] + fmt(end * e) + m[3];
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const nums = document.querySelectorAll(".proof .kpi .value");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { io.unobserve(e.target); run(e.target); } }), { threshold: 0.6 });
    nums.forEach((n) => io.observe(n));
  }
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
