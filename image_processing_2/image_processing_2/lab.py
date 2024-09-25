"""
6.101 Lab:
Image Processing 2
"""

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
import os
from PIL import Image

#OLD FILTERS
def get_pixel(image, row, col, edge = "zero"):
    if (row < 0 or row >= image["height"] or col < 0 or col >= image["width"]):
        if (edge == "zero"): return 0
        if (edge == "wrap"): 
            newRow = row % image["height"]
            newCol = col % image["width"]
        if (edge == "extend"): 
            newRow = (image["height"]-1 if row >= image["height"] else (0 if row < 0 else row))
            newCol = (image["width"]-1 if col >= image["width"] else (0 if col < 0 else col))
        return image["pixels"] [image["width"]*(newRow) + (newCol)]
    return image["pixels"][image["width"]*row+col]

def set_pixel(image, row, col, color):
    #print(image['width'], row, col)
    #print(image['pixels'][0])
    image["pixels"][image["width"]*row+col] = color


def apply_per_pixel(image, func):
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0]*image["width"]*image["height"],
    }
    for row in range(image["height"]):
        for col in range(image["width"]):
            color = get_pixel(image, row, col)
            #print(row, col, color)
            new_color = func(color)
            set_pixel(result, row, col, new_color)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda color: 255-color)


# HELPER FUNCTIONS

def correlate(image, kernel, boundary_behavior= "extend"):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings "zero", "extend", or "wrap",
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of "zero", "extend", or "wrap", return
    None.

    Otherwise, the output of this function should have the same form as a 6.101
    image (a dictionary with "height", "width", and "pixels" keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    """
    out = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0] * image["height"]*image["width"]
    }
    for row in range(image["height"]):
        for col in range(image["width"]):
            multiply(out, image, kernel, row, col, boundary_behavior)
    
    #out = round_and_clip_image(out)
    return out
    raise NotImplementedError

def multiply(out, im, kernel, row, col, bound):
    margin = (len(kernel[0])-1)//2;
    color = 0
    for i in range(-margin, margin+1): 
        for j in range(-margin, margin+1):
            color += get_pixel(im, row+i, col+j, bound) * kernel[margin+i][margin+j]
    set_pixel(out, row, col, color)

def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the "pixels" list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    image = apply_per_pixel(image, lambda color: 255 if color > 255 else (0 if color < 0 else (round(color))))
    return image
    #raise NotImplementedError

# FILTERS

def blurred(image, kernel_size):
    """
    Return a new image representing the result of applying a box blur (with the
    given kernel size) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)

    # then compute the correlation of the input image with that kernel

    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    out = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0]*image["height"]*image["width"]
    }
    kernel = generate_blur_kernel(kernel_size)
    out = correlate(image, kernel, "extend")
    out = round_and_clip_image(out)
    return out
    raise NotImplementedError

def generate_blur_kernel(size):
    kernel = [[1/size**2]*size]*size
    #print(kernel[0][0])
    return kernel

def sharpened(image, kernel_size):
    out = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0]*image["height"]*image["width"]
    }
    kernel = generate_sharpen_kernel(kernel_size)
    out = correlate(image, kernel, "extend")
    out = round_and_clip_image(out)
    return out

def generate_sharpen_kernel(size):
    kernel = [[-1/(size**2)]*size for i in range(size)]
    mid = (size-1)//2
    kernel[mid][mid] += 2
    #print(kernel)
    return kernel

def edges_no_rounding(image):
    out = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0]*image["height"]*image["width"]
    }

    K1 = [
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ]

    K2 = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]

    O1 = correlate(image, K1)
    O2 = correlate(image, K2)
    #save_greyscale_image(O2, "test_results/cat_K2.png")
    for row in range(out["height"]):
        for col in range(out["width"]):
            color1 = get_pixel(O1, row, col)
            color2 = get_pixel(O2, row, col)
            color = math.sqrt(color1**2 + color2**2)
            set_pixel(out, row, col, color)
    return out

def edges(image):
    out = edges_no_rounding(image)
    out = round_and_clip_image(out)
    return out


# VARIOUS FILTERS

def create_image_color(h, w, color):
    im = {
        "height": h,
        "width": w,
        "pixels" : [color for _ in range(w * h)]
    }

def split(image, color):
    out = {
        "height": image["height"],
        "width": image["width"]
    }
    if color == "R":
        out["pixels"] = [image["pixels"][i][0] for i in range(image["height"]*image["width"])]
    if color == "G":
        out["pixels"] = [image["pixels"][i][1] for i in range(image["height"]*image["width"])]
    if color == "B":
        out["pixels"] = [image["pixels"][i][2] for i in range(image["height"]*image["width"])]
    
    return out

def merge(R, G, B):
    out = {
        "height": R["height"],
        "width": R["width"],
        "pixels": [(R["pixels"][i], G["pixels"][i], B["pixels"][i]) for i in range(R["height"]*R["width"])]
    }
    
    return out

def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    def color_filter(image):
        R = filt(split(image, "R"))
        G = filt(split(image, "G"))
        B = filt(split(image, "B"))
        out = merge(R, G, B)
        return out
    return color_filter


def make_blur_filter(kernel_size):
    def blur_filter (image):
        return blurred(image, kernel_size)
    return blur_filter


def make_sharpen_filter(kernel_size):
    def sharpen_filter (image):
        return sharpened(image, kernel_size)
    return sharpen_filter



def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    def filter(image):
        out = {
            "height": image["height"],
            "width": image["width"],
            "pixels": [image["pixels"][i] for i in range(image["height"]*image["width"])]
        }
        for func in filters:
            out = func(out)
        return out
    return filter


# SEAM CARVING

# Main Seam Carving Implementation


def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image. Returns a new image.
    """
    out = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [image["pixels"][i] for i in range(len(image["pixels"]))]
    }
    for i in range(ncols):
        out = single_seam_carve(out)
        print(i)
    return out
    

def single_seam_carve(image):
    cem = filter_cascade([greyscale_image_from_color_image, compute_energy, cumulative_energy_map])(image)
    seam = minimum_energy_seam(cem)
    image = image_without_seam(image, seam)
    return image

# Optional Helper Functions for Seam Carving


def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    out = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [round(.299*image["pixels"][i][0] + .587*image["pixels"][i][1] + .114*image["pixels"][i][2]) for i in range(image["height"]*image["width"])]
    }
    return out

def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    out = edges(grey)
    return out

def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    out = {
        "height": energy["height"],
        "width": energy["width"],
        "pixels": [energy["pixels"][i] for i in range(energy["height"]*energy["width"])]
    }
    for row in range(out["height"]):
        for col in range(out["width"]):
            color = get_pixel(out, row, col) + min(get_pixel(out, row-1, col-1 if col > 0 else col), get_pixel(out, row-1, col),get_pixel(out, row-1, col+1 if (col < out["width"]-1) else col))
            set_pixel(out, row, col, color)
    #print(out["pixels"][676:682])
    return out
    #raise NotImplementedError

def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    #print_matrix(cem)
    def get_1D_index(width, row, col):
        return width*row + col
    
    height = cem["height"]
    width = cem["width"]

    list = [0] * height #contains indexes of min vals
    min_bottom_value = math.inf
    min_bottom_idx = 0
    for i in range(get_1D_index(width, height-1, 0), get_1D_index(width, height-1, width)):
        if cem["pixels"][i] < min_bottom_value:
            min_bottom_value = cem["pixels"][i]
            min_bottom_idx = i
    list[height-1] = min_bottom_idx
    #print(list)
    for i in reversed(range(height-1)):
        target_idx = list[i+1]-width
        if (target_idx % width == 0):
            list[i] = target_idx if (cem["pixels"][target_idx] <= cem["pixels"][target_idx+1]) else target_idx+1
        elif ((target_idx+1) % width == 0):
            list[i] = target_idx if (cem["pixels"][target_idx] < cem["pixels"][target_idx-1]) else target_idx-1
        else:
            chunk = cem["pixels"][target_idx-1 : target_idx+2]
            selector = chunk.index(min(chunk))
            idx_min = target_idx + selector - 1
            list[i] = idx_min
            #print(i, chunk, list)

    return list
    #raise NotImplementedError

def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    seam.sort()
    #print(seam)
    out = {
        "height": image["height"],
        "width": image["width"]-1,
        "pixels": [0]*image["height"]*(image["width"]-1)
    }
    for row in range(image["height"]):
        check = 0
        for col in range(image["width"]-1):
            if (seam[row] == image["width"]*row+col):
                check = 1
            color = get_pixel(image, row, col+check)
            set_pixel(out, row, col, color)

    return out
    #raise NotImplementedError

def custom_feature(image, color, x, y, radius):
    out = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [image["pixels"][i] for i in range(image["height"]*image["width"])]
    }
    for i in range(-radius, radius):
        set_pixel(out, x+round(math.sqrt(radius**2-i**2)), y+i, color)
        set_pixel(out, x-round(math.sqrt(radius**2-i**2)), y+i, color)
    return out
# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES


def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img = img.convert("RGB")  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_color_image(image, filename, mode="PNG"):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode="RGB", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()

def print_matrix(im):
    for row in range(im["height"]):
        for col in range(im["width"]):
            digit = get_pixel(im, row, col)
            char = " " if (digit > 99) else ("  " if (digit > 9) else "   ")
            print(digit, end = char)
        print()

if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    cat = load_color_image("test_images/cat.png")
    python = load_color_image("test_images/python.png")
    sparrowchick = load_color_image("test_images/sparrowchick.png")
    twocats = load_color_image("test_images/twocats.png")
    mushroom = load_color_image("test_images/smallmushroom.png")
    chess = load_color_image("test_images/chess.png")
    stronger2 = load_color_image("test_images/stronger2.png")
    
    #color_invert_filter = color_filter_from_greyscale_filter(inverted)
    #color_blur_filter = color_filter_from_greyscale_filter(make_blur_filter(9))
    #color_sharpen_filter = color_filter_from_greyscale_filter(make_sharpen_filter(7))
    #out_python = color_blur_filter(python)
    #out_sparrowchick = color_sharpen_filter(sparrowchick)
    #save_color_image(out_python, "test_results/blurred_python.png")
    #save_color_image(out_sparrowchick, "test_results/sharpened_sparrowchick.png")
    out = custom_feature(mushroom, (0, 0, 0), 10, 10, 10)
    save_color_image(out, "test_results/circle_mushroom.png")
    
    pass
