# robot

The `robot` project contains the software behind our fully autonomous FIRST robots

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

Before opening your editor, read this project's [contributing guide](https://github.com/uwreact/robot/blob/master/CONTRIBUTING.md) to learn about its development and contribution process.

### License

The `robot` project is [BSD 3-Clause licensed](https://github.com/uwreact/robot/blob/master/LICENSE).
