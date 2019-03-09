cmake_minimum_required(VERSION 2.8.3)
project(network_visualizer)
find_package(catkin REQUIRED)
catkin_package()
catkin_python_setup()
install(PROGRAMS scripts/open_network_visualizer
        DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

