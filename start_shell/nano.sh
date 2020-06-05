
#!/bin/bash
 
raspi_cam="rosrun rasp_cam rasp_cam"
t265="roslaunch realsense2_camera rs_t265.launch camera:=cam_2 serial_no:=948422110711"
d435i="roslaunch realsense2_camera rs_camera.launch camera:=cam_1 serial_no:=923322071436"
turtlebot="roslaunch turtlebot3_bringup turtlebot3_core.launch"

/bin/bash $raspi_cam&sleep 5&&$t265&sleep 10&&$d435i&sleep 15&&$turtlebot

pkill -9 -ef 'ros'
exit 0
