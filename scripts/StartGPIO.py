#import Paramiters to be used
import RPi.GPIO as GPIO

#set GPIO ports to GPIO mapped numbers and not pin number
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set GPIO pins to outputs
GPIO.setup(1, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

#Script
 
GPIO.output(1, GPIO.HIGH)
GPIO_Status = GPIO.input(1) #Save current state of port
print(GPIO_Status,file=open("/home/pi/savvyvan/GPIOStats/GPIO100.txt", "w"))

GPIO.output(7, GPIO.HIGH)
GPIO_Status = GPIO.input(7) #Save current state of port
print(GPIO_Status,file=open("/home/pi/savvyvan/GPIOStats/GPIO7.txt", "w"))

GPIO.output(8, GPIO.HIGH)
GPIO_Status = GPIO.input(8) #Save current state of port
print(GPIO_Status,file=open("/home/pi/savvyvan/GPIOStats/GPIO8.txt", "w"))

GPIO.output(12, GPIO.HIGH)
GPIO_Status = GPIO.input(12) #Save current state of port
print(GPIO_Status,file=open("/home/pi/savvyvan/GPIOStats/GPIO12.txt", "w"))

GPIO.output(16, GPIO.HIGH)
GPIO_Status = GPIO.input(16) #Save current state of port
print(GPIO_Status,file=open("/home/pi/savvyvan/GPIOStats/GPIO16.txt", "w"))

GPIO.output(20, GPIO.HIGH)
GPIO_Status = GPIO.input(20) #Save current state of port
print(GPIO_Status,file=open("/home/pi/savvyvan/GPIOStats/GPIO20.txt", "w"))

GPIO.output(21, GPIO.HIGH)
GPIO_Status = GPIO.input(21) #Save current state of port
print(GPIO_Status,file=open("/home/pi/savvyvan/GPIOStats/GPIO21.txt", "w"))

GPIO.output(25, GPIO.HIGH)
GPIO_Status = GPIO.input(25) #Save current state of port
print(GPIO_Status,file=open("/home/pi/savvyvan/GPIOStats/GPIO25.txt", "w"))
