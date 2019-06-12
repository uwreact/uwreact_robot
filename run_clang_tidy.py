#!/usr/bin/env python

##############################################################################
# Copyright (C) 2019, UW REACT
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of UW REACT, nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
##############################################################################

"""
A script to run clang-tidy on a ROS workspace
"""

from __future__ import print_function

import argparse
import json
import multiprocessing.pool
import subprocess
import os


def check_package(parameters):
    """
    Run clang-tidy on the specified package
    """
    args, pkg_name = parameters

    # Ensure that the specified package contains a compile_commands.json file
    cur_dir = '/'.join([args.build_dir, pkg_name])
    cur_file = '/'.join([args.build_dir, pkg_name, 'compile_commands.json'])
    if not os.path.isfile(cur_file):
        return False

    # Remove all entries from the compile_commands.json that contain 'gtest'
    all_entries = json.load(open(cur_file, 'r'))
    valid_entries = [entry for entry in all_entries if 'gtest' not in entry['directory']]
    json.dump(valid_entries, open(cur_file, 'w'))

    # Determine the output file, where required changes will be written
    output_file = '/'.join([args.ws, 'clang-tidy-fixes', pkg_name + '_fixes'])

    # Setup and run clang-tidy
    if args.fix:
        additional_args = ['-fix', '-format']
    else:
        additional_args = ['-export-fixes', output_file]

    devnull = open(os.devnull, 'w')
    subprocess.call(['run-clang-tidy-7', '-j', '8', '-p', cur_dir] + additional_args, stdout=devnull, stderr=devnull)

    # If fixing, assume that all changes were addressed and the file is now perfect
    if args.fix:
        if not args.quiet:
            print('Finished tidying ' + pkg_name)
        return_val = False

    # If not fixing, determine if required changes were found
    else:
        found_changes = os.stat(output_file).st_size != 0
        if not found_changes:
            os.remove(output_file)
            if not args.quiet:
                print('Finished checking ' + pkg_name + ', no changes required')
        else:
            if not args.quiet:
                print('Finished checking ' + pkg_name + ', changes required! See ' + output_file)
            if args.verbose:
                print(open(output_file).read())
        return_val = found_changes

    return return_val


def main():
    """
    Main function
    """

    parser = argparse.ArgumentParser(description='Wrapper for running clang-tidy on a catkin workspace.',
                                     epilog='Note: In order for clang-tidy to understand which files to tidy, ' +
                                     'the workspace must be built with -DCMAKE_EXPORT_COMPILE_COMMANDS=ON.')
    parser.add_argument('-f', '--fix', help='Attempt to automatically fix issues', action='store_true')
    parser.add_argument('-j', '--jobs', help='Number of packages to tidy concurrently (default=4)', default=4, type=int)
    parser.add_argument('-q', '--quiet', help='Do not produce any stdout output', action='store_true')
    parser.add_argument('-w', '--workspace', help='The ROS workspace containing the package', default=None)
    parser.add_argument('-v', '--verbose', help='Output generated changefiles to stdout', action='store_true')
    parser.add_argument('packages', nargs='*', help='List of packages to tidy')
    args = parser.parse_args()

    if args.verbose and args.quiet:
        print('Illegal usage, cannot set both quiet and verbose')
        exit(-1)

    # Determine the ROS workspace and build space
    if args.workspace is None:
        cwd = os.path.dirname(os.path.abspath(__file__))
    else:
        cwd = args.workspace

    try:
        args.ws = subprocess.check_output(['catkin', 'locate'], cwd=cwd).decode('utf-8').strip()
        config = subprocess.check_output(['catkin', 'config'], cwd=cwd).decode('utf-8').strip().split('\n')
        config = [c for c in config if 'Build Space:' in c][0]
        args.build_dir = '/' + config.split('/', 1)[1]
    except subprocess.CalledProcessError as error:
        print(error)
        exit(1)

    # Generate the list of packages to check
    package_list = []
    if len(args.packages) > 0:

        # Find all packages in the workspace src directory
        src_pkgs = subprocess.check_output(['find', '-L', args.ws + '/src', '-name', 'package.xml'])
        src_pkgs = src_pkgs.decode('utf-8').strip().split('\n')
        src_pkgs = [path.replace(args.ws + '/src/', '') for path in src_pkgs]
        src_pkgs = [path.replace('/package.xml', '') for path in src_pkgs]

        # Find matching packages in the workspace src directory
        src_matches = []
        for search_key in args.packages:
            src_matches.extend([pkg.split('/')[-1] for pkg in src_pkgs if search_key in pkg])

        # Find matching packages in the workspace build directory
        build_pkgs = os.listdir(args.build_dir)
        for key in src_matches:
            package_list.extend([(args, pkg) for pkg in build_pkgs if key in pkg])
    else:
        package_list = [(args, pkg) for pkg in os.listdir(args.build_dir)]

    # Create output dir
    output_dir = '/'.join([args.ws, 'clang-tidy-fixes'])
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Run clang-tidy on all matching packages
    pool = multiprocessing.pool.ThreadPool(args.jobs)
    returns = pool.map(check_package, package_list)

    if True in returns:
        if not args.quiet:
            print('Changes required')
        exit(1)
    else:
        exit(0)


if __name__ == '__main__':
    main()
