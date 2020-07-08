from PIL import Image
import make_pallete_image
import round_image
import analyze
import os


source_dir = "./source_images/"
images = os.listdir(source_dir)
images = [x for x in images if x.lower().endswith(".png")]

# load image
image = images[1]
im = Image.open(source_dir + image)
im = im.resize((22*12, 22*12))
data = list(im.getdata())

# make smooth & low-color image
rounded_image = round_image.roundimage(im, factor=50)
smooth_img = round_image.smoothimage(im, tolerance=50)
smooth_img = round_image.smoothimage(smooth_img, tolerance=75)

# rounded_image = rounded_image.resize((22*4, 22*4))
smooth_img = smooth_img.resize((22*8, 22*8))
counts = analyze.color_counts(smooth_img, roundThresh=50)
top = analyze.color_counts(smooth_img, roundThresh=50, total=5)
print(len(counts), len(top), (22*8)**2)
print(top)


from_pallete = round_image.from_pallete(smooth_img, [x[0] for x in top])

smooth_img.show()
from_pallete.show()

board_color = analyze.find_board_color([x[0] for x in top])
print(f"board color is: {board_color}, {counts[board_color]}")

# Make color pallete for visual check
pallete = Image.new("RGB", (len(top), 1))
pallete.putdata([x[0] for x in top])
pallete.show()

# colors = make_pallete_image.make_pallete(data, factor=20, out_count=4)
# make_pallete_image.make_output_image(colors, save_name="output.png")

# im.show()