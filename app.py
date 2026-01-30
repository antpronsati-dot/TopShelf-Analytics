"""
TopShelf Analytics v2.0 - Professional Women's Lacrosse Performance Analytics
High-fidelity sports analytics tool optimized for live-action data entry and deep post-game analysis.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime, timedelta

# Import custom modules
from data_manager import GameDataManager
from config import (DEFAULT_ROSTER, COLORS, APP_TITLE, APP_SUBTITLE, COPYRIGHT_TEXT,
                   EVENT_TYPES, THRESHOLDS, ACTIVE_FIELD_SIZE, APP_VERSION, POSITIONS)
from styles import get_custom_css

# --- PAGE CONFIG ---
st.set_page_config(
    page_title=f"{APP_TITLE} {APP_VERSION}",
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
        <span class="version-badge">{APP_VERSION}</span>
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
if 'active_12' not in st.session_state:
    # Initialize with first 12 players as active
    st.session_state.active_12 = set(DEFAULT_ROSTER[:12])
if 'bench' not in st.session_state:
    st.session_state.bench = set(DEFAULT_ROSTER[12:])
if 'game_clock_minutes' not in st.session_state:
    st.session_state.game_clock_minutes = 60
if 'game_clock_seconds' not in st.session_state:
    st.session_state.game_clock_seconds = 0
if 'clock_running' not in st.session_state:
    st.session_state.clock_running = False
if 'game_period' not in st.session_state:
    st.session_state.game_period = "1st Half"

# Helper function to toggle substitution
def toggle_sub(player):
    """Toggle a player between active and bench."""
    if player in st.session_state.active_12:
        st.session_state.active_12.remove(player)
        st.session_state.bench.add(player)
        st.session_state.data_manager.stop_player_tracking(player)
        st.session_state.data_manager.add_event(player, "Sub Out", game_time=get_game_time())
    else:
        if len(st.session_state.active_12) < ACTIVE_FIELD_SIZE:
            st.session_state.bench.discard(player)
            st.session_state.active_12.add(player)
            st.session_state.data_manager.start_player_tracking(player)
            st.session_state.data_manager.add_event(player, "Sub In", game_time=get_game_time())

def get_game_time():
    """Get current game time as string."""
    return f"{st.session_state.game_clock_minutes:02d}:{st.session_state.game_clock_seconds:02d}"

def get_performance_badge(value, thresholds, lower_is_better=False):
    """Get HTML badge for performance metric."""
    color = st.session_state.data_manager.get_performance_color(value, thresholds, lower_is_better)
    class_name = f"perf-{color}"
    return f'<span class="{class_name}">{value}%</span>'

# --- SIDEBAR: GAME CLOCK & QUICK ACTIONS ---
with st.sidebar:
    st.markdown("### ⏱️ Game Clock")
    
    # Game Clock Display
    st.markdown(f"""
        <div class="game-clock">
            {st.session_state.game_clock_minutes:02d}:{st.session_state.game_clock_seconds:02d}
            <div class="clock-label">{st.session_state.game_period}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Clock Controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start" if not st.session_state.clock_running else "⏸️ Pause", use_container_width=True):
            st.session_state.clock_running = not st.session_state.clock_running
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.game_clock_minutes = 60
            st.session_state.game_clock_seconds = 0
            st.session_state.clock_running = False
    
    # Period Selection
    st.session_state.game_period = st.selectbox(
        "Period:",
        ["1st Half", "2nd Half", "Overtime", "2nd OT"]
    )
    
    st.markdown("---")
    
    # Quick Action Panel
    st.markdown("### ⚡ Quick Actions")
    st.markdown('<div class="quick-action-panel">', unsafe_allow_html=True)
    
    st.markdown("**Penalties:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🟨 Yellow Card", use_container_width=True):
            st.session_state.data_manager.add_event(
                st.session_state.active_player, 
                "Yellow Card",
                game_time=get_game_time(),
                period=st.session_state.game_period
            )
            st.warning(f"Yellow card: {st.session_state.active_player}")
    with col2:
        if st.button("🟩 Green Card", use_container_width=True):
            st.session_state.data_manager.add_event(
                st.session_state.active_player,
                "Green Card",
                game_time=get_game_time(),
                period=st.session_state.game_period
            )
            st.info(f"Green card: {st.session_state.active_player}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Current Player Selection
    st.markdown("### 👤 Active Player")
    st.session_state.active_player = st.selectbox(
        "Select for quick actions:",
        DEFAULT_ROSTER,
        index=DEFAULT_ROSTER.index(st.session_state.active_player)
    )
    
    st.markdown("---")
    
    # Game Controls
    if st.button("🗑️ Clear All Data", use_container_width=True):
        st.session_state.data_manager.clear_data()
        st.session_state.shot_pending = False
        st.session_state.shot_coords = None
        st.rerun()

# --- MAIN TABS ---
tab1, tab2, tab3 = st.tabs(["🎯 Live Game", "👥 Lineup Manager", "📊 Post-Game Analytics"])

# ============================================================================
# TAB 1: LIVE GAME
# ============================================================================
with tab1:
    col_field, col_events = st.columns([3, 2])
    
    with col_field:
        st.markdown("### 🥍 Interactive Shot Map")
        
        # Load and display the lacrosse field
        field_path = os.path.join(os.path.dirname(__file__), "assets", "lacrosse_field.svg")
        if os.path.exists(field_path):
            st.image(field_path, use_container_width=True)
        else:
            st.warning("⚠️ Lacrosse field image not found.")
        
        # Create interactive shot chart
        shot_data = st.session_state.data_manager.get_shot_data()
        
        if not shot_data.empty and 'X' in shot_data.columns and 'Y' in shot_data.columns:
            fig = go.Figure()
            
            # Add shot markers
            for action in ['Goal', 'Save', 'Miss', 'Shot On Goal', 'Shot Wide']:
                action_data = shot_data[shot_data['Action'] == action]
                if not action_data.empty:
                    color = COLORS['scarlet'] if action == 'Goal' else (
                        COLORS['grey'] if action == 'Save' else COLORS['charcoal']
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
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Shot recording interface
        st.markdown("#### 📍 Record Shot")
        col_x, col_y = st.columns(2)
        with col_x:
            shot_x = st.slider("X Position", 0, 100, 50, key="shot_x")
        with col_y:
            shot_y = st.slider("Y Position", 0, 100, 50, key="shot_y")
        
        if st.button("📍 SET SHOT LOCATION", use_container_width=True, type="primary"):
            st.session_state.shot_pending = True
            st.session_state.shot_coords = (shot_x, shot_y)
            st.success("Shot position set! Select result →")
        
        # Shot result buttons
        if st.session_state.shot_pending:
            st.markdown("#### Shot Result:")
            c1, c2, c3 = st.columns(3)
            
            with c1:
                if st.button("🥅 GOAL", use_container_width=True, type="primary", key="goal_btn"):
                    st.session_state.data_manager.add_event(
                        st.session_state.active_player, "Goal",
                        x=st.session_state.shot_coords[0],
                        y=st.session_state.shot_coords[1],
                        game_time=get_game_time(),
                        period=st.session_state.game_period
                    )
                    st.session_state.shot_pending = False
                    st.rerun()
            
            with c2:
                if st.button("🧤 SAVE", use_container_width=True, key="save_btn"):
                    st.session_state.data_manager.add_event(
                        st.session_state.active_player, "Save",
                        x=st.session_state.shot_coords[0],
                        y=st.session_state.shot_coords[1],
                        game_time=get_game_time(),
                        period=st.session_state.game_period
                    )
                    st.session_state.shot_pending = False
                    st.rerun()
            
            with c3:
                if st.button("🚫 MISS", use_container_width=True, key="miss_btn"):
                    st.session_state.data_manager.add_event(
                        st.session_state.active_player, "Miss",
                        x=st.session_state.shot_coords[0],
                        y=st.session_state.shot_coords[1],
                        game_time=get_game_time(),
                        period=st.session_state.game_period
                    )
                    st.session_state.shot_pending = False
                    st.rerun()
    
    with col_events:
        st.markdown("### ⚡ Quick Event Recording")
        st.markdown(f"**Tracking: {st.session_state.active_player}**")
        
        st.markdown("#### Possession Events")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏐 GROUND BALL", use_container_width=True, type="primary"):
                st.session_state.data_manager.add_event(
                    st.session_state.active_player, "GB",
                    game_time=get_game_time(),
                    period=st.session_state.game_period
                )
        with col2:
            if st.button("🎯 DRAW WIN", use_container_width=True, type="primary"):
                st.session_state.data_manager.add_event(
                    st.session_state.active_player, "Draw Win",
                    game_time=get_game_time(),
                    period=st.session_state.game_period
                )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⚠️ TURNOVER", use_container_width=True):
                st.session_state.data_manager.add_event(
                    st.session_state.active_player, "TO",
                    game_time=get_game_time(),
                    period=st.session_state.game_period
                )
        with col2:
            if st.button("✨ CAUSED TO", use_container_width=True, type="primary"):
                st.session_state.data_manager.add_event(
                    st.session_state.active_player, "CT",
                    game_time=get_game_time(),
                    period=st.session_state.game_period
                )
        
        st.markdown("#### Team Play")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🤝 ASSIST", use_container_width=True, type="primary"):
                st.session_state.data_manager.add_event(
                    st.session_state.active_player, "Assist",
                    game_time=get_game_time(),
                    period=st.session_state.game_period
                )
        with col2:
            if st.button("✅ PASS COMPLETE", use_container_width=True, type="primary"):
                st.session_state.data_manager.add_event(
                    st.session_state.active_player, "Pass Complete",
                    game_time=get_game_time(),
                    period=st.session_state.game_period
                )
        
        # Quick stats for current player
        st.markdown("---")
        st.markdown("### 📊 Player Stats")
        player_stats = st.session_state.data_manager.get_player_stats(st.session_state.active_player)
        if player_stats:
            for action, count in list(player_stats.items())[:5]:
                st.metric(label=action, value=count)
        else:
            st.info("No stats yet for this player")

# ============================================================================
# TAB 2: LINEUP MANAGER
# ============================================================================
with tab2:
    st.markdown("## 👥 Lineup Manager")
    
    col_active, col_bench = st.columns(2)
    
    with col_active:
        st.markdown(f"### ✅ Active 12 ({len(st.session_state.active_12)}/12)")
        
        for player in sorted(st.session_state.active_12):
            time_on_field = st.session_state.data_manager.get_player_time_on_field(player)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                    <div class="player-card player-card-active">
                        <strong>{player}</strong><br>
                        ⏱️ {time_on_field} min on field
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("➡️ Bench", key=f"sub_out_{player}", use_container_width=True):
                    toggle_sub(player)
                    st.rerun()
    
    with col_bench:
        st.markdown(f"### 🪑 Bench ({len(st.session_state.bench)})")
        
        for player in sorted(st.session_state.bench):
            time_on_field = st.session_state.data_manager.get_player_time_on_field(player)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                    <div class="player-card player-card-bench">
                        <strong>{player}</strong><br>
                        ⏱️ {time_on_field} min on field
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                if len(st.session_state.active_12) < ACTIVE_FIELD_SIZE:
                    if st.button("⬅️ Field", key=f"sub_in_{player}", use_container_width=True):
                        toggle_sub(player)
                        st.rerun()
                else:
                    st.button("⬅️ Field", key=f"sub_in_{player}", disabled=True, use_container_width=True)
    
    # Time on Field Summary
    st.markdown("---")
    st.markdown("### ⏱️ Time on Field Summary")
    
    time_data = []
    for player in DEFAULT_ROSTER:
        time = st.session_state.data_manager.get_player_time_on_field(player)
        status = "Active" if player in st.session_state.active_12 else "Bench"
        time_data.append({"Player": player, "Time (min)": time, "Status": status})
    
    if time_data:
        time_df = pd.DataFrame(time_data).sort_values("Time (min)", ascending=False)
        st.dataframe(time_df, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 3: POST-GAME ANALYTICS
# ============================================================================
with tab3:
    st.markdown("## 📊 Post-Game Analytics")
    
    df = st.session_state.data_manager.get_dataframe()
    
    if not df.empty:
        # Overall Game Metrics
        st.markdown("### 🎯 Game Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        total_goals = len(df[df['Action'] == 'Goal'])
        total_shots = len(df[df['Action'].isin(['Goal', 'Save', 'Miss', 'Shot On Goal', 'Shot Wide'])])
        total_draws = len(df[df['Action'].isin(['Draw Win', 'Draw Loss'])])
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
        
        # Player Performance Dashboards
        st.markdown("### 👤 Player Performance Dashboards")
        
        # Select player for detailed view
        selected_player = st.selectbox("Select Player for Detailed Analysis:", DEFAULT_ROSTER)
        
        st.markdown(f'<div class="performance-dashboard">', unsafe_allow_html=True)
        st.markdown(f"#### {selected_player} - Performance Metrics")
        
        # Calculate all metrics
        shot_acc = st.session_state.data_manager.calculate_shot_accuracy(selected_player)
        save_pct = st.session_state.data_manager.calculate_save_percentage(selected_player)
        draw_pct = st.session_state.data_manager.calculate_draw_control_win_pct(selected_player)
        pass_pct = st.session_state.data_manager.calculate_pass_completion_pct(selected_player)
        to_ratio = st.session_state.data_manager.calculate_turnover_ratio(selected_player)
        time_on_field = st.session_state.data_manager.get_player_time_on_field(selected_player)
        
        # Display metrics with color coding
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Shot Accuracy:** {get_performance_badge(shot_acc, THRESHOLDS['shot_accuracy'])}", unsafe_allow_html=True)
            st.markdown(f"**Draw Control Win %:** {get_performance_badge(draw_pct, THRESHOLDS['draw_control'])}", unsafe_allow_html=True)
            st.markdown(f"**Pass Completion %:** {get_performance_badge(pass_pct, THRESHOLDS['pass_completion'])}", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**Save Percentage:** {get_performance_badge(save_pct, THRESHOLDS['save_percentage'])}", unsafe_allow_html=True)
            st.markdown(f"**Turnover Ratio:** {get_performance_badge(to_ratio, THRESHOLDS['turnover_ratio'], lower_is_better=True)}", unsafe_allow_html=True)
            st.markdown(f"**Time on Field:** {time_on_field} minutes")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Player Stats Breakdown
        player_stats = st.session_state.data_manager.get_player_stats(selected_player)
        if player_stats:
            st.markdown("#### Detailed Statistics")
            stats_df = pd.DataFrame(list(player_stats.items()), columns=['Action', 'Count'])
            stats_df = stats_df.sort_values('Count', ascending=False)
            
            fig = px.bar(stats_df, x='Action', y='Count', 
                        title=f"{selected_player} - Action Breakdown",
                        color_discrete_sequence=[COLORS['scarlet']])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Team Performance Summary
        st.markdown("### 🏆 Team Performance Summary")
        
        summary = st.session_state.data_manager.get_summary()
        if not summary.empty:
            st.dataframe(summary, use_container_width=True)
        
        # Visualizations
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            # Top Scorers
            goals_data = df[df['Action'] == 'Goal']['Player'].value_counts().head(5)
            if not goals_data.empty:
                fig = px.bar(x=goals_data.index, y=goals_data.values,
                           title="Top Scorers",
                           labels={'x': 'Player', 'y': 'Goals'},
                           color_discrete_sequence=[COLORS['scarlet']])
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
        
        with col_viz2:
            # Action Distribution
            action_counts = df['Action'].value_counts().head(8)
            fig = px.pie(values=action_counts.values, names=action_counts.index,
                        title="Action Distribution",
                        color_discrete_sequence=[COLORS['scarlet'], COLORS['charcoal'], 
                                               COLORS['grey'], COLORS['light_grey']])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        # Export
        st.markdown("---")
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Game Data (CSV)",
            data=csv,
            file_name=f"topshelf_game_data_{timestamp}.csv",
            mime="text/csv"
        )
    else:
        st.info("📊 No game data available yet. Start recording events in the Live Game tab!")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        {COPYRIGHT_TEXT}
    </div>
""", unsafe_allow_html=True)
