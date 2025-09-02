import app
import os
import json

@app.route("/machines")
def get_target_machines_list():
    machines = []
    data_folder = app.DATA_FOLDER
    if not os.path.exists(data_folder):
        return "No machines found"

    for machine in os.listdir(data_folder):
        machines.append(machine)
    return json.dumps(machines)

@app.route("/data/<machine>/years")
def get_years_list(machine):
    years = []
    machine_folder = os.path.join(app.DATA_FOLDER, machine)
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

