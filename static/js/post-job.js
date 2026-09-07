document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("apply-type"),
    link = document.getElementById("apply-link"),
    box = document.getElementById("apply-link-box");
  if (!select || !link) return;
  const toggle = () => {
    const external = select.value === "link";
    link.disabled = !external;
    link.required = external;
    if (box) box.classList.toggle("is-disabled", !external);
  };
  select.addEventListener("change", toggle);
  toggle();
});
