cmake_minimum_required(VERSION 2.8.3)
project(network_visualizer)

# Load catkin and package dependencies
find_package(catkin REQUIRED)

# Declare a catkin package
catkin_package()

# Setup the catkin package using setup.py
catkin_python_setup()

# Install scripts
install(PROGRAMS scripts/open_network_visualizer
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
