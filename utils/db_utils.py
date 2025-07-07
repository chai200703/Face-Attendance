import sqlite3 as db
from datetime import datetime
import pandas as pd

def get_connection():
    return db.connect("attendance.db", check_same_thread=False)

def view_logs():
    conn = get_connection()
    df=pd.read_sql_query("Select * FROM attendance",conn)
    conn.close()
    return df
    

def delete_today_logs():
    conn = db.connect("attendance.db", check_same_thread=False)
    today = datetime.now().strftime("%Y-%m-%d")
    conn.execute("DELETE FROM attendance WHERE date = ?", (today,))
    conn.close()

def delete_all_logs():
    conn = db.connect("attendance.db", check_same_thread=False)
    conn.execute("DELETE FROM attendance")
    conn.close()
    
def delete_logs_by_name(name):
    conn = db.connect("attendance.db", check_same_thread=False)
    conn.execute("DELETE FROM attendance WHERE name = ?",(name,))
    conn.close()

def get_today_logs():
    conn = get_connection()
    today = datetime.now().strftime("%Y-%m-%d")
    df=pd.read_sql_query("SELECT * FROM attendance WHERE date = ?",conn,params=(today,))
    conn.close()
    return df

def get_logs_by_name(name):
    conn=get_connection()
    df=pd.read_sql_query("Select * FROM attendance WHERE name= ?",conn,params=(name,))
    conn.close()
    return df