
#import Paramiters to be used
import RPi.GPIO as GPIO
from datetime import datetime
import os
import time

#set date strings
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
current_date = now.strftime("%Y%m%d")

#------------Set GPIO Port numbers------------
Buzzer=17 #Buzzer GPIO Port
GPIOPort=20 #Buzzer GPIO Port
#---------------------------------------------

#set GPIO ports to GPIO mapped numbers and not pin number
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set GPIO pins to outputs
GPIO.setup(GPIOPort, GPIO.OUT)
GPIO.setup(Buzzer, GPIO.OUT)

#Script
#Tap Noise
GPIO.output(Buzzer,GPIO.HIGH)
time.sleep(0.02)
GPIO.output(Buzzer,GPIO.LOW)

GPIO_Status = GPIO.input(GPIOPort) #Save current state of port
GPIO_Status_Log = str(GPIO_Status) #save data to string for log concastination
GPIOPortSTR = str(GPIOPort) #save data to string for Flag concastination

#print(current_time + " "  + os.path.realpath(__file__) + " Start PinStatus=" + GPIO_Status_Log,file=open("log/master" +current_date+ ".txt", "a")) #write to log

if GPIO_Status > 0: #If the port is set to 1 then set to 0
    GPIO.output(GPIOPort, GPIO.LOW)
else: # Otherwise set to 1
    GPIO.output(GPIOPort, GPIO.HIGH)

GPIO_Status = GPIO.input(GPIOPort) #Save current state of port
GPIO_Status_Log = str(GPIO_Status)

print(GPIO_Status,file=open("/home/pi/savvyvan/GPIOStats/GPIO" + GPIOPortSTR + ".txt", "w")) #Set new flag for webapp
#print(current_time + " "  +os.path.realpath(__file__) + " Finish PinStatus=" + GPIO_Status_Log,file=open("log/master" +current_date+ ".txt", "a")) #write to log
