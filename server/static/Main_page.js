const modal = document.getElementById('machineNameModal');
const machineNameInput = document.getElementById('machineNameInput');
const machinesList = document.getElementById('machinesList');
const submitMachineName = document.getElementById('submitMachineName');
const errorMsg = document.getElementById('errorMsg');
const yearsModal = document.getElementById('yearsModal');
const yearsList = document.getElementById('yearsList');
const archiveContainer = document.getElementById("archive-results");
const btnYears = document.getElementById('get_years');

// --- Load saved machines from localStorage ---
function loadSavedMachines() {
    let machines = JSON.parse(localStorage.getItem('machines')) || [];
    machinesList.innerHTML = "";
    machines.forEach(name => {
        const option = document.createElement('option');
        option.value = name;
        machinesList.appendChild(option);
    });
}
loadSavedMachines();

// --- Submit machine name ---
submitMachineName.addEventListener('click', async () => {
    const machineName = machineNameInput.value.trim();
    if (!machineName) {
        errorMsg.style.display = 'block';
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/data/${machineName}/years`);
        if (!response.ok) {
            console.error("Error from server:", await response.text());
            errorMsg.style.display = 'block';
            return;
        }

        const years = await response.json();
        console.log("Years:", years);

        // Save machine
        let machines = JSON.parse(localStorage.getItem('machines')) || [];
        if (!machines.includes(machineName)) {
            machines.push(machineName);
            localStorage.setItem('machines', JSON.stringify(machines));
        }

        modal.style.display = 'none';
    } catch (error) {
        console.error("Fetch error:", error);
    }
});

// Enter key submits machine name
machineNameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') submitMachineName.click();
});

// --- Display archive results helper ---
function displayResults(results) {
    archiveContainer.innerHTML = "";
    if (results.length === 0) {
        archiveContainer.innerHTML = "<p>No results found</p>";
        return;
    }
    results.forEach(item => {
        const div = document.createElement("div");
        div.className = "archive-item";
        div.innerHTML = `<strong>${item.date} ${item.time}</strong> - ${item.content}`;
        archiveContainer.appendChild(div);
    });
}

// --- Search button ---
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

// --- Get years for machine ---
btnYears.addEventListener('click', async () => {
    const machineName = machineNameInput.value.trim();
    if (!machineName) {
        errorMsg.style.display = 'block';
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/data/${machineName}/years`);
        if (!response.ok) {
            console.error("Error fetching years:", await response.text());
            errorMsg.style.display = 'block';
            return;
        }

        const years = await response.json();
        yearsList.innerHTML = "";

        years.forEach(year => {
            const li = document.createElement('li');
            li.textContent = year;

            li.addEventListener('click', async () => {
                // Remove active from all years
                document.querySelectorAll('#yearsList li').forEach(el => el.classList.remove('active'));
                li.classList.add('active');

                try {
                    const respMonths = await fetch(`http://127.0.0.1:5000/data/${machineName}/${year}/months`);
                    if (!respMonths.ok) {
                        console.error("Error fetching months:", await respMonths.text());
                        return;
                    }

                    const months = await respMonths.json();

                    yearsModal.innerHTML = `
                        <h3>Months for ${year}</h3>
                        <div id="monthsContainer">
                            ${months.map(m => `<button class="month-btn">${m}</button>`).join('')}
                        </div>
                        <div id="dayContainer"></div>
                    `;

                    // --- Month buttons ---
                    document.querySelectorAll('.month-btn').forEach(monthBtn => {
                        monthBtn.addEventListener('click', async () => {
                            const month = monthBtn.textContent;

                            // Remove active from all months
                            document.querySelectorAll('.month-btn').forEach(el => el.classList.remove('active'));
                            monthBtn.classList.add('active');

                            try {
                                const respDays = await fetch(`http://127.0.0.1:5000/data/${machineName}/${year}/${month}/days`);
                                if (!respDays.ok) {
                                    console.error("Error fetching days:", await respDays.text());
                                    return;
                                }

                                const days = await respDays.json();

                                yearsModal.innerHTML = `
                                    <h3>Days for ${year}-${month}</h3>
                                    <div id="dayContainer" style="display:flex; gap:5px; flex-wrap:wrap;">
                                        ${days.map(day => `<button class="day-btn" style="padding:5px 10px; border-radius:5px; border:1px solid #333; cursor:pointer;">${day}</button>`).join('')}
                                    </div>
                                `;

                                // --- Day buttons ---
                                document.querySelectorAll('.day-btn').forEach(dayBtn => {
                                    dayBtn.addEventListener('click', async () => {
                                        const day = dayBtn.textContent;

                                        // Remove active from all days
                                        document.querySelectorAll('.day-btn').forEach(el => el.classList.remove('active'));
                                        dayBtn.classList.add('active');

                                        try {
                                            const respDayData = await fetch(`http://127.0.0.1:5000/data/${machineName}/${year}/${month}/${day}`);
                                            if (!respDayData.ok) {
                                                console.error("Error fetching day data:", await respDayData.text());
                                                return;
                                            }

                                            const dayContent = await respDayData.json();
                                            const dayContainer = document.getElementById('dayContainer');
                                            console.log(dayContent)
                                            console.log(dayContent['content']);
                                                

                                            dayContainer.innerHTML = `
                                            <pre style="background:#f0f0f0; padding:10px; border-radius:5px;">
                                                ${JSON.stringify(dayContent['content'], null, 2)}
                                            </pre>
                                        `;

                                            
                                            dayContainer.innerText = `<h2>${json(dayContent['content'])}</h2>`;
                                            //`<pre style="background:#f0f0f0; padding:10px; border-radius:5px;">${json(dayContent['content'])}</pre>`;

                                        } catch (error) {
                                            //console.log("Error fetching day data:");
                                        }
                                    });
                                });

                            } catch (error) {
                                console.error("Error fetching month data:", error);
                            }
                        });
                    });

                } catch (error) {
                    console.error("Error fetching months:", error);
                }
            });

            yearsList.appendChild(li);
        });

        yearsModal.style.display = 'block';
    } catch (error) {
        console.error("Network or code error:", error);
    }
});
