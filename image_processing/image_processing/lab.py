"""
6.101 Lab:
Image Processing
"""

import math

from PIL import Image

# NO ADDITIONAL IMPORTS ALLOWED!


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
    
def edges(image):
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
    out = round_and_clip_image(out)
    return out

# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image("test_images/cat.png")
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
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
    by the "mode" parameter.
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
    im = {
        "height": 5,
        "width": 5,
        "pixels": [35, 40, 41, 45, 50, 
                   40, 40, 42, 46, 52, 
                   42, 46, 50, 55, 55, 
                   48, 52, 56, 58, 60, 
                   56, 60, 65, 70, 75]
    }
    pixel = load_greyscale_image("test_images/centered_pixel.png")
    pigbird = load_greyscale_image("test_images/pigbird.png")
    cat = load_greyscale_image("test_images/cat.png")
    construct = load_greyscale_image("test_images/construct.png")
    
    kernel0 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    out = edges(construct)
    #out = round_and_clip_image(out)
    #print_matrix(out)
    #out1 = blurred(pixel, 3)
    #out2 = blurred(pixel, 5)
    save_greyscale_image(out, "test_results/construct_edges.png")
    #print_matrix(out)
    #print_matrix(out2)
    pass
