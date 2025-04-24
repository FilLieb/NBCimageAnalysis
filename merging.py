import pandas as pd
import os

# Set the path of the folder containing the TSV files
folder_path = r'C:\Users\liebs\sciebo\Teaching\NBC2023_add_code\2_image_processor_binarize_measure'

# Get a list of all the TSV files in the folder
tsv_files = [f for f in os.listdir(folder_path) if f.endswith('.tsv')]

# Create an empty list to store the DataFrames from each file
df_list = []

# Loop through each file and read it into a DataFrame
for file in tsv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path, sep='\t')
    df_list.append(df)

# Concatenate all the DataFrames into a single DataFrame
merged_df = pd.concat(df_list)

# Save the merged DataFrame as an Excel file
excel_file = folder_path + '\merged_data.xlsx'
merged_df.to_excel(excel_file, index=False)
