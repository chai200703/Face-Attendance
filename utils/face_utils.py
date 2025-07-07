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

def load_known_faces():
    dipanshu_image= frecog.load_image_file(r"datasets/dipanshu.jpg")
    dipanshu_encoding=frecog.face_encodings(dipanshu_image)[0]

    chaitanya_image=frecog.load_image_file(r"datasets\chaitanya.jpg")
    chaitanya_encoding=frecog.face_encodings(chaitanya_image)[0]

    navneet_image=frecog.load_image_file(r"datasets\navneet.jpg")
    navneet_encoding=frecog.face_encodings(navneet_image)[0]

    kface_encodings=[dipanshu_encoding,chaitanya_encoding,navneet_encoding]
    kface_names=["Dipanshu","Chaitanya","Navneet"]
    return kface_encodings,kface_names

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
