#Worked Code Last
import os
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # Hide the main window

# Open a dialog for selecting a folder
main_folder_path = filedialog.askdirectory(title="Select Folder")

print("Selected folder:", main_folder_path)



# Define patterns for matching
pattern_T_Front = r'(.*)_(T_Front\.jpg)'
pattern_N_Front = r'(.*)_(N_Front\.jpg)'
pattern_L_Front = r'(.*)_(L_Front\.jpg)'

pattern_T_Left = r'(.*)_(T_Left\.jpg)'
pattern_T_Right = r'(.*)_(T_Right\.jpg)'
pattern_T_Rear = r'(.*)_(T_Rear\.jpg)'

pattern_N_Left = r'(.*)_(N_Left\.jpg)'
pattern_N_Right = r'(.*)_(N_Right\.jpg)'
pattern_N_Rear = r'(.*)_(N_Rear\.jpg)'

pattern_L_Left = r'(.*)_(L_Left\.jpg)'
pattern_L_Right = r'(.*)_(L_Right\.jpg)'
pattern_L_Rear = r'(.*)_(L_Rear\.jpg)'

# Function to find matches and concatenate them
def get_matching_patterns(files, patterns):
    output = []
    for pattern in patterns:
        matching_files = [f for f in files if re.match(pattern, f)]
        if matching_files:
            # Remove .jpg extension
            output.append(os.path.splitext(matching_files[0])[0])
    return "~".join(output) if output else "null"

# Initialize an empty list to store the results
results = []

# Iterate over each subfolder in the main folder
for folder_name in os.listdir(main_folder_path):
    folder_path = os.path.join(main_folder_path, folder_name)
    
    if os.path.isdir(folder_path):
        # List all files in the subfolder
        files = os.listdir(folder_path)

        # Define pattern groups
        patterns_T = [pattern_T_Left, pattern_T_Right, pattern_T_Rear]
        patterns_N = [pattern_N_Left, pattern_N_Right, pattern_N_Rear]
        patterns_L = [pattern_L_Left, pattern_L_Right, pattern_L_Rear]

        # Get the concatenated results for each pattern group
        result_T = get_matching_patterns(files, patterns_T)
        result_N = get_matching_patterns(files, patterns_N)
        result_L = get_matching_patterns(files, patterns_L)

        # Combine results from all groups
        final_result = "~".join([res for res in [result_T, result_N, result_L] if res != "null"])
        final_result = final_result if final_result else "null"

        # Match front images and remove .jpg extension
        matching_pattern_T_Front = [os.path.splitext(f)[0] for f in files if re.match(pattern_T_Front, f)]
        matching_pattern_N_Front = [os.path.splitext(f)[0] for f in files if re.match(pattern_N_Front, f)]
        matching_pattern_L_Front = [os.path.splitext(f)[0] for f in files if re.match(pattern_L_Front, f)]

        # Extract thumbnail, normal_str, and large_str image names
        Thumb = matching_pattern_T_Front[0] if matching_pattern_T_Front else "null"
        normal_str = matching_pattern_N_Front[0] if matching_pattern_N_Front else "null"
        large_str = matching_pattern_L_Front[0] if matching_pattern_L_Front else "null"

        # Append the results to the list
        results.append({
            'F': folder_name,
            'Thumb': Thumb,
            'Normal': normal_str,
            'Large': large_str,
            'Left       Rear       Right    ( 2 sizes of each)': final_result
        })

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Specify the file path on Google Drive where you want to save the Excel file
file_path = 'C:/Users/KBhingradiya/OneDrive - VAN DYK BALER/Documents/folder_contents.xlsx'


# Save the DataFrame to an Excel file
df.to_excel(file_path, index=False)

print(f"Data has been saved to {file_path}")
