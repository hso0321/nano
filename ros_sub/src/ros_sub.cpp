#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <sensor_msgs/Imu.h>
#include <sensor_msgs/image_encodings.h>

void sub_imu_cam_callback(const sensor_msgs::Imu::ConstPtr& msg)
{
    ROS_INFO("t265 receive suceess");
}

void sub_rgb_cam_callback(const sensor_msgs::Image::ConstPtr& msg)
{
    ROS_INFO("d435i receive suceess");
}

void sub_rasp_cam_callback(const sensor_msgs::Image::ConstPtr& msg)
{
    ROS_INFO("jetson_camera receive success");
}

int main(int argc, char **argv)
{
    //초기설정
    ros::init(argc, argv, "ros_subscribe");
    //노드 제어
    ros::NodeHandle n;
    ros::Subscriber sub_rasp_cam = n.subscribe("/jetbot_camera/raw", 2, sub_rasp_cam_callback);
    ros::Subscriber sub_rgb_cam = n.subscribe("/cam_1/color/image_raw", 2, sub_rgb_cam_callback);
    ros::Subscriber sub_imu_cam = n.subscribe("/imu", 2, sub_imu_cam_callback);

    ros::spin();

    return 0;
}