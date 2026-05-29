# =========================
# SAMPLE DATA CLEAR + SALARY DETAILS VERSION
# =========================

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Attendance & Salary Management System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.main {
    background: linear-gradient(to right,#020b16,#071426,#020b16);
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(to bottom,#020b16,#071426,#020b16);
}

h1,h2,h3,h4,h5,h6,p,label,div {
    color: white !important;
}

.metric-card {
    padding: 22px;
    border-radius: 18px;
    color: white;
    box-shadow: 0px 0px 12px rgba(255,255,255,0.08);
}

.green-card {
    background: linear-gradient(135deg,#1b5e20,#43a047);
}

.blue-card {
    background: linear-gradient(135deg,#0d47a1,#1e88e5);
}

.purple-card {
    background: linear-gradient(135deg,#4a148c,#8e24aa);
}

.orange-card {
    background: linear-gradient(135deg,#e65100,#fb8c00);
}

.salary-card {
    background: linear-gradient(135deg,#004d40,#009688);
}

.table-box {
    background: rgba(255,255,255,0.03);
    padding: 15px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.08);
}

.footer {
    text-align:center;
    color:gray;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Attendance & Salary\nManagement System")

menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Manual Attendance",
        "Salary Details",
        "View Attendance",
        "Export Data"
    ]
)

# =========================
# EMPTY DATAFRAME
# =========================
if "attendance_data" not in st.session_state:

    st.session_state.attendance_data = pd.DataFrame(columns=[
        "Employee Name",
        "Date",
        "Shift",
        "Status",
        "OT Hours",
        "Salary Per Day"
    ])

df = st.session_state.attendance_data

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.title("Attendance & Salary Dashboard")

    total_present = len(df[df["Status"] == "Present"])
    total_absent = len(df[df["Status"] == "Absent"])
    total_leave = len(df[df["Status"] == "Leave"])
    total_ot = df["OT Hours"].sum()

    if len(df) > 0:
        total_salary = (
            df[df["Status"] == "Present"]["Salary Per Day"].sum()
        )
    else:
        total_salary = 0

    # =========================
    # TOP CARDS
    # =========================
    c1,c2,c3,c4,c5 = st.columns(5)

    with c1:
        st.markdown(f"""
        <div class="metric-card green-card">
        <h4>Total Present</h4>
        <h1>{total_present}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card blue-card">
        <h4>Total Absent</h4>
        <h1>{total_absent}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card purple-card">
        <h4>Total Leave</h4>
        <h1>{total_leave}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card orange-card">
        <h4>Total OT Hours</h4>
        <h1>{total_ot}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="metric-card salary-card">
        <h4>Total Salary</h4>
        <h1>₹ {total_salary}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # =========================
    # ATTENDANCE TABLE
    # =========================
    st.subheader("Attendance Records")

    st.dataframe(df, use_container_width=True)

    # =========================
    # PIE CHART
    # =========================
    if len(df) > 0:

        chart_df = pd.DataFrame({
            "Status":["Present","Absent","Leave"],
            "Count":[
                total_present,
                total_absent,
                total_leave
            ]
        })

        fig = px.pie(
            chart_df,
            values="Count",
            names="Status",
            hole=0.5
        )

        fig.update_layout(
            paper_bgcolor="#071426",
            plot_bgcolor="#071426",
            font_color="white"
        )

        st.plotly_chart(fig, use_container_width=True)

# =========================
# MANUAL ATTENDANCE
# =========================
elif menu == "Manual Attendance":

    st.title("Manual Attendance Entry")

    with st.form("attendance_form"):

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

        status = st.selectbox(
            "Status",
            [
                "Present",
                "Absent",
                "Leave"
            ]
        )

        ot_hours = st.number_input(
            "OT Hours",
            min_value=0.0,
            max_value=12.0,
            step=0.5
        )

        salary_per_day = st.number_input(
            "Salary Per Day",
            min_value=0,
            step=100
        )

        submit = st.form_submit_button("Save Attendance")

        if submit:

            new_row = {
                "Employee Name": emp_name,
                "Date": str(date),
                "Shift": shift,
                "Status": status,
                "OT Hours": ot_hours,
                "Salary Per Day": salary_per_day
            }

            st.session_state.attendance_data = pd.concat(
                [
                    st.session_state.attendance_data,
                    pd.DataFrame([new_row])
                ],
                ignore_index=True
            )

            st.success("Attendance Saved Successfully!")

# =========================
# SALARY DETAILS
# =========================
elif menu == "Salary Details":

    st.title("Salary Details")

    if len(df) == 0:
        st.warning("No attendance records found.")
    else:

        salary_df = df.copy()

        salary_df["OT Salary"] = salary_df["OT Hours"] * 100

        salary_df["Total Salary"] = (
            salary_df["Salary Per Day"] +
            salary_df["OT Salary"]
        )

        st.dataframe(
            salary_df,
            use_container_width=True
        )

        st.subheader("Salary Summary")

        total_salary = salary_df["Total Salary"].sum()

        st.markdown(f"""
        <div class="table-box">

        <h3>Total Salary : ₹ {total_salary}</h3>

        </div>
        """, unsafe_allow_html=True)

# =========================
# VIEW ATTENDANCE
# =========================
elif menu == "View Attendance":

    st.title("View Attendance")

    st.dataframe(
        df,
        use_container_width=True
    )

# =========================
# EXPORT DATA
# =========================
elif menu == "Export Data":

    st.title("Export Data")

    csv = df.to_csv(index=False)

    st.download_button(
        "Download Attendance CSV",
        csv,
        "attendance_data.csv",
        "text/csv"
    )

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
Made with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
