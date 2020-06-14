#!/usr/bin/python2
#-*- coding:utf-8 -*

import rospy
import numpy as np
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

lasterror = 0
Max_vel = 0.12
Min_lin = 0.2
Min_ang = 2.0

def cbFollowLane(desired_center):
    print('sub data at', rospy.get_rostime().secs, rospy.get_rostime().nsecs)
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
    print('pub cmd vel at', rospy.get_rostime().secs, rospy.get_rostime().nsecs)
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

if __name__ == '__main__':

    rospy.init_node('control_lane')
    sub_lane = rospy.Subscriber('/detect/lane', Float64, cbFollowLane, queue_size=1)
    pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.on_shutdown(fnShutDown)
    rospy.spin()
