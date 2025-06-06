# what packages are needed and install them

import importlib.metadata, subprocess, sys
required  = {'aicsimageio', 'scikit-image', 'matplotlib'}
installed = {pkg.metadata['Name'] for pkg in importlib.metadata.distributions()}
missing   = required - installed

if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])


# load packages
from matplotlib import pyplot as plt
from aicsimageio import AICSImage
from skimage.io import imshow

# load an nd2 file
img = AICSImage('../data/tif/Lucie_condensation Sf9_WT_own_parameters_G3-Image003.tif')
data = img.get_image_data("TZCYX")  # Choose the correct dimension order
print(data.shape)

# Pick the first timepoint and z-slice
t_index = 0
z_index = 0

# Extract each channel slice (assume 3 channels, for example)
channel_0 = data[t_index, 0, z_index, :, :]
channel_1 = data[t_index, 1, z_index, :, :]


# make a quick figure to display individual channels
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].imshow(channel_0, cmap='gray')
axes[0].set_title("Channel 0")

axes[1].imshow(channel_1, cmap='gray')
axes[1].set_title("Channel 1")

plt.tight_layout()
plt.show()

# extract meta data, i.e. size of voxel in µm
def get_voxel_size_from_aics_image(aics_image):
    return (aics_image.physical_pixel_sizes.Z,
            aics_image.physical_pixel_sizes.Y,
            aics_image.physical_pixel_sizes.X)


voxel = get_voxel_size_from_aics_image(img)

print(voxel)
