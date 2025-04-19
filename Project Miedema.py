import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
            except Exception as e:
                st.warning(f"Could not read file {filename}: {e}")

    # Display results
    if miedema_lines:
        df = pd.DataFrame(miedema_lines)
        st.dataframe(df)
    else:
        st.info("No lines found containing 'Miedema'.")
