#!/bin/bash

roscore&rosrun vscode_test control_lane_test.py;

pkill -9 -ef 'ros'

exit 0
