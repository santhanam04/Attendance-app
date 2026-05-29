import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# ---------------- DATABASE ---------------- #
conn = sqlite3.connect("attendance.db", check_same_thread=False)
c = conn.cursor()

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

# ---------------- PAGE ---------------- #
st.set_page_config(
    page_title="Attendance & OT Management",
    layout="wide"
)

st.title("📋 Attendance & OT Management System")

menu = [
    "Manual Attendance Entry",
    "View Attendance",
    "Weekly Report",
    "Monthly Report"
]

choice = st.sidebar.selectbox("Select Menu", menu)

# ---------------- ADD ATTENDANCE ---------------- #
if choice == "Manual Attendance Entry":

    st.header("Manual Attendance Entry")

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

# ---------------- VIEW ATTENDANCE ---------------- #
elif choice == "View Attendance":

    st.header("Attendance Records")

    df = pd.read_sql_query(
        "SELECT * FROM attendance ORDER BY date DESC",
        conn
    )

    st.dataframe(df, use_container_width=True)

    total_present = len(df[df["attendance"] == "Present"])
    total_ot = df["ot_hours"].sum()

    col1, col2 = st.columns(2)

    col1.metric("Total Attendance", total_present)
    col2.metric("Total OT Hours", round(total_ot, 2))

# ---------------- WEEKLY REPORT ---------------- #
elif choice == "Weekly Report":

    st.header("Weekly Attendance & OT Report")

    employee = st.text_input("Enter Employee Name")

    if st.button("Generate Weekly Report"):

        today = datetime.today()
        week_ago = today - timedelta(days=7)

        query = f"""
        SELECT * FROM attendance
        WHERE emp_name='{employee}'
        AND date >= '{week_ago.date()}'
        """

        df = pd.read_sql_query(query, conn)

        if not df.empty:

            st.dataframe(df, use_container_width=True)

            total_present = len(
                df[df["attendance"] == "Present"]
            )

            total_ot = df["ot_hours"].sum()

            col1, col2 = st.columns(2)

            col1.metric(
                "Weekly Attendance",
                total_present
            )

            col2.metric(
                "Weekly OT Hours",
                round(total_ot, 2)
            )

        else:
            st.warning("No Weekly Records Found")

# ---------------- MONTHLY REPORT ---------------- #
elif choice == "Monthly Report":

    st.header("Monthly Attendance & OT Report")

    employee = st.text_input("Employee Name")

    if st.button("Generate Monthly Report"):

        current_month = datetime.today().strftime("%Y-%m")

        query = f"""
        SELECT * FROM attendance
        WHERE emp_name='{employee}'
        AND date LIKE '{current_month}%'
        """

        df = pd.read_sql_query(query, conn)

        if not df.empty:

            st.dataframe(df, use_container_width=True)

            total_present = len(
                df[df["attendance"] == "Present"]
            )

            total_ot = df["ot_hours"].sum()

            col1, col2 = st.columns(2)

            col1.metric(
                "Monthly Attendance",
                total_present
            )

            col2.metric(
                "Monthly OT Hours",
                round(total_ot, 2)
            )

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "Download Report CSV",
                csv,
                "monthly_report.csv",
                "text/csv"
            )

        else:
            st.warning("No Monthly Records Found")
