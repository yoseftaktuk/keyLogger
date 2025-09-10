// ----------------- Main JS for Archive & Live -----------------

const modal = document.getElementById('machineNameModal');
const machineNameInput = document.getElementById('machineNameInput');
const machinesList = document.getElementById('machinesList');
const submitMachineName = document.getElementById('submitMachineName');
const errorMsg = document.getElementById('errorMsg');
const yearsModal = document.getElementById('yearsModal');
const yearsList = document.getElementById('yearsList');
const archiveContainer = document.getElementById('archive-results');
const btnYears = document.getElementById('get_years');

// Load saved machine names
function loadSavedMachines() {
    let machines = JSON.parse(localStorage.getItem('machines')) || [];
    machinesList.innerHTML = '';
    machines.forEach(name => {
        const option = document.createElement('option');
        option.value = name;
        machinesList.appendChild(option);
    });
}
loadSavedMachines();

// Submit machine name
submitMachineName.addEventListener('click', async () => {
    const machineName = machineNameInput.value.trim();
    if (!machineName) {
        errorMsg.style.display = 'block';
        return;
    }
    try {
        const response = await fetch(`http://127.0.0.1:5000/data/${machineName}/years`);
        if (!response.ok) {
            errorMsg.style.display = 'block';
            return;
        }
        let machines = JSON.parse(localStorage.getItem('machines')) || [];
        if (!machines.includes(machineName)) {
            machines.push(machineName);
            localStorage.setItem('machines', JSON.stringify(machines));
        }
        modal.style.display = 'none';
    } catch (e) {
        errorMsg.style.display = 'block';
    }
});

machineNameInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') submitMachineName.click();
});

// Sample archive data
const archiveData = [
    {date: '2025-08-31', time: '13:00', content: 'Content item 1'},
    {date: '2025-08-31', time: '14:30', content: 'Content item 2'},
    {date: '2025-08-30', time: '10:15', content: 'Content item 3'},
    {date: '2025-08-29', time: '09:00', content: 'Content item 4'}
];

function displayResults(results) {
    archiveContainer.innerHTML = '';
    if (results.length === 0) {
        archiveContainer.innerHTML = '<p>No results found</p>';
        return;
    }
    results.forEach(item => {
        const div = document.createElement('div');
        div.className = 'archive-item';
        div.innerHTML = `<strong>${item.date} ${item.time}</strong> - ${item.content}`;
        archiveContainer.appendChild(div);
    });
}

// Search button
document.getElementById('search-button').addEventListener('click', () => {
    const startDate = document.getElementById('start-date').value;
    const startTime = document.getElementById('start-time').value || '00:00';
    const endDate = document.getElementById('end-date').value;
    const endTime = document.getElementById('end-time').value || '23:59';
    if (!startDate || !endDate) {
        displayResults([]);
        return;
    }
    const startDateTime = new Date(`${startDate}T${startTime}`);
    const endDateTime = new Date(`${endDate}T${endTime}`);
    const filtered = archiveData.filter(item => {
        const itemDateTime = new Date(`${item.date}T${item.time}`);
        return itemDateTime >= startDateTime && itemDateTime <= endDateTime;
    });
    displayResults(filtered);
});

// Years button
btnYears.addEventListener('click', async () => {
    const machineName = machineNameInput.value.trim();
    if (!machineName) {
        errorMsg.style.display = 'block';
        return;
    }
    try {
        const response = await fetch(`http://127.0.0.1:5000/data/${machineName}/years`);
        if (!response.ok) { errorMsg.style.display = 'block'; return; }
        const years = await response.json();
        yearsList.innerHTML = '';
        years.forEach(year => {
            const li = document.createElement('li');
            li.textContent = year;
            li.addEventListener('click', async () => {
                document.querySelectorAll('#yearsList li').forEach(el => el.classList.remove('active'));
                li.classList.add('active');
                try {
                    const respMonths = await fetch(`http://127.0.0.1:5000/data/${machineName}/${year}/months`);
                    if (!respMonths.ok) return;
                    const months = await respMonths.json();
                    yearsModal.innerHTML = `
                        <h3>Months for ${year}</h3>
                        <div id="monthsContainer">${months.map(m => `<button class="month-btn">${m}</button>`).join('')}</div>
                        <div id="dayContainer"></div>
                `;
    document.querySelectorAll('.month-btn').forEach(monthBtn => {
        monthBtn.addEventListener('click', async () => {
    const month = monthBtn.textContent;
    document.querySelectorAll('.month-btn').forEach(el => el.classList.remove('active'));
    monthBtn.classList.add('active');
    try {
        const respDays = await fetch(`http://127.0.0.1:5000/data/${machineName}/${year}/${month}/days`);
        if (!respDays.ok) return;
        const days = await respDays.json();
        const dayButtons = days.map(day => `<button class="day-btn" style="padding:5px 10px; border-radius:5px; border:1px solid #333; cursor:pointer;">${day}</button>`).join('');
        yearsModal.innerHTML = `
            <h3>Days for ${year}-${month}</h3>
            <div id="dayContainer" style="display:flex; gap:5px; flex-wrap:wrap; margin-bottom:10px;">
                ${dayButtons}
            </div>
            <pre id="dayContent" style="background:#f0f0f0; padding:10px; border-radius:5px; max-height:240px; overflow:auto;"></pre>
        `;
        document.querySelectorAll('.day-btn').forEach(dayBtn => {
            dayBtn.addEventListener('click', async () => {
                            const day = dayBtn.textContent;
        document.querySelectorAll('.day-btn').forEach(el => el.classList.remove('active'));
        dayBtn.classList.add('active');
        try {
            const respDayData = await fetch(`http://127.0.0.1:5000/data/${machineName}/${year}/${month}/${day}`);
            if (!respDayData.ok) return;
            const txt = await respDayData.text();
            const safe = txt.replace(/[<>&]/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;'}[c]));
            const pre = document.getElementById('dayContent');
            if (pre) pre.innerHTML = safe;
                    } catch (e) {}
                });
                                });
                            } catch(e){}
                        });
                    });
                } catch(e){}
            });
            yearsList.appendChild(li);
        });
        yearsModal.style.display = 'block';
    } catch(e){}
});

  

document.getElementById("search-button").addEventListener("click", async () => {
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;
    const startTime = document.getElementById("start-time").value || "00:00:00";
    const endTime = document.getElementById("end-time").value || "23:59:59";

    if (!startDate || !endDate) {
        alert("אנא מלא תאריכים התחלה וסיום");
        return;
    }

    const start = `${startDate}T${startTime}`;
    const end = `${endDate}T${endTime}`;

    try {
        const resp = await fetch(`http://127.0.0.1:5000/api/search/${start}/${end}`);
        if (!resp.ok) throw new Error(await resp.text());
        const data = await resp.json();

        
        let html = `<h3>תוצאות חיפוש: ${start} עד ${end}</h3>`;
        if (data.length === 0) {
            html += "<p>לא נמצאו תוצאות</p>";
        } else {
            html += `
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
                <thead>
                    <tr>
                        <th>מכונה</th>
                        <th>תאריך ושעה</th>
                        <th>תוכן</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(item => `
                        <tr>
                            <td>${item.machine}</td>
                            <td>${item.datetime}</td>
                            <td>${item.content}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>`;
        }

        const container = document.getElementById("archive-results");
        container.innerHTML = html;

    } catch (err) {
        console.error("שגיאת חיפוש:", err);
        alert("קרתה שגיאה בעת בקשת החיפוש");
    }
});

const button = document.getElementById('machines_list');
const dropdown = document.getElementById('machines_dropdown');
const output = document.getElementById('machines_output');
const arrow = document.getElementById('arrow');


button.addEventListener('click', function() {
    if (dropdown.classList.contains('show')) {
        dropdown.classList.remove('show');
        arrow.classList.remove('open');
        return;
    }

    fetch('/machines')
        .then(response => response.json())
        .then(data => {
            output.innerHTML = '';
            data.forEach(machine => {
                const li = document.createElement('li');
                li.textContent = machine;

                // מאזין ללחיצה על כל מכונה
                li.addEventListener('click', () => {
                    machineNameInput.value = machine; // העתקת השם ל-input
                    dropdown.classList.remove('show'); // סוגר את הרשימה
                    arrow.classList.remove('open');
                    console.log(machineNameInput)
                    console.log(machineNameInput.value)
                });

                output.appendChild(li);
            });

            dropdown.classList.add('show');
            arrow.classList.add('open');
        })
        .catch(error => console.error('Error:', error));
});

// סוגר את ה-dropdown אם לוחצים מחוץ
document.addEventListener('click', function(event) {
    if (!dropdown.contains(event.target) && event.target !== button) {
        dropdown.classList.remove('show');
        arrow.classList.remove('open');
    }
});

const selct = document.getElementById('list') 

selct.addEventListener('click', async() => {
    response = await fetch()
});




const listBtn = document.getElementById('list');
const machinesContainer = document.getElementById('machinesContainer');


listBtn.addEventListener('click', async () => {
    try {
        // קבלת רשימת השנים של כל המכונות (כאן בעצם "מכונות קיימות")
        const response = await fetch('/machines'); // אם אין נתיב כזה, אפשר להשתמש ב: fetch('/data') עם שינוי Flask
        if (!response.ok) throw new Error(await response.text());
        const machines = await response.json();

        machinesList.innerHTML = '';
        machines.forEach(machine => {
            const li = document.createElement('li');
            li.textContent = machine;
            li.style.cursor = 'pointer';
            li.style.padding = '5px';
            li.style.borderBottom = '1px solid #ccc';

            li.addEventListener('click', async () => {
                const confirmDelete = confirm(`אתה בטוח שאתה רוצה למחוק את המכונה: ${machine}?`);
                if (!confirmDelete) return;

                try {
                    const delResp = await fetch(`/data/${machine}/delete`, { method: 'DELETE' });
                    const result = await delResp.json();
                    if (!delResp.ok) throw new Error(result.error || 'Error');
                    alert(result.message);
                    li.remove(); // מסיר את המכונה מהרשימה
                } catch (err) {
                    console.error(err);
                    alert('קרתה שגיאה בעת המחיקה');
                }
            });

            machinesList.appendChild(li);
        });

        machinesContainer.style.display = 'block';

    } catch (err) {
        console.error('Error fetching machines:', err);
        alert('לא ניתן להביא את רשימת המכונות');
    }
});
