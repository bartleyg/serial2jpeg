# Python 2 script receives one JPEG image binary over USB serial from Arduino saving the file locally
import binascii
import serial
import time
import datetime
import sys

serial = serial.Serial("/dev/tty.usbmodem740901", baudrate=115200)
    
# make filename for new jpeg file
now = datetime.datetime.now()
filename = "%d.%02d.%02d.%02d.%02d.%02d.jpg" % \
(now.year,now.month,now.day,now.hour,now.minute,now.second)
file = open("./" + filename, 'wb')

data_last = 0
while 1:    # this needed b/c serial seems to be buffered on sent/receipt
    if (serial.inWaiting() > 0):
    	data = serial.read()
    	file.write(data)
    	if (data_last == b'\xFF' and data == b'\xD9'):
    		break   # exit loop and close file on jpeg footer FFD9
    	data_last = data

# Close the file
file.close()
print "Image written"
