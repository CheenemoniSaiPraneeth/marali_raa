import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Elite Execution Tracker", layout="wide")

# Use persistent disk if available (Render), else fallback to local
DATA_FILE = "/data/habit_data.csv" if os.path.exists("/data") else "habit_data.csv"

# --- DATA HANDLING ---
COLUMNS = [
    "Date", "DSA", "Research", "Bus_Time", "Gym", "Walk", 
    "No_Social", "No_Junk", "No_Chat", "No_TT", "No_Phone_AM",
    "Wake_Early", "Sleep_Early", "Score"
]

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except:
            st.warning("⚠️ Data file corrupted. Resetting...")
    
    df = pd.DataFrame(columns=COLUMNS)
    df.to_csv(DATA_FILE, index=False)
    return df

def save_data(df):
    temp_file = DATA_FILE + ".tmp"
    df.to_csv(temp_file, index=False)
    os.replace(temp_file, DATA_FILE)  # atomic write

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

if st.sidebar.button("💾 Save Daily Progress"):
    results = [dsa, research, bus, gym, walk, social, junk, chat, tt, phone, wake, sleep]
    score = sum(results)

    new_entry = pd.DataFrame([[
        str(date), dsa, research, bus, gym, walk,
        social, junk, chat, tt, phone, wake, sleep, score
    ]], columns=COLUMNS)

    # Replace existing entry for the same date
    df = df[df['Date'] != str(date)]
    df = pd.concat([df, new_entry], ignore_index=True)

    save_data(df)
    st.sidebar.success(f"✅ Saved! Score: {score}/12")

    st.rerun()

# --- MAIN DASHBOARD ---
st.title("🏆 Daily Execution Dashboard")

if not df.empty:
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # --- METRICS ---
    m1, m2, m3 = st.columns(3)
    avg_score = df['Score'].mean()

    m1.metric("📊 Average Score", f"{avg_score:.1f} / 12")
    m2.metric("📅 Days Tracked", len(df))
    m3.metric("🔥 Last Score", f"{df['Score'].iloc[-1]} / 12")

    st.divider()

    # --- PERFORMANCE GRAPH ---
    st.subheader("📈 Performance Trend")
    fig = px.line(
        df,
        x='Date',
        y='Score',
        markers=True,
        title="Daily Efficiency Score",
        color_discrete_sequence=['#00CC96']
    )
    fig.update_layout(yaxis_range=[0, 12])
    st.plotly_chart(fig, use_container_width=True)

    # --- HABIT ANALYSIS ---
    st.subheader("🔍 Weak Areas Analysis")
    habit_cols = df.columns[1:-1]

    completion_rates = (df[habit_cols].mean() * 100).sort_values()

    fig_bar = px.bar(
        completion_rates,
        orientation='h',
        labels={'value': 'Success Rate (%)', 'index': 'Habit'},
        title="Consistency by Habit",
        color=completion_rates,
        color_continuous_scale='RdYlGn'
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # --- STREAK TRACKER ---
    st.subheader("🔥 Streak Analysis")
    df['Perfect'] = df['Score'] == 12

    streak = 0
    max_streak = 0

    for val in df['Perfect']:
        if val:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0

    st.info(f"🏅 Longest Perfect Streak: {max_streak} days")

    # --- RAW DATA ---
    with st.expander("📂 View Raw History"):
        st.dataframe(df.sort_values('Date', ascending=False), use_container_width=True)

else:
    st.info("👉 No data yet. Start logging from the sidebar!")
