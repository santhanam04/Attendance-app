
import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import date

st.set_page_config(page_title="Attendance & Salary Management", layout="wide")

DB="attendance.db"

def conn():
    return sqlite3.connect(DB, check_same_thread=False)

c = conn()
cur = c.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS attendance(
id INTEGER PRIMARY KEY AUTOINCREMENT,
employee_name TEXT,
work_date TEXT,
shift TEXT,
status TEXT,
ot_hours REAL,
salary_per_day REAL
)
""")
c.commit()

def hp(x):
    return hashlib.sha256(x.encode()).hexdigest()

if "logged_in" not in st.session_state:
    st.session_state.logged_in=False

if not st.session_state.logged_in:
    mode=st.sidebar.radio("Auth",["Login","Register"])

    if mode=="Register":
        st.title("Register")
        u=st.text_input("Username")
        p=st.text_input("Password",type="password")
        if st.button("Create Account"):
            try:
                cur.execute("INSERT INTO users(username,password) VALUES(?,?)",(u,hp(p)))
                c.commit()
                st.success("Account created")
            except:
                st.error("Username exists")
    else:
        st.title("Login")
        u=st.text_input("Username")
        p=st.text_input("Password",type="password")
        if st.button("Login"):
            r=cur.execute("SELECT * FROM users WHERE username=? AND password=?",(u,hp(p))).fetchone()
            if r:
                st.session_state.logged_in=True
                st.session_state.user=u
                st.rerun()
            else:
                st.error("Invalid credentials")
    st.stop()

st.sidebar.success(f"Welcome {st.session_state.user}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in=False
    st.rerun()

menu=st.sidebar.radio("Menu",[
"Dashboard","Manual Attendance","View Attendance",
"Salary Details","Delete Attendance","Export Data"
])

df=pd.read_sql_query("SELECT * FROM attendance ORDER BY work_date DESC", c)

if menu=="Dashboard":
    st.title("Attendance Dashboard")
    col1,col2,col3,col4=st.columns(4)
    col1.metric("Present", len(df[df["status"]=="Present"]) if len(df) else 0)
    col2.metric("Absent", len(df[df["status"]=="Absent"]) if len(df) else 0)
    col3.metric("Leave", len(df[df["status"]=="Leave"]) if len(df) else 0)
    col4.metric("OT Hours", float(df["ot_hours"].sum()) if len(df) else 0)
    st.dataframe(df,use_container_width=True)

elif menu=="Manual Attendance":
    st.title("Attendance Entry")
    with st.form("att"):
        emp=st.text_input("Employee Name")
        d=st.date_input("Date", value=date.today())
        shift=st.selectbox("Shift",[
            "6:30 AM - 3:00 PM",
            "3:00 PM - 11:30 PM",
            "11:30 PM - 6:30 AM"
        ])
        status=st.selectbox("Status",["Present","Absent","Leave"])
        ot=st.number_input("OT Hours",0.0,12.0,0.0,0.5)
        sal=st.number_input("Salary Per Day",0.0,step=100.0)
        ok=st.form_submit_button("Save")

    if ok:
        dup=pd.read_sql_query(
            "SELECT * FROM attendance WHERE employee_name=? AND work_date=?",
            c, params=(emp,str(d))
        )
        if len(dup):
            st.error("Attendance already entered")
        else:
            cur.execute("""
            INSERT INTO attendance(employee_name,work_date,shift,status,ot_hours,salary_per_day)
            VALUES(?,?,?,?,?,?)
            """,(emp,str(d),shift,status,ot,sal))
            c.commit()
            st.success("Saved")

elif menu=="View Attendance":
    st.title("Attendance Records")
    st.dataframe(df,use_container_width=True)

elif menu=="Salary Details":
    st.title("Salary Details")
    if len(df):
        sdf=df.copy()
        sdf["OT Salary"]=sdf["ot_hours"]*100
        sdf["Total Salary"]=sdf["salary_per_day"]+sdf["OT Salary"]
        st.dataframe(sdf,use_container_width=True)
        st.metric("Grand Total", f"₹ {sdf['Total Salary'].sum():,.2f}")
    else:
        st.info("No data")

elif menu=="Delete Attendance":
    st.title("Delete Attendance")
    st.dataframe(df,use_container_width=True)
    rid=st.number_input("Attendance ID", min_value=1, step=1)
    if st.button("Delete"):
        cur.execute("DELETE FROM attendance WHERE id=?",(int(rid),))
        c.commit()
        st.success("Deleted")

elif menu=="Export Data":
    st.title("Export")
    csv=df.to_csv(index=False)
    st.download_button("Download CSV", csv, "attendance.csv", "text/csv")
