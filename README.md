# EE106A Final Project Gomoku_robot

## Project Overview: 

We builds an AI-based robot that can play Gomoku with human players on a physical chessboard.

The gomoku robot is able to determine the chessboard states by the vision sensors and then use the Gomoku game engine to decide the next step according to the current board scenario, and finally the robot controller will control Baxter to place/mark a real-life stone/symbol on the board. Also in order to increase the functionality of the robot, a cheating detective feature will be built-in as well: If the human player doesn’t follow the Gomoku rules to make valid steps, the  system is able to detect the invalid steps and make an attempt to reverse it. More details on https://gomokuee106a.wixsite.com/home

## Code Usage
### 1. Building the package
Run the command from the gomoku_robot directory.

`catkin_make`

“Sourcing” this script will prepare your ROS environment for using the packages contained in this workspace

`source devel/setup.bash`

### 2. Enable gomoku_brain node
First, change the permission of the following file under gomoku_brain/src:

`chmod  a+x  camera_srv.py image_process.py`

Ensure that a webcam is connected to your computer. Depending on which type you select, you may need to modify the parameters in the launch file. (The default is the Microsoft cameras.) Run this launch file using the command:

`roslaunch gomoku_brain run_cam.launch`

It should display the image from the camera. We can press Enter to capture the chessboard image once the chessboard is in the correct location.


### 3. Enable gomoku_controller node
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
