import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Apply FiveThirtyEight theme to plots
plt.style.use('fivethirtyeight')

# Sidebar menu
menu = st.sidebar.radio("Menu", ["Scouting", "Analysis", "Contact"])

# Title
st.title("Miedema Data Viewer - Arsenal Stats")

# Season selection dropdown
seasons = [f"Arsenal {year}-{year+1}" for year in range(2017, 2024)] + ["Manchester City 2024-2025"]
selected_season = st.selectbox("Choose Season", seasons)
folder_path = selected_season

# Stat type dropdown
stat_choice = st.selectbox("Choose statistic to view", ["Goals", "Passes"])

# Initialize line chart data
season_totals = []

# Layout for side-by-side display
col1, col2 = st.columns(2)

# Check if folder exists
if not os.path.exists(folder_path):
    st.error(f"Folder '{folder_path}' not found.")
else:
    goals_count = 0
    passes_count = 0

    # Loop through all CSV files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if filename.endswith(".csv"):
            try:
                df = pd.read_csv(file_path)
                # Filter for V. Miedema and count typeId
                if 'playerName' in df.columns and 'typeId' in df.columns:
                    goals_count += df[(df['playerName'] == 'V. Miedema') & (df['typeId'] == 16)].shape[0]
                    passes_count += df[(df['playerName'] == 'V. Miedema') & (df['typeId'] == 1)].shape[0]
            except Exception as e:
                st.warning(f"Could not read CSV file {filename}: {e}")

    # Get the selected stat count
    if stat_choice == "Goals":
        count = goals_count
        label = "Goals"
    else:
        count = passes_count
        label = "Passes"

    # Create circular visual using matplotlib in col1
    with col1:
        fig, ax = plt.subplots(figsize=(4, 4))
        circle = plt.Circle((0.5, 0.5), 0.4, color='#30a2da', ec='black')
        ax.add_patch(circle)
        plt.text(0.5, 0.5, str(count), fontsize=28, fontweight='bold', ha='center', va='center')
        plt.text(0.5, 0.15, label, fontsize=14, ha='center', va='center')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        st.pyplot(fig)

# Build line chart data for all seasons
line_data = []
for season in seasons:
    path = season
    g_count = 0
    p_count = 0
    if os.path.exists(path):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if filename.endswith(".csv"):
                try:
                    df = pd.read_csv(file_path)
                    if 'playerName' in df.columns and 'typeId' in df.columns:
                        g_count += df[(df['playerName'] == 'V. Miedema') & (df['typeId'] == 16)].shape[0]
                        p_count += df[(df['playerName'] == 'V. Miedema') & (df['typeId'] == 1)].shape[0]
                except:
                    continue
    line_data.append({"Season": season, "Goals": g_count, "Passes": p_count})

# Convert to DataFrame and plot line chart in col2
line_df = pd.DataFrame(line_data)
with col2:
    fig2, ax2 = plt.subplots()
    ax2.plot(line_df["Season"], line_df[stat_choice], marker='o')
    ax2.set_title(f"V. Miedema - {stat_choice} Over Seasons")
    ax2.set_ylabel(stat_choice)
    ax2.set_xlabel("Season")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig2)
