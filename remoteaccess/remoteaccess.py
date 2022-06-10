import urllib.request
import subprocess
import os
from socket import timeout
import random
import string
import time
import psutil

#Define Varabile
host = "http://www.google.co.uk"
host1 = "http://remote.savvyvan.co.uk"
timeout = 10
status = False
process_active = True
repeat = True

#Define process check
def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

#Check to see if the subdomain has been created, if so load, if not create random
file_path = 'subdomain.txt'
# check if size of file is 0
if os.stat(file_path).st_size == 0:
	letters = string.ascii_lowercase
	subdomain = (''.join(random.choice(letters) for i in range(10)) )
	print(subdomain,file=open("subdomain.txt", "w"))
	print("Subdoman was empty, created: " + subdomain)
	
else:
	fileObject = open("subdomain.txt", "r")
	subdomain = fileObject.read()
	print("Subdomain was already created: " + subdomain)
	fileObject.close()

subdomain = subdomain.replace(" ","")

#Main Script
while repeat==True:

	#Check if LocalTunnel is currently active
	if checkIfProcessRunning('node'):
		print('Remote Access process is running')
		time.sleep(60)

	#If not active, check for internet cnnectivity
	else:
		
		#Check Internet connection. Attempt to connect to Host, if failure try Host1
		while status==False:
			def connect():
				try:
					urllib.request.urlopen(host, timeout=timeout) #Python 3.x
					return True
				except:
					return False

			status = connect()
			if status >= True:
				remoteaccess = str("Internet Connected, Please Wait for Remote Access to be Established...")
			else:
				def connect():
					try:
						urllib.request.urlopen(host1, timeout=timeout) #Python 3.x
						return True
					except:
						return False
				
				#Return result to remoteaccess
				status = connect()
				if status >= True :
					remoteaccess = str("Internet Connected, Please Wait for Remote Access to be Established..")
				else:
					remoteaccess = str("No Internet Connection")
			print(remoteaccess,file=open("/home/pi/savvyvan/message.txt", "w"))
			print(remoteaccess)
			time.sleep(60)

		
		#Connect Remote access and display results
		remoteaccess = str('Connecting...')
		print(remoteaccess,file=open("/home/pi/savvyvan/remoteaccess/message.txt", "w"))
		#subprocess.call(["lt", "--port", "3001", "--host", "http://remote.savvyvan.co.uk:8080", "--subdomain", subdomain, ">>", "message.txt"]) # enter the remote access script here. (Spaces need "Text", "More text", "Etc")
		#remoteaccess = ("Your Remote Access URL is:\nhttp://"+ subdomain +".remote.savvyvan.co.uk:8080")
		#print(remoteaccess)
		print(str("Your Remote Access URL is: \n http://" + subdomain + ".remote.savvyvan.co.uk:8080"),file=open("/home/pi/savvyvan/remoteaccess/message.txt", "w"))
		os.system("lt --port 3001 --host http://remote.savvyvan.co.uk:8080 --subdomain " + subdomain)
		print('Disconnected')
		remoteaccess = str('Disconnected')
		print(remoteaccess,file=open("/home/pi/savvyvan/remoteaccess/message.txt", "w"))
			
	time.sleep(60)
		

