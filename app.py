import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="TopShelf Analytics", layout="wide")

# Rutgers Branding
st.markdown("""
    <style>
    .stButton > button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #cc0033; color: white; }
    .stMetric { background-color: white; padding: 10px; border-radius: 10px; box-shadow: 1px 1px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- ROSTER & STATE ---
# You can update this list with the actual Rutgers roster!
ROSTER = ["#12 Sarah S.", "#4 Julie R.", "#21 Mo K.", "#15 Mia T.", "#9 Gabi L."]

if 'game_data' not in st.session_state:
    st.session_state.game_data = []
if 'active_player' not in st.session_state:
    st.session_state.active_player = ROSTER[0]

# --- SIDEBAR: ROSTER MANAGEMENT ---
with st.sidebar:
    st.title("🥍 Roster Subs")
    st.session_state.active_player = st.radio("Current Active Player", ROSTER)
    st.markdown("---")
    if st.button("End Game & Clear Data"):
        st.session_state.game_data = []
        st.rerun()

# --- MAIN DASHBOARD ---
st.title(f"TopShelf: Tracking {st.session_state.active_player}")

col_field, col_actions = st.columns([6, 4])

with col_field:
    st.subheader("Interactive Shot Chart")
    # This captures the click on a 100x100 grid representing the field
    field_click = st.button("🎯 Tap Here to Record Shot Location")
    if field_click:
        # In a real iPad app, we'd use a canvas. Here we simulate the popup.
        st.warning("Coordinate Captured! Select Result below.")
    
    # Action Buttons
    c1, c2, c3 = st.columns(3)
    if c1.button("GOAL 🥅"):
        st.session_state.game_data.append({"Player": st.session_state.active_player, "Action": "Goal"})
    if c2.button("SAVE 🧤"):
        st.session_state.game_data.append({"Player": st.session_state.active_player, "Action": "Save"})
    if c3.button("WIDE/PIPE 🚫"):
        st.session_state.game_data.append({"Player": st.session_state.active_player, "Action": "Miss"})

with col_actions:
    st.subheader("Live Stat Attribution")
    # Your "Big Four" + Caused Turnovers
    a1, a2 = st.columns(2)
    if a1.button("GROUND BALL (GB)"):
        st.session_state.game_data.append({"Player": st.session_state.active_player, "Action": "GB"})
    if a2.button("TURNOVER (TO)"):
        st.session_state.game_data.append({"Player": st.session_state.active_player, "Action": "TO"})
    
    b1, b2 = st.columns(2)
    if b1.button("CAUSED TO (CT)"):
        st.session_state.game_data.append({"Player": st.session_state.active_player, "Action": "CT"})
    if b2.button("ASSIST (A)"):
        st.session_state.game_data.append({"Player": st.session_state.active_player, "Action": "A"})

# --- LIVE REPORT ---
st.markdown("---")
if st.session_state.game_data:
    df = pd.DataFrame(st.session_state.game_data)
    
    st.subheader("Live Game Stats")
    # Quick Summary Table for the Coach
    summary = df.groupby(['Player', 'Action']).size().unstack(fill_value=0)
    st.dataframe(summary, use_container_width=True)
    
    # Mini Heat Map Preview
    shot_df = df[df['Action'].isin(['Goal', 'Save', 'Miss'])]
    if not shot_df.empty:
        st.plotly_chart(px.bar(shot_df, x="Player", color="Action", title="Shooting Efficiency by Player"))
else:
    st.info("No data recorded. Start tapping actions to build the halftime report!")
