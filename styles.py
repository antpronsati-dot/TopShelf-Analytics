"""
CSS styling for TopShelf Analytics v2.0.
Provides professional sports analytics themed styling.
"""

def get_custom_css():
    """Returns custom CSS for the application."""
    return """
    <style>
    /* Main App Styling */
    .main {
        background-color: #F5F5F5;
    }
    
    /* Header Branding */
    .header-container {
        background: linear-gradient(135deg, #CC0033 0%, #2B2B2B 100%);
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        text-align: center;
        border: 2px solid #CC0033;
    }
    
    .header-title {
        color: white;
        font-size: 3.5em;
        font-weight: bold;
        margin: 0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        letter-spacing: 2px;
    }
    
    .header-subtitle {
        color: #F5F5F5;
        font-size: 1.3em;
        margin-top: 8px;
        font-weight: 300;
    }
    
    .version-badge {
        color: #CC0033;
        background: white;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.8em;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }
    
    /* Tile-Style Buttons */
    .stButton > button {
        width: 100%;
        height: 70px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1.2em;
        border: 3px solid #2B2B2B;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        cursor: pointer;
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        color: #2B2B2B;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.25);
        border-color: #CC0033;
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    
    /* Primary Action Buttons (Scarlet Tiles) */
    .stButton > button[kind="primary"] {
        background: linear-gradient(145deg, #CC0033, #A00028);
        color: white;
        border-color: #CC0033;
    }
    
    /* Secondary Action Buttons (Charcoal Tiles) */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(145deg, #2B2B2B, #1A1A1A);
        color: white;
        border-color: #2B2B2B;
    }
    
    /* Performance Indicators */
    .perf-green {
        color: #28A745;
        font-weight: bold;
        background-color: rgba(40, 167, 69, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
    }
    
    .perf-yellow {
        color: #FFC107;
        font-weight: bold;
        background-color: rgba(255, 193, 7, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
    }
    
    .perf-red {
        color: #DC3545;
        font-weight: bold;
        background-color: rgba(220, 53, 69, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
    }
    
    /* Metrics and Cards */
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        border-left: 6px solid #CC0033;
    }
    
    /* Player Cards */
    .player-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin: 8px 0;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #CC0033;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .player-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .player-card-active {
        background: linear-gradient(90deg, #CC0033 0%, #E6003D 100%);
        color: white;
        border-left: 5px solid #2B2B2B;
    }
    
    .player-card-bench {
        background: #F5F5F5;
        border-left: 5px solid #63666A;
    }
    
    /* Game Clock */
    .game-clock {
        background: linear-gradient(135deg, #2B2B2B, #1A1A1A);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        border: 3px solid #CC0033;
        margin-bottom: 20px;
    }
    
    .clock-label {
        font-size: 0.4em;
        color: #CC0033;
        margin-top: 5px;
    }
    
    /* Data Tables */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F5F5F5 0%, #E8E8E8 100%);
        border-right: 3px solid #CC0033;
    }
    
    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(90deg, #2B2B2B 0%, #1A1A1A 100%);
        color: white;
        text-align: center;
        padding: 12px;
        font-size: 0.9em;
        z-index: 999;
        box-shadow: 0 -4px 8px rgba(0,0,0,0.2);
        border-top: 2px solid #CC0033;
    }
    
    /* Shot Map Container */
    .shot-map-container {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.12);
        margin-bottom: 25px;
        border: 2px solid #2B2B2B;
    }
    
    /* Section Headers */
    h1, h2, h3 {
        color: #CC0033;
        border-bottom: 3px solid #CC0033;
        padding-bottom: 12px;
        font-weight: 700;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #2B2B2B;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: #F5F5F5;
        border-radius: 8px;
        color: #2B2B2B;
        font-weight: bold;
        font-size: 1.1em;
        padding: 0 30px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(145deg, #CC0033, #A00028);
        color: white;
    }
    
    /* Info Boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 6px solid #CC0033;
    }
    
    /* Quick Action Panel */
    .quick-action-panel {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 2px solid #CC0033;
        margin-bottom: 20px;
    }
    
    /* Remove extra padding at bottom for footer */
    .main .block-container {
        padding-bottom: 70px;
    }
    
    /* Performance Dashboard */
    .performance-dashboard {
        background: linear-gradient(135deg, #FFFFFF 0%, #F5F5F5 100%);
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        border: 3px solid #2B2B2B;
        margin: 15px 0;
    }
    
    .metric-row {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid #E0E0E0;
    }
    
    .metric-label {
        font-weight: bold;
        color: #2B2B2B;
    }
    
    .metric-value {
        font-size: 1.2em;
        font-weight: bold;
    }
    </style>
    """

