#!/usr/bin/env python
"""
Path Planning Script for Lab 8
Author: Valmik Prabhu
"""

import sys
import tf2_ros
import rospy
import numpy as np
import time

from moveit_msgs.msg import OrientationConstraint
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
from std_msgs.msg import String

from path_planner import PathPlanner
from baxter_interface import Limb
from baxter_interface import gripper as robot_gripper

import argparse

import baxter_interface
import baxter_external_devices

from baxter_interface import CHECK_VERSION
import time

def listener(target_frame):
    source_frame = "base"
    tfBuffer = tf2_ros.Buffer()
    tfListener = tf2_ros.TransformListener(tfBuffer)
    while not rospy.is_shutdown():
        try:
            tran = tfBuffer.lookup_transform(target_frame,source_frame,rospy.Time())
            position = tran.transform.translation
            print(position)
            #return (position.x,position.y,position.z)
        except (tf2_ros.LookupException,tf2_ros.ConnectivityException,tf2_ros.ExtrapolationException):
            continue

def action(hand,m,n):
    '''
    Left hand or right hand
    '''
    left_gripper = robot_gripper.Gripper('left')
    left_gripper.calibrate()
    left_gripper.command_position(0)

    p0x = 0.768
    p0y = 0.220
    p0z = -0.121
    p1x = 0.378
    p1y =-0.200
    p1z = -0.121
    

    arm = hand + "_arm"
    planner = PathPlanner(arm)
    if hand == "left":
        tool = "marker"
    else:
        tool = "eraser"

    init_px = p0x#0.795#
    init_py = p0y
    x_interval = (p1x-p0x)/9#-0.045
    y_interval = (p1y-p0y)/9#-0.046
    
    if hand == "left":
        px = init_px + x_interval * m
        py = init_py + y_interval * n
        pz = -0.200
    else:
        px = init_px + (x_interval) * m - 0.02
        py = init_py + (y_interval+0.001) * n - 0.017
        pz = -0.224

    Kp = 0.1 * np.array([0.3, 2, 1, 1.5, 2, 2, 3]) # Stolen from 106B Students
    Kd = 0.01 * np.array([2, 1, 2, 0.5, 0.5, 0.5, 0.5]) # Stolen from 106B Students
    Ki = 0.01 * np.array([1, 1, 1, 1, 1, 1, 1]) # Untuned
    Kw = np.array([0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]) # Untuned

    planner.remove_obstacle("low_table")
    planner.remove_obstacle("high_table")
    planner.remove_obstacle("front")
    planner.remove_obstacle("leftmost")
    planner.remove_obstacle("rightmost")
    planner.remove_obstacle("eye")
    
    def setObstacle(x,y,z,frame):
        ob = PoseStamped()
        ob.header.frame_id = frame
        ob.pose.position.x = x 
        ob.pose.position.y = y
        ob.pose.position.z = z
        ob.pose.orientation.x = 0.0
        ob.pose.orientation.y = 0.0
        ob.pose.orientation.z = 0.0
        ob.pose.orientation.w = 1.0
        return ob

    ob_low_table = setObstacle(px,py,pz-0.018,"base")
    planner.add_box_obstacle((1.50, 1.20, 0.01),"low_table",ob_low_table)
    ob_leftmost = setObstacle(0.0,1.1,0.0,"base")
    planner.add_box_obstacle((1.50, 0.01, 1.50),"leftmost",ob_leftmost)
    ob_rightmost = setObstacle(0.0,-1.1,0.0,"base")
    planner.add_box_obstacle((1.50, 0.01, 1.50),"rightmost",ob_rightmost)
    ob_front = setObstacle(1.2,0.0,0.0,"base")
    planner.add_box_obstacle((0.01, 3.00, 1.50),"front",ob_front)
    ob_back = setObstacle(-0.23,0.0,0.0,"base")
    planner.add_box_obstacle((0.01, 3.00, 1.00),"back",ob_back)

    def plan_move(x,y,z,px,py,pz,pw):
        while not rospy.is_shutdown():
            try:
                goal = PoseStamped()
                goal.header.frame_id = "base"

                goal.pose.position.x = x
                goal.pose.position.y = y 
                goal.pose.position.z = z

                goal.pose.orientation.x = px
                goal.pose.orientation.y = py
                goal.pose.orientation.z = pz
                goal.pose.orientation.w = pw

                plan = planner.plan_to_pose(goal,list())
                if not planner.execute_plan(plan):
                    raise Exception("Execution failed")
            except Exception as e:
                print e
            else:
                break

    '''
    Move to target
    '''
    print("move to target:{},{},{}".format(px,py,pz))
    plan_move(px,py,pz,0.0,-1.0,0.0,0.0)

    
    '''
    Rotate the hand with two circles and moves inward more and more
    '''
    shou = baxter_interface.Limb(hand)
    joints = shou.joint_names()
    joints_speed = dict()
    for name in joints:
        joints_speed[name] = 0
    save_joint = hand + "_s1"
    which_joint = hand + "_w2"
    joints_speed[save_joint] = -0.018
    if hand == "left":
        round_num = 3
    else:
        round_num = 1
    for i in range(round_num):
        left_gripper.command_position(60-20*i)
        joints_speed[which_joint] = 4.6
        start = time.time()
        while time.time() - start < 1.8:
            shou.set_joint_velocities(joints_speed) 
        print("{}: tick {}".format(tool,i))
        joints_speed[which_joint] = -4.6
        start = time.time()
        while time.time() - start < 1.8:
            shou.set_joint_velocities(joints_speed) 
        print("{}: tock {}".format(tool,i))


    '''
    Reset arms back to origin position
    '''
    print("Move to origin")
    if hand == "left":
        plan_move(0.300,0.854,0.116,0.0,-1.0,0.0,0.0)
    else:
        plan_move(0.300,-0.854,0.116,0.0,-1.0,0.0,0.0)


##############################################################################################################################

if __name__ == '__main__':
    rospy.init_node('moveit_node')


    # print("Locate the following positions with left hand")
    '''
    raw_input("Locate the position of (0,0) on the board. Press ENTER to continue")
    p0x,p0y,p0z = listener('left_gripper')
    print(p0x,p0y,p0z)
    raw_input("Locate the position of (9,9) on the board. Press ENTER to continue")
    p1x,p1y,p1z = listener('left_gripper')
    print(p1x,p1y,p1z)
    raw_input('Locate the position of origin of marker. Press ENTER to continue')
    p2x,p2y,p2z = listener('left_gripper')
    print(p2x,p2y,p2z)
    '''

    # p0x = 0.758
    # p0y = 0.220pro
    # p0z = -0.121
    # p1x = 0.378
    # p1y =-0.200
    # p1z = -0.121
    # p2x =0.552
    # p2y =0.569
    # p2z =0.052

    while not rospy.is_shutdown():
      hand = raw_input("Which hand: left or right? Or stop\n")
      while(hand != "left" and hand != "right" and hand != "stop"):
          print("WRONG!\n\t --- By Trump")
          hand = raw_input("Which hand: left or right? or stop\n")
      if hand == "stop":
          break
      m,n = [int(pos) for pos in raw_input("Index: {m,n}, divided with colon\n").split(",")]
        
      action(hand,m,n)