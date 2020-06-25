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

std_max_vel = 0.09
std_min_lin = 0.15
std_min_ang = 1.5

# std_max_vel = 0.05
# std_min_lin = 0.08
# std_min_ang = 0.8

max_vel = 0
min_lin = 0

min_ang = 0
# min_ang = 4.0
# vertical_variable
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

    # print("cases_static = {}, {}, {}, {}, {}, {}".format(cases_static[0], cases_static[1], cases_static[2], cases_static[3], cases_static[4], cases_static[5]))
    print("cases_dynamic = {}, {}, {}, {}".format(cases_dynamic[0], cases_dynamic[1], cases_dynamic[2], cases_dynamic[3]))
    if(center > 0) :
        if vertical_flag == 1:
            print('vertical_flag success')
            if cases_dynamic[2] == 0:      # red light
                fnShutDown()

            elif cases_dynamic[3] == 0:     # green light
                vertical_flag = 1
                force_drive(6)                            # 강제 직진


            elif cases_static[4] == 0:      # 로터리
                        # 강제 직진
                print("I'am lottery")
                fnShutDown()
                if cases_dynamic[1] ==0 :
                    print("tuetle")
                    rospy.sleep(2)
                    force_drive(6)
                    vertical_flag=0

            elif cases_static[0] == 0:      # turn limit
                print('turn limit!')
                fnShutDown()
                rospy.sleep(1)
                force_drive(0)                # 강제 직진
                vertical_flag =0

            else:
                print('STOP!')
                # rospy.Timer(rospy.Duration(0.5), fnShutDown, oneshot=True)      # 강제 직진
                fnShutDown()                # 일단 정지
        else:                               # 정지선을 안 만났을때
            if cases_dynamic[0] == 0:       # find people
                print('meet people!')
                fnShutDown()
                rospy.sleep(2)
            elif cases_dynamic[1] == 0:     # 터틀봇
                print("i see turtlebot!!!")
                fnShutDown()
            elif cases_static[5] == 0:      # turnnel
                fnDrive(center)
                # force_drive(5)               # 터널 강제기동
                # fnShutDown()
            elif cases_static[3] == 0:      # unlimit
                max_vel = std_max_vel
                min_lin = std_min_lin
                min_ang = std_min_ang
                fnDrive(center)
                print('To origin setting!')
            elif cases_static[2] == 0:      # children zone
                print('children zone')
                max_vel = 0.5 * std_max_vel
                min_lin = 0.5 * std_min_lin
                min_ang = 0.5 * std_min_ang
                fnDrive(center)
            elif cases_static[1] == 0:      # limit low_vel
                print('limit lowest_vel!')
                max_vel = 2 * std_max_vel
                min_lin = 2 * std_min_lin
                min_ang = 2 * std_min_ang
                fnDrive(center)
            
            else:
                print('just drive!')
                fnDrive(center)
    else:
        print("error")
        return -1
        
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
    twist.linear.x = 0.05
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

    start_t = rospy.get_time()
    if case != 6:               # 6일 경우는 플래그를 안 바꿈.
        cases_static[case] = 1
    while(rospy.get_time() < start_t + 3):
                print("whiling")
                move_forward()
                rospy.sleep(0.04)
    
    return

def depth_call_back(msg):
    global cases_dynamic, cases_static, vertical_flag

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
    if depth_class[6] != 0 :
        print('find turn limit!')
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
    if depth_class[2] != 0 :
        cases_static[4] = 0

    # 6.turnel
    if 320 < depth_class[5] <= 360 :
        # bool_msg = Bool()
        # bool_msg.data = True
        # if cases_static[5] == 1 :
            # start_t = rospy.get_time()
            # while(rospy.get_time() < start_t + 4) :
            #     tunnel_vel.publish(bool_msg)
            # bool_msg.data = False
            # tunnel_vel.publish(bool_msg)
        start_t = rospy.get_time()
        while(rospy.get_time() < start_t + 4) :
            cases_static[5] = 0
        cases_static[5] = 1

                

    # if 400 < depth_class[5] <= 450 :
    #     Bool_msg = Bool()
    #     Bool_msg.data = True
    #     if cases_static[5] == 1 : 
    #         start_t = rospy.get_time()
    #         while(rospy.get_time() < start_t + 2) :
    #             tunnel_vel.publish(Bool_msg)
    #         Bool_msg.data = False
    #         tunnel_vel.publish(Bool_msg)
    #     cases_static[5] = 0


    # dynamic

    # 1.people
    if 0 < depth_class[4] <= 540 :
        cases_dynamic[0] = 0
    else :
        cases_dynamic[0] = 1

    # 2.turtle
    if 0 < depth_class[7] <= 550 :
        cases_dynamic[1] = 0

    else :
        cases_dynamic[1] = 1

    # 3.red_light(taffic)
    if 500 < depth_class[9] <= 540 :
        cases_dynamic[2] = 0
    else :
        cases_dynamic[2] = 1

    # 4.green_light(traffic)
    if 400 < depth_class[10] <=500 :
        cases_dynamic[3] = 0
    else :
        cases_dynamic[3] = 1

    # print("cases_static = {}, {}, {}, {}, {}, {}".format(cases_static[0], cases_static[1], cases_static[2], cases_static[3], cases_static[4], cases_static[5]))
    # print("cases_dynamic = {}, {}, {}, {}".format(cases_dynamic[0], cases_dynamic[1], cases_dynamic[2], cases_dynamic[3]))

    print(depth_class)

    return

def cbStopLane(bool_msg):
    global vertical_flag
    bool_msg = Bool()
    print('bool_msg =', bool_msg.data)

    if((bool_msg.data == False) and (cases_static[5] ==1)) :
        print('find horizon line!')
        vertical_flag = 1

    return

if __name__ == '__main__':
    max_vel = std_max_vel
    min_lin = std_min_lin
    min_ang = std_min_ang

    rospy.init_node('control_lane')
    sub_lane = rospy.Subscriber('/detect/lane', Float64, cbFollowLane, queue_size=1)
    stop = rospy.Subscriber('/detect/stop', Bool, cbStopLane, queue_size=1)
    pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    tunnel_vel = rospy.Publisher('/tunnel', Bool, queue_size=1)
    depth_data_sub = rospy.Subscriber('/project_pub', BoundingBoxes, depth_call_back , queue_size=1)
    rospy.on_shutdown(fnShutDown)
    rospy.spin()
