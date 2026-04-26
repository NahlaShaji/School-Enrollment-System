from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# This function ensures the database and table exist every time you start
def init_db():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    # We use the table name 'Students' to match your SQLite Viewer
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            RollNo INTEGER PRIMARY KEY, 
            FullName TEXT NOT NULL, 
            Class TEXT NOT NULL, 
            BirthDate TEXT NOT NULL, 
            Address TEXT NOT NULL, 
            EnrollDate TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    # Connects to the local file named school.db
    conn = sqlite3.connect('school.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# Step 2: Check if the Roll No exists
@app.route('/check/<int:roll_no>')
def check_student(roll_no):
    try:
        conn = get_db_connection()
        student = conn.execute('SELECT * FROM Students WHERE RollNo = ?', (roll_no,)).fetchone()
        conn.close()
        
        if student:
            # If found, return the data as JSON
            return jsonify({
                "exists": True, 
                "data": dict(student)
            })
        return jsonify({"exists": False})
    except Exception as e:
        print(f"Database Error: {e}")
        return jsonify({"error": str(e)}), 500

# Step 3: Handle Save and Update buttons
@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        conn = get_db_connection()
        
        # Check if Roll No is already in the database
        existing = conn.execute('SELECT 1 FROM Students WHERE RollNo = ?', (data['RollNo'],)).fetchone()
        
        if existing:
            # UPDATE logic
            conn.execute('''
                UPDATE Students 
                SET FullName=?, Class=?, BirthDate=?, Address=?, EnrollDate=? 
                WHERE RollNo=?''',
                (data['FullName'], data['Class'], data['BirthDate'], data['Address'], data['EnrollDate'], data['RollNo']))
        else:
            # INSERT logic
            conn.execute('''
                INSERT INTO Students (RollNo, FullName, Class, BirthDate, Address, EnrollDate) 
                VALUES (?, ?, ?, ?, ?, ?)''',
                (data['RollNo'], data['FullName'], data['Class'], data['BirthDate'], data['Address'], data['EnrollDate']))
        
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Submit Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()  # This builds the table automatically
    app.run(debug=True)