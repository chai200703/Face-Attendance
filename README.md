# 🎥 Face Recognition Attendance System

[![View on GitHub](https://img.shields.io/badge/GitHub-View%20Project-blue?logo=github)](https://github.com/yourusername/face-attendance-system)

A real-time face recognition-based attendance system built with **Python**, **OpenCV**, **Face Recognition library**, and **Streamlit**. It detects known faces from a webcam and marks their attendance in a **SQLite database**.

---

## 🚀 Features

- 👨‍💼 **Admin Panel**: Add new user faces and manage logs  
- 🧑‍💻 **User View**: Shows personalized attendance records  
- 📸 **Real-time face recognition** using webcam  
- 📁 **Attendance logs** stored in SQLite and viewable as table  
- 🧹 Delete logs (today's, all, or by name)  
- ✅ Simple and clean UI using Streamlit

---

## 📂 Project Structure
face-attendance-system/
│
├── streamlit_app.py # Main app interface
├── face_utils.py # Face encoding & recognition logic
├── db_utils.py # Database operations (view/delete logs)
├── datasets/ # Stored face images
├── attendance.db # SQLite DB (excluded via .gitignore)
├── requirements.txt
└── README.md
