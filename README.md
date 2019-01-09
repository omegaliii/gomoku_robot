# EE106A Final Project Gomoku_robot
More details on https://gomokuee106a.wixsite.com/home

## 1. Building the package
Run the command from the gomoku_robot directory.

`catkin_make`

“Sourcing” this script will prepare your ROS environment for using the packages contained in this workspace

`source devel/setup.bash`

## 2. Enable gomoku_brain node
Ensure that a webcam is connected to your computer. Depending on which type you select, you may need to modify the parameters in the launch file. (The default is the Microsoft cameras.) Run this launch file using the command:

`roslaunch gomoku_brain run_cam.launch`

It should display the image from the camera. We can press Enter to capture the chessboard image once the chessboard is in the correct location.


## 3. Enable gomoku_controller node
At the root of your workspace (the gomoku_robot directory), create a symbolic link to the baxter.sh script by running

`ln -s /scratch/shared/baxter_ws/baxter.sh ~/ros_workspaces/`

To interacte with Baxter, run:

`./baxter.sh [name-of-robot].local` 

`source devel/setup.bash`

then enable Baxter’s joints by running

`rosrun baxter_tools enable_robot.py -e`

start MoveIt with 

`roslaunch baxter_moveit_config demo_baxter.launch right_electric_gripper:=true left_electric_gripper:=true`

Next, in a new window, start the gomoku_controller node:

`./baxter.sh [name-of-robot].local` 

`source devel/setup.bash`

`rosrun gomoku_controller gomoku_sub`
