#!/usr/bin/env python
import argparse
import json
import multiprocessing.pool
import subprocess
import os


def check_package(pkg_name):
    cur_dir = '/'.join([build_dir, pkg_name])
    cur_file = '/'.join([build_dir, pkg_name, 'compile_commands.json'])
    if not os.path.isfile(cur_file):
        return False

    with open(cur_file, 'r') as f:
        parsed = json.load(f)
        valid = []

        for p in parsed:
            if 'gtest' not in p['directory']:
                valid.append(p)

    with open(cur_file, 'w') as f:
        json.dump(valid, f)

    output_dir = '/'.join([ws, 'clang-tidy-fixes'])
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    output_file = '/'.join([ws, 'clang-tidy-fixes', pkg_name + '_fixes'])
    devnull = open(os.devnull, 'w')

    if args.fix:
        additional_args = ['-fix', '-format']
    else:
        additional_args = ['-export-fixes', output_file]

    subprocess.call(['run-clang-tidy-7', '-j', '8', '-p', cur_dir] + additional_args, stdout=devnull, stderr=devnull)

    if args.fix:
        if not args.quiet:
            print('Finished tidying ' + pkg_name)
        return False
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
        return found_changes


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Wrapper for running clang-tidy on a catkin workspace.',
                                     epilog='Note: In order for clang-tidy to understand which files to tidy, ' +
                                     'the workspace must be built with -DCMAKE_EXPORT_COMPILE_COMMANDS=ON.')
    parser.add_argument('-f', '--fix', help='Attempt to automatically fix issues', action='store_true')
    parser.add_argument('-j', '--jobs', help='Number of packages to tidy concurrently (default=4)', default=4, type=int)
    parser.add_argument('-q', '--quiet', help='Do not produce any stdout output', action='store_true')
    parser.add_argument('-v', '--verbose', help='Output generated changefiles to stdout', action='store_true')
    parser.add_argument('packages', nargs='*', help='List of packages to tidy')
    args = parser.parse_args()

    if args.verbose and args.quiet:
        print('Illegal usage, cannot set both quiet and verbose')
        exit(-1)

    cwd = os.path.dirname(os.path.realpath(__file__))
    ws = subprocess.check_output(['catkin', 'locate'], cwd=cwd).decode('utf-8').strip()
    build_dir = subprocess.check_output(
        'catkin config | grep "Build Space:" | grep -o "/.*"', cwd=cwd, shell=True).decode('utf-8').strip()

    # Generate the list of packages to check
    package_list = []
    if len(args.packages) > 0:

        # Find all packages in the workspace src directory
        src_pkgs = subprocess.check_output(['find', ws + '/src', '-name',
                                            'package.xml']).decode('utf-8').strip().split('\n')
        src_pkgs = [path.replace(ws, '') for path in src_pkgs]
        src_pkgs = [path.replace('src/', '') for path in src_pkgs]
        src_pkgs = [path.replace('/package.xml', '') for path in src_pkgs]

        # Find matching packages in the workspace src directory
        src_matches = []
        for search_key in args.packages:
            src_matches.extend([pkg.split('/')[-1] for pkg in src_pkgs if search_key in pkg])

        # Find matching packages in the workspace build directory
        build_pkgs = os.listdir(build_dir)
        for key in src_matches:
            package_list.extend([pkg for pkg in build_pkgs if key in pkg])
    else:
        package_list = os.listdir(build_dir)

    pool = multiprocessing.pool.ThreadPool(args.jobs)
    returns = pool.map(check_package, package_list)

    if True in returns:
        if not args.quiet:
            print('Changes required')
        exit(1)
    else:
        exit(0)
