const butten = document.getElementById('butten')


      const btn = document.getElementById("send");
      const resultDiv = document.getElementById("result");
btn.onclick = async function(){ 
    window.location.href = "http://127.0.0.1:5000/machine"     
     ;
     
}

       
     

// search.addEventListener("click", async () => {
//   try {
//     // שולחים בקשת GET לשרת
//     const response = await fetch("http://127.0.0.1:5000/machine");
    
//   } catch (error) {
//     console.error("שגיאה בבקשת GET:", error);
//   }
// });


const archiveData = [
    {date: "2025-08-31", time: "13:00", content: "Content item 1"},
    {date: "2025-08-31", time: "14:30", content: "Content item 2"},
    {date: "2025-08-30", time: "10:15", content: "Content item 3"},
    {date: "2025-08-29", time: "09:00", content: "Content item 4"}
];

function displayResults(results) {
    const container = document.getElementById("archive-results");
    container.innerHTML = "";
    if (results.length === 0) {
        container.innerHTML = "<p>No results found</p>";
        return;
    }
    results.forEach(item => {
        const div = document.createElement("div");
        div.className = "archive-item";
        div.innerHTML = `<strong>${item.date} ${item.time}</strong> - ${item.content}`;
        container.appendChild(div);
    });
}

document.getElementById("search-button").addEventListener("click", () => {
    const startDate = document.getElementById("start-date").value;
    const startTime = document.getElementById("start-time").value || "00:00";
    const endDate = document.getElementById("end-date").value;
    const endTime = document.getElementById("end-time").value || "23:59";

    const startDateTime = new Date(`${startDate}T${startTime}`);
    const endDateTime = new Date(`${endDate}T${endTime}`);

    const filtered = archiveData.filter(item => {
        const itemDateTime = new Date(`${item.date}T${item.time}`);
        return itemDateTime >= startDateTime && itemDateTime <= endDateTime;
    });

    displayResults(filtered);
});