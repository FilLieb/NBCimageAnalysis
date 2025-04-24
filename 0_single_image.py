# load packages
from matplotlib import pyplot as plt
from aicsimageio import AICSImage
from skimage.io import imshow
from skimage.filters import gaussian, threshold_otsu, median

# extract meta data, i.e. size of voxel in µm
def get_voxel_size_from_aics_image(aics_image):
    return (aics_image.physical_pixel_sizes.Z,
            aics_image.physical_pixel_sizes.Y,
            aics_image.physical_pixel_sizes.X)

# load an nd2 file
img = AICSImage('data/WT_001.nd2')
data = img.get_image_data("TCZYX")  # Choose the correct dimension order

# pick the first timepoint and z-slice
t_index = 0
z_index = 0

# Let's start working with one channel, mScarlet-gephyrin
gphn = data[t_index, 1, z_index, :, :]
voxel = get_voxel_size_from_aics_image(img)

x_dimension = data.shape[4] * voxel[1]
y_dimension = data.shape[3] * voxel[1]

print(f"length in x: {x_dimension:.2f} µm")
print(f"length in y: {y_dimension:.2f} µm")

imshow(gphn)
plt.show()

# Process Gphn channel (Difference of Gaussian)
low = gaussian(gphn, sigma=2)
high = gaussian(gphn, sigma=10)
dog = low - high

# make a quick figure to display individual channels
fig, axes = plt.subplots(1, 4, figsize=(12, 4))

axes[0].imshow(gphn, cmap='gray')
axes[0].set_title("original")

axes[1].imshow(low, cmap='gray')
axes[1].set_title("low gaussian")

axes[2].imshow(high, cmap='gray')
axes[2].set_title("high gaussian")

axes[3].imshow(dog, cmap='gray')
axes[3].set_title("difference")

plt.tight_layout()
plt.show()


dog = dog - gaussian(dog, sigma=10)  # Subtract background
