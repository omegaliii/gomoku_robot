#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from gomoku_brain.srv import ImageSrv, ImageSrvResponse
import cv2, time, sys
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from numpy.linalg import *

import cvh
import display_helper

from gomoku_brain.msg import ToDoList
from gomoku_brain.msg import Position
import wegame as gomoku_ai

cheated = False

OLD_BROAD = [[0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0]]


# Create a CvBridge to convert ROS messages to OpenCV images
bridge = CvBridge()

# Converts a ROS Image message to a NumPy array to be displayed by OpenCV
def ros_to_np_img(ros_img_msg):
  return np.array(bridge.imgmsg_to_cv2(ros_img_msg,'bgr8'))

def list_to_ToDoList(py_eraser, py_drawer):
  toDoListObj = ToDoList()
  if len(py_eraser) != 0:
      for tup in py_eraser:
          point = Position()
          point.x = tup[0]
          point.y = tup[1]
          toDoListObj.eraser.append(point)
  
  if len(py_drawer) != 0:
      for tup in py_drawer:
          point = Position()
          point.x = tup[0]
          point.y = tup[1]
          toDoListObj.drawer.append(point)
  
  return toDoListObj

# Define the total number of clicks we are expecting (4 corners)
TOT_CLICKS = 6

if __name__ == '__main__':
  
  # Waits for the image service to become available
  rospy.wait_for_service('last_image')
  
  # Initializes the image processing node
  rospy.init_node('image_processing_node')

  pub = rospy.Publisher('gomoku_channel', ToDoList, queue_size=10)
  r = rospy.Rate(10) 
  
  # Creates a function used to call the 
  # image capture service: ImageSrv is the service type
  last_image_service = rospy.ServiceProxy('last_image', ImageSrv)




  display_helper.send_image('gomoku')

  while not rospy.is_shutdown():
    
    try:
      # Waits for a key input to continue
      raw_input('Press enter to capture an image:')
    except KeyboardInterrupt:
      print 'Break from raw_input'
      break
    
    try:
      # Request the last image from the image service
      # And extract the ROS Image from the ImageSrv service
      # Remember that ImageSrv.image_data was
      # defined to be of type sensor_msgs.msg.Image
      # display_helper.send_image('gomoku')
      ros_img_msg = last_image_service().image_data

      # Convert the ROS message to a NumPy image
      np_image = ros_to_np_img(ros_img_msg)
      cv2.imshow("pic", np_image)      

      try:
        board_martix = cvh.pic2matrix(np_image)
      except Exception:
        board_martix = None


      print(board_martix)
      print(OLD_BROAD)

      # gomuku_ai.next would generate 
      # a python list of points to erease
      # and a python list of points to draw
      try:
        erasing_list, drawing_list = gomoku_ai.detector(OLD_BROAD, board_martix)
      except Exception:
        erasing_list, drawing_list = [], []

      OLD_BROAD = board_martix
      for point in erasing_list:
        OLD_BROAD[point[0],point[1]] = 0
      for point in drawing_list:
        OLD_BROAD[point[0],point[1]] = 2

      if(board_martix is not None):
        if gomoku_ai.check_win(board_martix, 1) == 'player':
          display_helper.send_image('win')
          break
      elif(board_martix is not None and gomoku_ai.check_win(board_martix, 2) == 'robot'):
        display_helper.send_image('lose')
        break

      # ereasing_list = [(1,2),(3,4)]
      # drawing_list = []
      print("erasing_list",erasing_list)
      print("drawing_list", drawing_list)

      # Parsing the two python list to the toDoList object
      to_pub_toDoList = list_to_ToDoList(erasing_list, drawing_list)

      # Publish the toDoList to the topic 'gomuku_channel'
      pub.publish(to_pub_toDoList)
      r.sleep()


    except KeyboardInterrupt:
      print 'Keyboard Interrupt, exiting'
      # This is placeholder code that will draw a 4 by 3 grid in the corner of
      # the image
      break

    # Catch if anything went wrong with the Image Service
    except rospy.ServiceException, e:
      print "image_process: Service call failed: %s"%e
    
  cv2.destroyAllWindows()

