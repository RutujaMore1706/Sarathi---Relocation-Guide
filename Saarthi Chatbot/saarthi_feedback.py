import streamlit as st
import datetime
from saarthi_analytics import (
    init_duckdb_connection,
    create_table,
    get_all_records,
    get_filtered_records,
    get_total_users,
)
import pandas as pd
import plotly.express as px

# Initialize connection and create table
@st.cache_resource
def init_db():
    conn = init_duckdb_connection()
    create_table(conn)
    return conn

conn = init_db()

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&family=Inter:wght@400&display=swap');
    
    .banner {
        background: linear-gradient(to right, #4B9FE1, #8867C5);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
    }
    .banner h1 {
        font-family: 'Poppins', sans-serif;
        color: white;
        font-size: 4.5em;
        font-weight: 700;
        margin: 0;
        padding: 0;
        letter-spacing: 1px;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
    }
    .banner p {
        font-family: 'Inter', sans-serif;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.4em;
        margin: 0;
        padding: 0;
        margin-top: -5px;
        letter-spacing: 0.5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Banner with improved typography
st.markdown("""
    <div class="banner">
        <h1>Saarthi</h1>
        <p>Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

# Fetch required data
total_users = get_total_users(conn)
df_all = get_all_records(conn)
total_records = len(df_all)

# --- Top Section: Cards for Total Users and Total Records ---
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div style="
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            background-color: #f9f9f9;">
            <h4 style="margin: 0; font-family: sans-serif; color: #333;">Total No. of Users</h4>
            <h2 style="margin-top: 10px; font-size: 1.8em; font-weight: bold; font-family: sans-serif; color: #007bff;">
                {total_users}
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div style="
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            background-color: #f9f9f9;">
            <h4 style="margin: 0; font-family: sans-serif; color: #333;">No. of Conversations</h4>
            <h2 style="margin-top: 10px; font-size: 1.8em; font-weight: bold; font-family: sans-serif; color: #007bff;">
                {total_records}
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Bar Chart Section: Rating Distribution ---
st.subheader("Ratings Distribution")

# Compute rating distribution
rating_counts = df_all["rating"].value_counts().sort_index()
rating_df = rating_counts.reset_index()
rating_df.columns = ["rating", "count"]

# Create a bar chart with a gradient color scale using Plotly
fig = px.bar(
    rating_df,
    x="rating",
    y="count",
    color="count",
    color_continuous_scale=["#dceefb", "#1c64f2"],
    labels={"rating": "Rating", "count": "Count"}
)
fig.update_layout(width=700, height=400)

st.plotly_chart(fig, use_container_width=True)

# --- Filter Form Section ---
st.subheader("Filter Records")

# Initialize session states for filters and filtered dataframe
if "df_filtered" not in st.session_state:
    st.session_state["df_filtered"] = df_all

with st.form(key="filter_form"):
    col1, col2 = st.columns(2)
    with col1:
        rating = st.selectbox(
            "Select Rating", options=["All"] + [1, 2, 3, 4, 5], key="rating_filter"
        )
    with col2:
        filter_date = st.date_input("Select Date", value=datetime.date.today(), key="date_filter")

    # Submit button
    filter_button = st.form_submit_button("Apply Filters")

# Apply filters on form submission
if filter_button:
    if rating == "All":
        st.session_state["df_filtered"] = df_all[
            df_all["summary_timestamp"].dt.date == filter_date
        ]
    else:
        st.session_state["df_filtered"] = df_all[
            (df_all["rating"] == rating)
            & (df_all["summary_timestamp"].dt.date == filter_date)
        ]

# --- Filtered Data Display Section ---
st.subheader("Filtered Records")

filtered_df = st.session_state["df_filtered"]

if filtered_df.empty:
    st.write("No records found for the selected filters.")
else:
    st.dataframe(filtered_df)
