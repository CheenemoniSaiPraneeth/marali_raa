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
        df = pd.read_csv(DATA_FILE)

        df = df.rename(columns={
            "Research": "Early_Morning_Study",
            "Bus_Time": "Evening_Study",
            "No_TT": "No_Ludo"
        })

        return df
    else:
        return pd.DataFrame(columns=[
            "Date",
            "DSA",
            "Early_Morning_Study",
            "Evening_Study",
            "Walk",
            "No_Social",
            "No_Chat",
            "No_Ludo",
            "No_Phone_AM",
            "Anime_Less_1Hr",
            "Wake_Early",
            "Sleep_Early",
            "Score"
        ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# --- SIDEBAR ---
st.sidebar.header("📅 Daily Log")
date = st.sidebar.date_input("Select Date", datetime.date.today())

st.sidebar.subheader("🎯 Core Tasks")
dsa = st.sidebar.checkbox("5 DSA Questions")
early = st.sidebar.checkbox("Early Morning Study")
evening = st.sidebar.checkbox("Evening Study")
walk = st.sidebar.checkbox("Walk 4 KM")

st.sidebar.subheader("🚫 Control Rules")
social = st.sidebar.checkbox("No Social Media")
chat = st.sidebar.checkbox("No Unnecessary Chatting")
ludo = st.sidebar.checkbox("No Ludo")
phone = st.sidebar.checkbox("No Phone (First 30m)")
anime = st.sidebar.checkbox("Anime < 1 Hour")

st.sidebar.subheader("🛌 Discipline")
wake = st.sidebar.checkbox("Wake before 5 AM")
sleep = st.sidebar.checkbox("Sleep before 10 PM")

if st.sidebar.button("Save Daily Progress"):
    data_dict = {
        "Date": str(date),
        "DSA": dsa,
        "Early_Morning_Study": early,
        "Evening_Study": evening,
        "Walk": walk,
        "No_Social": social,
        "No_Chat": chat,
        "No_Ludo": ludo,
        "No_Phone_AM": phone,
        "Anime_Less_1Hr": anime,
        "Wake_Early": wake,
        "Sleep_Early": sleep
    }

    score = sum([v for k, v in data_dict.items() if k != "Date"])
    data_dict["Score"] = score

    new_entry = pd.DataFrame([data_dict])

    # Ensure df has same columns
    df = df.reindex(columns=new_entry.columns)

    # Remove old entry for same date
    df = df[df['Date'] != str(date)]

    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)

    st.sidebar.success(f"Saved! Daily Score: {score}/11")

# --- DISPLAY NAME MAPPING ---
rename_map = {
    "DSA": "DSA",
    "Early_Morning_Study": "Early Morning Study",
    "Evening_Study": "Evening Study",
    "Walk": "Walk 4 KM",
    "No_Social": "No Social Media",
    "No_Chat": "No Chat",
    "No_Ludo": "No Ludo",
    "No_Phone_AM": "No Phone (Morning)",
    "Anime_Less_1Hr": "Anime < 1 Hour",
    "Wake_Early": "Wake Early",
    "Sleep_Early": "Sleep Early"
}

# --- MAIN DASHBOARD ---
st.title("🏆 Daily Execution Dashboard")

if not df.empty:
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # Metrics
    m1, m2, m3 = st.columns(3)
    avg_score = df['Score'].mean()
    m1.metric("Average Score", f"{avg_score:.1f} / 11")
    m2.metric("Total Days Tracked", len(df))
    m3.metric("Last Score", f"{df['Score'].iloc[-1]} / 11")

    st.divider()

    # GRAPH
    st.subheader("📈 Performance Trend")
    fig = px.line(df, x='Date', y='Score', markers=True)
    fig.update_layout(yaxis_range=[0, 12])
    st.plotly_chart(fig, use_container_width=True)

    # HABIT ANALYSIS (FIXED NAMES)
    st.subheader("🔍 What are you missing?")
    habit_cols = df.columns[1:-1]
    completion_rates = (df[habit_cols].mean() * 100).sort_values()

    # Rename for display
    completion_rates.index = [rename_map.get(col, col) for col in completion_rates.index]

    fig_bar = px.bar(
        completion_rates,
        orientation='h',
        labels={'value': 'Success Rate (%)', 'index': 'Habit'},
        color=completion_rates,
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # TABLE (RENAMED)
    with st.expander("See Raw History"):
        display_df = df.rename(columns=rename_map)
        st.dataframe(display_df.sort_values('Date', ascending=False))

else:
    st.info("No data found. Log your first day 👉")
