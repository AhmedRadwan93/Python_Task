#!/usr/bin/env python
import math
import rospy
from nav_msgs.msg import Odometry
from  geometry_msgs.msg import Twist
# converting from quanternion into euler form.
from tf.transformations import euler_from_quaternion, quaternion_from_euler

# initializing the thre angle variables.
roll = pitch = yaw = 0.0
#initializing the required heading of the robot

print("Kindly, Enter the target angle you want the robot to move to!")
target = int(input(""))
kP = 0.5
def calculate_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)


rospy.init_node('gettingeuler')

#subscribing to the odometry topic
sub = rospy.Subscriber ('/odom', Odometry, calculate_rotation)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
r = rospy.Rate(10)
command = Twist()


while not rospy.is_shutdown():  
# yaw: is the current heading of the robot, target: is the required heading 
    target_rad = target * math.pi/180
    command.angular.z = kP * (target_rad - yaw)
    pub.publish(command)
    print("Target={}  Current:{}".format(target_rad,yaw))
    r.sleep()
