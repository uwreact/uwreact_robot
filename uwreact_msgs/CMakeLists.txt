cmake_minimum_required(VERSION 2.8.3)
project(uwreact_msgs)

# Load catkin and package dependencies
find_package(catkin REQUIRED COMPONENTS
  message_generation
  geometry_msgs
  shape_msgs
  std_msgs
)

# List messages for generation
add_message_files(
  FILES
    EntityArray.msg
    FieldState.msg
    GenericEntity.msg
    RobotEntity.msg
)

# Generate messages with the specified dependencies
generate_messages(
  DEPENDENCIES
    geometry_msgs
    shape_msgs
    std_msgs
)

# Declare a catkin package
catkin_package(
  CATKIN_DEPENDS
    message_runtime
    geometry_msgs
    shape_msgs
    std_msgs
)
