#!/usr/bin/python2
#-*- coding:utf-8 -*-

import rospy                      # rospy
import numpy as np                # numpy
import cv2                        # OpenCV2
from sensor_msgs.msg import Image # ROS Image message
from std_msgs.msg import Float64
from cv_bridge import CvBridge, CvBridgeError # ROS Image message -> OpenCV2 image converter
import math
import sys

#Instantiate CV Bridge
bridge = CvBridge()

vertices = [(0, 0), (0, 115), (72, 240), (268, 240), (320, 152), (320, 0)]
src = np.float32(((222, 250), (124, 480), (587, 480), (480, 250)))
dst = np.float32([[210, 0], [210, 480], [640 - 210, 480], [640 - 210, 0]])
mini_histo_roi = np.float32([[150, 400], [150, 480], [460, 480], [460, 400]])
warped_roi = np.float32([[0, 0], [150, 480], [460, 480], [640, 0]])

Matrix = np.array([[702.79573591, 0., 639.68721137], [0., 700.36468219, 351.49375006], [0., 0., 1.]], dtype=np.float32)
Distortion = np.array([[-0.24512458, -0.09374123, -0.01451455, -0.00190292, 0.22375519]], dtype=np.float32)

msg_data = [0, 0, 0, 0]


def distort(img):
    return cv2.undistort(img, Matrix, Distortion, None, Matrix)


def resize(image, size):
    if image.shape[0] == 480 and image.shape[1] == 640:
        return image
    else:
        return cv2.resize(image, dsize=size)


def ready_process(image):
    distorted_img = distort(image)
    resized_img = resize(distorted_img, (320, 240))
    # return cv2.rotate(resized_img, cv2.ROTATE_180)
    return resized_img


def warp(image, source, destination):
    # Compute and apply perpective transform
    img_size = (image.shape[1], image.shape[0])
    m = cv2.getPerspectiveTransform(source, destination)
    return cv2.warpPerspective(image, m, img_size, flags=cv2.INTER_NEAREST)  # keep same size as input image



# @logging_time
def bird_view(image):
    h, w = image.shape[:2]
    gap = 80
    bird_src = np.float32([[105, 105], [40, 240], [285, 240], [220, 105]])
    bird_dst = np.float32([[w/2 - gap, 0], [w/2 - gap, h], [w/2 + gap, h], [w/2 + gap, 0]])
    # return cv2.bitwise_not(warp(cv2.bitwise_not(image), bird_src, bird_dst))
    return warp(image, bird_src, bird_dst)

def make_roi(image):
    ROI = image[184:225, 47:269]
    return ROI

def choice_white(image):
    