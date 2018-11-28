# robot 

The `robot` project contains the software behind our fully autonomous FIRST robots

## Dependency Setup

To get all required dependencies, navigate to the project root directory and run: 
```
./update_dependencies.sh
```
Put all future dependencies that DO NOT have binaries hosted on the apt repository in the dependencies.rosinstall file. Dependencies should only be listed in the dependencies.rosinstall file if they need to be built from source, else rosdep should resolve them properly (provided that they are declared properly in the package xml).

## Coding Standards
For **C++** code, we follow the ROS coding guidelines. There is a `.clang_format` file that can automatically format your C++ code in the correct style.

To run the formatter, install the package `clang-format`
```
sudo apt install clang-format
```
Once the package is installed, you can run the following command:
```
cd <folder containing repository>/Workspace/src
find . -name '*.h' -or -name '*.hpp' -or -name '*.cpp' | xargs clang-format -i -style=file $1
```

For **Python** code, we follow the PEP8 standard. Install `pycodestyle` to find any styling errors.
```
sudo pip install pycodestyle
```
To check your Python files:
```
cd <folder containing repository>/Workspace/src
find . -name '*.py' -exec pycodestyle {} \;
```

## Contributing

We facilitate a completely open source environment for all of our projects, and are always welcoming contributors.

### Contributing Guide

Before opening your editor, read this project's [contributing guide](https://github.com/uwreact/robot/blob/master/CONTRIBUTING.md) to learn about its development and contribution process.

### License

The `robot` project is [BSD 3-Clause licensed](https://github.com/uwreact/robot/blob/master/LICENSE).

