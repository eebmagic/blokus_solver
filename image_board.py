from PIL import Image
from PIL import ImageEnhance
import round_image
import analyze
import os
from sklearn.cluster import KMeans


source_dir = "./source_images/"
images = os.listdir(source_dir)
images = [x for x in images if x.lower().endswith(".png")]

# Load image
image = images[0]
im = Image.open(source_dir + image)
im = im.resize((22*12, 22*12))
data = list(im.getdata())

# Make smooth & low-color image
smooth_img = round_image.smoothimage(im, tolerance=50)
smooth_img = round_image.smoothimage(smooth_img, tolerance=75)


# Make KMeans based labels
colors = list(smooth_img.getdata())
colors = [x[:3] for x in colors]
est = KMeans(n_clusters=5)
est.fit(colors)
labels = est.labels_

# Separate colors into groups by labels
groups = {}
for i in range(5):
    groups[i] = []

for ind, color in enumerate(colors):
    l = labels[ind]
    groups[l].append(color)

# Make pallete with average of color for each group
pallete = [None] * 5
for group in groups:
    pallete[group] = analyze.average_color(groups[group])


# Make image with pallete from smooth image
from_pallete = round_image.from_labeled_pallete(smooth_img, colors, labels, pallete)

# Find and replace board color with white
board_color = analyze.find_board_color(from_pallete)
print(f"board color is: {board_color}")
from_pallete = round_image.replace_color(from_pallete, board_color, (255, 255, 255))


# Make color pallete image for visual check
pallete_img = Image.new("RGB", (len(pallete), 1))
pallete_img.putdata(pallete)


# Show images
# rounded_image.show()
smooth_img.show()
from_pallete.show()
# pallete_img.show()

