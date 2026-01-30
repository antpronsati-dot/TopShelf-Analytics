# TopShelf Analytics

**High-performance spatial data tracking and visual shot-mapping for elite Women's Lacrosse.**

Custom-built for Rutgers Athletics to modernize live-game stat attribution and player performance insights.

## 🎯 Features

### Visual Interface
- **Interactive Shot Map**: Lacrosse field overlay with coordinate-based shot tracking
- **Plotly Charts**: High-quality, interactive data visualizations including:
  - Shot location scatter plots
  - Shooting performance bar charts
  - Action distribution pie charts
  - Player statistics tables

### Live Game Dashboard
- **Large Touch-Friendly Buttons**: Designed for iPad and tablet use during games
- **Quick Event Tracking**:
  - Ground Balls (GB)
  - Draw Controls
  - Turnovers (TO)
  - Caused Turnovers (CT)
  - Assists
  - Goals/Saves/Misses with location data
- **Real-time Statistics**: Player quick stats update instantly

### Player Management
- **Substitution Tracking**: SUB IN/SUB OUT functionality
- **On-Field Roster**: Visual display of currently active players
- **Player Selection**: Easy dropdown for selecting active player

### Analytics Dashboard
- **Game Metrics**: Total goals, shots, draw controls, ground balls
- **Player Statistics**: Comprehensive breakdown by player and action
- **Top Performers**: Leaderboards for goals, draws, and ground balls
- **Visual Charts**: Interactive Plotly visualizations

### Game Log
- **Detailed Event Log**: Complete game history with all events
- **CSV Export**: Download game data for further analysis

## 🎨 Branding

- **Color Palette**: Rutgers Scarlet (#CC0033), Grey (#63666A), and White
- **Professional Design**: Modern, clean interface with gradient headers
- **Copyright**: © 2026 TopShelf Analytics

## 🏗️ Architecture

The application is built with a clean, modular Python structure:

```
TopShelf-Analytics/
├── app.py              # Main Streamlit application
├── data_manager.py     # Game data and statistics management
├── config.py           # Configuration, roster, and constants
├── styles.py           # CSS styling and branding
├── assets/
│   └── lacrosse_field.svg  # Field diagram for shot map
└── requirements.txt    # Python dependencies
```

## 🚀 Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/antpronsati-dot/TopShelf-Analytics.git
cd TopShelf-Analytics

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📊 Usage

1. **Select Active Player**: Use the sidebar to choose the player you're tracking
2. **Record Events**: Click the large buttons to record game events
3. **Track Shots**: 
   - Adjust X/Y sliders to position the shot
   - Click "RECORD SHOT POSITION"
   - Select the result (Goal/Save/Miss)
4. **Manage Substitutions**: Use SUB IN/SUB OUT buttons in the sidebar
5. **View Analytics**: Switch to the Analytics tab for visualizations
6. **Export Data**: Download CSV from the Game Log tab

## 🔧 Customization

### Update Roster
Edit `config.py` and modify the `DEFAULT_ROSTER` list:

```python
DEFAULT_ROSTER = [
    "#12 Sarah S.",
    "#4 Julie R.",
    # Add your players here
]
```

### Customize Colors
Modify the `COLORS` dictionary in `config.py`:

```python
COLORS = {
    "scarlet": "#CC0033",
    "white": "#FFFFFF",
    "grey": "#63666A",
    # Add custom colors
}
```

## 🛠️ Technology Stack

- **Streamlit**: Web application framework
- **Plotly**: Interactive data visualizations
- **Pandas**: Data manipulation and analysis
- **Python 3.8+**: Core programming language

## 📝 Future Enhancements

- Direct click-on-field shot recording (using streamlit-plotly-events)
- Database integration for persistent storage
- Multi-game tracking and historical analysis
- Video integration and timestamp linking
- Real-time team analytics
- Advanced statistical models
- Mobile app version

## 📄 License

© 2026 TopShelf Analytics. All rights reserved.

## 👤 Author

Built for Rutgers Women's Lacrosse by antpronsati-dot

---

**Coach-Ready. Data-Driven. Championship-Focused.**
