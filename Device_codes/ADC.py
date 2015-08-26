import spidev
import time
import math
from time import strftime
#import pywapi
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

'''
def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:     #just to check if adcnum is out of the A/D converters channel range
        return -1
    r = spi.xfer2([4 + (adcnum >> 2), (adcnum & 3) << 6, 0])  
#send the three bytes to the A/D in the format the A/D's datasheet explains(take time to 
#doublecheck these
    adcout = ((r[1] & 15) << 8) + r[2] 
#use AND operation with the second byte to get the last  4 bits, and then make way 
#for the third data byte with the "move 8 bits to left" << 8 operation
    #print spi.readbytes(8)
    return adcout
'''

while True:
	print readadc(0)
	time.sleep(1)
