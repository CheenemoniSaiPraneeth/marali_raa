import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Elite Execution Tracker", layout="wide")
DATA_FILE = "habit_data.csv"

# --- DATA HANDLING ---
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Date", "DSA", "Research", "Bus_Time", "Gym", "Walk", 
            "No_Social", "No_Junk", "No_Chat", "No_TT", "No_Phone_AM",
            "Wake_Early", "Sleep_Early", "Score"
        ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# --- SIDEBAR: LOGGING ---
st.sidebar.header("📅 Daily Log")
date = st.sidebar.date_input("Select Date", datetime.date.today())

st.sidebar.subheader("🎯 Core Tasks")
dsa = st.sidebar.checkbox("5–10 DSA Questions")
research = st.sidebar.checkbox("30–60 min Research")
bus = st.sidebar.checkbox("Productive Bus Time (≥1hr)")
gym = st.sidebar.checkbox("Gym Done Properly")
walk = st.sidebar.checkbox("Walk 4 KM")

st.sidebar.subheader("🚫 Control Rules")
social = st.sidebar.checkbox("No Social Media")
junk = st.sidebar.checkbox("No Junk Food")
chat = st.sidebar.checkbox("No Unnecessary Chatting")
tt = st.sidebar.checkbox("No Table Tennis")
phone = st.sidebar.checkbox("No Phone (First 30m)")

st.sidebar.subheader("🛌 Discipline")
wake = st.sidebar.checkbox("Wake before 6 AM")
sleep = st.sidebar.checkbox("Sleep before 11 PM")

if st.sidebar.button("Save Daily Progress"):
    results = [dsa, research, bus, gym, walk, social, junk, chat, tt, phone, wake, sleep]
    score = sum(results)
    
    new_entry = pd.DataFrame([[
        str(date), dsa, research, bus, gym, walk, social, junk, chat, tt, phone, wake, sleep, score
    ]], columns=df.columns)
    
    # Remove old entry for same date if exists, then add new
    df = df[df['Date'] != str(date)]
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)
    st.sidebar.success(f"Saved! Daily Score: {score}/12")

# --- MAIN DASHBOARD ---
st.title("🏆 Daily Execution Dashboard")

if not df.empty:
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # Metrics
    m1, m2, m3 = st.columns(3)
    avg_score = df['Score'].mean()
    m1.metric("Average Score", f"{avg_score:.1f} / 12")
    m2.metric("Total Days Tracked", len(df))
    m3.metric("Last Score", f"{df['Score'].iloc[-1]} / 12")

    st.divider()

    # Performance Graph
    st.subheader("📈 Performance Trend")
    fig = px.line(df, x='Date', y='Score', markers=True, 
                 title="Daily Efficiency Score", color_discrete_sequence=['#00CC96'])
    fig.update_layout(yaxis_range=[0,13])
    st.plotly_chart(fig, use_container_width=True)

    # Habit Analysis (Heatmap-style)
    st.subheader("🔍 What are you missing?")
    habit_cols = df.columns[1:-1]
    completion_rates = (df[habit_cols].mean() * 100).sort_values()
    
    fig_bar = px.bar(
        completion_rates, 
        orientation='h', 
        labels={'value': 'Success Rate (%)', 'index': 'Habit'},
        title="Consistency by Category",
        color=completion_rates,
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Raw Data Table
    with st.expander("See Raw History"):
        st.dataframe(df.sort_values('Date', ascending=False))
else:
    st.info("No data found. Log your first day in the sidebar! 👉")
