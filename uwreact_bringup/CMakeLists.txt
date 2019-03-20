cmake_minimum_required(VERSION 2.8.3)
project(uwreact_bringup)

# Load catkin and package dependencies
find_package(catkin REQUIRED)

# Declare a catkin package
catkin_package()

# Install launch files
install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
