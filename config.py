"""
Configuration settings for TopShelf Analytics.
Includes roster, colors, and branding.
"""

# Rutgers Branding Colors
COLORS = {
    "scarlet": "#CC0033",
    "white": "#FFFFFF",
    "grey": "#63666A",
    "dark_grey": "#333333",
    "light_grey": "#F5F5F5"
}

# Default Roster (can be updated)
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
    "#11 Sam T."
]

# Game Event Types
EVENT_TYPES = {
    "scoring": ["Goal", "Save", "Miss"],
    "possession": ["GB", "TO", "CT", "Draw"],
    "team": ["Assist", "Sub In", "Sub Out"]
}

# Application Branding
APP_TITLE = "TopShelf Analytics"
APP_SUBTITLE = "Women's Lacrosse Performance Tracking"
COPYRIGHT_TEXT = "© 2026 TopShelf Analytics"

# UI Settings
BUTTON_HEIGHT = 60  # Large touch-friendly buttons
