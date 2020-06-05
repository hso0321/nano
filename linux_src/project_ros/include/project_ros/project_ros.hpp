#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cv_bridge/cv_bridge.h>
#include <vector>
#include <string>
#include <sensor_msgs/Image.h>
#include <sensor_msgs/Imu.h>
#include <sensor_msgs/image_encodings.h>
#include <std_msgs/UInt8MultiArray.h>
#include <mutex>

// darknet_ros_msgs

#include <darknet_ros_msgs/BoundingBox.h>
#include <darknet_ros_msgs/BoundingBoxes.h>
#include <darknet_ros_msgs/CheckForObjectsAction.h>
#include <darknet_ros_msgs/ObjectCount.h>

// 동영상 저장을 위한 변수
cv::VideoWriter writer_rasp;
cv::VideoWriter writer_d435i;

// 박스의 수를 저장하기 위한 변수
int Boxes;

// lock을 위한 변수
std::mutex mutex;

// depth 한장을 저장하기 위한 변수
cv::Mat dst;

// function
void sub_imu_cam_callback(const sensor_msgs::Imu::ConstPtr& msg);
void sub_rgb_cam_callback(const sensor_msgs::Image::ConstPtr& msg);
void sub_rasp_cam_callback(const sensor_msgs::Image::ConstPtr& msg);
void sub_depth_callback(const sensor_msgs::Image::ConstPtr& msg);
void sub_yolo_count_callback(const darknet_ros_msgs::ObjectCount::ConstPtr &msg);
void sub_yolo_callback(const darknet_ros_msgs::BoundingBoxes::ConstPtr &msg);

ros::Subscriber sub_rasp_cam;
ros::Subscriber sub_rgb_cam;
ros::Subscriber sub_imu_cam;
ros::Subscriber sub_depth;
ros::Subscriber sub_yolo_count;
ros::Subscriber sub_yolo;

// publisher
ros::Publisher projectPublisher_;

