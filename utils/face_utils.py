import os
import face_recognition as frecog
from datetime import datetime
import sqlite3 as db
conn=db.connect("attendance.db",check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        time TEXT,
        date TEXT
    )
""")
conn.commit()

def load_known_faces(folder="datasets"):
    known_encodings = []
    known_names = []

    for filename in os.listdir(folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(folder, filename)
            image = frecog.load_image_file(image_path)
            encodings = frecog.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
            else:
                print(f"No face found in {filename} — skipping.")

    return known_encodings, known_names

def mark_attendance(name):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT * FROM attendance
        WHERE name = ? AND date = ?
    """, (name, current_date))
    
    result = cursor.fetchone()

    if result is None:
        cursor.execute("""
            INSERT INTO attendance (name, time, date)
            VALUES (?, ?, ?)
        """, (name, current_time, current_date))
        conn.commit()
