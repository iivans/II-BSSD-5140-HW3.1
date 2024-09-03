from PIL import Image

def store_pixels(image):
    """Store pixel data from an image and return it as a list."""
    pixels = list(image.getdata())
    return pixels

def pixels_to_points(size, pixels, mode='RGB'):
    """Convert a list of pixel data to an image."""
    img = Image.new(mode, size)
    img.putdata(pixels)
    return img

def grayscale(image):
    """Convert an image to grayscale."""
    return image.convert('L')

def compare_pixels(px1, px2):
    """Compare two pixels."""
    return px1[0] - px2[0]  # Assuming px1 and px2 are tuples (r, g, b)
