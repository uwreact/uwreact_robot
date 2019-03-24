cmake_minimum_required(VERSION 2.8.3)
project(uwreact_description)

# Load catkin and package dependencies
find_package(catkin REQUIRED)

# Declare a catkin package
catkin_package()

# Install shared files
install(DIRECTORY config meshes urdf worlds
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
