from PIL import Image
import sys
from pathlib import Path
from tqdm import tqdm

image_PATH = None

def valid_path(inputString):
    try:
        with open(inputString) as tempfile:
            return True
    except OSError:
        print(f"###Error: invalid file path: {inputString}")
        return False


def round_pixel(inputPixel, factor=5):
    pix_list = list(inputPixel)
    new = [x - (x % factor) for x in pix_list]
    return tuple(new)


def make_pallete(data, factor=80, out_count=16):
    ## Iterate over and count colors
    counts = {}
    for pixel in tqdm(data):
        pixel = round_pixel(pixel, factor)
        if pixel not in counts:
            counts[pixel] = 1
        else:
            counts[pixel] += 1

    ## Get top colors
    top = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True)[:out_count])
    output_data = list(top.keys())
    print(output_data, top.values())
    print(f"number of entries: {len(counts)}")

    return output_data


def make_output_image(colors, save_name=None):
    # assert (len(colors) == 16), "16 colors must be passed to make output image"

    if save_name == None:
        global image_PATH
        splits = image_PATH.split(".")
        splits.append(splits[-1])
        splits[-2] = "_pallete"
        save_name = ".".join(splits)

    im = Image.new("RGB", (4, 4))
    im.putdata(colors)
    im.save(save_name)

    print(f"Saving file to: {save_name}")



if __name__ == "__main__":
    # Get the input image
    if len(sys.argv) > 1:
        for entry in sys.argv:
            if entry.split(".")[-1].lower() in ["png", "jpg"]:
                if valid_path(entry):
                    image_PATH = entry

    while image_PATH == None:
        image_PATH = input("\nDrag file here: ").strip()
        if not valid_path(image_PATH):
            image_PATH = None

    print(f"Image path is: {image_PATH}")


    ## Get the colors of the image
    source_im = Image.open(image_PATH)
    print("loading pixel data...")
    data = list(source_im.getdata())
    print("FINISHED loading data")
    # print(data)

    ## Make pallete
    output_data = make_pallete(data, factor=20)

    ## Make output image
    print("\nMaking output image")
    make_output_image(output_data)
    print("FINISHED making image")