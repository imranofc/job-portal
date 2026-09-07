document.addEventListener("DOMContentLoaded", function () {
  const pauseButton = document.querySelector(".pause-btn");
  if (!pauseButton) {
    console.log("Pause button not found.");
    return;
  }
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  pauseButton.addEventListener("click", function () {
    const csrfToken = getCookie("csrftoken");
    fetch(window.location.href, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({
        action: "pause",
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Job paused successfully.");
          location.reload();
        } else {
          alert(data.message || "Failed to pause the job.");
        }
      })
      .catch((error) => {
        console.error(error);
        alert("Something went wrong.");
      });
  });
});
