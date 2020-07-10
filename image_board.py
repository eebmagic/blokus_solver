from PIL import Image
from PIL import ImageEnhance
import os
from sklearn.cluster import KMeans

import round_image
import analyze
import trimmer
from board import Board


source_dir = "./source_images/"
images = os.listdir(source_dir)
images = [x for x in images if x.lower().endswith(".png")]

# Load image
image = images[2]
im = Image.open(source_dir + image)
im = im.resize((22*12, 22*12))
data = list(im.getdata())

# Make smooth & low-color image
print("Smoothing image...")
smooth_img = round_image.smoothimage(im, tolerance=50)
print("Smoothing image again...")
smooth_img = round_image.smoothimage(smooth_img, tolerance=75)

# Make KMeans based labels
print("Doing KMeans calculations...")
colors = list(smooth_img.getdata())
colors = [x[:3] for x in colors]
est = KMeans(n_clusters=5)
est.fit(colors)
labels = est.labels_

# Separate colors into groups by labels
print("Separating colors and making pallete...")
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
print("Making palleted image...")
from_pallete = round_image.from_labeled_pallete(smooth_img, colors, labels, pallete)

# Find and replace board color with white
print("Determining board color...")
board_color = analyze.find_board_color(from_pallete)
print(f"\tBoard color is: {board_color}")
from_pallete = round_image.replace_color(from_pallete, board_color, (255, 255, 255))

# Fix and crop out edges
print("Cropping image...")
fixed = round_image.pull_to_board(from_pallete, (255, 255, 255))
cropped = trimmer.full_clean(fixed)

# Make board string and board
board_string = analyze.make_boardstring(cropped, pallete)
board = Board()
board.load(board_string)

######################################################
print("Displaying generated images...")
# Make color pallete image for visual check
pallete_img = Image.new("RGB", (len(pallete), 1))
pallete_img.putdata(pallete)

# Show images
im.show()
# rounded_image.show()
# smooth_img.show()
# from_pallete.show()
# fixed.show()
cropped.show()
board.show()
# print(pallete)
# pallete_img.show()