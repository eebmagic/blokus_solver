from PIL import Image
import math
from tqdm import tqdm
import numpy as np
import cv2


def rounddata(inputdata, factor=20, withCounts=False):
    '''
    TODO: This should probably be refactored to round_data()
    '''
    outdata = []
    print(f"rounding with factor: {factor}")
    counts = {}
    for x in inputdata:
        new_point = []
        for y in x[:3]:
            new_point.append(y - (y % factor))
        new_point = tuple(new_point)
        
        outdata.append(new_point)
        if new_point not in counts:
            counts[new_point] = 1
        else:
            counts[new_point] += 1

    if withCounts:
        return outdata, counts
    return outdata


def roundimage(inputimage, factor=20):
    '''
    TODO: This should probably be refactored to round_image()
    '''
    inputdata = list(inputimage.getdata())
    
    newdata = rounddata(inputdata, factor)

    new_im = Image.new("RGB", inputimage.size)
    # print(newdata)
    new_im.putdata(newdata)

    return new_im


def color_distance(x, y):
    r = y[0] - x[0]
    g = y[1] - x[1]
    b = y[2] - x[2]
    
    total = (r * r) + (g * g) + (b * b)

    try:
        return math.sqrt(total)
    except ValueError as e:
        print(f"trying sqrt of: {total}")
        raise(e)


def min_diff_color_index(value, pallete):
    mindist = float('inf')
    mincolor = None

    for ind, color in enumerate(pallete):
        dist = color_distance(value, color)
        if dist < mindist:
            mindist = dist
            mincolor = ind

    return mincolor


def avg_color(colorset):
    r, g, b = 0, 0, 0
    for point in colorset:
        r += point[0]
        g += point[1]
        b += point[2]

    r = int(r / len(colorset))
    g = int(g / len(colorset))
    b = int(b / len(colorset))

    return (r, g, b)


def most_common(colorset):
    counts = {}
    m = 0
    m_point = None
    for point in colorset:
        if point in counts:
            counts[point] += 1
        else:
            counts[point] = 1

        if counts[point] > m:
            m = counts[point]
            m_point = point

    return m_point


def smoothimage(inputimage, tolerance=50, withavg=True):
    '''
    TODO: This should probably be refactored to smooth_image()
    '''
    data = list(inputimage.getdata())
    width = inputimage.size[0]

    for i in tqdm(range(len(data))):
        inds = [i-1, i+1, i-width, i+width, i-width-1, i-width+1, i+width-1, i+width+1]
        neighbors = [data[i]]
        for x in inds:
            if x >= 0 and x < len(data):
                dist = color_distance(data[i], data[x])
                if dist < tolerance:
                    neighbors.append(data[x])

        if len(neighbors) > 1:
            if withavg:
                data[i] = avg_color(neighbors)
            else:
                data[i] = most_common(neighbors)

    newim = Image.new("RGB", inputimage.size)
    newim.putdata(data)

    return newim


def nearest_option(pixel, pallete):
    m = float("inf")
    m_color = None
    for option in pallete:
        if option == pixel:
            return option
        else:
            dist = color_distance(pixel, option)
            if dist < m:
                m = dist
                m_color = option

    return m_color


def from_pallete(inputimage, pallete):
    data = list(inputimage.getdata())

    for ind, val in enumerate(data):
        data[ind] = nearest_option(val, pallete)

    newim = Image.new("RGB", inputimage.size)
    newim.putdata(data)

    return newim


def from_labeled_pallete(inputimage, data, labels, pallete):
    newdata = []
    for ind, color in enumerate(data):
        l = labels[ind]
        newdata.append(pallete[l])

    newim = Image.new("RGB", inputimage.size)
    newim.putdata(newdata)

    return newim


def replace_color(inputimage, oldcolor, newcolor):
    data = list(inputimage.getdata())
    
    newdata = []
    for point in data:
        if point[:3] == oldcolor:
            newdata.append(newcolor)
        else:
            newdata.append(point)

    newim = Image.new("RGB", inputimage.size)
    newim.putdata(newdata)

    return newim


def pil_to_cv(inputimage):
    '''
    convert PIL Image object to opencv numpy array
    '''
    cv = np.array(inputimage)
    cv = cv[:, :, ::-1].copy()

    return cv


def pull_to_board(inputimage, newcolor, size=8):

    data = list(inputimage.getdata())
    width, height = inputimage.size

    newdata = []
    for y in range(height):
        if y <= size or height-y <= size:
            newdata = newdata + ([newcolor] * width)

        else:
            for x in range(width):
                if x <= size or width-x <= size:
                    newdata.append(newcolor)
                else:
                    newdata.append(data[(y * width) + x])

    newim = Image.new("RGB", inputimage.size)
    newim.putdata(newdata)

    return newim
