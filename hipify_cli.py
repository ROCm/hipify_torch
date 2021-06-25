#!/usr/bin/env python

# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import sys
import argparse
from hipify import hipify_python

parser = argparse.ArgumentParser(
    description='Top-level script for HIPifying, filling in most common parameters')
parser.add_argument(
    '--project-directory',
    type=str,
    default=os.getcwd(),
    help="The root of the project. (default: %(default)s)",
    required=False)

parser.add_argument(
    '--output-directory',
    type=str,
    default=os.getcwd(),
    help="The Directory to Store the Hipified Project",
    required=False)

parser.add_argument(
    '--list-files-only',
    action='store_true',
    help="Only print the list of hipify files.")

parser.add_argument(
    '--includes',
    default=['*'],
    help="Source files to be included for hipify")
    required=False)

parser.add_argument(
    '--ignores',
    default=[],
    help="Source files to be excluded for hipify")
    required=False)

args = parser.parse_args()
print(args)

amd_build_dir = os.path.dirname(os.path.realpath(__file__))
proj_dir = os.path.join(os.path.dirname(os.path.dirname(amd_build_dir)))

if args.project_directory:
    proj_dir = args.project_directory

out_dir = proj_dir
if args.output_directory:
    out_dir = args.output_directory

hipify_python.hipify(
    project_directory=proj_dir,
    output_directory=out_dir,
    includes=args.includes,
    ignores=args.ignores,
    is_pytorch_extension=True)
