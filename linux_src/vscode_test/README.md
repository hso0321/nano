# Linux PC 차량제어 노드

## 목적
Linux pc에서 차선인식 결과(/detect/lane&/detect/stop)와 물체인식,거리측정 값(/project_pub)을 구독하고, 차량제어를 위한 결과(/cmd_vel)를 발행한다.

## 개발환경
HW : Intel Core i7-9700 / GeForce GTX 2080 super 
SW : Ubuntu18.04.4 LTS / ROS melodic / OpenCV 3.4.2

## 세부함수구성

cbFollowLane : 차선인식 데이터를 구독할 때 시나리오 구분을 위한 배열을 체크하고, 그에 맞는 함수를 불러온다.
depth_call_back : 물체인식 데이터를 구도할 때 어떤 물체인지 구분하고, 거리 값을 판별하여 배열에 기록한다.
cbStopLane : 가로선이라는 메세지를 구독할 때 flag를 바꿔준다.

fnDrive : 차선인식 데이터로 부터 차량의 움직임을 계산하고, 모터제어를 위한 메세지를 발행한다.
move_forward : 정해진 속도로 직진하도록 메세지를 발행한다.
fnShutDown : 정지하도록 메세지를 발행한다.
force_drive : 직진이 필요할 때 move_forward를 불러오고, 시나리오 flag를 되돌린다.

## 주의점

차선인식 데이터가 값이 없을 경우 움직이지 않습니다.
