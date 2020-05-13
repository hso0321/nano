#!/bin/bash

roscore&rosrun turtlebot3_teleop turtlebot3_teleop_key;

pkill -9 -ef 'ros'

exit 0
