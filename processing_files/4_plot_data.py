import os
import matplotlib.pyplot as plt
import pandas as pd

# Setup directories
chosen_dir = "../data"  # You can replace this with a file picker if needed

# Process all .xlsx files in a directory recursively
def process_files(directory):
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.xlsx'):
                filepath = os.path.join(root, file)
                print(f"Processing: {filepath}")
                process_table(filepath)

# Process a single xlsx file
def process_table(filepath):
    original_name = os.path.basename(filepath)  # Gets the filename with extension
    folder_path = os.path.dirname(filepath)     # Gets the full path to the folder
    folder_name = os.path.basename(folder_path) # Gets just the folder name

    just_name = os.path.splitext(original_name)[0]

    new_name = just_name + "_" + folder_name + "_new.xlsx"
    file = pd.read_excel(filepath)
    # Use folder_path instead of filepath when joining paths
    output_path = os.path.join(chosen_dir, new_name)
    #file.to_excel(output_path, index=False)
    make_fig(folder_name, file)

def make_fig(group, table):
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))

    axes[0, 0].scatter(table['condition'], table['area_gphn'])
    axes[0, 0].set_ylabel("gephyrin area [µm^2]")

    axes[0, 1].scatter(table['condition'], table['intensity_gphn'])
    axes[0, 1].set_ylabel("gephyrin intensity [a.u.]")

    axes[1, 0].scatter(table['condition'], table['area_map2_total'])
    axes[1, 0].set_ylabel("MAP2 area [µm^2]")

    axes[1, 1].scatter(table['condition'], table['num_gphn_per_area'])
    axes[1, 1].set_ylabel("num of gephyrin clusters [µm^-2]")

    fig.suptitle(group)  # Changed plt.title to fig.suptitle for better positioning
    plt.tight_layout()
    plt.show()

process_files(chosen_dir)