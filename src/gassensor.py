#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32MultiArray
import RPi.GPIO as GPIO
import dht11

#init node
rospy.init_node('AirQualitySensor')
publisher = rospy.Publisher('/AirQuality', Float32MultiArray, queue_size=1)
rate = rospy.Rate(3)

#setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup

# create sensor
sensor = dht11.DHT11(pin = 21)

while not rospy.is_shutdown():
    array = Float32MultiArray()
    #get data and send
    measurement = sensor.read()
    if(measurement.is_valid()):
        array.data = [measurement.humidity, measurement.temperature]
        publisher.publish(array)
    rate.sleep()
