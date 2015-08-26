import subprocess
import os
import time

def runCommand(comm):
	'''
	Using the subprocess library this runs the command passed 
	'''
	proc = subprocess.Popen(comm.split(), stdout=subprocess.PIPE)
	outputstr = ''
	for line in proc.stdout.readlines():
		    outputstr+=line.rstrip()+"\n"	    
	return outputstr[:-1]
	


#output = runCommand("ifconfig wlan0")

def verifyConnection(interface):
	log = open("test.txt", 'w+')
	command = "ifconfig %s | grep Bcast > test.txt" % (interface)
	os.system(command)
	result = log.read()
	
	if len(result) < 1:
		#No internet present, return 0 to show it 
		print "No internet present"
		return 0
	else:
		#Internet present, so return the IP address of the gateway
		return 1
		
def getGateway(interface):
	if(verifyConnection(interface)==1):
		try:
			command = "route -n | grep UG | grep %s > test.txt" % (interface) 
			#print command
			os.system(command)
			log = open("test.txt", 'r')
			result = log.read()
			gateway = result.split()[1]
			return gateway
		except:
			return 0
	else: 
		return 0
	
def getIP(interface):
	log = open("test.txt", 'w+')
	command = "ifconfig %s | grep Bcast > test.txt" % (interface)
	os.system(command)
	result = log.read()
	
	if len(result) < 1:
		#No internet present, return 0 to show it 
		print "No internet present"
		return 0
	else:
		#Internet present, so return the IP address of the gateway
		return result.split(':')[1].split()[0]

	
	
	


