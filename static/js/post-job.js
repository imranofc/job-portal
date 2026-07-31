document.addEventListener("DOMContentLoaded", function () {

    console.log("DOM fully loaded and parsed");
    const applyLink = document.getElementById("apply-link");
    const applyTypeSelect = document.getElementById("apply-type");

    function toggleFields() {
        if (applyTypeSelect.value === "link") {
            applyLink.disabled = false;
        } else {
            applyLink.disabled = true;
        }
    }

    applyTypeSelect.addEventListener("change", toggleFields);
    toggleFields();
});