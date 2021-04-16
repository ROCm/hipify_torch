# hipify-torch

hipify-torch is a python utility to convert CUDA C/C++ code into HIP C/C++ code.
It is NOT a parser; it does a smart but basic search-and-replace based on CUDA-to-HIP mappings which are specified in the hipify-torch module.
It can also "hipify" the header include statements in your source code to ensure that it's the hipified header files that are included.

# Intended users

This module can be used to build [PyTorch](https://github.com/pytorch/pytorch), as well as PyTorch CUDA extensions such as [torchvision](https://github.com/pytorch/vision), [detectron2](https://github.com/facebookresearch/detectron2) etc.
