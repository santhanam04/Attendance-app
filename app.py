import streamlit as st
import sqlite3
import pandas as pd

# Database Connection
conn = sqlite3.connect("attendance.db", check_same_thread=False)
c = conn.cursor()

# Create Table
c.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_name TEXT,
    date TEXT,
    shift TEXT,
    attendance TEXT,
    ot_hours REAL
)
""")
conn.commit()

st.set_page_config(page_title="Attendance & OT System", layout="wide")

st.title("📋 Attendance & OT Management System")

menu = ["Add Attendance", "View Attendance", "Monthly Report"]

choice = st.sidebar.selectbox("Menu", menu)

# Add Attendance
if choice == "Add Attendance":

    st.subheader("Manual Attendance Entry")

    emp_name = st.text_input("Employee Name")

    date = st.date_input("Date")

    shift = st.selectbox(
        "Shift",
        [
            "6:30 AM - 3:00 PM",
            "3:00 PM - 11:30 PM",
            "11:30 PM - 6:30 AM"
        ]
    )

    attendance = st.selectbox(
        "Attendance Status",
        ["Present", "Absent", "Leave"]
    )

    ot_hours = st.number_input(
        "OT Hours",
        min_value=0.0,
        max_value=12.0,
        step=0.5
    )

    if st.button("Save Attendance"):

        c.execute("""
        INSERT INTO attendance
        (emp_name, date, shift, attendance, ot_hours)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            emp_name,
            str(date),
            shift,
            attendance,
            ot_hours
        ))

        conn.commit()

        st.success("Attendance Saved Successfully!")

# View Attendance
elif choice == "View Attendance":

    st.subheader("Attendance Records")

    df = pd.read_sql_query(
        "SELECT * FROM attendance",
        conn
    )

    st.dataframe(df, use_container_width=True)

    total_present = len(df[df["attendance"] == "Present"])
    total_ot = df["ot_hours"].sum()

    col1, col2 = st.columns(2)

    col1.metric("Total Present Days", total_present)
    col2.metric("Total OT Hours", total_ot)

# Monthly Report
elif choice == "Monthly Report":

    st.subheader("Employee Monthly Report")

    employee = st.text_input("Enter Employee Name")

    if st.button("Generate Report"):

        query = f"""
        SELECT * FROM attendance
        WHERE emp_name='{employee}'
        """

        df = pd.read_sql_query(query, conn)

        if not df.empty:

            st.dataframe(df, use_container_width=True)

            total_present = len(
                df[df["attendance"] == "Present"]
            )

            total_ot = df["ot_hours"].sum()

            st.success(f"Total Present Days: {total_present}")
            st.success(f"Total OT Hours: {total_ot}")

            csv = df.to_csv(index=False).encode('utf-8')

            st.download_button(
                "Download CSV",
                csv,
                "attendance_report.csv",
                "text/csv"
            )

        else:
            st.warning("No Records Found")
