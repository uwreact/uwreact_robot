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

In order to build anything zed related, you'll also need to install CUDA 10 and the ZED SDK

### CUDA 10

[Download CUDA 10](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=1804&target_type=deblocal) and follow install instructions according to which installation method you prefer

### ZED SDK

[Download the appropriate ZED SDK](https://www.stereolabs.com/developers/release/#sdkdownloads_anchor), then to install:
```
chmod +x ZED_SDK_{YOUR VERSION}.run
./ZED_SDK_{YOUR VERSION}.run
```

## Code Style

We largely follow the ROS coding guidelines, with a few noteable exceptions. To make development easy, we provide configuration files for standard linting and static analysis tools such as [clang-format](https://clang.llvm.org/docs/ClangFormat.html), [clang-tidy](https://clang.llvm.org/extra/clang-tidy) and [yapf](https://github.com/google/yapf).

To install the linters:

```
sudo apt install clang-format-7 clang-tidy-7
pip install yapf pylint --user

# If ~/.local/bin is not on your path:
echo "PATH=\"$PATH:$HOME/.local/bin\"" >> ~/.bashrc
```

To run the formatters:

```
find . -name "*.h" -o -name "*.cpp" | xargs clang-format-7 -i -style=file
yapf -ir .
```

To run the linters:

```
./run_clang_tidy.py uwreact_robot
find . -iname "*.py" -o -iregex ".*/scripts/.*" | xargs pylint
```

## Contributing

We facilitate a completely open source environment for all of our projects, and are always welcoming contributors.

### Contributing Guide

Before opening your editor, read this project's [contributing guide](CONTRIBUTING.md) to learn about its development and contribution process.

### License

The `uwreact_robot` project is [BSD 3-Clause licensed](LICENSE).
