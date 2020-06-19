#!/usr/bin/python2
#-*- coding:utf-8 -*

import rospy
import numpy as np
from std_msgs.msg import Float64
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
from darknet_ros_msgs.msg import BoundingBoxes

lasterror = 0
# max_vel = 0.12 # 왜 최저속도보다 낮은가?
max_vel = 0.12
min_lin = 0.2

min_ang = 2.0
# min_ang = 4.0
vertical_flag = 0

# driving flags
# default is 1
# turn_limit, limit_speed, child, unlimit, lottery, turnel
cases_static = [1,1,1,1,1,1]
# people, turtle, red_light(traffic), green(traffic)
cases_dynamic= [1,1,1,1]

# for buffer effect index
idx = 0
buf_div = 30        


def cbFollowLane(desired_center):
    global lasterror, max_vel, min_ang, min_lin
    global cases_static, cases_dynamic, vertical_flag
    center = desired_center.data

    if vertical_flag == 1:
        print('find horizon line')
        if cases_dynamic[2] == 0:      # red light
            fnShutDown()
        elif cases_dynamic[3] == 0:     # green light
            fnShutDown()       # 강제 직진
        elif cases_dynamic[1] == 0:     # turtle bot
            fnShutDown()       # 회피기동
        elif cases_static[0] == 0:  # 우회전 금지
            fnShutDown()       # 강제 직진
        elif cases_static[4] == 0:  # 로터리
            fnShutDown()       # 강제 직진
    else:
        if cases_dynamic[0] == 0:       # find people
            print('meet people!')
            fnShutDown()
        elif cases_static[1] == 0:      # limit low_vel
            print('limit lowest_vel!')
            max_vel=0.24
            min_lin= 0.4
            fnDrive(center)
        elif cases_static[2] == 0:      # children zone
            print('children zone')
            # max_vel = 0.06[855, 431, 0, 0, 0, 0, 0, 0, 587, 0, 0]
            # min_lin = 0.1
            # fnDrive(center)
            fnShutDown()
        elif cases_static[5] == 0:      # turnnel
            pass            # 터널 강제기동

        elif cases_static[3] == 0:     # unlimit
            max_vel = 0.12
            min_lin = 0.2
            fnDrive(center)
            print('To origin setting!')
        else:
            print('just drive!')
            fnDrive(center)
        
    return 


def fnDrive(center):
    global lasterror, max_vel, min_lin, min_ang



    error = center - 160

    # Kp = 0.0025
    Kp = 0.005
    Kd = 0.007

    angular_z = Kp * error + Kd * (error - lasterror)
    lasterror = error

    twist = Twist()
    twist.linear.x = min(max_vel * ((1 - abs(error) / 160) ** 2.2), min_lin)
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = -max(angular_z , -min_ang) if angular_z < 0 else -min(angular_z, min_ang)
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
    global idx, buf_div

    # depth of class
    # child, limit_speed, lottery, park, people, tunnel, turn_limit, turtle, unlimit, red_light, green_light
    # default is 0
    depth_class = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # for buffer effect
    div = idx % buf_div

    # for using global_val
    global cases_static, cases_dynamic

    for box in range(0, 11):
        depth_class[box] = 0

    # box number in ymax(in first box)
    if div == 29 :
        for box in range(0, msg.bounding_boxes[0].ymax) :
            # save depth
            if msg.bounding_boxes[box].Class == 'child':
                depth_class[0] = msg.bounding_boxes[box].xmax
            elif msg.bounding_boxes[box].Class == 'limit_speed':
                depth_class[1] = msg.bounding_boxes[box].xmax
            elif msg.bounding_boxes[box].Class == 'lottery':
                depth_class[2] = msg.bounding_boxes[box].xmax
            elif msg.bounding_boxes[box].Class == 'park':
                depth_class[3] = msg.bounding_boxes[box].xmax
            elif msg.bounding_boxes[box].Class == 'people':
                depth_class[4] = msg.bounding_boxes[box].xmax
            elif msg.bounding_boxes[box].Class == 'tunnel':
                depth_class[5] = msg.bounding_boxes[box].xmax
            elif msg.bounding_boxes[box].Class == 'turn_limit':
                depth_class[6] = msg.bounding_boxes[box].xmax
            elif msg.bounding_boxes[box].Class == 'turtle':
                depth_class[7] = msg.bounding_boxes[box].xmax
            elif msg.bounding_boxes[box].Class == 'unlimit':
                depth_class[8] = msg.bounding_boxes[box].xmax
            elif msg.bounding_boxes[box].Class == 'red_light':
                depth_class[9] = msg.bounding_boxes[box].xmax
            elif msg.bounding_boxes[box].Class == 'green_light':
                depth_class[10] = msg.bounding_boxes[box].xmax

    print(depth_class)
        
    # scenario
    # static

    # 1.turn_limit
    if 280 < depth_class[4] <= 320 :
        cases_static[0] = 0
    
    # 2.limit_speed
    if 280 < depth_class[1] <= 320 :
        cases_static[1] = 0

    # 3.child
    if 280 < depth_class[0] <= 320 :
        cases_static[2] = 0

    # 4.unlimit
    if 280 < depth_class[8] <= 320 :
        cases_static[3] = 0

    # 5.lottery
    if 280 < depth_class[2] <= 320 :
        cases_static[4] = 0

    # 6.turnel
    if 280 < depth_class[5] <= 320 :
        cases_static[5] = 0

    # dynamic

    # 1.people
    if 280 < depth_class[4] <= 320 :
        cases_dynamic[0] = 0
    else :
        cases_dynamic[0] = 1

    # 2.turtle
    if 280 < depth_class[7] <= 320 :
        cases_dynamic[1] = 0
    else :
        cases_dynamic[1] = 1

    # 3.red_light(taffic)
    if 280 < depth_class[9] <= 320 :
        cases_dynamic[2] = 0
    else :
        cases_dynamic[2] = 1

    # 4.green_light(traffic)
    if 280 < depth_class[10] <= 320 :
        cases_dynamic[3] = 0
    else :
        cases_dynamic[3] = 1
    
    print("cases_static = {}, {}, {}, {}, {}, {}".format(cases_static[0], cases_static[1], cases_static[2], cases_static[3], cases_static[4], cases_static[5]))
    print("cases_dynamic = {}, {}, {}, {}".format(cases_dynamic[0], cases_dynamic[1], cases_dynamic[2], cases_dynamic[3]))

    idx+=1

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
