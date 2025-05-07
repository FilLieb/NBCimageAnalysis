# load packages
from matplotlib import pyplot as plt
from aicsimageio import AICSImage
from skimage.io import imshow
from skimage import filters
from skimage.filters import gaussian, median
import numpy as np

# extract meta data, i.e. size of voxel in µm
def get_voxel_size_from_aics_image(aics_image):
    return (aics_image.physical_pixel_sizes.Z,
            aics_image.physical_pixel_sizes.Y,
            aics_image.physical_pixel_sizes.X)

# load an nd2 file
img = AICSImage('../data/nd2/WT_001.nd2')
data = img.get_image_data("TCZYX")  # Choose the correct dimension order

# pick the first timepoint and z-slice
t_index = 0
z_index = 0

# Let's start working with one channel, vGAT
vGAT = data[t_index, 1, z_index, :, :]
voxel = get_voxel_size_from_aics_image(img)

threshold = filters.threshold_otsu(vGAT)
binary_image = vGAT >= threshold


def sub_to_zero(a, b):
    return np.maximum(a - b, 0)

def diff_of_gauss(image, sigma_l, sigma_h):
    low = gaussian(image, sigma=sigma_l, preserve_range=True)
    high = gaussian(image, sigma=sigma_h, preserve_range=True)
    return sub_to_zero(low,high)

denoised = diff_of_gauss(vGAT, 1, 15)


threshold = filters.threshold_otsu(denoised)
binary_image_denoised = vGAT >= threshold

denoised = median(vGAT)

threshold = filters.threshold_otsu(denoised)
binary_image_denoised = vGAT >= threshold


imshow(binary_image_denoised)
plt.show()
