const liveButton = document.getElementById("live-button");
const liveImg = document.getElementById("live-img");
const liveDataScript = document.getElementById("live-data");
const liveData = JSON.parse(liveDataScript.textContent || "[]");
let index = 0;

liveButton.addEventListener("click", () => {
    if (liveImg.style.display !== "none") {
        liveImg.style.display = "none";
        liveButton.classList.add("full-screen");
    }
    if (liveData.length > 0) {
        liveButton.innerHTML = `${liveData[index]}<div class="live-dot"></div>`;
        index = (index + 1) % liveData.length;
    }
});
