#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>
#include <vector>
#include <sensor_msgs/Image.h>
#include <sensor_msgs/Imu.h>
#include <sensor_msgs/image_encodings.h>
#include <std_msgs/UInt8MultiArray.h>

void sub_imu_cam_callback(const sensor_msgs::Imu::ConstPtr& msg)
{
    ROS_INFO("t265 receive suceess");
}

void sub_rgb_cam_callback(const sensor_msgs::Image::ConstPtr& msg)
{
    try
    {
        cv_bridge::CvImagePtr cvi;
        cvi=cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
        cv::imshow("d435i_view", cvi->image);
        cv::waitKey(1);
        ROS_INFO("d435i receive suceess");
    }
    catch(const std::exception& e)
    {
        ROS_ERROR("cannot decode d435i image");
        std::cerr << e.what() << '\n';
    }
    

}

void sub_rasp_cam_callback(const sensor_msgs::Image::ConstPtr& msg)
{
    try
    {
        cv_bridge::CvImagePtr cvi;
        cvi=cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
        cv::imshow("rasp_view", cvi->image);
        cv::waitKey(1);
        ROS_INFO("rasp_cam receive suceess");
    }
    catch(const std::exception& e)
    {
        ROS_ERROR("cannot decode d435i image");
        std::cerr << e.what() << '\n';
    }
}

int main(int argc, char **argv)
{
    //초기설정
    ros::init(argc, argv, "ros_subscribe");

    cv::namedWindow("d435i_view");
    cv::namedWindow("rasp_view");
    cv::startWindowThread();

    //노드 제어
    ros::NodeHandle n;
    ros::Subscriber sub_rasp_cam = n.subscribe("/jetbot_camera/raw", 2, sub_rasp_cam_callback);
    ros::Subscriber sub_rgb_cam = n.subscribe("/cam_1/color/image_raw", 2, sub_rgb_cam_callback);
    ros::Subscriber sub_imu_cam = n.subscribe("/imu", 2, sub_imu_cam_callback);

    ros::spin();

    cv::destroyAllWindows();

    return 0;
}