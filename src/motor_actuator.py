#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32MultiArray
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

servo0pin = 12
servo1pin = 13

neutral = 12

GPIO.setup(servo0pin, GPIO.OUT)
p0 = GPIO.PWM(servo0pin, 50)

GPIO.setup(servo1pin, GPIO.OUT)
p1 = GPIO.PWM(servo1pin, 50)

#Callback for received messages from roscore
def direction_callback(msg):
    duty0 = neutral
    duty1 = neutral

    #Map values of 0 to 265 to 0 to 12
    duty0 = 6 + maprange((0, 256), (0, 12), msg.data[0])
    duty1 = 6 + maprange((256, 0), (0, 12), msg.data[1])

    #If deadman's switch is active stop robot
    if msg.data[2] == 1:
        duty0 = 0;
        duty1 = 0;

    #Print received values
    print(f"{msg.data[0]} : {msg.data[1]} : {msg.data[2]}")

    #Update duty Cycles
    p0.ChangeDutyCycle(duty0)
    p1.ChangeDutyCycle(duty1)

#Function for mapping values
def maprange( a, b, s):
    (a1, a2), (b1, b2) = a, b
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

#Function for starting up servos
def servocontrol():
    p0.start(0)
    p1.start(0)

    rospy.spin()

if __name__ == "__main__":
    try:
        rospy.init_node('motor_actuator')
        rospy.Subscriber('direction_topic', Float32MultiArray, direction_callback)
        servocontrol()
    except KeyboardInterrupt:
        p0.stop()
        p1.stop()
        GPIO.cleanup()
