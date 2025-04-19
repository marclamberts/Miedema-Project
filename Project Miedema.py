import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Apply FiveThirtyEight theme to plots
plt.style.use('fivethirtyeight')

# Title
st.title("Miedema Data Viewer - Arsenal 2017/2018")

# Folder path
folder_path = "Arsenal 2017-2018"

# Check if folder exists
if not os.path.exists(folder_path):
    st.error(f"Folder '{folder_path}' not found.")
else:
    miedema_lines = []
    goals_count = 0
    assists_count = 0

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Only process text or CSV files
        if filename.endswith(".txt") or filename.endswith(".csv"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        if "Miedema" in line:
                            miedema_lines.append({"filename": filename, "line": line.strip()})

                            # Try to parse line as JSON and count goals/assists
                            try:
                                data = json.loads(line)
                                if data.get("typeId") == 16:
                                    goals_count += 1
                                elif data.get("typeId") == 15:
                                    assists_count += 1
                            except:
                                pass
            except Exception as e:
                st.warning(f"Could not read file {filename}: {e}")

    # Display results
    if miedema_lines:
        df = pd.DataFrame(miedema_lines)
        st.dataframe(df)

        # Dropdown menu for stat type
        stat_choice = st.selectbox("Choose statistic to view", ["Goals", "Assists"])

        # Get the selected stat count
        if stat_choice == "Goals":
            count = goals_count
            label = "Goals"
        else:
            count = assists_count
            label = "Assists"

        # Create circular visual using matplotlib
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

    else:
        st.info("No lines found containing 'Miedema'.")
