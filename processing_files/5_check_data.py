import os
import matplotlib.pyplot as plt
import pandas as pd
import random

from aicsimageio import AICSImage

from skimage import filters, measure
from skimage.filters import gaussian, difference_of_gaussians
from skimage.restoration import rolling_ball
from skimage.measure import label

import numpy as np
import openpyxl

# Setup directories
chosen_dir = "../data/groups"  # You can replace this with a file picker if needed

# Process all .xlsx files in a directory recursively
def process_files(directory):
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Keep track of processed folders to avoid duplicates
    processed_folders = set()
    
    for root, _, files in os.walk(directory):
        # Skip if no .tif files or if folder already processed
        if root in processed_folders:
            continue
            
        # Get all .tif files in current folder
        tif_files = [f for f in files if f.lower().endswith('.tif')]
        
        if tif_files:  # Only process if there are .tif files
            # Select one random .tif file from the folder
            random_file = random.choice(tif_files)
            filepath_random = os.path.join(root, random_file)
            
            # Process the randomly selected image
            process_image(filepath_random, directory)
            
            # Mark this folder as processed
            processed_folders.add(root)


# Process a single image
def process_image(filepath, save_dir):
    img = AICSImage(filepath)
    data = img.get_image_data("TCZYX")  # Choose the correct dimension order

    original_name = os.path.basename(filepath)  # Gets the filename with extension
    folder_path = os.path.dirname(filepath)     # Gets the full path to the folder
    folder_name = os.path.basename(folder_path) # Gets just the folder name

    just_name = os.path.splitext(original_name)[0]

    # Pick the first timepoint and z-slice
    t_index = 0
    z_index = 0

    # Extract each channel slice (4 channels)
    map2 = data[t_index, z_index, 1, :, :]
    gphn = data[t_index, z_index, 2, :, :]

    binary_map2 = threshold_map2(map2)
    labeled_map2 = label(binary_map2)

    binary_gphn = threshold_gphn(gphn)
    labeled_gphn = label(binary_gphn)


    image_name = just_name
    word = 'Antimycin'
    if word in image_name:
        condition = 'Antimycin A'
    else:
        condition = 'CNTRL'

    make_fig(condition, folder_name, gphn, map2, binary_gphn, binary_map2)

def threshold_map2(image):
    denoised = gaussian(image, sigma=2, preserve_range=True)
    threshold = filters.threshold_otsu(denoised)
    binary_image = denoised >= threshold
    return binary_image

def threshold_gphn(image):
    background_rolling = rolling_ball(image, radius=10)
    rolling = image - background_rolling
    dog_roll = difference_of_gaussians(rolling, 1, 10)
    threshold_gphn = filters.threshold_triangle(dog_roll)
    binary_gphn = dog_roll >= threshold_gphn
    return binary_gphn

def make_fig(treat, group, gphn, map2, binary_gphn, binary_map2):

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].imshow(gphn, cmap=plt.cm.gray)
    axes[0].contour(binary_gphn, [0.5], linewidths=1.2, colors='r')
    axes[0].set_title("gephyrin")

    axes[1].imshow(map2, cmap=plt.cm.gray)
    axes[1].contour(binary_map2, [0.5], linewidths=1.2, colors='r')
    axes[1].set_title("MAP2")

    fig.suptitle(group + treat)  # Changed plt.title to fig.suptitle for better positioning
    plt.tight_layout()
    plt.show()

# Run the full batch
process_files(chosen_dir)