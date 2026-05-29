# app.py
# Attendance & OT Management System
# Streamlit Full Dashboard UI

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(
    page_title="Attendance & OT Management System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

body {
    background-color: #050b16;
}

.main {
    background: linear-gradient(to right,#020b16,#071426,#020b16);
    color: white;
}

h1,h2,h3,h4,h5,h6,p,label,div {
    color: white !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(to bottom,#020b16,#061427,#020b16);
}

.metric-card {
    padding: 20px;
    border-radius: 16px;
    color: white;
    box-shadow: 0px 0px 15px rgba(255,255,255,0.08);
}

.card-green {
    background: linear-gradient(135deg,#1b5e20,#2e7d32);
}

.card-blue {
    background: linear-gradient(135deg,#0d47a1,#1565c0);
}

.card-purple {
    background: linear-gradient(135deg,#4527a0,#5e35b1);
}

.card-orange {
    background: linear-gradient(135deg,#e65100,#ef6c00);
}

.table-box {
    background-color: rgba(255,255,255,0.03);
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
st.sidebar.title("Attendance & OT\nManagement System")

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

st.sidebar.markdown("---")

# =========================
# FILTERS
# =========================
st.sidebar.subheader("Filters")

employee = st.sidebar.selectbox(
    "Employee Name",
    ["All Employees", "SANTHANA MARIAPPAN"]
)

start_date = st.sidebar.date_input(
    "Start Date",
    datetime(2025,5,23)
)

end_date = st.sidebar.date_input(
    "End Date",
    datetime(2025,5,29)
)

st.sidebar.button("Apply Filter")

st.sidebar.markdown("---")

st.sidebar.subheader("Shift Timings")

st.sidebar.markdown("""
• 6:30 AM - 3:00 PM

• 3:00 PM - 11:30 PM

• 11:30 PM - 6:30 AM
""")

# =========================
# SAMPLE DATA
# =========================
data = {
    "ID":[16,15,14,13,12,11,10,9,8,7],
    "Employee Name":["SANTHANA MARIAPPAN"]*10,
    "Date":[
        "2025-05-29",
        "2025-05-28",
        "2025-05-27",
        "2025-05-26",
        "2025-05-24",
        "2025-05-23",
        "2025-05-22",
        "2025-05-21",
        "2025-05-20",
        "2025-05-19"
    ],
    "Shift":[
        "6:30 AM - 3:00 PM",
        "3:00 PM - 11:30 PM",
        "6:30 AM - 3:00 PM",
        "3:00 PM - 11:30 PM",
        "3:00 PM - 11:30 PM",
        "6:30 AM - 3:00 PM",
        "3:00 PM - 11:30 PM",
        "6:30 AM - 3:00 PM",
        "3:00 PM - 11:30 PM",
        "6:30 AM - 3:00 PM"
    ],
    "Status":[
        "Present",
        "Present",
        "Present",
        "Present",
        "Present",
        "Present",
        "Absent",
        "Present",
        "Leave",
        "Present"
    ],
    "OT Hours":[2,2,2,2,2,2,0,2.5,0,2]
}

df = pd.DataFrame(data)

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.title("Attendance & OT Management System")
    st.write("Track attendance, overtime and generate reports")

    # =========================
    # TOP CARDS
    # =========================
    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card card-green">
        <h4>Total Attendance</h4>
        <h5>(Present Days)</h5>
        <h1>12</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card card-blue">
        <h4>This Week</h4>
        <h5>(Present Days)</h5>
        <h1>5</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card card-purple">
        <h4>This Month</h4>
        <h5>(Present Days)</h5>
        <h1>12</h1>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card card-orange">
        <h4>Total OT Hours</h4>
        <h1>24.50</h1>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # =========================
    # WEEKLY + MONTHLY
    # =========================
    col5,col6 = st.columns(2)

    with col5:
        st.subheader("Weekly Summary")

        weekly_df = pd.DataFrame({
            "Day":["Fri (23)","Sat (24)","Sun (25)","Mon (26)","Tue (27)","Wed (28)","Thu (29)"],
            "Present":[1,1,0,1,1,1,0],
            "Absent":[0,0,0,0,0,0,0],
            "Leave":[0,0,0,0,0,0,0],
            "OT Hours":[2,2,0,2,2,2,0]
        })

        st.dataframe(
            weekly_df,
            use_container_width=True,
            hide_index=True
        )

    with col6:
        st.subheader("Monthly Summary")

        monthly_df = pd.DataFrame({
            "Metric":[
                "Total Present Days",
                "Total Absent Days",
                "Total Leave Days",
                "Total OT Hours",
                "Avg OT per Day"
            ],
            "Total":[12,2,1,24.50,2.04]
        })

        st.dataframe(
            monthly_df,
            use_container_width=True,
            hide_index=True
        )

    st.write("")

    # =========================
    # ATTENDANCE RECORDS
    # =========================
    st.subheader("Recent Attendance Records")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.write("")

    # =========================
    # PIE CHART + QUICK STATS
    # =========================
    col7,col8 = st.columns([2,1])

    with col7:

        st.subheader("Attendance Overview (May 2025)")

        pie_df = pd.DataFrame({
            "Status":["Present","Absent","Leave"],
            "Count":[12,2,1]
        })

        fig = px.pie(
            pie_df,
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

    with col8:

        st.subheader("Quick Stats")

        st.markdown("""
        <div class="table-box">

        <h4>Total Employees : 1</h4>

        <h4>Total Records : 16</h4>

        <h4>First Record : 2025-05-19</h4>

        <h4>Latest Record : 2025-05-29</h4>

        </div>
        """, unsafe_allow_html=True)

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
            ["Present","Absent","Leave"]
        )

        ot = st.number_input(
            "OT Hours",
            min_value=0.0,
            max_value=12.0,
            step=0.5
        )

        submit = st.form_submit_button("Save Attendance")

        if submit:
            st.success("Attendance Saved Successfully!")

# =========================
# VIEW ATTENDANCE
# =========================
elif menu == "View Attendance":

    st.title("View Attendance")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

# =========================
# EMPLOYEE REPORT
# =========================
elif menu == "Employee Report":

    st.title("Employee Report")

    st.info("Employee performance report section.")

# =========================
# EXPORT DATA
# =========================
elif menu == "Export Data":

    st.title("Export Attendance Data")

    csv = df.to_csv(index=False)

    st.download_button(
        "Download CSV",
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
