# Jetson nano 이미지 처리 노드

## 목적 
Jetson nano 보드 안에서 Pi camera v2(sony IMX 219)로 촬영한 사진을 영상처리하고 퍼블리싱하는 ROS 패키지입니다.

PD제어를 위해 특정 행의 차선 중앙값을 ROS 메세지로 발행합니다.

## 개발환경
HW : Nvidia jetson nano / Sony IMX219(Pi cam v2) / Intel d435i

SW : Ubuntu18.04.4 LTS / ROS melodic / OpenCV 4.1.1

## 세부함수구성
distort : 카메라의 왜곡되어 촬영된 이미지를 opencv의 undistort 함수를 이용하여 보정합니다.

resize : 이미지를 320*240 사이즈로 조정합니다.

warp : 이미지를 위에서 바라본 것처럼 왜곡시킵니다.

lab_combine : RGB 색상체계인 본래 이미지를 CIE LAB 색상 체계로 바꾸고, 밝기(L) 이미지를 블러 필터를 사용하여 조명에 대한 이미지를 생성 후, 조명에 영향을 줄입니다.
흰색과 노랑색을 추출하기 위해 밝기(L) 이미지와 카메라의 강제 화이트밸런스로 인한 붉은 색을 적절히 반영하고자, 빨강과 초록(A) 이미지를 가우시안 블러로 필터링하고, 합쳐서 이진화한다.

find_line : 이진화한 이미지 중 하단 30열을 가로에 더해 히스토그램을 만들어, 가로선을 찾는다.

find_first : 차선에 대한 line class의 속성을 확인하여, 좌,우측 차선의 발견 유무에 따라 히스토그램으로 이미지 하단에서 차선을 발견하고, line class의 속성을 갱신한다.

sliding_window : line class의 속성을 확인하여, 차선 시작점을 중심으로 하는 윈도우를 만들어 차선을 검증하고, 추적한다.

blind_search : line class의 속성을 확인하여, find_first 함수를 불러올지 바로 sliding_window 함수를 불러올지 판단하여 실행한다.

prev_window_refer : sliding_window와 유사한 역할을 수행한다.

find_LR_lines : line class의 속성을 확인하여 blind_search 함수를 실행할지, prev_window_refer 함수를 실행할지 결정한다.

make_center : line class에 기록된 좌우 차선의 계산된 2차 함수의 fitting 데이터를 가지고, 이미지 2/3 높이에서의 차선 중앙값을 ROS를 통해 발행한다.

image_callback : 카메라로 부터 이미지를 구독할 때, OpenCV 라이브러리를 사용하기 위한 포멧으로 변환한다.

image_listener : 노드가 발행하거나 구독할 토픽과 콜백함수를 정의한다.