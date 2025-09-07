const modal = document.getElementById('machineNameModal');
const machineNameInput = document.getElementById('machineNameInput');
const machinesList = document.getElementById('machinesList');
const submitMachineName = document.getElementById('submitMachineName');
const errorMsg = document.getElementById('errorMsg');

function loadSavedMachines() {
    let machines = JSON.parse(localStorage.getItem('machines')) || [];

    if (!machines.includes("test")) {
        machines.push("test");
        localStorage.setItem('machines', JSON.stringify(machines));
    }

    machinesList.innerHTML = "";
    machines.forEach(name => {
        const option = document.createElement('option');
        option.value = name;
        machinesList.appendChild(option);
    });
}

submitMachineName.addEventListener('click', async () => {
    const name = machineNameInput.value.trim();
    try {
        const response = await fetch(`http://127.0.0.1:5000/data/${name}/years`);
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();
        console.log(data);

    } catch (error) {
        console.error("Fetch error: ", error);
    }

    if (name) {
        let machines = JSON.parse(localStorage.getItem('machines')) || [];
        if (!machines.includes(name)) {
            machines.push(name);
            localStorage.setItem('machines', JSON.stringify(machines));
        }
        modal.style.display = 'none';
    } else {
        errorMsg.style.display = 'block';
    }
});

machineNameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        submitMachineName.click();
    }
});

loadSavedMachines();

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
