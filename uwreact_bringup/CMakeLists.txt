cmake_minimum_required(VERSION 2.8.3)
project(uwreact_bringup)

# Load catkin and package dependencies
find_package(catkin REQUIRED)

# Declare a catkin package
catkin_package()

# Install config and launch files
install(DIRECTORY config launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
