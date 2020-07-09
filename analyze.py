import numpy as np
import cv2
from statistics import stdev

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


if __name__ == "__main__":
    source_path = "source_images/one.png"
    lines = square_size(source_path)


    print("MAKING LINES IMAGE")
    line_layover = cv2.imread(source_path)
    # for line in lines:
    #     x1, y1, x2, y2 = line[0]
    #     print(line[0])
    #     cv2.line(line_layover, (x1, y1), (x2, y2), (0, 0, 255), 1)
    lines = [x[0] for x in lines]
    for x1,y1,x2,y2 in linesx:
        print(x1, y1, x2, y2)
        cv2.line(line_layover, (x1,y1), (x2,y2), (0,255,0), 2)

    cv2.imshow('generated_lines', line_layover)

    # cv2.imshow("lines", lines)
    cv2.waitKey(0)
    cv2.destroyAllWindows()