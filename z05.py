"""This module implements image conversion to grayscale using CUDA."""

__author__ = "Maty Masaryk, Matúš Jokay, Tomáš Vavro"
__email__ = "xmasarykm1@stuba.sk"
__license__ = "MIT"

from numba import cuda
import matplotlib.pyplot as plt
import glob
import numpy as np
import time
from math import ceil

IMAGE_DIR_PATH = "images"  # Input images should be stored in this dir
OUTPUT_DIR_PATH = "output"  # Converted images will be stored to this dir
MAX_IMAGES = 100  # Maximum number of converted images
TBP_HEIGHT = 10  # Threads per block vertically
TBP_WIDTH = 10  # Threads per block horizontally


def grayscale_cpu(in_data: list, out_data: list, height: int, width: int):
    """
    Convert pixels to grayscale sequentially, using CPU.

    Parameters:
        in_data -- color pixels from input image, list
        out_data -- greyscale pixels in output image, list
        height -- image height = number of rows, integer
        width -- image width = number of columns, integer
    """
    for i in range(height):
        for j in range(width):
            # Calculate grayscale
            new_color = 0.299 * in_data[i][j][0] + \
                        0.587 * in_data[i][j][1] + \
                        0.114 * in_data[i][j][2]
            # Save to output
            out_data[i][j] = [new_color, new_color, new_color]


@cuda.jit
def grayscale_gpu(in_data: np.array, out_data: list, height: int, width: int):
    """
    Convert pixels to grayscale parallelly, using GPU.

    Parameters:
        in_data -- color pixels from input image, numpy array
        out_data -- greyscale pixels in output image, list
        height -- image height = number of rows, integer
        width -- image width = number of columns, integer
    """
    row, col = cuda.grid(2)
    if row < height and col < width:
        # Calculate grayscale
        new_color = 0.299 * in_data[row][col][0] + \
                    0.587 * in_data[row][col][1] + \
                    0.114 * in_data[row][col][2]
        # Save to output
        out_data[row][col] = [new_color, new_color, new_color]


def transform_to_grayscale(input_pixels: list, use_gpu: bool):
    """
    Transform pixels to grayscale, using either CPU or GPU.

    Calculate execution time of the process.

    Parameters:
        input_pixels -- color pixels from input image, list
        use_gpu -- True = use GPU, False = use CPU, boolean

    Returns:
        out_data -- greyscale pixels in output image, list
        total_time -- execution time of function, integer
    """
    start_time = time.time()
    height = len(input_pixels)
    width = len(input_pixels[0])
    output_pixels = input_pixels.copy()
    # Run using GPU
    if use_gpu:
        # Set threads per block
        tpb = (TBP_HEIGHT, TBP_WIDTH)
        # Set blocks per grid
        bpg = (ceil(height / tpb[0]), ceil(width / tpb[1]))
        # Run kernel
        grayscale_gpu[tpb, bpg](np.array(input_pixels),
                                output_pixels, height, width)
    # Run using CPU
    else:
        grayscale_cpu(input_pixels, output_pixels, height, width)
    end_time = time.time()
    total_time = end_time - start_time
    return output_pixels, total_time


def transform_images(use_gpu: bool):
    """
    Iterate through images in given directory and transform them.

    Print statistics.

    Parameters:
        use_gpu -- True = use GPU, False = use CPU, boolean
    """
    exec_times = []
    for i, filename in enumerate(glob.iglob(f'{IMAGE_DIR_PATH}/*')):
        # Read pixels
        pixels = plt.imread(filename)
        # Get transformed pixels
        new_pixels, runtime = transform_to_grayscale(pixels, use_gpu)
        exec_times.append(runtime)
        # Save to output file
        plt.imsave(filename.replace(IMAGE_DIR_PATH, OUTPUT_DIR_PATH),
                   new_pixels, format="jpg")
        if i > MAX_IMAGES - 2:
            break

    print(f"Using {'GPU' if use_gpu else 'CPU'} -> "
          f"Images converted: {len(exec_times)}, "
          f"Total time: {sum(exec_times)}, "
          f"Average time: {np.mean(exec_times)}")


def main():
    """
    Main function.

    Runs code using CPU, then using GPU.
    """
    # Run with CPU
    transform_images(False)
    # Run with GPU
    transform_images(True)


if __name__ == "__main__":
    main()
