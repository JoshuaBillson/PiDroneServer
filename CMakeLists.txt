cmake_minimum_required(VERSION 3.0.2)
project(pi_drone_server)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  rospy
)


## Python Setup
catkin_python_setup()

## catkin specific configuration
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES pi_drone_server
#  CATKIN_DEPENDS geometry_msgs rospy
#  DEPENDS system_lib
)


## Specify additional locations of header files
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

## Mark executable scripts (Python etc.) for installation
catkin_install_python(PROGRAMS
  nodes/pi_drone_server
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

