from detect import * 

while 1:
	if(verifyConnection("wlan0")==0):
		os.system("ifdown wlan0")
		os.system("ifup wlan0")
		time.sleep(20)
	else:
		time.sleep(2)
