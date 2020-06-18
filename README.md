ROS와 물체인식을 이용한 자율주행 시스템

주제  
 jetson nano 보드를 이용한 간이 차체를 제작하여 자율주행을 합니다. 자율주행을 위해서는 많은 센서가 필요하고 유기적으로 작동을 하기 위해 ROS를 사용합니다. 구체적으로 차체에 장착하는 모듈은 raspberry pi camera를 이용하여 도로를 인식하고, d435i를 이용하여 차량 전방의 물체를 인식하고 거리(depth)를 측정합니다. 동시에 Server와 차량은 통신을 실시간으로 합니다. Server는 차체에서 송신하는 데이터를 받아 미리 학습된 AI(yolov3-tiny)를 통해 객체를 실시간으로 인식하여 주행에 대한 판단을 전송합니다. 마지막으로 차량은 이 데이터를 수신하여 자율주행을 합니다.

개발환경  
 Server : Ubuntu18.04.4 LTS / GeForce GTX 2080 super / Intel Core i7-9700  
 Board  : Nvidia jetson nano / RaspberryPi CameraV2 / d435i(Intel)  

사용 기술  
 머신러닝 플랫폼 : darnet  
 인공지능 모델   : yolov3-tiny  
 사용 라이브러리 : OpenCV 3.4.2(Server, darkent 프레임워크 사용을 위해), OpenCV 4.1.1(jetson nano보드에서 사용), ROS melodic  
 개발언어 : Python2.7, C++, Matlab  
 개발 지원 도구  : GitLab, Git, Anaconda, VScode, PyCham  

내용  
 linux_src  : Server에서 사용하는 ROS source  
 nano_src   : jetson nano에서 사용하는 ROS source  
 start_shell: 시스템을 구동하는데 기본적으로 필요한 ROS 명령어를 간단한 shell로 묶어놓은 파일  

 ROS source는 ~/catkin/src 밑에 복사해서 사용  
 start_shell은 아무곳에서나 실행

darknet_ros(cuda를 먼저 설치하신 후 opencv를 설치하십시오.)  

yolov3-tiny를 사용한 이유는 실시간으로 서버와 이미지를 송수신해야 하기 때문입니다. Test를 시행한 결과, yolov3에서는 50-60의 FPS가 나오고, yolov3-tiny에서는 200-210FPS가 나오는 것을 확인했습니다.

학습된 데이터는 총 656장의 이미지를 이용하였습니다. 학습 횟수는 약 20000번 정도의 학습을 했습니다.  

아래의 url을 참고하여 다운 받으시면 됩니다.  
https://taemian.tistory.com/6

<div>
<img width="200" src="https://user-images.githubusercontent.com/61136992/84970278-4c614100-b155-11ea-8b98-d66856f9cd48.png">
</div>