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

def direction_callback(msg):
    duty0 = 12
    duty1 = 12

    #pot0 = ((msg[0] / 2) / 10) / 2
    #pot1 = ((msg[1] / 2) / 10) / 2

    #val = 2 + (msg[0] * 12.75)

    duty0 = 6 + maprange((0, 256), (0, 12), msg.data[0])
    duty1 = 6 + maprange((256, 0), (0, 12), msg.data[1])

    #if (msg.data[0] - 128) < 15:
    #    duty0 = 0;

    #if (msg.data[1] - 128) < 15:
    #    duty1 = 0;

    print(f"{msg.data[0]}: {duty0}")
    print(f"{msg.data[1]}: {duty1}")

    p0.ChangeDutyCycle(duty0)
    p1.ChangeDutyCycle(duty1)

def maprange( a, b, s):
    (a1, a2), (b1, b2) = a, b
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

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
