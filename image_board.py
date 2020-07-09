from PIL import Image
from PIL import ImageEnhance
import make_pallete_image
import round_image
import analyze
import os


source_dir = "./source_images/"
images = os.listdir(source_dir)
images = [x for x in images if x.lower().endswith(".png")]

# Load image
image = images[1]
im = Image.open(source_dir + image)
im = im.resize((22*12, 22*12))
data = list(im.getdata())

# Make smooth & low-color image
rounded_image = round_image.roundimage(im, factor=50)
smooth_img = round_image.smoothimage(im, tolerance=50)
smooth_img = round_image.smoothimage(smooth_img, tolerance=75)

# Increase exposure of rounded image
enhancer = ImageEnhance.Brightness(smooth_img)
brightness_increase = 1.2
brightened = enhancer.enhance(brightness_increase)

# Resize and get counts
# rounded_image = rounded_image.resize((22*4, 22*4))
# smooth_img = smooth_img.resize((22*8, 22*8))
# counts = analyze.color_counts(smooth_img, roundThresh=50)
# top = analyze.color_counts(smooth_img, roundThresh=50, total=5)
brightened = brightened.resize((22*8, 22*8))
counts = analyze.color_counts(brightened, roundThresh=75)
top = analyze.color_counts(brightened, roundThresh=75, total=6)
pallete = [x[0] for x in top]
print(len(counts), len(top), (22*8)**2)
print(top)


# Make image with pallete from smooth image
# from_pallete = round_image.from_pallete(smooth_img, [x[0] for x in top])
from_pallete = round_image.from_pallete(brightened, pallete)

# Find board color
board_color = analyze.find_board_color(from_pallete)
print(f"board color is: {board_color}, {counts[board_color]}")
# Replace board color with pure white
from_pallete = round_image.replace_color(from_pallete, board_color, (255, 255, 255))

# Show images
# smooth_img.show()
brightened.show()
from_pallete.show()

# Make color pallete image for visual check
pallete = Image.new("RGB", (len(top), 1))
pallete.putdata([x[0] for x in top])
pallete.show()

