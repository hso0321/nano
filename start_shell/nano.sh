#!/bin/bash
 
raspi_cam="rosrun rasp_cam rasp_cam"
d435i="roslaunch realsense2_camera rs_camera.launch camera:=cam_1"
turtlebot="roslaunch turtlebot3_bringup turtlebot3_core.launch"
image_processing="rosrun vscode_test image_process_test3.py"

/bin/bash $raspi_cam&sleep 5&&$d435i&sleep 10&&$turtlebot&sleep 15&&$image_processing

pkill -9 -ef 'ros'
exit 0
