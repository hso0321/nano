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
max_vel = 0.09
min_lin = 0.15

min_ang = 1.5
# min_ang = 4.0
vertical_flag = 0

# driving flags
# default is 1
# turn_limit, limit_speed, child, unlimit, lottery, turnel
cases_static = [1,1,1,1,1,1]
# people, turtle, red_light(traffic), green(traffic)
cases_dynamic= [1,1,1,1]

def cbFollowLane(desired_center):
    global lasterror, max_vel, min_ang, min_lin
    global cases_static, cases_dynamic, vertical_flag
    center = desired_center.data

    if vertical_flag == 1:
        print('vertical_flag success')
        if cases_dynamic[2] == 0:      # red light
            fnShutDown()

        elif cases_dynamic[3] == 0:     # green light
            rospy.Timer(rospy.Duration(0.5), fnShutDown, oneshot=True)      # 강제 직진
            force_drive(6)

        # elif cases_dynamic[1] == 0:     # turtle bot 로터리 상황
        #     fnShutDown() 

        elif cases_static[4] == 0:      # 로터리
            # fnShutDown()                # 강제 직진
            # if(cases_dynamic[1] == 0):
            #     force_drive(6)
            # rospy.Timer(rospy.Duration(0.5), fnShutDown, oneshot=True)
            if cases_dynamic[1] == 0:
                force_drive(4)
            else:
                fnShutDown()

        elif cases_static[0] == 0:      # 우회전 금지
            force_drive(0)                # 강제 직진

        else:
            print('STOP!')
            # rospy.Timer(rospy.Duration(0.5), fnShutDown, oneshot=True)      # 강제 직진
            fnShutDown()                # 일단 정지
    else:
        if cases_dynamic[0] == 0:       # find people
            print('meet people!')
            fnShutDown()
        elif cases_dynamic[1] == 0:     # 터틀봇
            if cases_dynamic[1] == 0:
                fnShutDown()
            else:
                fnDrive(center)
        elif cases_static[5] == 0:      # turnnel
            # force_drive(5)               # 터널 강제기동
            fnShutDown()
            # cases_static[5] = 1
        elif cases_static[3] == 0:      # unlimit
            max_vel = 0.09
            min_lin = 0.15
            min_ang = 1.5
            fnDrive(center)
            print('To origin setting!')
        elif cases_static[2] == 0:      # children zone
            print('children zone')
            max_vel =0.05
            min_lin = 0.07
            min_ang = 0.7
            fnDrive(center)
        elif cases_static[1] == 0:      # limit low_vel
            print('limit lowest_vel!')
            max_vel=0.18
            min_lin= 0.3
            min_ang=3.0
            fnDrive(center)
        

       
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

    # print('pub cmd vel at', rospy.get_rostime().secs, rospy.get_rostime().nsecs,'\n')
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


def move_forward():
    twist = Twist()
    twist.linear.x = 0.15
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 0
    pub_cmd_vel.publish(twist)
    return


def force_drive(case):
    # 강제 직진 코드를 짜주세요
    global cases_static
    if case == 6 :
        move_forward()
        rospy.sleep(1.0)
    else:
        if cases_static[case] == 0:
            move_forward()
            rospy.sleep(1.0)
            cases_static[case] == 1
    return

def depth_call_back(msg):
    global cases_dynamic, cases_static

    # depth of class
    # child, limit_speed, lottery, park, people, tunnel, turn_limit, turtle, unlimit, red_light, green_light
    # default is 0
    depth_class = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for box in range(0, 11):
        depth_class[box] = 0

    # box number in ymax(in first box)
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
    rospy.sleep(0.2)
    # scenario
    # static

    # 1.turn_limit
    if 250 < depth_class[6] <= 350 :
        print('turn limit!')
        cases_static[0] = 0
    
    # 2.limit_speed
    if 500 < depth_class[1] <= 540 :
        cases_static[1] = 0

    # 3.child
    if 500 < depth_class[0] <= 540 :
        cases_static[2] = 0

    # 4.unlimit
    if 500 < depth_class[8] <= 540 :
        cases_static[3] = 0

    # 5.lottery
    if 500 < depth_class[2] <= 540 :
        cases_static[4] = 0

    # 6.turnel
    if 500 < depth_class[5] <= 540 :
        cases_static[5] = 0

    # dynamic

    # 1.people
    if 500 < depth_class[4] <= 540 :
        cases_dynamic[0] = 0
    else :
        cases_dynamic[0] = 1

    # 2.turtle
    if 100 < depth_class[7] <= 240 :
        cases_dynamic[1] = 0
    else :
        cases_dynamic[1] = 1

    # 3.red_light(taffic)
    if 500 < depth_class[9] <= 540 :
        cases_dynamic[2] = 0
    else :
        cases_dynamic[2] = 1

    # 4.green_light(traffic)
    if 500 < depth_class[10] <=540 :
        cases_dynamic[3] = 0
    else :
        cases_dynamic[3] = 1

    print("cases_static = {}, {}, {}, {}, {}, {}".format(cases_static[0], cases_static[1], cases_static[2], cases_static[3], cases_static[4], cases_static[5]))
    # print("cases_dynamic = {}, {}, {}, {}".format(cases_dynamic[0], cases_dynamic[1], cases_dynamic[2], cases_dynamic[3]))

    print(depth_class)

    return

def cbStopLane(bool_msg):
    global vertical_flag
    bool_msg = Bool()
    print('bool_msg =', bool_msg.data)
    if bool_msg.data == False:
        vertical_flag = 1
        print('find horizon line!')
    return

if __name__ == '__main__':

    rospy.init_node('control_lane')
    sub_lane = rospy.Subscriber('/detect/lane', Float64, cbFollowLane, queue_size=1)
    stop = rospy.Subscriber('/detect/stop', Bool, cbStopLane, queue_size=1)
    pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    depth_data_sub = rospy.Subscriber('/project_pub', BoundingBoxes, depth_call_back , queue_size=1)
    rospy.on_shutdown(fnShutDown)
    rospy.spin()
