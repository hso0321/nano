#!/bin/bash

rosrun jetbot_ros jetbot_camera& #라즈베리파이 카메라
roslaunch realsense2_camera rs_t265.launch camera:=cam_2 serial_no:=000094842211071&	#T265
roslaunch realsense2_camera rs_camera.launch camera:=cam_1 serial_no:=923322071436&	#d435i
roslaunch turtlebot3_bringup turtlebot3_core.launch&	#turtlebot(opencv보드, 모터)
