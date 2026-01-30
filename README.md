# TopShelf-Analytics
TopShelf Analytics: High-performance spatial data tracking and visual shot-mapping for elite Women's Lacrosse. Custom-built for Rutgers Athletics to modernize live-game stat attribution and player performance insights.

## 🚀 How to Open and Run app.py

### Prerequisites
- Python 3.7 or higher installed on your system
- pip (Python package manager)

### Installation & Setup

1. **Clone or download this repository** (if you haven't already)
   ```bash
   git clone https://github.com/antpronsati-dot/TopShelf-Analytics.git
   cd TopShelf-Analytics
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application**
   ```bash
   streamlit run app.py
   ```

4. **View the app in your browser**
   - The app will automatically open in your default web browser
   - If it doesn't open automatically, look for the URL in the terminal (usually `http://localhost:8501`)
   - Copy and paste the URL into your web browser

### Usage
Once the app is running, you can:
- Select active players from the sidebar roster
- Track shots, goals, saves, and misses on the interactive shot chart
- Record ground balls, turnovers, caused turnovers, and assists
- View live game statistics and shooting efficiency charts
- Clear data at the end of the game

### Troubleshooting
- **Port already in use?** Try: `streamlit run app.py --server.port 8502`
- **Module not found?** Make sure you've installed requirements: `pip install -r requirements.txt`
- **Python not found?** Install Python from [python.org](https://www.python.org/downloads/)
