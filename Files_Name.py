#Worked Code 06-06-2024
import os
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # Hide the main window

# Open a dialog for selecting a folder
main_folder_path = filedialog.askdirectory(title="Select Folder")

# Define patterns for matching
pattern_T_Front = r'(.*)_(T_Front\.jpg)'
pattern_N_Front = r'(.*)_(N_Front\.jpg)'
pattern_L_Front = r'(.*)_(L_Front\.jpg)'

pattern_T_Left = r'(.*)_(T_Left\.jpg)'
pattern_L_Left = r'(.*)_(L_Left\.jpg)'

pattern_T_Right = r'(.*)_(T_Right\.jpg)'
pattern_L_Right = r'(.*)_(L_Right\.jpg)'

pattern_T_Rear = r'(.*)_(T_Rear\.jpg)'
pattern_L_Rear = r'(.*)_(L_Rear\.jpg)'

# Function to find pairs of images and concatenate them

def get_pairs(files, t_pattern, l_pattern):
    pairs = []
    for t_file in files:
        if re.match(t_pattern, t_file):
            l_file = t_file.replace('_T_', '_L_')
            if l_file in files:
                pairs.append(f"images/{t_file}~images/{l_file}~")
    return "|".join(pairs) if pairs else "null"

# Initialize an empty list to store the results
results = []

# Iterate over each subfolder in the main folder
for folder_name in os.listdir(main_folder_path):
    folder_path = os.path.join(main_folder_path, folder_name)

    if os.path.isdir(folder_path):
        # List all files in the subfolder
        files = os.listdir(folder_path)

        # Get the concatenated results for each pattern pair
        result_Left = get_pairs(files, pattern_T_Left, pattern_L_Left)
        result_Right = get_pairs(files, pattern_T_Right, pattern_L_Right)
        result_Rear = get_pairs(files, pattern_T_Rear, pattern_L_Rear)
        
        # Combine results from all pairs, separated by "|"
        final_result = "|".join([res for res in [result_Left, result_Right, result_Rear] if res != "null"])
        final_result = final_result if final_result else "null"

        # Match front images and keep .jpg extension
        matching_pattern_T_Front = [f for f in files if re.match(pattern_T_Front, f)]
        matching_pattern_N_Front = [f for f in files if re.match(pattern_N_Front, f)]
        matching_pattern_L_Front = [f for f in files if re.match(pattern_L_Front, f)]

        # Extract thumbnail, normal_str, and large_str image names
        Thumb = matching_pattern_T_Front[0] if matching_pattern_T_Front else "null"
        normal_str = matching_pattern_N_Front[0] if matching_pattern_N_Front else "null"
        large_str = matching_pattern_L_Front[0] if matching_pattern_L_Front else "null"

        # Append the results to the list
        results.append({
            'SKU': folder_name,
            'Thumb': f"images/{Thumb}",
            'pic': f"images/{normal_str}",
            'lg_pic': f"images/{large_str}",
            'multi_pic': final_result
        })

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Specify the file path on Google Drive where you want to save the Excel file
file_path = 'C:/Users/KBhingradiya/OneDrive - VAN DYK BALER/Documents/folder_contents.xlsx'

# Save the DataFrame to an Excel file
df.to_excel(file_path, index=False)

print(f"Data has been saved to {file_path}")
