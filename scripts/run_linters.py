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
Run all of our linters and CI checks to ensure we only commit quality code
"""

from __future__ import print_function

import difflib
import os
import subprocess


def install_program(program, pip=False):
    """
    Check if the specified function is installed on the system. If not, install it.
    """

    ret = subprocess.call('command -v {0} > /dev/null'.format(program), shell=True)
    if ret != 0:
        print('{0} not installed!'.format(program))
        if pip:
            print('Installing via pip...')
            ret = subprocess.call(['pip', 'install', program, '-q'])
        else:
            # -qq isn't very helpful here, since dpkg will continue to output to stdout
            # Therefore, we simply pipe stdout to /dev/null
            print('Installing via apt...')
            ret = subprocess.call(['apt', 'install', program, '-y', '--no-install-recommends'],
                                  stdout=open(os.devnull, 'w'))

    if ret != 0:
        print('Unable to find or install {0}! Aborting...'.format(program))

    return ret


def test_git_diff():
    """
    Run git diff --check
    """

    print('\n----------\n')
    print('Checking for trailing whitespace, correct EOF with git diff')
    ret = subprocess.call(['git', 'diff', '--check'])
    if ret != 0:
        print('git diff failed!')
        return 1

    print('git diff passed successfully!')
    return 0


def test_clang_format():
    """
    Check if clang-format wants to make changes
    """

    print('\n----------\n')
    print('Checking C++ code formatting with clang-format')

    # Ensure clang-format-7 is installed
    if install_program('clang-format-7') != 0:
        return 1

    # List all files to format
    files = subprocess.check_output(['find', '-L', '.', '-name', '*.h', '-o', '-name', '*.cpp'])
    files = files.decode('utf-8').strip().split('\n')
    files = [f for f in files if '.ci_config' not in f and f != '']

    changes_required = False

    # Check each file for required changes
    for filepath in files:
        with open(filepath, 'r') as f:
            unformatted = f.read()
        formatted = subprocess.check_output(['clang-format-7', '-style=file', filepath])
        if unformatted != formatted:
            changes_required = True
            print('File {0} requires changes:'.format(filepath))
            diff = difflib.unified_diff(unformatted.splitlines(), formatted.splitlines(), n=0, lineterm='')
            for line in diff:
                print('    {0}'.format(line))

    if changes_required:
        print('Code does not meet style requirements! Please run clang-format to format the code.')
        return 1

    print('clang-format passed successfully!')
    return 0


def test_clang_tidy():
    """
    Check code quality with clang-tidy
    """

    print('\n----------\n')
    print('Checking C++ code quality with clang-tidy')

    # Ensure clang-tidy-7 is installed
    if install_program('clang-tidy-7') != 0:
        return 1

    # Find the catkin workspace to run in. Default to '/root/catkin_ws', the directory used in our CI config.
    try:
        workspace = subprocess.check_output(['catkin', 'locate'], stderr=open(os.devnull, 'w'))
        workspace = workspace.decode('utf-8').strip()
        print('Using workspace {0}'.format(workspace))
    except subprocess.CalledProcessError:
        workspace = '/root/catkin_ws'
        print('Using default workspace {0}'.format(workspace))

    # Run clang-tidy
    script = os.path.dirname(os.path.abspath(__file__)) + '/run_clang_tidy.py'
    ret = subprocess.call([script, '-w', workspace, 'uwreact_robot', '--verbose'])

    if ret != 0:
        print('C++ code does not meet quality requirements!')
        return 1

    print('clang-tidy passed successfully!')
    return 0


def test_yapf():
    """
    Check if yapf wants to make changes
    """

    print('\n----------\n')
    print('Checking for python code formatting with yapf')

    # Ensure pylint is installed
    if install_program('yapf', pip=True) != 0:
        return 1

    ret = subprocess.call(['yapf', '--diff', '--recursive', '-e', '.ci_config/*', '.'])
    if ret != 0:
        print('Code does not meet style requirements! Please run yapf to format the code.')
        return 1

    print('yapf passed successfully!')
    return 0


def test_pylint():
    """
    Check code quality with pylint
    """

    print('\n----------\n')
    print('Checking for python code quality with pylint')

    # Ensure pylint is installed
    if install_program('pylint', pip=True) != 0:
        return 1

    # Find all files with extension .py or files in script dirs with no extension
    files = subprocess.check_output(['find', '.', '-name', '*.py', '-o', '-iregex', '.*/scripts/\\w+', '-type', 'f'])
    files = files.decode('utf-8').strip().split('\n')
    files = [f for f in files if '.ci_config' not in f and f != '']
    if len(files) != 0:
        ret = subprocess.call(['pylint', '--persistent', 'n', '-s', 'n'] + files)
    else:
        ret = 0

    if ret != 0:
        print('Python code does not meet quality requirements!')
        return 1

    print('pylint passed successfully!')
    return 0


def test_catkin_lint():
    """
    Run catkin_lint
    """

    print('\n----------\n')
    print('Checking for catkin files for validity')

    # Ensure pylint is installed
    if install_program('catkin_lint', pip=True) != 0:
        return 1

    # Get the parent dir of the logical working directory in order to be compatible with the CI
    parent = subprocess.check_output(['pwd', '-L']).decode('utf-8').strip()
    parent = parent.rsplit('/', 1)[0]

    ret = subprocess.call(['catkin_lint', '.', '--resolve-env', '-W1', '--quiet', '--strict', '--package-path', parent])
    if ret != 0:
        print('catkin_lint failed!')
        return 1

    print('catkin_lint passed successfully!')
    return 0


def main():
    """
    Main function
    """

    # Make sure pip is up to date
    subprocess.call(['pip', 'install', '--upgrade', 'pip', '-q'])

    fails = 0

    # Trailing whitespace, general file formatting
    fails += test_git_diff()

    # Catkin files
    fails += test_catkin_lint()

    # C++ code format
    fails += test_clang_format()

    # C++ code quality
    fails += test_clang_tidy()

    # Python code format
    fails += test_yapf()

    # Python code quality
    fails += test_pylint()

    print('\n----------------------------------------\n')

    if fails != 0:
        print('{0} checks failed!'.format(fails))
        return 1

    print('All checks passed, codebase meets requirements')
    return 0


if __name__ == '__main__':
    exit(main())
