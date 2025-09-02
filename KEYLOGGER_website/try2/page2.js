document.addEventListener("DOMContentLoaded", () => {
  const searchType = document.getElementById("search-type");
  const keywordInput = document.getElementById("keyword-input");
  const datetimeInputs = document.getElementById("datetime-inputs");
  const liveBtn = document.getElementById("live-btn");
  const livePopup = document.getElementById("live-popup");
  const liveContent = document.getElementById("live-content");

  searchType.addEventListener("change", () => {
    if (searchType.value === "keyword") {
      keywordInput.classList.remove("hidden");
      datetimeInputs.classList.add("hidden");
    } else {
      keywordInput.classList.add("hidden");
      datetimeInputs.classList.remove("hidden");
    }
  });

  liveBtn.addEventListener("click", () => {
    livePopup.classList.toggle("hidden");
    liveContent.innerHTML = "<p>Streaming live data...</p>";
  });
});
