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
                                const dayButtons = days.map(day => `<button class="day-btn">${day}</button>`).join('');
                                yearsModal.innerHTML = `
                                    <h3>Days for ${year}-${month}</h3>
                                    <div id="dayContainer">${dayButtons}</div>
                                    <pre id="dayContent"></pre>
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
                                            document.getElementById('dayContent').innerHTML = safe;
                                        } catch(e) {}
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

// ---------------- Source/Website/path modal ----------------
const extractLinkBtn = document.getElementById('extractLinkBtn');

let bottomLinksModal = document.createElement('div');
bottomLinksModal.id = 'bottomLinksModal';
bottomLinksModal.style.position = 'fixed';
bottomLinksModal.style.bottom = '-250px';
bottomLinksModal.style.left = '0';
bottomLinksModal.style.width = '100%';
bottomLinksModal.style.maxHeight = '250px';
bottomLinksModal.style.backgroundColor = '#fff';
bottomLinksModal.style.borderTop = '2px solid #333';
bottomLinksModal.style.boxShadow = '0 -2px 15px rgba(0,0,0,0.3)';
bottomLinksModal.style.overflowY = 'auto';
bottomLinksModal.style.padding = '10px 20px';
bottomLinksModal.style.zIndex = 9999;
bottomLinksModal.style.transition = 'bottom 0.4s ease-in-out';
bottomLinksModal.style.fontSize = '18px';
bottomLinksModal.style.fontFamily = 'Arial, sans-serif';

// Title
let modalTitle = document.createElement('div');
modalTitle.textContent = 'Extracted Links';
modalTitle.style.fontWeight = 'bold';
modalTitle.style.fontSize = '20px';
modalTitle.style.marginBottom = '10px';
bottomLinksModal.appendChild(modalTitle);

// Close button
let closeBtn = document.createElement('button');
closeBtn.textContent = 'Close';
closeBtn.style.float = 'right';
closeBtn.style.marginBottom = '5px';
closeBtn.style.cursor = 'pointer';
closeBtn.addEventListener('click', () => { bottomLinksModal.style.bottom = '-250px'; });
bottomLinksModal.appendChild(closeBtn);

// Links container
let linksList = document.createElement('div');
linksList.style.clear = 'both';
bottomLinksModal.appendChild(linksList);

document.body.appendChild(bottomLinksModal);

extractLinkBtn.addEventListener('click', async () => {
    const pre = document.getElementById('dayContent');
    if (!pre || !pre.textContent.trim()) {
        linksList.innerHTML = '<p>No text available to extract links.</p>';
        bottomLinksModal.style.bottom = '0';
        return;
    }
    const textToCheck = pre.textContent.trim();
    try {
        const response = await fetch('http://127.0.0.1:5000/extract_link', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: textToCheck })
        });
        if (!response.ok) { linksList.innerHTML = '<p>Error fetching links.</p>'; bottomLinksModal.style.bottom='0'; return; }
        const data = await response.json();
        linksList.innerHTML = '';
        if (data.links && data.links.length > 0) {
            data.links.forEach(link => {
                let a = document.createElement('a');
                a.href = link.startsWith('http') ? link : 'https://' + link;
                a.textContent = link;
                a.target = '_blank';
                a.style.display = 'block';
                a.style.marginBottom = '5px';
                linksList.appendChild(a);
            });
        } else { linksList.innerHTML = '<p>No links found.</p>'; }
        bottomLinksModal.style.bottom = '0';
    } catch(e) {
        console.error(e);
        linksList.innerHTML = '<p>Error connecting to server.</p>';
        bottomLinksModal.style.bottom = '0';
    }
});


