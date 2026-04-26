from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# --- CONFIGURATION ---
JPDB_TOKEN = "90935260|-31949237328396187|90958499"
DB_NAME = "SCHOOL-DB"
REL_NAME = "STUDENT-TABLE"
JPDB_BASE_URL = "http://api.login2xlore.com:5577"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-roll', methods=['POST'])
def check_roll():
    roll_no = request.json.get('roll_no')
    
    # Logic to check if Roll No exists in JsonPowerDB
    query = {
        "token": JPDB_TOKEN,
        "cmd": "GET_BY_KEY",
        "dbName": DB_NAME,
        "rel": REL_NAME,
        "jsonStr": json.dumps({"Roll-No": roll_no})
    }
    
    try:
        response = requests.post(f"{JPDB_BASE_URL}/api/irl", json=query)
        res_data = response.json()
        
        # If status is 200, the record exists
        if res_data.get("status") == 200:
            record = json.loads(res_data.get("data")).get("record")
            return jsonify({"exists": True, "data": record})
        return jsonify({"exists": False})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save-student', methods=['POST'])
def save_student():
    student_data = request.json
    
    # Logic to save new record
    put_request = {
        "token": JPDB_TOKEN,
        "cmd": "PUT",
        "dbName": DB_NAME,
        "rel": REL_NAME,
        "jsonStr": json.dumps(student_data)
    }
    
    response = requests.post(f"{JPDB_BASE_URL}/api/iml", json=put_request)
    return jsonify(response.json())

@app.route('/update-student', methods=['POST'])
def update_student():
    student_data = request.json
    roll_no = student_data.get("Roll-No")
    
    # Logic to update existing record based on Roll-No
    update_request = {
        "token": JPDB_TOKEN,
        "cmd": "UPDATE",
        "dbName": DB_NAME,
        "rel": REL_NAME,
        "jsonStr": json.dumps({roll_no: student_data})
    }
    
    response = requests.post(f"{JPDB_BASE_URL}/api/iml", json=update_request)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
