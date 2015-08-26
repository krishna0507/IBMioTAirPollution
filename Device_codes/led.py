from detect import *
import RPi.GPIO as GPIO  
import time  
# blinking function  
def on(pin):  
        GPIO.output(pin,GPIO.HIGH)  
        time.sleep(1)  
	return
def off(pin):
        GPIO.output(pin,GPIO.LOW)  
        time.sleep(1)  
        return

# to use Raspberry Pi board pin numbers  
GPIO.setmode(GPIO.BOARD)  
# set up GPIO output channel  
GPIO.setup(11, GPIO.OUT)   


while(1):
	if verifyConnection("wlan0") == 1:
		off(11)
		print "Internet Present"
	else:
		on(11)

GPIO.cleanup()
