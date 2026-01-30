"""
Data management module for TopShelf Analytics v2.0.
Handles game data, player stats, event tracking, and performance analytics.
"""
import pandas as pd
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta


class GameDataManager:
    """Manages game data and statistics for lacrosse analytics."""
    
    def __init__(self):
        """Initialize the data manager."""
        self.game_events: List[Dict[str, Any]] = []
        self.player_time_tracking: Dict[str, Dict[str, Any]] = {}
        self.game_start_time: datetime = None
        
    def add_event(self, player: str, action: str, x: float = None, y: float = None, 
                  period: str = None, time: str = None, game_time: str = None):
        """
        Add a game event to the data.
        
        Args:
            player: Player identifier
            action: Type of action (Goal, Save, GB, TO, etc.)
            x: X coordinate for shot location (optional)
            y: Y coordinate for shot location (optional)
            period: Game period (optional)
            time: Time of event (optional)
            game_time: Game clock time (optional)
        """
        event = {
            "Player": player,
            "Action": action,
            "Timestamp": datetime.now().strftime("%H:%M:%S")
        }
        if x is not None:
            event["X"] = x
        if y is not None:
            event["Y"] = y
        if period:
            event["Period"] = period
        if time:
            event["Time"] = time
        if game_time:
            event["GameTime"] = game_time
            
        self.game_events.append(event)
    
    def start_player_tracking(self, player: str):
        """Start tracking time on field for a player."""
        if player not in self.player_time_tracking:
            self.player_time_tracking[player] = {
                "total_time": 0,
                "current_session_start": None,
                "sessions": []
            }
        
        if self.player_time_tracking[player]["current_session_start"] is None:
            self.player_time_tracking[player]["current_session_start"] = datetime.now()
    
    def stop_player_tracking(self, player: str):
        """Stop tracking time on field for a player."""
        if player in self.player_time_tracking:
            if self.player_time_tracking[player]["current_session_start"] is not None:
                session_start = self.player_time_tracking[player]["current_session_start"]
                session_duration = (datetime.now() - session_start).total_seconds() / 60  # in minutes
                self.player_time_tracking[player]["total_time"] += session_duration
                self.player_time_tracking[player]["sessions"].append({
                    "start": session_start,
                    "duration": session_duration
                })
                self.player_time_tracking[player]["current_session_start"] = None
    
    def get_player_time_on_field(self, player: str) -> float:
        """Get total time on field for a player in minutes."""
        if player not in self.player_time_tracking:
            return 0.0
        
        total = self.player_time_tracking[player]["total_time"]
        
        # Add current session if active
        if self.player_time_tracking[player]["current_session_start"] is not None:
            current = (datetime.now() - self.player_time_tracking[player]["current_session_start"]).total_seconds() / 60
            total += current
        
        return round(total, 1)
    
    def get_dataframe(self) -> pd.DataFrame:
        """Get game events as a pandas DataFrame."""
        if not self.game_events:
            return pd.DataFrame()
        return pd.DataFrame(self.game_events)
    
    def get_summary(self) -> pd.DataFrame:
        """Get summary statistics by player and action."""
        if not self.game_events:
            return pd.DataFrame()
        df = self.get_dataframe()
        try:
            return df.groupby(['Player', 'Action']).size().unstack(fill_value=0)
        except ValueError:
            # Fallback for cases where unstack fails (e.g., single player or action)
            summary = df.groupby(['Player', 'Action']).size().reset_index(name='Count')
            return summary.pivot(index='Player', columns='Action', values='Count').fillna(0)
    
    def get_shot_data(self) -> pd.DataFrame:
        """Get only shooting-related events."""
        if not self.game_events:
            return pd.DataFrame()
        df = self.get_dataframe()
        return df[df['Action'].isin(['Goal', 'Save', 'Miss', 'Shot On Goal', 'Shot Wide'])]
    
    def clear_data(self):
        """Clear all game data."""
        self.game_events = []
        self.player_time_tracking = {}
    
    def get_player_stats(self, player: str) -> Dict[str, int]:
        """Get statistics for a specific player."""
        if not self.game_events:
            return {}
        df = self.get_dataframe()
        player_data = df[df['Player'] == player]
        if player_data.empty:
            return {}
        return player_data['Action'].value_counts().to_dict()
    
    def calculate_shot_accuracy(self, player: str) -> float:
        """Calculate shot accuracy percentage for a player."""
        stats = self.get_player_stats(player)
        goals = stats.get('Goal', 0)
        total_shots = goals + stats.get('Save', 0) + stats.get('Miss', 0) + stats.get('Shot On Goal', 0) + stats.get('Shot Wide', 0)
        
        if total_shots == 0:
            return 0.0
        return round((goals / total_shots) * 100, 1)
    
    def calculate_save_percentage(self, player: str) -> float:
        """Calculate save percentage for a goalie."""
        stats = self.get_player_stats(player)
        saves = stats.get('Save', 0)
        goals_against = stats.get('Goal', 0)  # Goals scored against this goalie
        total_shots = saves + goals_against
        
        if total_shots == 0:
            return 0.0
        return round((saves / total_shots) * 100, 1)
    
    def calculate_draw_control_win_pct(self, player: str) -> float:
        """Calculate draw control win percentage."""
        stats = self.get_player_stats(player)
        wins = stats.get('Draw Win', 0)
        losses = stats.get('Draw Loss', 0)
        total = wins + losses
        
        if total == 0:
            return 0.0
        return round((wins / total) * 100, 1)
    
    def calculate_pass_completion_pct(self, player: str) -> float:
        """Calculate pass completion percentage."""
        stats = self.get_player_stats(player)
        complete = stats.get('Pass Complete', 0)
        incomplete = stats.get('Pass Incomplete', 0)
        total = complete + incomplete
        
        if total == 0:
            return 0.0
        return round((complete / total) * 100, 1)
    
    def calculate_turnover_ratio(self, player: str) -> float:
        """Calculate turnover ratio (turnovers per possession)."""
        stats = self.get_player_stats(player)
        turnovers = stats.get('TO', 0)
        # Approximate possessions as sum of key possession events
        possessions = (stats.get('GB', 0) + stats.get('Draw Win', 0) + 
                      stats.get('Pass Complete', 0) + turnovers)
        
        if possessions == 0:
            return 0.0
        return round((turnovers / possessions) * 100, 1)
    
    def get_performance_color(self, metric_value: float, thresholds: Dict[str, float], 
                            lower_is_better: bool = False) -> str:
        """
        Get color code for performance metric.
        
        Args:
            metric_value: The calculated metric value (as percentage)
            thresholds: Dict with 'excellent' and 'good' threshold values
            lower_is_better: If True, reverse the color logic (for turnovers)
        
        Returns:
            Color code: 'green', 'yellow', or 'red'
        """
        excellent = thresholds.get('excellent', 0) * 100  # Convert to percentage
        good = thresholds.get('good', 0) * 100
        
        if lower_is_better:
            if metric_value <= excellent:
                return 'green'
            elif metric_value <= good:
                return 'yellow'
            else:
                return 'red'
        else:
            if metric_value >= excellent:
                return 'green'
            elif metric_value >= good:
                return 'yellow'
            else:
                return 'red'

