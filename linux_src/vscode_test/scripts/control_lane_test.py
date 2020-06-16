#!/usr/bin/python2
#-*- coding:utf-8 -*

import rospy
import numpy as np
from std_msgs.msg import Float64
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
# from darknet_ros_msgs import bounding_boxes
from darknet_ros_msgs.msg import BoundingBoxes

lasterror = 0
Max_vel = 0.12
Min_lin = 0.2
Min_ang = 2.0

# driving flags
# stop, low_vel(limit_vel), low_vel(child) high_vel, 
# default is 1
cases = [1,1,1,1]

# depth of class
# child, limit_speed, lottery, park, people, tunnel, turn_limit, turtle, unlimit, red_light, green_light
# default is 0
depth_class = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def cbFollowLane(desired_center):
    global lasterror
    center = desired_center.data
    
    error = center - 160

    Kp = 0.0025
    Kd = 0.007

    angular_z = Kp * error + Kd * (error - lasterror)
    lasterror = error

    twist = Twist()
    twist.linear.x = min(Max_vel * ((1 - abs(error) / 160) ** 2.2), Min_lin)
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = -max(angular_z , -Min_ang) if angular_z < 0 else -min(angular_z, Min_ang)
    pub_cmd_vel.publish(twist)

    print('pub cmd vel at', rospy.get_rostime().secs, rospy.get_rostime().nsecs,'\n')
    return 

def fnShutDown():
    twist = Twist()
    twist.linear.x = 0
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 0
    pub_cmd_vel.publish(twist)

    return

def depth_call_back(msg):
    # for using global_val
    global cases, depth_class

    # box number in ymax(in first box)
    for box in range(0, msg.bounding_boxes[0].ymax) :
            # save depth
            if msg.bounding_boxes[box].Class == 'child':
                depth_class[0] = msg.bounding_boxes[box].xmax
            else:
                depth_class[0] = 0
            if msg.bounding_boxes[box].Class == 'limit_speed':
                depth_class[1] = msg.bounding_boxes[box].xmax
            else:
                depth_class[1] = 0
            if msg.bounding_boxes[box].Class == 'lottery':
                depth_class[2] = msg.bounding_boxes[box].xmax
            else:
                depth_class[2] = 0
            if msg.bounding_boxes[box].Class == 'park':
                depth_class[3] = msg.bounding_boxes[box].xmax
            else:
                depth_class[3] = 0
            if msg.bounding_boxes[box].Class == 'people':
                depth_class[4] = msg.bounding_boxes[box].xmax
            else:
                depth_class[4] = 0
            if msg.bounding_boxes[box].Class == 'tunnel':
                depth_class[5] = msg.bounding_boxes[box].xmax
            else:
                depth_class[5] = 0
            if msg.bounding_boxes[box].Class == 'turn_limit':
                depth_class[6] = msg.bounding_boxes[box].xmax
            else:
                depth_class[6] = 0
            if msg.bounding_boxes[box].Class == 'turtle':
                depth_class[7] = msg.bounding_boxes[box].xmax
            else:
                depth_class[7] = 0
            if msg.bounding_boxes[box].Class == 'unlimit':
                depth_class[8] = msg.bounding_boxes[box].xmax
            else:
                depth_class[8] = 0
            if msg.bounding_boxes[box].Class == 'red_light':
                depth_class[9] = msg.bounding_boxes[box].xmax
            else:
                depth_class[9] = 0
            if msg.bounding_boxes[box].Class == 'green_light':
                depth_class[10] = msg.bounding_boxes[box].xmax
            else:
                depth_class[10] = 0
        
    # scenario
    # 1.stop people
    if depth_class[4] > 300 :
        cases[0] = 0
    else :
        cases[0] = 1

    # 2. low_vel limit_speed
    if depth_class[1] > 300 :
        cases[1] = 0
    else :
        cases[1] = 1

    # 3. low_vel child
    if depth_class[0] > 300 :
        cases[2] = 0
    else :
        cases[2] = 1

    # 4. high_vel unlimit
    if depth_class[8] > 300 :
        cases[3] = 0
    else :
        cases[3] = 1

    print("{}, {}, {}, {}".format(cases[0], cases[1], cases[2], cases[3]))

    #  for debug
    for i in range(0, len(depth_class)): 
        if depth_class[i] != 0 :
            print(depth_class[i])

    return

def cbStopLane(bool_msg):
    bool_msg = Bool()
    if bool_msg.data == True:
        fnShutDown()
    return

if __name__ == '__main__':

    rospy.init_node('control_lane')
    sub_lane = rospy.Subscriber('/detect/lane', Float64, cbFollowLane, queue_size=1)
    stop = rospy.Subscriber('/detect/stop', Bool, cbStopLane, queue_size=1)
    pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    depth_data_sub = rospy.Subscriber('/project_pub', BoundingBoxes, depth_call_back , queue_size=1)
    rospy.on_shutdown(fnShutDown)
    rospy.spin()
