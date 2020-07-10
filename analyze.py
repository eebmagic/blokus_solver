from PIL import Image
from PIL import ImageFilter
import numpy as np
import cv2
from statistics import stdev
import round_image

def square_size(imagepath):
    im = cv2.imread(imagepath)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    print("processing lines...")
    # lines = cv2.HoughLines(gray, 1, np.pi / 180, 100)
    lines = cv2.HoughLinesP(gray,1,np.pi/180,100,10,1000)
    # print(lines)
    return lines


def round_pixel(pixel, roundThresh):
    r, g, b = pixel
    r = r - (r % roundThresh)
    g = g - (g % roundThresh)
    b = b - (b % roundThresh)
    return tuple((r, g, b))


def color_counts(inputimage, roundThresh=10, total=None):
    data = list(inputimage.getdata())

    counts = {}
    for point in data:
        point = round_pixel(point, roundThresh)
        if point not in counts:
            counts[point] = 1
        else:
            counts[point] += 1

    if not total:
        return counts
    else:
        top = sorted(counts.items(), key=lambda x: x[1])[-total:]
        return top[::-1]


def find_board_color(inputimage):
    '''
    Board color is probably the color that makes up the longest consecutive line of pixels
    '''
    data = list(inputimage.getdata())
    
    longestColor = None
    maxlen = 0
    lastColor = data[0]
    count = 0
    for point in data:
        if point == lastColor:
            count += 1
        else:
            # update if longer
            if count > maxlen:
                longestColor = lastColor
                maxlen = count
            
            # reset
            count = 1
            lastColor = point

    return longestColor[:3]


def average_color(colorset):
    r = 0
    g = 0
    b = 0
    for x, y, z in colorset:
        r += x
        g += y
        b += z

    r //= len(colorset)
    g //= len(colorset)
    b //= len(colorset)

    return (r, g, b)


def make_palletestring(pallete):
    output = ""
    presets = [(255, 255, 255), (39, 34, 129), (168, 32, 45), (205, 177, 39), (9, 136, 93)]

    for color in pallete:
        closest = round_image.min_diff_color_index(color, presets)
        output += "0bryg"[closest]

    return output


def make_boardstring(inputimage, pallete):
    # Resize to be closer to board dimensions
    cellsize = 9
    resized = inputimage.resize((20*cellsize, 20*cellsize))
    data = list(resized.getdata())
    width, height = resized.size

    output = ""
    pallete_string = make_palletestring(pallete)
    for y in range(20):
        for x in range(20):
            ind = (((y * cellsize) + (cellsize//2)) * width) + (x * cellsize) + (cellsize//2)

            curr_color = data[ind]
            char = pallete_string[round_image.min_diff_color_index(curr_color, pallete)]
            output += char

            data[ind] = (0, 0, 0)

        if y != 19:
            output += "\n"

    # Temp image for debug
    sampled = Image.new("RGB", resized.size)
    sampled.putdata(data)
    # sampled.show()

    # inputimage.show()
    # resized.show()

    return output.strip()


if __name__ == "__main__":
    path = "example_boards/cropped_example.png"
    im = Image.open(path)

    # blur image
    im = im.filter(ImageFilter.GaussianBlur(radius=2))

    # quick make pallete
    data = list(im.getdata())
    pallete = []
    for point in data:
        if point not in pallete:
            pallete.append(point[:3])

    # Make outputstring
    outstring = make_boardstring(im, pallete)

    # Make Board from string
    from board import Board
    b = Board()
    b.load(outstring)
    b.show()
