"""
Configuration settings for TopShelf Analytics v2.0.
Includes roster, colors, branding, and game settings.
"""

# Professional Theme Colors (v2.0)
COLORS = {
    "scarlet": "#CC0033",
    "charcoal": "#2B2B2B",
    "white": "#FFFFFF",
    "light_grey": "#F5F5F5",
    "grey": "#63666A",
    "green": "#28A745",
    "yellow": "#FFC107",
    "red": "#DC3545"
}

# Extended Roster (15 players for Active 12 + Bench)
DEFAULT_ROSTER = [
    "#12 Sarah S.",
    "#4 Julie R.",
    "#21 Mo K.",
    "#15 Mia T.",
    "#9 Gabi L.",
    "#7 Emma C.",
    "#3 Kate D.",
    "#18 Olivia P.",
    "#22 Alex M.",
    "#11 Sam T.",
    "#5 Riley B.",
    "#16 Jordan W.",
    "#23 Taylor H.",
    "#8 Casey N.",
    "#14 Morgan F."
]

# Player Positions
POSITIONS = {
    "Attack": ["#12 Sarah S.", "#4 Julie R.", "#21 Mo K."],
    "Midfield": ["#15 Mia T.", "#9 Gabi L.", "#7 Emma C.", "#3 Kate D."],
    "Defense": ["#18 Olivia P.", "#22 Alex M.", "#11 Sam T."],
    "Goalie": ["#5 Riley B."],
    "Bench": ["#16 Jordan W.", "#23 Taylor H.", "#8 Casey N.", "#14 Morgan F."]
}

# Game Event Types
EVENT_TYPES = {
    "scoring": ["Goal", "Save", "Miss", "Shot On Goal", "Shot Wide"],
    "possession": ["GB", "TO", "CT", "Draw Win", "Draw Loss"],
    "team": ["Assist", "Pass Complete", "Pass Incomplete", "Sub In", "Sub Out"],
    "penalty": ["Yellow Card", "Green Card", "Red Card"]
}

# Application Branding
APP_TITLE = "TopShelf Analytics"
APP_SUBTITLE = "Professional Women's Lacrosse Performance Analytics"
APP_VERSION = "v2.0"
COPYRIGHT_TEXT = "Proprietary Software of TopShelf Analytics | TopShelf Analytics v2.0"

# UI Settings
BUTTON_HEIGHT = 60  # Large touch-friendly buttons
ACTIVE_FIELD_SIZE = 12  # Number of players allowed on field
GAME_DURATION = 60  # minutes

# Performance Thresholds (for color coding)
THRESHOLDS = {
    "shot_accuracy": {"excellent": 0.50, "good": 0.35},  # Goals/Shots
    "save_percentage": {"excellent": 0.60, "good": 0.45},  # Saves/Shots Against
    "draw_control": {"excellent": 0.60, "good": 0.45},  # Draws Won/Total Draws
    "pass_completion": {"excellent": 0.80, "good": 0.65},  # Complete/Total Passes
    "turnover_ratio": {"excellent": 0.10, "good": 0.20}  # Turnovers/Possessions (lower is better)
}

