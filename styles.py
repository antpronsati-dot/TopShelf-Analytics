"""
CSS styling for TopShelf Analytics.
Provides professional Rutgers-themed styling.
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
        background: linear-gradient(135deg, #CC0033 0%, #8B0025 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .header-title {
        color: white;
        font-size: 3em;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        color: #F5F5F5;
        font-size: 1.2em;
        margin-top: 5px;
    }
    
    /* Large Touch-Friendly Buttons */
    .stButton > button {
        width: 100%;
        height: 60px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.1em;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Primary Action Buttons (Scarlet) */
    .stButton > button[kind="primary"] {
        background-color: #CC0033;
        color: white;
    }
    
    /* Secondary Action Buttons */
    .stButton > button[kind="secondary"] {
        background-color: #63666A;
        color: white;
    }
    
    /* Metrics and Cards */
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 4px solid #CC0033;
    }
    
    /* Data Tables */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: white;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #F5F5F5;
        border-right: 2px solid #CC0033;
    }
    
    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #333333;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 0.9em;
        z-index: 999;
        box-shadow: 0 -2px 4px rgba(0,0,0,0.1);
    }
    
    /* Shot Map Container */
    .shot-map-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Section Headers */
    h2, h3 {
        color: #CC0033;
        border-bottom: 2px solid #CC0033;
        padding-bottom: 10px;
    }
    
    /* Info Boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #CC0033;
    }
    
    /* Radio Buttons */
    .stRadio > label {
        font-weight: bold;
        color: #333333;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: white;
        border-radius: 10px;
        border: 2px solid #CC0033;
    }
    
    /* Remove extra padding at bottom for footer */
    .main .block-container {
        padding-bottom: 60px;
    }
    </style>
    """
