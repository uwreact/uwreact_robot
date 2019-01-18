# uwreact_robot

[![Build Status](https://travis-ci.com/uwreact/uwreact_robot.svg?branch=master)](https://travis-ci.com/uwreact/uwreact_robot)

The software behind our fully autonomous FIRST robots

## Setup and Installation

First, clone this repo into your catkin workspace. We then use `rosinstall` and `rosdep` to install non-indexed and indexed packages respectively.

```
# Ensure rosinstall and rosdep are installed and up to date
sudo apt install python-rosinstall python-rosdep
sudo rosdep init
rosdep update

# Clone the repo
cd <workspace>/src
git clone https://github.com/uwreact/uwreact_robot.git

# Install all dependencies
rosinstall --catkin . uwreact_robot/uwreact_robot.rosinstall
rosdep install --from-paths . --ignore-src -r -y
```

## Coding Standards

For **C++** code, we mostly follow the ROS coding guidelines, with a few exceptions.
There is a `.clang_format` file that can automatically format your C++ code in the correct style.

To run the formatter, install the package `clang-format`
```
sudo apt install clang-format
```
Once the package is installed, you can run the following command:
```
cd <workspace>/src
find . -name '*.h' -or -name '*.cpp' | xargs clang-format -i -style=file $1
```

For **Python** code, we follow the PEP8 standard. Install `pycodestyle` to find any styling errors.
```
sudo pip install pycodestyle
```
To check your Python files:
```
cd <workspace>/src
find . -name '*.py' -exec pycodestyle {} \;
```

## Contributing

We facilitate a completely open source environment for all of our projects, and are always welcoming contributors.

### Contributing Guide

Before opening your editor, read this project's [contributing guide](CONTRIBUTING.md) to learn about its development and contribution process.

### License

The `uwreact_robot` project is [BSD 3-Clause licensed](LICENSE).
