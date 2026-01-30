"""
TopShelf Analytics - Women's Lacrosse Performance Tracking
High-fidelity, coach-ready Streamlit application for real-time lacrosse data analytics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Import custom modules
from data_manager import GameDataManager
from config import DEFAULT_ROSTER, COLORS, APP_TITLE, APP_SUBTITLE, COPYRIGHT_TEXT
from styles import get_custom_css

# --- PAGE CONFIG ---
st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS styling
st.markdown(get_custom_css(), unsafe_allow_html=True)

# --- HEADER BRANDING ---
st.markdown(f"""
    <div class="header-container">
        <h1 class="header-title">🥍 {APP_TITLE}</h1>
        <p class="header-subtitle">{APP_SUBTITLE}</p>
    </div>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = GameDataManager()
if 'active_player' not in st.session_state:
    st.session_state.active_player = DEFAULT_ROSTER[0]
if 'shot_pending' not in st.session_state:
    st.session_state.shot_pending = False
if 'shot_coords' not in st.session_state:
    st.session_state.shot_coords = None
if 'on_field' not in st.session_state:
    st.session_state.on_field = set(DEFAULT_ROSTER[:7])  # Start with 7 players on field

# --- SIDEBAR: ROSTER & SUBSTITUTIONS ---
with st.sidebar:
    st.markdown("### 🏃‍♀️ Player Management")
    
    # Active Player Selection
    st.session_state.active_player = st.selectbox(
        "Select Active Player:",
        DEFAULT_ROSTER,
        index=DEFAULT_ROSTER.index(st.session_state.active_player)
    )
    
    st.markdown("---")
    st.markdown("### 🔄 Substitutions")
    
    # Show who's on field
    st.markdown("**Currently On Field:**")
    for player in sorted(st.session_state.on_field):
        st.markdown(f"✓ {player}")
    
    st.markdown("")
    
    # Sub In/Out buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("SUB IN", use_container_width=True, type="primary"):
            st.session_state.on_field.add(st.session_state.active_player)
            st.session_state.data_manager.add_event(
                st.session_state.active_player, 
                "Sub In"
            )
            st.success(f"{st.session_state.active_player} subbed in!")
    
    with col2:
        if st.button("SUB OUT", use_container_width=True):
            if st.session_state.active_player in st.session_state.on_field:
                st.session_state.on_field.remove(st.session_state.active_player)
            st.session_state.data_manager.add_event(
                st.session_state.active_player, 
                "Sub Out"
            )
            st.warning(f"{st.session_state.active_player} subbed out!")
    
    st.markdown("---")
    st.markdown("### ⚙️ Game Controls")
    
    if st.button("🔄 Clear All Data", use_container_width=True):
        st.session_state.data_manager.clear_data()
        st.session_state.shot_pending = False
        st.session_state.shot_coords = None
        st.rerun()

# --- MAIN DASHBOARD ---
# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["🎯 Live Game", "📊 Analytics", "📋 Game Log"])

with tab1:
    # Live Game Dashboard
    col_shot, col_events = st.columns([3, 2])
    
    with col_shot:
        st.markdown("### 🎯 Shot Map")
        
        # Load and display the lacrosse field
        field_path = os.path.join(os.path.dirname(__file__), "assets", "lacrosse_field.svg")
        if os.path.exists(field_path):
            with open(field_path, 'r') as f:
                field_svg = f.read()
            st.image(field_path, use_container_width=True)
        
        # Create interactive shot chart using Plotly
        shot_data = st.session_state.data_manager.get_shot_data()
        
        if not shot_data.empty and 'X' in shot_data.columns and 'Y' in shot_data.columns:
            fig = go.Figure()
            
            # Add shot markers
            for action in ['Goal', 'Save', 'Miss']:
                action_data = shot_data[shot_data['Action'] == action]
                if not action_data.empty:
                    color = COLORS['scarlet'] if action == 'Goal' else (
                        COLORS['grey'] if action == 'Save' else COLORS['dark_grey']
                    )
                    fig.add_trace(go.Scatter(
                        x=action_data['X'],
                        y=action_data['Y'],
                        mode='markers',
                        name=action,
                        marker=dict(size=15, color=color),
                        text=action_data['Player'],
                        hovertemplate='<b>%{text}</b><br>Action: ' + action + '<extra></extra>'
                    ))
            
            fig.update_layout(
                xaxis=dict(range=[0, 100], showgrid=False, zeroline=False),
                yaxis=dict(range=[0, 100], showgrid=False, zeroline=False),
                height=300,
                showlegend=True,
                hovermode='closest',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True, key="shot_chart")
        
        # Shot recording interface
        st.markdown("#### Record Shot Location")
        st.info("👆 Click on the field above to record a shot location (coordinate-based tracking coming in next update)")
        
        # For now, use a simplified coordinate input
        col_x, col_y = st.columns(2)
        with col_x:
            shot_x = st.slider("Shot X Position", 0, 100, 50, key="shot_x")
        with col_y:
            shot_y = st.slider("Shot Y Position", 0, 100, 50, key="shot_y")
        
        if st.button("📍 RECORD SHOT POSITION", use_container_width=True, type="primary"):
            st.session_state.shot_pending = True
            st.session_state.shot_coords = (shot_x, shot_y)
            st.success("Shot position recorded! Now select the result →")
        
        # Shot result buttons
        if st.session_state.shot_pending:
            st.markdown("#### Shot Result:")
            c1, c2, c3 = st.columns(3)
            
            with c1:
                if st.button("🥅 GOAL", use_container_width=True, type="primary"):
                    if st.session_state.shot_coords:
                        st.session_state.data_manager.add_event(
                            st.session_state.active_player, 
                            "Goal",
                            x=st.session_state.shot_coords[0],
                            y=st.session_state.shot_coords[1]
                        )
                    else:
                        st.session_state.data_manager.add_event(
                            st.session_state.active_player, "Goal"
                        )
                    st.session_state.shot_pending = False
                    st.rerun()
            
            with c2:
                if st.button("🧤 SAVE", use_container_width=True):
                    if st.session_state.shot_coords:
                        st.session_state.data_manager.add_event(
                            st.session_state.active_player, 
                            "Save",
                            x=st.session_state.shot_coords[0],
                            y=st.session_state.shot_coords[1]
                        )
                    else:
                        st.session_state.data_manager.add_event(
                            st.session_state.active_player, "Save"
                        )
                    st.session_state.shot_pending = False
                    st.rerun()
            
            with c3:
                if st.button("🚫 MISS", use_container_width=True):
                    if st.session_state.shot_coords:
                        st.session_state.data_manager.add_event(
                            st.session_state.active_player, 
                            "Miss",
                            x=st.session_state.shot_coords[0],
                            y=st.session_state.shot_coords[1]
                        )
                    else:
                        st.session_state.data_manager.add_event(
                            st.session_state.active_player, "Miss"
                        )
                    st.session_state.shot_pending = False
                    st.rerun()
    
    with col_events:
        st.markdown("### ⚡ Quick Events")
        st.markdown(f"**Tracking: {st.session_state.active_player}**")
        
        st.markdown("#### Possession Events")
        
        # Ground Ball
        if st.button("🏐 GROUND BALL (GB)", use_container_width=True, type="primary"):
            st.session_state.data_manager.add_event(st.session_state.active_player, "GB")
            st.success("Ground Ball recorded!")
        
        # Draw Control
        if st.button("🎯 DRAW CONTROL", use_container_width=True, type="primary"):
            st.session_state.data_manager.add_event(st.session_state.active_player, "Draw")
            st.success("Draw Control recorded!")
        
        # Turnover
        if st.button("⚠️ TURNOVER (TO)", use_container_width=True):
            st.session_state.data_manager.add_event(st.session_state.active_player, "TO")
            st.warning("Turnover recorded!")
        
        # Caused Turnover
        if st.button("✨ CAUSED TO (CT)", use_container_width=True, type="primary"):
            st.session_state.data_manager.add_event(st.session_state.active_player, "CT")
            st.success("Caused Turnover recorded!")
        
        st.markdown("#### Assists")
        
        # Assist
        if st.button("🤝 ASSIST", use_container_width=True, type="primary"):
            st.session_state.data_manager.add_event(st.session_state.active_player, "Assist")
            st.success("Assist recorded!")
        
        # Quick Stats Display
        st.markdown("---")
        st.markdown("### 📊 Player Quick Stats")
        player_stats = st.session_state.data_manager.get_player_stats(st.session_state.active_player)
        if player_stats:
            for action, count in player_stats.items():
                st.metric(label=action, value=count)
        else:
            st.info("No stats yet for this player")

with tab2:
    # Analytics Dashboard
    st.markdown("### 📊 Game Analytics")
    
    df = st.session_state.data_manager.get_dataframe()
    
    if not df.empty:
        # Summary Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        total_goals = len(df[df['Action'] == 'Goal'])
        total_shots = len(df[df['Action'].isin(['Goal', 'Save', 'Miss'])])
        total_draws = len(df[df['Action'] == 'Draw'])
        total_gbs = len(df[df['Action'] == 'GB'])
        
        with col1:
            st.metric("Total Goals", total_goals)
        with col2:
            st.metric("Total Shots", total_shots)
        with col3:
            st.metric("Draw Controls", total_draws)
        with col4:
            st.metric("Ground Balls", total_gbs)
        
        st.markdown("---")
        
        # Player Summary Table
        st.markdown("### 📋 Player Statistics")
        summary = st.session_state.data_manager.get_summary()
        if not summary.empty:
            st.dataframe(summary, use_container_width=True)
        
        # Visualizations
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            # Shooting Efficiency
            shot_df = st.session_state.data_manager.get_shot_data()
            if not shot_df.empty:
                fig = px.bar(
                    shot_df, 
                    x="Player", 
                    color="Action",
                    title="Shooting Performance by Player",
                    color_discrete_map={
                        'Goal': COLORS['scarlet'],
                        'Save': COLORS['grey'],
                        'Miss': COLORS['dark_grey']
                    }
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col_viz2:
            # Action Distribution
            action_counts = df['Action'].value_counts()
            fig = px.pie(
                values=action_counts.values,
                names=action_counts.index,
                title="Action Distribution",
                color_discrete_sequence=[COLORS['scarlet'], COLORS['grey'], 
                                        COLORS['dark_grey'], COLORS['light_grey']]
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Top Performers
        st.markdown("### 🏆 Top Performers")
        
        col_top1, col_top2, col_top3 = st.columns(3)
        
        with col_top1:
            st.markdown("**Goals Leaders**")
            goals_df = df[df['Action'] == 'Goal']['Player'].value_counts().head(5)
            for player, count in goals_df.items():
                st.markdown(f"- {player}: {count}")
        
        with col_top2:
            st.markdown("**Draw Control Leaders**")
            draws_df = df[df['Action'] == 'Draw']['Player'].value_counts().head(5)
            for player, count in draws_df.items():
                st.markdown(f"- {player}: {count}")
        
        with col_top3:
            st.markdown("**Ground Ball Leaders**")
            gb_df = df[df['Action'] == 'GB']['Player'].value_counts().head(5)
            for player, count in gb_df.items():
                st.markdown(f"- {player}: {count}")
    else:
        st.info("📊 No game data available yet. Start recording events in the Live Game tab!")

with tab3:
    # Game Log
    st.markdown("### 📋 Detailed Game Log")
    
    df = st.session_state.data_manager.get_dataframe()
    
    if not df.empty:
        # Show most recent events first
        st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
        
        # Export option
        st.markdown("---")
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Game Data (CSV)",
            data=csv,
            file_name="topshelf_game_data.csv",
            mime="text/csv"
        )
    else:
        st.info("📋 No events recorded yet. Start tracking in the Live Game tab!")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        {COPYRIGHT_TEXT}
    </div>
""", unsafe_allow_html=True)
