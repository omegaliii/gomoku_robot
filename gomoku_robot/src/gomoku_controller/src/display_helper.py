import os
import sys
import argparse

import rospy

import cv2
import cv_bridge

from sensor_msgs.msg import (
    Image,
)


def send_image(image_name):
    """
    Send the image located at the specified path to the head
    display on Baxter.
    @param path: path to the image file to load and send
    """
    # '/scratch/shared/baxter_ws/src/baxter_examples/share/images/baxterworking.png'

    abs_path = '/home/cc/ee106a/fa18/class/ee106a-adp/ros_workspaces/gomoku_robot/src/gomoku_cv/image/'+ image_name +'.jpg'
    img = cv2.imread(os.path.join(abs_path))
    msg = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
    pub = rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=1)
    pub.publish(msg)
    # Sleep to allow for image to be published.
    rospy.sleep(1)
