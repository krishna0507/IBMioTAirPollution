
from detect import *
import time
import sys
import pprint
import uuid
from uuid import getnode as get_mac
import requests
import subprocess

try:
	import ibmiotf.application
	import ibmiotf.device
except ImportError:
	# This part is only required to run the sample from within the samples
	# directory when the module itself is not installed.
	#
	# If you have the module installed, just use "import ibmiotf.application" & "import ibmiotf.device"
	import os
	import inspect
	cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src")))
	if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)
	import ibmiotf.application
	import ibmiotf.device

import spidev
import math
from time import strftime
import string

spi = spidev.SpiDev()
spi.open(0, 0)

def readadc(adcnum):
# read SPI data from MCP3208 chip, 8 possible adc's (0 thru 7)
        if adcnum > 7 or adcnum < 0:
                return -1
        r = spi.xfer2([1, 8 + adcnum << 4, 0])
        adcout = ((r[1] & 3) << 8) + r[2]
        return adcout

def runCommand(comm):
	'''
	Using the subprocess library this runs the command passed 
	'''
	proc = subprocess.Popen(comm.split(), stdout=subprocess.PIPE)
	outputstr = ''
	for line in proc.stdout.readlines():
		    outputstr+=line.rstrip()+"\n"	    
	return outputstr[:-1]	

def myAppEventCallback(event):
	print("Received live data from %s (%s) sent at %s: hello=%s x=%s" % (event.deviceId, event.deviceType, event.timestamp.strftime("%H:%M:%S"), data['hello'], data['x']))

def myCommandCallback(cmd):
  print("Command received: %s" % cmd.payload)
  if cmd.command == "setInterval":
    if 'interval' not in cmd.data:
      print("Error - command is missing required information: 'interval'")
    else:
      interval = cmd.data['interval']
  elif cmd.command == "print":
    if 'message' not in cmd.data:
      print("Error - command is missing required information: 'message'")
    else:
      print(cmd.data['message'])
      
      
organization = "5a7kml"
#organization = "6i6moq"
#deviceType = "rajeshpi"
deviceType = "RajeshPi"
#deviceId = str(hex(int(get_mac())))[2:]
deviceId = "b827eb1771d4"
appId = str(uuid.uuid4())
authMethod = "token"
#authToken = "nwn)7uuNo&PcHFFKEl"
authToken = "a)pg&0Wo9HUvRkeP!V"

# Initialize the device client.
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
except Exception as e:
	print(str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
connect = 0

root_url = ""
while not connect:
	try:
		
		print "in while connect"
		deviceCli.connect()
		connect = 1
	except Exception as e:
		print "Exception while Connecting"
		connect = 0
	
flag = 0
try:
	temp = getGateway("wlan0")
	requests.get("http://"+temp+":8080")
	flag = 1
	root_url = "http://"+temp+":8080"

except Exception as e:
	print "Exception on Gateway Check"
	flag = 0		

deviceCli.commandCallback = myCommandCallback
x=0
lat = "static"
long = "static"

#root_url='http://192.168.43.1:8080'
while(1):
	air_ppm = readadc(0)
	if flag != 0:
		d = requests.get(root_url).text
		#if(d.split(',')[0]!='lat'):
		#push data 
		lat = d.split(',')[0]
		long = d.split(',')[1]

	data = { 'ppm' : air_ppm, 'lat' : lat ,'long' : long , 'weight' :2 }
	deviceCli.publishEvent("Air Quality", data)
	print lat, long
	time.sleep(5)
	
	#data = { 'ppm' : air_ppm, 'lat' : 71 ,'long' : 70 , 'weight' : 2}
	#deviceCli.publishEvent("Air Quality", data)
	#time.sleep(5)
		

# Disconnect the device and application from the cloud
deviceCli.disconnect()
#appCli.disconnect()

