# Assignment 05: CUDA

The goal of the assignment is to implement a program to convert images to grayscale, also utilizing CUDA.

## Usage

The program is used by running the `main` function. It first runs the code using CPU and then using GPU.

You can modify global constants to change input and output directories:
    
    IMAGE_DIR_PATH -- Input images should be stored in this directory
    OUTPUT_DIR_PATH -- Converted images will be stored to this directory
    MAX_IMAGES -- Maximum number of images taken from the directory
    TBP_HEIGHT -- Threads per block vertically
    TBP_WIDTH  -- Threads per block horizontally

## Implementation

### Function `transform_images`

Function `transform_images` iterates through images in given directory and transforms them, utilizing other functions.
It also prints statistics.

#### Parameters:

    use_gpu -- True = use GPU, False = use CPU, boolean
    
#### Behavior:
Iterate through directory IMAGE_DIR_PATH using *iglob* from the **glob** library. For every image, read its pixels using
*pyplot.imread* from **matplotlib**. Get output pixels with `transform_to_grayscale` function. Write output to file using
*pyplot.imsave*.

Print statistics: number of images converted, total time and average time.

### Function `transform_to_grayscale`

Function `transform_to_grayscale` transforms pixels to grayscale, utilizing either `grayscale_gpu` or `grayscale_cpu` functions.
It also calculates execution time of the process.

#### Parameters:

    input_pixels -- color pixels from input image, list
    use_gpu -- True = use GPU, False = use CPU, boolean
    
#### Returns:

    out_data -- greyscale pixels in output image, list
    total_time -- execution time of function, integer

#### Behavior:
Initialize output pixels array and find out with and height of image (input array).

If use_gpu is False, simply use `grayscale_cpu` to calculate output.

If use_gpu is True, first set threads per block and blocks per grid variables, then run cuda kernel `grayscale_gpu` to calculate output.

Return output and function runtime.

### Function `grayscale_cpu`
Function `grayscale_cpu` converts pixels to grayscale sequentially, using CPU.

#### Parameters:

    in_data -- color pixels from input image, list
    out_data -- greyscale pixels in output image, list
    height -- image height = number of rows, integer
    width -- image width = number of columns, integer
    
#### Behavior:
Iterate through input pixels array and convert each pixel to grayscale using the formula defined in *Formula* segment.
Save modified pixels to output.

### Function `grayscale_gpu`
Function `grayscale_gpu` converts pixels to grayscale parallelly, using GPU.

#### Parameters:

    in_data -- color pixels from input image, numpy array
    out_data -- greyscale pixels in output image, list
    height -- image height = number of rows, integer
    width -- image width = number of columns, integer
    
#### Behavior:
Get current row and column from grid using *cuda.grid* from the **numba** library.

If row and column are in range of input pixels array, convert pixel at row and column in input pixels array to grayscale
using the formula defined in *Formula* segment.

Save modified pixel to output.

## Formula
To calculate grayscale pixels from RGB, we used the *Linear approximation of gamma compression* formula. It gives a weighted
average of RGB channels, with weights resulting from the linear approximation of gamma compression.

Formula:

    Y = 0.299*R + 0.587*G + 0.111*B
    
## Testing

### Image results
Here are 5 examples of converted images.
Original             |  Grayscale
:-------------------------:|:-------------------------:
![1](https://github.com/MatyMasaryk/Masaryk_103043_feippds/blob/05/images/image-1.jpg)  |  ![1g](https://github.com/MatyMasaryk/Masaryk_103043_feippds/blob/05/output/image-1.jpg)
![2](https://github.com/MatyMasaryk/Masaryk_103043_feippds/blob/05/images/image-2.jpg)  |  ![2g](https://github.com/MatyMasaryk/Masaryk_103043_feippds/blob/05/output/image-2.jpg)
![3](https://github.com/MatyMasaryk/Masaryk_103043_feippds/blob/05/images/image-3.jpg)  |  ![3g](https://github.com/MatyMasaryk/Masaryk_103043_feippds/blob/05/output/image-3.jpg)
![4](https://github.com/MatyMasaryk/Masaryk_103043_feippds/blob/05/images/image-4.jpg)  |  ![4g](https://github.com/MatyMasaryk/Masaryk_103043_feippds/blob/05/output/image-4.jpg)
![5](https://github.com/MatyMasaryk/Masaryk_103043_feippds/blob/05/images/image-5.jpg)  |  ![5g](https://github.com/MatyMasaryk/Masaryk_103043_feippds/blob/05/output/image-5.jpg)

### Statistics
After running program with 50 200x200 images, these are the results:

    Using CPU -> Images converted: 50, Total time: 12.007004737854004, Average time: 0.2401400947570801
    Using GPU -> Images converted: 50, Total time: 469.3261909484863, Average time: 9.386523818969726
    
GPU is slower than CPU, because we are using CUDA emulation, by adding NUMBA_ENABLE_CUDASIM=1 to enviroment variable of configuration.

Otherwise, a good GPU should use the parallelism of CUDA to run faster than the CPU. This should be especially significant
for converting larger scale images.
