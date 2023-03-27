#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32MultiArray
import ccs811
#import board
#import adafruit_ccs811
# import RPi.GPIO as GPIO

#i2c = board.I2C()  # uses board.SCL and board.SDA
#ccs811 = adafruit_ccs811.CCS811(i2c)
rospy.init_node('AirQualitySensor')
publisher = rospy.Publisher('/AirQuality', Float32MultiArray, queue_size=1)
rate = rospy.Rate(3)

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.cleanup

# CCS811address = 0x5A
# sensorSCL = 3
# sensorSDA = 2
# I2Cbus = 1 #according documentation RPi.GPIO

# CCs811 = GPIO.i2c_open(I2Cbus, CCS811address, 0)

ccs = ccs811.CCS811

ccs.setup()

# Wait for the sensor to be ready
while not ccs.data_available():
    pass



while not rospy.is_shutdown():
    ccs.read_logorithm_results()
    array = Float32MultiArray()
    #get data and send
    array.data = [ccs.CO2, ccs.tVOC]
    publisher.publish(array)
    rate.sleep()
