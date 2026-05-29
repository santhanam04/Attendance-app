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

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Attendance & OT Management System",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Attendance & OT Management System")
st.caption("Track attendance, overtime and generate reports")

# ---------------- SIDEBAR ---------------- #
menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Manual Attendance",
        "View Attendance",
        "Employee Report",
        "Export Data"
    ]
)

# ---------------- FETCH DATA ---------------- #
df = pd.read_sql_query(
    "SELECT * FROM attendance ORDER BY date DESC",
    conn
)

# ---------------- DASHBOARD ---------------- #
if menu == "Dashboard":

    total_present = len(df[df["attendance"] == "Present"])
    total_absent = len(df[df["attendance"] == "Absent"])
    total_leave = len(df[df["attendance"] == "Leave"])
    total_ot = df["ot_hours"].sum() if not df.empty else 0

    today = datetime.today()
    week_start = today - timedelta(days=7)
    current_month = today.strftime("%Y-%m")

    weekly_df = df[
        pd.to_datetime(df["date"]) >= pd.to_datetime(week_start)
    ] if not df.empty else pd.DataFrame()

    monthly_df = df[
        df["date"].str.startswith(current_month)
    ] if not df.empty else pd.DataFrame()

    weekly_present = len(
        weekly_df[weekly_df["attendance"] == "Present"]
    ) if not weekly_df.empty else 0

    monthly_present = len(
        monthly_df[monthly_df["attendance"] == "Present"]
    ) if not monthly_df.empty else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Attendance", total_present)
    col2.metric("This Week", weekly_present)
    col3.metric("This Month", monthly_present)
    col4.metric("Total OT Hours", round(total_ot, 2))

    st.divider()

    st.subheader("Recent Attendance Records")

    if not df.empty:
        st.dataframe(df.head(20), use_container_width=True)

# ---------------- MANUAL ATTENDANCE ---------------- #
elif menu == "Manual Attendance":

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

        c.execute(
            """
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
            )
        )

        conn.commit()

        st.success("Attendance Saved Successfully!")

# ---------------- VIEW ATTENDANCE ---------------- #
elif menu == "View Attendance":

    st.subheader("View Attendance")

    if not df.empty:

        employee_filter = st.selectbox(
            "Employee Name",
            ["All Employees"] + list(df["emp_name"].unique())
        )

        if employee_filter != "All Employees":
            filtered_df = df[df["emp_name"] == employee_filter]
        else:
            filtered_df = df

        st.dataframe(filtered_df, use_container_width=True)

        total_present = len(
            filtered_df[
                filtered_df["attendance"] == "Present"
            ]
        )

        total_ot = filtered_df["ot_hours"].sum()

        col1, col2 = st.columns(2)

        col1.metric("Total Attendance", total_present)
        col2.metric("Total OT Hours", round(total_ot, 2))

# ---------------- EMPLOYEE REPORT ---------------- #
elif menu == "Employee Report":

    st.subheader("Employee Report")

    employee = st.text_input("Enter Employee Name")

    if st.button("Generate Report"):

        query = f"""
        SELECT * FROM attendance
        WHERE emp_name='{employee}'
        ORDER BY date DESC
        """

        report_df = pd.read_sql_query(query, conn)

        if not report_df.empty:

            st.dataframe(report_df, use_container_width=True)

            total_present = len(
                report_df[
                    report_df["attendance"] == "Present"
                ]
            )

            total_absent = len(
                report_df[
                    report_df["attendance"] == "Absent"
                ]
            )

            total_leave = len(
                report_df[
                    report_df["attendance"] == "Leave"
                ]
            )

            total_ot = report_df["ot_hours"].sum()

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Present", total_present)
            col2.metric("Absent", total_absent)
            col3.metric("Leave", total_leave)
            col4.metric("OT Hours", round(total_ot, 2))

# ---------------- EXPORT DATA ---------------- #
elif menu == "Export Data":

    st.subheader("Export Attendance Data")

    if not df.empty:

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download CSV File",
            data=csv,
            file_name="attendance_data.csv",
            mime="text/csv"
        )

st.divider()
st.caption("Made with ❤️ using Streamlit")
