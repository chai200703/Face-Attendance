import streamlit as st
from utils import face_utils,db_utils
from main import start_attendance_system
import os
import face_recognition as frecog
from PIL import Image
import numpy as np

st.set_page_config(page_title="Face Attendance System", layout="wide")

# --- App Title --- #
st.title("📸 Face Recognition Attendance System")

# --- Sidebar Menu --- #
menu = st.sidebar.selectbox("Select Section", ["Home", "User", "Admin"])

# --- Home Page --- #
if menu == "Home":
    st.image("https://cdn-icons-png.flaticon.com/512/2920/2920322.png", width=100)
    st.header("🏠 Welcome to the Smart Attendance System")

    st.markdown("""
    This is a secure, real-time **Face Recognition Attendance System** built using Python, OpenCV, and Streamlit.

    ### 🎯 Key Features:
    - ✅ Real-time face detection & recognition
    - 🧑‍🎓 User panel for marking attendance and viewing logs
    - 🛠️ Admin dashboard for managing logs, deleting entries, and exporting data

    ---

    ### 👨‍💼 Who Should Use This?
    - Students: Easily mark attendance using your face
    - Faculty/Admins: Monitor and manage attendance data securely

    ---

    ### 📍 How To Get Started:
    1. Go to the **User** section to mark your attendance and view your records.
    2. Admins can go to the **Admin** section to view, delete, and export logs (password protected).

    """)

# --- User Section --- #
elif menu == "User":
    st.header("🙋‍♂️ User Panel")

    if st.button("Mark My Attendance"):
        start_attendance_system()

    st.write("---")
    st.subheader("📅 View My Attendance Logs")
    user_name = st.text_input("Enter your name:")
    if user_name:
        user_logs = db_utils.get_logs_by_name(user_name.strip())
        if not user_logs.empty:
            st.dataframe(user_logs)
        else:
            st.warning("No attendance records found.")

# --- Admin Section --- #
elif menu == "Admin":
    st.header("🛠️ Admin Panel")
    admin_pass = st.text_input("Enter Admin Password", type="password")

    if admin_pass == "admin123":
        st.success("Access granted")

        tab1, tab2, tab3, tab4= st.tabs(["View Logs", "Delete Logs", "Export Logs","Add New Face"])

        with tab1:
            st.subheader("📋 View Logs")
            view_option = st.radio("Select:", ["Today's Logs", "All Logs"])
            if view_option == "Today's Logs":
                logs = db_utils.get_today_logs()
                if logs.empty:
                    st.info("There are no logs to show")
                else:
                    st.dataframe(logs)

            else:
                logs = db_utils.view_logs()
                if logs.empty:
                    st.info("There are no logs to show")
                else:
                    st.dataframe(logs)

            

        with tab2:
            st.subheader("🧹 Delete Attendance Logs")
            delete_selection = st.selectbox("Choose what you want to delete:", ["Today's Logs", "All Logs", "Logs by Name"])

            if delete_selection == "Logs by Name":
                name_to_delete = st.text_input("Enter the name to delete:")

            if st.button("Delete Logs"):
                if delete_selection == "Today's Logs":
                    db_utils.delete_today_logs()
                    st.success("✅ Today's attendance logs deleted.")
                    

                elif delete_selection == "All Logs":
                    db_utils.delete_all_logs()
                    st.success("✅ All attendance logs deleted.")
                    

                elif delete_selection == "Logs by Name":
                    if name_to_delete.strip():
                        db_utils.delete_logs_by_name(name_to_delete.strip())
                        st.success(f"✅ Logs for '{name_to_delete}' deleted.")
                        
                    else:
                        st.warning("⚠️ Please enter a name.")

        with tab3:
            st.subheader("📤 Export Logs")
            logs = db_utils.view_logs()
            if not logs.empty:
                csv = logs.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", csv, "attendance_logs.csv", "text/csv")
            else:
                st.info("No logs to export.")
        with tab4:
            os.makedirs("datasets", exist_ok=True)

            st.subheader("📥 Add New Face to Attendance System")

            with st.form("add_face_form"):
                new_name = st.text_input("Enter full name of the person")
                uploaded_image = st.file_uploader("Upload a front-facing image", type=["jpg", "jpeg", "png"])
                submitted = st.form_submit_button("➕ Add Face")

            if submitted:
                if not new_name or not uploaded_image:
                    st.warning("⚠️ Please provide both name and image.")
                else:
                # Save uploaded image temporarily
                    image = Image.open(uploaded_image).convert("RGB")
                    image_np = np.array(image)

            # Try to extract face encoding
                encodings = frecog.face_encodings(image_np)

                if len(encodings) == 0:
                    st.error("❌ No face detected. Please upload a clear front-facing photo.")
                elif len(encodings) > 1:
                    st.error("❌ Multiple faces detected. Please upload a photo with one person only.")
                else:
                # Save the image with the name
                    image_save_path = os.path.join("datasets", f"{new_name}.jpg")

                    if os.path.exists(image_save_path):
                        st.warning("⚠️ A face with this name already exists. Overwriting...")

                    image.save(image_save_path)
                    st.success(f"✅ Face for '{new_name}' added successfully! You can now mark their attendance.")


    elif admin_pass:
        st.error("Incorrect password")

st.sidebar.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: left;
        padding: 10px;
        font-size: 14px;
        color: #999999;
    }
    </style>

    <div class="footer">
        Made with ❤️ by <b><a href="https://github.com/chai200703" target="_blank">Chaitanya Joshi</b>
    </div>
""", unsafe_allow_html=True)
