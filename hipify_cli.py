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
    default=None,
    help="The root of the project. (default: %(default)s)",
    required=False)

parser.add_argument(
    '--output-directory',
    type=str,
    default=None,
    help="The Directory to Store the Hipified Project",
    required=False)

parser.add_argument(
    '--list-files-only',
    action='store_true',
    help="Only print the list of hipify files.")

parser.add_argument(
    '--includes',
    default=['*'],
    help="Source files to be included for hipify",
    required=False)

parser.add_argument(
    '--ignores',
    default=[],
    help="Source files to be excluded for hipify",
    required=False)

args = parser.parse_args()
print(args)

# set directories
cwd = os.getcwd()
if args.project_directory and args.output_directory:
    proj_dir = args.project_directory
    out_dir = args.output_directory
elif args.project_directory and not args.output_directory:
    proj_dir = args.project_directory
    out_dir = proj_dir
elif not args.project_directory and args.output_directory:
    proj_dir = cwd
    out_dir = args.output_directory
else:
    proj_dir = cwd
    out_dir = cwd

# call hipify
print(proj_dir, out_dir, args.includes, args.ignores)
hipify_python.hipify(
    project_directory=proj_dir,
    output_directory=out_dir,
    includes=args.includes,
    ignores=args.ignores,
    is_pytorch_extension=True)
