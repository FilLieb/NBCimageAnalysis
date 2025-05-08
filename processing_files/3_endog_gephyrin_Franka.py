# what packages are needed and install them
import importlib.metadata, subprocess, sys

# Only include the packages we actually need
required = {'pyclesperanto-prototype==0.24.5', 'openpyxl'}
installed = {pkg.metadata['Name'] for pkg in importlib.metadata.distributions()}
missing = required - installed

if missing:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        # Add --no-deps flag to avoid dependency conflicts
        for package in missing:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--no-deps', package])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install packages: {e}")
        sys.exit(1)


import os
from aicsimageio import AICSImage

from skimage import filters, measure
from skimage.filters import gaussian, difference_of_gaussians
from skimage.restoration import rolling_ball
from skimage.measure import label

import pandas as pd
import numpy as np
import openpyxl

# Setup result storage
results = []

# Setup directories
chosen_dir = "../data/test"  # You can replace this with a file picker if needed

# Process all .tif files in a directory recursively
def process_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.tif'):
                filepath = os.path.join(root, file)
                print(f"Processing: {filepath}")
                process_image(filepath, directory)

# Process a single image
def process_image(filepath, save_dir):
    img = AICSImage(filepath)
    data = img.get_image_data("TCZYX")  # Choose the correct dimension order

    original_image_name = os.path.basename(filepath)
    just_name = os.path.splitext(original_image_name)[0]

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

    voxel = get_voxel_size_from_aics_image(img)

    properties_gphn = measure.regionprops(labeled_gphn, intensity_image=gphn)
    num_gphn = labeled_gphn.max()
    properties_map2 = measure.regionprops(labeled_map2, intensity_image=map2)
    map2_area_total = np.sum([p.area * voxel[1] * voxel[2] for p in properties_map2])

    statistics = {
        'area_gphn': [p.area * voxel[1] * voxel[2] for p in properties_gphn],
        'intensity_gphn': [p.mean_intensity for p in properties_gphn],
        'num_gphn': [num_gphn for p in properties_gphn],
        'area_map2_total': [map2_area_total for p in properties_gphn]
    }

    df = pd.DataFrame(statistics)
    column_mean = df.mean()

    # creating additional info
    num_gphn_per_area = column_mean['num_gphn'] / column_mean['area_map2_total']

    image_name = just_name
    word = 'CNTRL'
    if word in image_name:
        condition = 'CNTRL'
    else:
        condition = 'Antimycin A'

    result = {
        'area_gphn': [column_mean['area_gphn']],
        'intensity_gphn': [column_mean['intensity_gphn']],
        'num_gphn': [column_mean['num_gphn']],
        'area_map2_total': [column_mean['area_map2_total']],
        'num_gphn_per_area': [num_gphn_per_area],
        'image': [image_name],
        'condition': [condition]
    }

    dr = pd.DataFrame(result)

    save_results(dr, just_name, save_dir)

# extract meta data, i.e. size of voxel in µm
def get_voxel_size_from_aics_image(aics_image):
    return (aics_image.physical_pixel_sizes.Z,
            aics_image.physical_pixel_sizes.Y,
            aics_image.physical_pixel_sizes.X)

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


def save_results(result, just_name, save_dir):
    # Make sure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Append the dictionary result, not the DataFrame
    results.append(result)
    
    # Create DataFrame for individual file
    df = pd.DataFrame(result)
    output_path = os.path.join(save_dir, f"ClusterAnalysis_{just_name}.tsv")
    # Ensure the output directory for this specific file exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, sep='\t', index=False)

# Run the full batch
process_files(chosen_dir)

# After processing all files, concatenate all results
final_df = pd.concat([pd.DataFrame(r) for r in results], ignore_index=True)
final_df.to_excel(os.path.join(chosen_dir, "ClusterAnalysis_All.xlsx"), index=False)