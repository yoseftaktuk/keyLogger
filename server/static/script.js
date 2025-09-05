const buttons = Array.from(document.querySelectorAll('.menu button'));
const content = document.getElementById('content');

const btn1 = document.getElementById("btn1");
btn1.addEventListener("click", async () => {
const machineName = prompt("הכנס שם מחשב:");
    
if (!machineName) return;


try {
const response = await fetch(`http://127.0.0.1:5000/data/${machineName}/years`);
if (!response.ok) {
throw new Error("שגיאה בשרת");
}
const data = await response.json();
setContent("תשובת השרת", JSON.stringify(data));
} catch (error) {
console.error("שגיאה:", error);
setContent("שגיאה", "לא ניתן להביא את הנתונים");
}
});


// בחירה 2
const btn2 = document.getElementById("btn2");

btn2.addEventListener("click", async () => {
    const machineName = prompt('הכנס שם מחשב למחיקה:');
    if (!machineName) return;

    const year = prompt('הכנס שנה למחיקה:');
    if (!year) return;

    try {
        const response = await fetch(`http://127.0.0.1:5000/data/${machineName}/${year}/delete`,{method:'DELETE'});

        if (!response.ok) {
            throw new Error('שגיאה בשרת');
        }

        const data = await response.json();
        setContent(JSON.stringify(data)); // ← תיקון JSON.stringify
    } catch (error) {
        console.error('שגיאה:', error);
        setContent("יש בעיה");
    }

    setContent("בחירה 2", "בחרת באפשרות השנייה.");
});


// בחירה 3
const btn3 = document.getElementById("btn3");
btn3.addEventListener("click", () => {
setActive("בחירה 3", "בחרת באפשרות השלישית.");
});
function setActive(index){
buttons.forEach((b,i)=> b.classList.toggle('active', i===index));
if(index===0){
content.innerHTML = `<h2>בחירה 1</h2><p>תוכן עבור בחירה 1 — כאן אפשר להכניס טקסט, טבלאות או בקשות לשרת.</p>`;
} else if(index===1){
content.innerHTML = `<h2>בחירה 2</h2><p>תוכן עבור בחירה 2 — ניתן להציג תוצאות, גרפים וכדומה.</p>`;}
 else if(index===2) {
content.innerHTML = `<h2>בחירה 3</h2><p>תוכן עבור בחירה 3 — דף זה מדגים כפתורים מאוזנים בתפריט עליון.</p>`;
}}

// buttons.forEach((b,i)=> b.classList.toggle('active', i===index));
// btn3.addEventListener('click', () => {
//     if(index === 2)
//         content.innerHTML = `<h2>בחירה 3</h2><p>תוכן עבור בחירה 3 — דף זה מדגים כפתורים מאוזנים בתפריט עליון.</p>`;
//     })

const btn4 = document.getElementById('btn4');
btn4.addEventListener('click', () => {
   content.innerHTML = `<h2>בחירה</h2><input id='mechina_name' type="text" placeholder="הכנס שם מחשב"> <button id='send' type='submit'>לחץ כאן</button>`;


buttons.forEach((btn, i) => btn.addEventListener('click', () => setActive(i)))

const send = document.getElementById('send')

const mechina_name = document.getElementById('mechina_name')
send.addEventListener('click', () =>{
    const response = fetch(`http://127.0.0.1:5000/data/${mechina_name}/years`)
})
})