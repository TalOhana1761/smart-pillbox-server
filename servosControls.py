import RPi.GPIO as gpio
import time

#may need to add gpio.cleanup() in main code

motorDict = {"2":11, "3":13, "1":15, "4":16}

def setupForMotors():
    gpio.setmode(gpio.BOARD)
    gpio.setup(11,gpio.OUT)
    gpio.setup(13,gpio.OUT)
    gpio.setup(15,gpio.OUT)
    gpio.setup(16,gpio.OUT)
    servo1 = gpio.PWM(11,26)
    servo1.start(0)
    servo2 = gpio.PWM(13,26)
    servo2.start(0)
    servo3 = gpio.PWM(15,26)
    servo3.start(0)
    servo4 = gpio.PWM(16,26)
    servo4.start(0)
    global servo
    servo = [servo1 , servo2 , servo3 , servo4]

# def setMotors(channel):
#     #gpio.setmode(gpio.BOARD)
#     #gpio.setwarnings(False)
#     #gpio.setup(motorDict[channel],gpio.OUT)
#     global servo
#     servo = gpio.PWM(motorDict[channel],26)
#     servo.start(0)
# 
# def moveServo(channel):
#     servo[channel - 1].start(1.9)
#     time.sleep(0.02)
#     servo[channel - 1].start(0)
#     time.sleep(0.04)

def setMotors(channel):
    servo[channel - 1].start(1.9)
    time.sleep(0.04)
    servo[channel - 1].start(0)
    time.sleep(0.4)

    
    
