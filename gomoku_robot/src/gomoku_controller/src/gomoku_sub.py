#!/usr/bin/env python
#The line above tells Linux that this file is a Python script,
#and that the OS should use the Python interpreter in /usr/bin/env
#to run it. Don't forget to use "chmod +x [filename]" to make
#this script executable.

#Import the dependencies as described in example_pub.py
import rospy
from gomoku_brain.msg import ToDoList
from gomoku_brain.msg import Position
import progresser as gomoku_mover


import display_helper

def toDoList_to_List(toDoMsg):
    eraser_list = []
    drawer_list = []


    if(len(toDoMsg.eraser) != 0):
        for p in toDoMsg.eraser:
            tup = (p.x, p.y)
            eraser_list.append(tup)

    if(len(toDoMsg.drawer) != 0):
        for p in toDoMsg.drawer:
            tup = (p.x, p.y)
            drawer_list.append(tup)    

    return eraser_list, drawer_list


#Define the callback method which is called whenever this node receives a 
#message on its subscribed topic. The received message is passed as the 
#first argument to callback().
def callback(toDoMsg):

    #Print the contents of the message to the console
    # print("Eraser %s" % len(toDoMsg.eraser))
    # print("Drawer %s" % len(toDoMsg.drawer))
    display_helper.send_image('robot')

    eraser_list, drawer_list = toDoList_to_List(toDoMsg)
    print("Eraser %s" % eraser_list)
    print("Drawer %s" % drawer_list)

    if(len(eraser_list) != 0 or len(drawer_list) > 1):
        display_helper.send_image('cheat')

    for tup in eraser_list:
        x,y = tup[0], tup[1]
        gomoku_mover.action('right',x,y)

    for tup in drawer_list:
        x,y = tup[0], tup[1]
        gomoku_mover.action('left',x,y)

    display_helper.send_image('turn')



#Define the method which contains the node's main functionality
def listener():

    #Run this program as a new node in the ROS computation graph
    #called /listener_<id>, where <id> is a randomly generated numeric
    #string. This randomly generated name means we can start multiple
    #copies of this node without having multiple nodes with the same
    #name, which ROS doesn't allow.
    rospy.init_node('gomoku_listener', anonymous=True)

    #Create a new instance of the rospy.Subscriber object which we can 
    #use to receive messages of type std_msgs/String from the topic /chatter_talk.
    #Whenever a new message is received, the method callback() will be called
    #with the received message as its first argument.
    rospy.Subscriber("gomoku_channel", ToDoList, callback)


    #Wait for messages to arrive on the subscribed topics, and exit the node
    #when it is killed with Ctrl+C
    rospy.spin()


#Python's syntax for a main() method
if __name__ == '__main__':
    listener()
