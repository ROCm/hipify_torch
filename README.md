# Hipify-torch

hipify-torch is a python utility to convert CUDA C/C++ code into HIP C/C++ code.
It is NOT a parser; it does a smart but basic search-and-replace based on CUDA-to-HIP mappings which are specified in the hipify-torch module.
It can also "hipify" the header include statements in your source code to ensure that it's the hipified header files that are included.

<!-- toc -->

- [Interface](#interface)
  - [Through cmake](#through-cmake)
  - [Through python](#through-python)
- [Utilities](#utilities)
  - [CMake utility function](#cmake-utility-function)
- [Intended users](#intended-users)

<!-- tocstop -->

# Interface

## Through cmake

From the parent `CMakeLists.txt` file include the `Hipify.cmake` file from `./cmake/Hipify.cmake`

### API function -- ***hipify()***

This function executes the hipify conversion logic on an input directory recursively.

```
function(hipify CUDA_SOURCE_DIR HIP_CONFIG_DIR CONFIG_FILE)
```
- Takes 3 optional arguments, either CUDA_SOURCE_DIR or CONFIG_FILE argument is required
- `CUDA_SOURCE_DIR` - Full path of input cuda source directory which needs to be hipified.
- `HIP_SOURCE_DIR` - Full path of output directory where the hipified files will be placed.
                     If not provided, it is set to CUDA_SOURCE_DIR.
- `CONFIG_FILE` - JSON format file, which provides additional arguments for hipify_cli.py file.
                  When set, it is having higher precendence over CUDA_SOURCE_DIR/HIP_SOURCE_DIR.

#### Usage examples

```
list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/hipify-torch/cmake")
include(Hipify)
# Example invocation - Provides cuda source dir and output hip source dir
hipify(CUDA_SOURCE_DIR ${PROJECT_SOURCE_DIR} HIP_SOURCE_DIR "${PROJECT_SOURCE_DIR}/hip")

# Example invocation - Only cuda source dir provide and output hip files into same dir.
hipify(CUDA_SOURCE_DIR "/home/usr/project_sources/")

# Example invocation - Through config file
hipify(CONFIG_FILE "project_hipify_config_file.json")
```
Note: Update the CMAKE_MODULE_PATH list accordingly, if the hipify-torch repo is cloned into a different directory.

Above lines trigger the hipify script for all sources & header files under the `CUDA_SOURCE_DIR`

## Through python

```
from <path to hipify-torch>.hipify.hipify_python import hipify
```
Note: We are in the process of making hipify-torch as an installable python package, then `<path to hipify-torch>` isn't required.

# Utilities

## CMake utility function

### API function -- ***get_hipified_list()***

This utility function can be used to get a list of hipified files from a list of cuda files.

```
function(get_hipified_list INPUT_LIST OUTPUT_LIST)
```
- `INPUT_LIST` - CMake list containing a list of cuda file names
- `OUTPUT_LIST` - Cmake list containing a list of hipified files names. If the cuda file name is not changed after hipify, then it is NOT replaced in the list.

#### Usage example

```
get_hipified_list("${TP_CUDA_SRCS}" TP_CUDA_SRCS)
```

Here the `TP_CUDA_SRCS` in the input list containing cuda source files and doing a inplace update with  output list `TP_CUDA_SRCS`
For the file suffix unique string, list variable name itself is passed as a string.

# Intended users

This module can be used to
- Build [PyTorch](https://github.com/pytorch/pytorch)
- PyTorch CUDA extensions such as [torchvision](https://github.com/pytorch/vision), [detectron2](https://github.com/facebookresearch/detectron2) etc.
- PyTorch submodules CMake-based such as [tensorpipe](https://github.com/pytorch/tensorpipe), etc.
- And any other repo having CUDA files requiring to hipify to build on ROCm.
