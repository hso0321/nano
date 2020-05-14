jetson nano code입니다.

ros_sub 디렉터리는 ubuntu pc(server)에서 subscribe를 하기 위한 ros source입니다. ~/catkin/src 밑에 복사해서 사용하세요.

src 디렉터리는 jetson nano의 ros code입니다

start_shell은 ros의 명령어를 기본적으로 실행하기 위한 것입니다. nano.sh은 jetson nano에서 ./nano.sh로 실행하시고, server.sh은 ubuntu pc(server)에서, 그리고 ros_sub_recieve.sh도 ubuntu pc(server)에서 실행하시면 됩니다.

ros_sub_recieve.sh은 imu, d435i의 RGB, raspcam의 RGB를 subscribe하는 노드입니다.


test