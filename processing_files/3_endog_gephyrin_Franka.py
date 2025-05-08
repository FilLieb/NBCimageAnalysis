import os
from aicsimageio import AICSImage

from skimage import filters, measure
from skimage.filters import gaussian, difference_of_gaussians
from skimage.restoration import rolling_ball
from skimage.measure import label

import pandas as pd
import numpy as np

# Setup result storage
results = []

# Setup directories
chosen_dir = "../data/group3"  # You can replace this with a file picker if needed

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

    series = pd.Series([just_name])
    index = ['image']
    series.index = index
    w_name = pd.concat([column_mean, series])
    save_results(w_name, just_name, save_dir)

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

    results.append(result)
    df = pd.DataFrame([result])
    output_path = os.path.join(save_dir, f"ClusterAnalysis_{just_name}.tsv")
    # Ensure the output directory for this specific file exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, sep='\t', index=False)


# Run the full batch
process_files(chosen_dir)

# After processing all files, save the combined results
final_df = pd.DataFrame(results)
final_df.to_csv(os.path.join(chosen_dir, "ClusterAnalysis_All.csv"), index=False)
