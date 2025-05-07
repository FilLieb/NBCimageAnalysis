import os
from aicsimageio import AICSImage
import numpy as np
import pandas as pd
from skimage.measure import label, regionprops
from skimage.filters import threshold_otsu
from skimage.util import img_as_ubyte
from scipy.ndimage import binary_fill_holes

# Setup result storage
results = []

# Setup directories
chosen_dir = "../data/artificial"  # You can replace this with a file picker if needed

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
    image = AICSImage(filepath)
    data = image.get_image_data("TZCYX")  # Choose the correct dimension order
    print(data.shape)

    original_image_name = os.path.basename(filepath)
    just_name = os.path.splitext(original_image_name)[0]

    # Extract each channel slice (3 channels)
    t_index = 0
    z_index = 0

    Gphn = data[t_index, z_index, 0, :, :]
    vGAT = data[t_index, z_index, 1, :, :]
    BFP = data[t_index, z_index, 2, :, :]

    voxel = get_voxel_size_from_aics_image(image)

    if Gphn.max() == 0:
        abort(original_image_name, just_name, save_dir, BFP, voxel)
        return


    # Analyze Gphn
    Gphn_thresh = Gphn > threshold_otsu(Gphn)
    Gphn_labeled, Gphn_mask = analyze_particles(Gphn_thresh)
    GphnClusterNumber = len(Gphn_labeled)
    GphnClusterSize = voxel[1] * voxel[1] * np.sum([r.area for r in Gphn_labeled]) / GphnClusterNumber if GphnClusterNumber else 'NA'

    # Analyze vGAT
    vGAT_thresh = vGAT > threshold_otsu(vGAT)
    vGAT_labeled, vGAT_mask = analyze_particles(vGAT_thresh)

    # Synaptic clusters (overlap)
    overlap = np.logical_and(Gphn_mask, vGAT_mask)
    overlap_labeled, _ = analyze_particles(overlap)
    SynClusterNumber = len(overlap_labeled)

    # Cell size from BFP
    BFP_thresh = BFP > threshold_otsu(BFP)
    CellSize = voxel[1] * voxel[1] * np.sum(BFP_thresh)

    save_results(GphnClusterNumber, GphnClusterSize, SynClusterNumber, CellSize, original_image_name, just_name, save_dir)

# extract meta data, i.e. size of voxel in µm
def get_voxel_size_from_aics_image(aics_image):
    return (aics_image.physical_pixel_sizes.Z,
            aics_image.physical_pixel_sizes.Y,
            aics_image.physical_pixel_sizes.X)

# Helper function to analyze particles
def analyze_particles(binary_img):
    labeled = label(binary_img)
    regions = regionprops(labeled)
    mask = labeled > 0
    return regions, mask

# abort function, when no Gphn clusters are detected
def abort(original_image_name, just_name, save_dir, BFP, voxel):
    GphnClusterNumber = 0
    GphnClusterSize = 'NA'
    SynClusterNumber = 'NA'
    BFP_thresh = BFP > threshold_otsu(BFP)
    CellSize = voxel[1] * voxel[1] * np.sum(BFP_thresh)
    save_results(GphnClusterNumber, GphnClusterSize, SynClusterNumber, CellSize, original_image_name, just_name, save_dir)


def save_results(GphnClusterNumber, GphnClusterSize, SynClusterNumber, CellSize, image_name, just_name, save_dir):
    result = {
        'ClusterNumber': GphnClusterNumber,
        'ClusterSize': GphnClusterSize,
        'SynClusterNumber': SynClusterNumber,
        'CellSize': CellSize,
        'Cell': image_name
    }
    results.append(result)
    df = pd.DataFrame([result])
    df.to_csv(os.path.join(save_dir, f"ClusterAnalysis_{just_name}.tsv"), sep='\t', index=False)


# Run the full batch
process_files(chosen_dir)

# After processing all files, save the combined results
final_df = pd.DataFrame(results)
final_df.to_csv(os.path.join(chosen_dir, "ClusterAnalysis_All.csv"), index=False)
