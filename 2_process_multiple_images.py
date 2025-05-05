import os
import tifffile
import numpy as np
import pandas as pd
from skimage import io, filters, measure, morphology
from skimage.measure import label, regionprops
from skimage.morphology import binary_closing
from skimage.filters import threshold_otsu
from skimage.util import img_as_ubyte
from scipy.ndimage import binary_fill_holes

# Setup result storage
results = []

# Setup directories
chosen_dir = "data/artificial"  # You can replace this with a file picker if needed

# Helper function to analyze particles
def analyze_particles(binary_img):
    labeled = label(binary_img)
    regions = regionprops(labeled)
    mask = labeled > 0
    return regions, mask

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
    image = tifffile.imread(filepath)
    if image.ndim == 5:  # Assumes image is in XYCTZ format
        image = image[:, :, :, 0, 0]  # Take the first time point and z-slice

    original_image_name = os.path.basename(filepath)
    just_name = os.path.splitext(original_image_name)[0]

    # Split channels (C1: Gphn, C2: vGAT, C3: BFP)
    Gphn = image[0]
    vGAT = image[1]
    BFP = image[2]

    if Gphn.max() == 0:
        abort(original_image_name, just_name, save_dir, BFP)
        return

    # Analyze Gphn
    Gphn_thresh = Gphn > threshold_otsu(Gphn)
    Gphn_labeled, Gphn_mask = analyze_particles(Gphn_thresh)
    GphnClusterNumber = len(Gphn_labeled)
    GphnClusterSize = np.sum([r.area for r in Gphn_labeled]) / GphnClusterNumber if GphnClusterNumber else 'NA'

    # Analyze vGAT
    vGAT_thresh = vGAT > threshold_otsu(vGAT)
    vGAT_labeled, vGAT_mask = analyze_particles(vGAT_thresh)

    # Synaptic clusters (overlap)
    overlap = np.logical_and(Gphn_mask, vGAT_mask)
    overlap_labeled, _ = analyze_particles(overlap)
    SynClusterNumber = len(overlap_labeled)

    # Cell size from BFP
    BFP_thresh = BFP > threshold_otsu(BFP)
    CellSize = np.sum(BFP_thresh)

    save_results(GphnClusterNumber, GphnClusterSize, SynClusterNumber, CellSize, original_image_name, just_name, save_dir)


def abort(original_image_name, just_name, save_dir, BFP):
    GphnClusterNumber = 0
    GphnClusterSize = 'NA'
    SynClusterNumber = 'NA'
    BFP_thresh = BFP > threshold_otsu(BFP)
    CellSize = np.sum(BFP_thresh)
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
