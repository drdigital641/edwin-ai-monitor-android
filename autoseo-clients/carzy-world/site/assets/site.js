// Small helper only: all page content is already in the HTML.
(() => {
  const btn = document.getElementById("menu-btn");
  const nav = document.getElementById("nav");
  if (!btn || !nav) return;
  btn.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.firstElementChild.textContent = open ? "✕" : "☰";
  });
  nav.addEventListener("click", (e) => {
    if (e.target.closest("a")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.firstElementChild.textContent = "☰"; }
  });
})();
