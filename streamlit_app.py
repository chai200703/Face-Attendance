import streamlit as st
from utils import face_utils,db_utils
from main import start_attendance_system

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

        tab1, tab2, tab3 = st.tabs(["View Logs", "Delete Logs", "Export Logs"])

        with tab1:
            st.subheader("📋 View Logs")
            view_option = st.radio("Select:", ["Today's Logs", "All Logs"])
            if view_option == "Today's Logs":
                logs = db_utils.get_today_logs()
            else:
                logs = db_utils.view_logs()

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
    elif admin_pass:
        st.error("Incorrect password")
