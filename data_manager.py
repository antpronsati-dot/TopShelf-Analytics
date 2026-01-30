"""
Data management module for TopShelf Analytics.
Handles game data, player stats, and event tracking.
"""
import pandas as pd
from typing import List, Dict, Any


class GameDataManager:
    """Manages game data and statistics for lacrosse analytics."""
    
    def __init__(self):
        """Initialize the data manager."""
        self.game_events: List[Dict[str, Any]] = []
        
    def add_event(self, player: str, action: str, x: float = None, y: float = None, 
                  period: str = None, time: str = None):
        """
        Add a game event to the data.
        
        Args:
            player: Player identifier
            action: Type of action (Goal, Save, GB, TO, etc.)
            x: X coordinate for shot location (optional)
            y: Y coordinate for shot location (optional)
            period: Game period (optional)
            time: Time of event (optional)
        """
        event = {
            "Player": player,
            "Action": action
        }
        if x is not None:
            event["X"] = x
        if y is not None:
            event["Y"] = y
        if period:
            event["Period"] = period
        if time:
            event["Time"] = time
            
        self.game_events.append(event)
    
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
        return df.groupby(['Player', 'Action']).size().unstack(fill_value=0)
    
    def get_shot_data(self) -> pd.DataFrame:
        """Get only shooting-related events."""
        if not self.game_events:
            return pd.DataFrame()
        df = self.get_dataframe()
        return df[df['Action'].isin(['Goal', 'Save', 'Miss'])]
    
    def clear_data(self):
        """Clear all game data."""
        self.game_events = []
    
    def get_player_stats(self, player: str) -> Dict[str, int]:
        """Get statistics for a specific player."""
        if not self.game_events:
            return {}
        df = self.get_dataframe()
        player_data = df[df['Player'] == player]
        if player_data.empty:
            return {}
        return player_data['Action'].value_counts().to_dict()
