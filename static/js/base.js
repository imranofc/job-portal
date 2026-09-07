document.addEventListener("DOMContentLoaded", () => {
  const btn = document.querySelector(".menu-btn"),
    nav = document.querySelector("nav");
  if (!btn || !nav) return;
  btn.addEventListener("click", () => {
    const open = nav.classList.toggle("active");
    btn.setAttribute("aria-expanded", open);
    btn.querySelector("i").className = open
      ? "fa-solid fa-xmark"
      : "fa-solid fa-bars";
  });
  document
    .querySelectorAll("nav a")
    .forEach((link) =>
      link.addEventListener("click", () => nav.classList.remove("active")),
    );
});