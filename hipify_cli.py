#!/usr/bin/env python

# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import sys
import argparse
import json
from hipify import hipify_python

def main():
    parser = argparse.ArgumentParser(
        description='Top-level script for HIPifying, filling in most common parameters')
    parser.add_argument(
        '--project-directory',
        type=str,
        help="The root of the project. (default: %(default)s)")

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
        '--header-include-dirs',
        default=[],
        help="Directories to add to search path for header includes",
        required=False)

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

    parser.add_argument(
        '--dump-dict-file',
        type=str,
        help="The file to Store the return dict output after hipification",
        required=False)

    parser.add_argument(
        '--config-json',
        type=str,
        help="relative path of hipify config json which contains arguments to hipify",
        required=False)


    args = parser.parse_args()
    if(os.path.exists(args.config_json)):
        with open(args.config_json) as jsonf:
            json_args = json.load(jsonf)
            if(json_args.get('project_directory') is not None):
                project_directory = os.path.join(os.path.dirname(args.config_json), json_args['project_directory'])
            else:
                raise ValueError('relative path to project_dir to config_json should be mentioned')
            if(json_args.get('output_directory') is not None):
                output_directory = os.path.join(os.path.dirname(args.config_json), json_args['output_directory'])
            else:
                output_directory = project_directory
            if(json_args.get('includes') is not None):
                includes = json_args['includes']
            else:
                includes = ['*']
            if(json_args.get('header_include_dirs') is not None):
                header_include_dirs = json_args['header_include_dirs']
            else:
                header_include_dirs = []
            if(json_args.get('ignores') is not None):
                ignores = json_args['ignores']
            else:
                ignores = []
    else:
        if args.project_directory is not None:
            project_directory=args.project_directory;
        else:
            raise ValueError('If not using config json , project_directory should be mentioned in commadline')
        if args.output_directory:
            output_directory = args.output_directory
        else:
            output_directory = args.project_directory
        includes=args.includes
        ignores=args.ignores
        header_include_dirs=args.header_include_dirs
    dump_dict_file = args.dump_dict_file
    print("project_directory :",project_directory , " output_directory: ", output_directory, " includes: ", includes, " ignores: ", ignores, " header_include_dirs: ", header_include_dirs)

    HipifyFinalResult = hipify_python.hipify(
        project_directory=project_directory,
        output_directory=output_directory,
        includes=includes,
        ignores=ignores,
        header_include_dirs=header_include_dirs,
        is_pytorch_extension=True)

    if dump_dict_file:
        with open(dump_dict_file, 'w') as dict_file:
            dict_file.write(json.dumps(HipifyFinalResult))
    else:
        raise ValueError ('dump_dict_file should be defined')

if __name__ == "__main__":
    main()
