#!/usr/bin/python

speed = 1 #speed variable[global] is used for controlling speed
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math


def pose_callback(msg):
    global theta                       

    theta = math.degrees(msg.theta)   #converting the theta values to degrees and storing them in variable-theta

    if theta < 0:
        theta += 360                  #converting theta's range from -180:180 to 0:360 for better calculations


def main():

    global speed
    global theta
    
    var_handle_pub = rospy.Publisher('/turtle1/cmd_vel', Twist,queue_size=15)  #creating a handle for publishing the velocity

    rospy.Subscriber('/turtle1/pose', Pose, pose_callback)  # subscribe to pose and attaching the callback function

    rospy.init_node('node_turtle_revolve', anonymous=True)  # Initialize the Node

    if theta is None:						#if theta is null,call the callback function once again
        rospy.Subscriber('/turtle1/pose', Pose, pose_callback)

    init_theta = theta	           #storing the initial theta value in a variable			

    #moving the turtle in a circle
    vel_msg = Twist()                                                          
    vel_msg.linear.x = speed
    vel_msg.angular.z = speed
    var_handle_pub.publish(vel_msg)

    rospy.loginfo(vel_msg) #print the initial value of velocity

    while True:				#infinite loop
        if (theta - init_theta) > 305:  #if the difference between initial angle and current angle is greater than 305(value obtained from trial and error),then stop the turtle  
            break

	#moving the turtle
        vel_msg = Twist()
        vel_msg.linear.x = speed
        vel_msg.angular.z = speed
        var_handle_pub.publish(vel_msg)
        rospy.loginfo(theta) #print the initial value of velocity
    
    #stop the turtle,since one revolution is complete
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0


if __name__ == '__main__':
    try:
        main()
        r = rospy.Rate(30)
        r.sleep()
    except rospy.ROSInterruptException:
        pass

