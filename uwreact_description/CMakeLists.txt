cmake_minimum_required(VERSION 2.8.3)
project(uwreact_description)

find_package(catkin REQUIRED)

catkin_package()

install(DIRECTORY config meshes urdf worlds
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
