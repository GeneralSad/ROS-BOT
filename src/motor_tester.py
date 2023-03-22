#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32MultiArray
import time

def main():
    pub = rospy.Publisher('direction_topic', Int32MultiArray, queue_size = 10)
       #rospy.Subscriber('direction_topic', Int32MultiArray, direction_callback)
    rospy.init_node('motor_tester')

    val1 = 255
    val2 = 255

    while not rospy.is_shutdown():
        val3 = Int32MultiArray()
        val3.data = [val1, val2]

        pub.publish(val3)

        val1 -= 10
        val2 -= 10

        if val1 <= 0:
            val1 = 255
            val2 = 255

        time.sleep(1)

if __name__ == '__main__':
    main()
