#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32MultiArray
import board
import adafruit_ccs811

i2c = board.I2C()  # uses board.SCL and board.SDA
ccs811 = adafruit_ccs811.CCS811(i2c)
rospy.init_node('AirQualitySensor')
publisher = rospy.Publisher('/AirQuality', Float32MultiArray, queue_size=1)
rate = rospy.Rate(3)

# Wait for the sensor to be ready
while not ccs811.data_ready:
    pass

while not rospy.is_shutdown():
    array = Float32MultiArray()
    #get data and send
    array.data = [ccs811.eco2, ccs811.tvoc]
    publisher.publish(array)
    rate.sleep()
