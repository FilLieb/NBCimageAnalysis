# what packages are needed and install them

import importlib.metadata, subprocess, sys
required  = {'aicsimageio', 'readlif>=0.6.4', 'scikit-image'}
installed = {pkg.metadata['Name'] for pkg in importlib.metadata.distributions()}
missing   = required - installed

if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])


# load packages
from matplotlib import pyplot as plt
from aicsimageio import AICSImage
from skimage.io import imshow

# load a lif file
img = AICSImage('data/Project.lif')
data = img.get_image_data("TCZYX")  # Choose the correct dimension order
print(data.shape)

# Pick the first timepoint and z-slice
t_index = 0
z_index = 0

# Extract each channel slice (assume 3 channels, for example)
channel_0 = data[t_index, 0, z_index, :, :]
channel_1 = data[t_index, 1, z_index, :, :]
channel_2 = data[t_index, 2, z_index, :, :]
channel_3 = data[t_index, 3, z_index, :, :]

# make a quick figure to display individual channels
fig, axes = plt.subplots(1, 4, figsize=(12, 4))

axes[0].imshow(channel_0, cmap='gray')
axes[0].set_title("Channel 0")

axes[1].imshow(channel_1, cmap='gray')
axes[1].set_title("Channel 1")

axes[2].imshow(channel_2, cmap='gray')
axes[2].set_title("Channel 2")

axes[3].imshow(channel_3, cmap='gray')
axes[3].set_title("Channel 3")

plt.tight_layout()
plt.show()

# extract meta data, i.e. size of voxel in µm
def get_voxel_size_from_aics_image(aics_image):
    return (aics_image.physical_pixel_sizes.Z,
            aics_image.physical_pixel_sizes.Y,
            aics_image.physical_pixel_sizes.X)


voxel = get_voxel_size_from_aics_image(img)

print(voxel)
