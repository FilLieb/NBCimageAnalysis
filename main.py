from matplotlib import pyplot as plt
from aicsimageio import AICSImage

img = AICSImage('data/WT_001.nd2')
data = img.get_image_data("TCZYX")  # Choose the correct dimension order
print(data.shape)

# Pick the first timepoint and z-slice
t_index = 0
z_index = 0

# Extract each channel slice (assume 3 channels, for example)
channel_0 = data[t_index, 0, z_index, :, :]
channel_1 = data[t_index, 1, z_index, :, :]
channel_2 = data[t_index, 2, z_index, :, :]


fig, axes = plt.subplots(1, 3, figsize=(12, 4))

axes[0].imshow(channel_0, cmap='gray')
axes[0].set_title("Channel 0")

axes[1].imshow(channel_1, cmap='gray')
axes[1].set_title("Channel 1")

axes[2].imshow(channel_2, cmap='gray')
axes[2].set_title("Channel 2")

plt.tight_layout()
plt.show()
