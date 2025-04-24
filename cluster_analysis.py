import os
import numpy as np
import pandas as pd
from aicsimageio import AICSImage
from skimage.filters import gaussian, threshold_otsu, median
from skimage.morphology import closing, disk
from skimage.measure import label, regionprops_table
from skimage.segmentation import clear_border
from scipy.ndimage import binary_fill_holes
from skimage import img_as_ubyte
from skimage.util import img_as_bool
import tifffile as tiff

# Setup directories
chosen_dir = "data/"  # You can replace this with a file picker if needed

results = []

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".nd2"):
                full_path = os.path.join(root, file)
                print(f"Processing {full_path}")
                analyze_nd2(full_path)

def analyze_nd2(file_path):
    img = AICSImage(file_path)
    image_name = os.path.basename(file_path)
    just_name = os.path.splitext(image_name)[0]

    # Get the individual channels (assuming shape: TCZYX)
    data = img.get_image_data("CZYX", T=0)  # C x Z x Y x X

    gphn = data[0].max(axis=0)  # C1: Gphn (mScarlet)
    vgat = data[1].max(axis=0)  # C2: vGAT (e.g., GFP)
    bfp = data[2].max(axis=0)   # C3: BFP (e.g., cell fill)

    # Process Gphn channel (Difference of Gaussian)
    low = gaussian(gphn, sigma=2)
    high = gaussian(gphn, sigma=10)
    dog = low - high
    dog = dog - gaussian(dog, sigma=10)  # Subtract background

    maxima = dog > np.percentile(dog, 99.5)  # Fake Find Maxima
    gphn_mask = img_as_bool(maxima)

    # Process vGAT
    vgat_blur = gaussian(vgat, sigma=2)
    vgat_thresh = vgat_blur > threshold_otsu(vgat_blur)

    # Process BFP (cell mask)
    bfp_med = median(bfp, disk(10))
    bfp_dend = bfp_med.copy()
    bfp_thresh_1 = bfp > threshold_otsu(bfp)
    bfp_thresh_2 = bfp_dend > threshold_otsu(bfp_dend)
    bfp_mask = binary_fill_holes(bfp_thresh_1 | bfp_thresh_2)
    bfp_mask = closing(bfp_mask, disk(5))

    # Analyze particles
    gphn_labels = label(gphn_mask)
    gphn_props = regionprops_table(gphn_labels, properties=["area"])
    gphn_cluster_number = len(gphn_props["area"])
    gphn_cluster_size = np.mean(gphn_props["area"]) if len(gphn_props["area"]) > 0 else 0

    vgat_labels = label(vgat_thresh)
    vgat_props = regionprops_table(vgat_labels, properties=["area"])

    # Overlap = synaptic clusters
    overlap_mask = gphn_mask & vgat_thresh
    overlap_labels = label(overlap_mask)
    syn_cluster_number = np.max(overlap_labels)

    cell_area = np.sum(bfp_mask)

    # Store results
    results.append({
        "Cell": image_name,
        "ClusterNumber": gphn_cluster_number,
        "ClusterSize": gphn_cluster_size,
        "SynClusterNumber": syn_cluster_number,
        "CellSize": cell_area
    })

    # Optional: Save masks if needed
    # tiff.imwrite(f"{chosen_dir}/Cluster_Gphn_{just_name}.tif", img_as_ubyte(gphn_mask))
    # tiff.imwrite(f"{chosen_dir}/Cluster_vGAT_{just_name}.tif", img_as_ubyte(vgat_thresh))
    # tiff.imwrite(f"{chosen_dir}/Cluster_overlap_{just_name}.tif", img_as_ubyte(overlap_mask))
    # tiff.imwrite(f"{chosen_dir}/CellMask_{just_name}.tif", img_as_ubyte(bfp_mask))

# Run the full batch
process_directory(chosen_dir)

# Save all results to TSV
results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join(chosen_dir, "ClusterAnalysis_All.tsv"), sep="\t", index=False)