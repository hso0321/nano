#include "project_ros/project_ros.hpp"

int main(int argc, char **argv)
{
    //초기설정
    ros::init(argc, argv, "ros_subscribe");

    //저장을 위한 초기설정
    double rasp_fps = 30.0;
    cv::Size size_rasp = cv::Size(1280, 720);
    writer_rasp.open("/home/kim/test_video/rasp_cam.avi", cv::VideoWriter::fourcc('M', 'J', 'P', 'G'), rasp_fps, size_rasp, true);
    if(!writer_rasp.isOpened())
    {
        std::cout<<"동영상을 저장하기 위한 초기화 작업 중 에러 발생"<<std::endl;
        return 1;
    }
    double d435i_fps = 30.0;
    cv::Size size_d435i = cv::Size(640, 480);
    writer_d435i.open("/home/kim/test_video/d435i_cam.avi", cv::VideoWriter::fourcc('M', 'J', 'P', 'G'), d435i_fps, size_d435i, true);
    if (!writer_d435i.isOpened())
    {
        std::cout << "동영상을 저장하기 위한 초기화 작업 중 에러 발생" << std::endl;
        return 1;
    }
    cv::namedWindow("d435i_view");
    cv::namedWindow("rasp_view");
    cv::startWindowThread();

    // 노드 제어
    ros::NodeHandle n;
    
    projectPublisher_ = n.advertise<darknet_ros_msgs::BoundingBoxes>("projet_pub", 1);

    sub_rasp_cam = n.subscribe("/rasp_cam_pub", 1, sub_rasp_cam_callback);
    sub_rgb_cam = n.subscribe("/cam_1/color/image_raw", 2, sub_rgb_cam_callback);
    sub_imu_cam = n.subscribe("/imu", 2, sub_imu_cam_callback);
    sub_depth = n.subscribe("/cam_1/depth/image_rect_raw", 2, sub_depth_callback);
    sub_yolo_count = n.subscribe("/darknet_ros/found_object", 2, sub_yolo_count_callback);
    sub_yolo = n.subscribe("/darknet_ros/bounding_boxes", 2, sub_yolo_callback);

    ros::spin();
    cv::destroyAllWindows();

    return 0;
}

void sub_imu_cam_callback(const sensor_msgs::Imu::ConstPtr& msg)
{
    try
    {
        //ROS_INFO("t265 receive suceess");
    }
    catch(const std::exception& e)
    {
        ROS_ERROR("t265 imu error");
        std::cerr << e.what() << '\n';
    }
}

void sub_rgb_cam_callback(const sensor_msgs::Image::ConstPtr& msg)
{
    try
    {
        cv_bridge::CvImagePtr cvi;
        cvi=cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);

        //ROS_INFO("image_width : %d, image_height : %d ",cvi->image.cols, cvi->image.rows);
        //저장
        //writer_d435i.write(cvi->image); 

        cv::imshow("d435i_view", cvi->image);
        cv::waitKey(1);
        //ROS_INFO("d435i receive suceess");
    }
    catch(const std::exception& e)
    {
        ROS_ERROR("d435i image error");
        std::cerr << e.what() << '\n';
    }
}

void sub_rasp_cam_callback(const sensor_msgs::Image::ConstPtr& msg)
{
    try
    {
        cv_bridge::CvImagePtr cvi;
        cvi=cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);

        //저장
        //writer_rasp.write(cvi->image);
        cv::imshow("rasp_view", cvi->image);
        cv::waitKey(1);
        //ROS_INFO("rasp_cam receive suceess");
    }
    catch(const std::exception& e)
    {
        ROS_ERROR("rasp_cam image error");
        std::cerr << e.what() << '\n';
    }
}

/*
//for get cut location
void CallBackFunc(int event, int x, int y, int flags, void* userdata)
{
    if(event == CV_EVENT_LBUTTONDOWN)
    {
        ROS_INFO("마우스 버튼 클릭.. 좌표 = (%d, %d)", x, y);
    }
}
*/

void sub_depth_callback(const sensor_msgs::Image::ConstPtr& msg)
{
    try
    {
        cv::Mat mid;
        cv_bridge::CvImagePtr cvi;
        cvi = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::TYPE_16UC1);

        //ROI for between depth and RGB(d435i)
        cv::Rect rect(85, 85, 400, 315);
        mid = cvi->image(rect);

        // resize 이후 dst(전역변수)에 이미지 저장
        cv::resize(mid, dst, cv::Size(640, 480));

        //for constrast increase
        //for view
        cv::Mat image_view;
        image_view = dst * 40.0;
        cv::imshow("depth", image_view);

        //for get cut location
        //cv::setMouseCallback("depth", CallBackFunc, NULL);

        cv::waitKey(1);
        //ROS_INFO("rasp_cam receive suceess");
    }
    catch (const std::exception &e)
    {
        ROS_ERROR("d435i depth error");
        std::cerr << e.what() << '\n';
    }
}

void sub_yolo_count_callback(const darknet_ros_msgs::ObjectCount::ConstPtr &msg)
{
    try
    {
        //배열의 갯수
        Boxes = msg->count;
    }
    catch (const std::exception &e)
    {
        ROS_ERROR("Yolo receive count error");
        std::cerr << e.what() << '\n';
    }
}

void sub_yolo_callback(const darknet_ros_msgs::BoundingBoxes::ConstPtr &msg)
{
    try
    {
        darknet_ros_msgs::BoundingBoxes pub_data;
        mutex.lock();
        for (int idx = 0; idx < Boxes; idx++)
        {
            darknet_ros_msgs::BoundingBox box;
            //copy for publish
            box.probability = msg->bounding_boxes[idx].probability;
            box.xmin = (int)((msg->bounding_boxes[idx].xmin + msg->bounding_boxes[idx].xmax) / 2);
            box.ymin = (int)((msg->bounding_boxes[idx].ymin + msg->bounding_boxes[idx].ymax) / 2);
            box.Class = msg->bounding_boxes[idx].Class;
            box.id = msg->bounding_boxes[idx].id;

            // depth 저장
            box.xmax = (dst.at<unsigned short>(box.ymin, box.xmin));

            pub_data.bounding_boxes.push_back(box);
        }

        pub_data.header.stamp = ros::Time::now();
        pub_data.header.frame_id = "detection";
        projectPublisher_.publish(pub_data);

        mutex.unlock();
    }
    catch (const std::exception &e)
    {
        ROS_ERROR("Yolo receive error");
        std::cerr << e.what() << '\n';
    }
}