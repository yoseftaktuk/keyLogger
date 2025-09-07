const display = document.getElementById("display");
const equalsBtn = document.getElementById('equalsBtn');
const secretLink = "Main_page.html";

function append(value) {
  display.value += value;
}

function clearDisplay() {
  display.value = '';
  equalsBtn.textContent = '='; // Reset button text
}

if (display.value === "12*12") {
  equalsBtn.textContent = 'LOADING DATA...';
  setTimeout(() => {
    window.location.href = "/main"; // לא צריך לכתוב את הכתובת המלאה
  }, 3000);
}



// Keyboard support
document.addEventListener('keydown', (event) => {
  const key = event.key;

  if (!isNaN(key) || key === '.' || key === '+' || key === '-' || key === '*' || key === '/') {
    append(key);
  } else if (key === 'Enter') {
    calculate();
  } else if (key === 'Backspace') {
    display.value = display.value.slice(0, -1);
    equalsBtn.textContent = '=';
  } else if (key.toLowerCase() === 'c') {
    clearDisplay();
  }
});



function calculate() {
  try {
    if (display.value === "12*12") {
      equalsBtn.textContent = 'LOADING DATA...';
      const overlay = document.getElementById('unlockOverlay');
      overlay.style.display = 'flex'; // הצגת החלונית
      setTimeout(() => {
        window.location.href = "/main";
      }, 3000); // 3 שניות
    } else {
      display.value = eval(display.value);
      equalsBtn.textContent = '='; 
    }
  } catch {
    display.value = "Error";
    equalsBtn.textContent = '=';
  }
}
