# Python 2 script receives two JPEG image binaries over USB serial from Arduino saving the files locally
import binascii
import serial
import time
import datetime
import sys

serial = serial.Serial("/dev/tty.usbmodem740901", baudrate=115200)

pics = 0
# loop receiving 2 jpeg files
while pics < 2:    
    
    # make filename for new jpeg file
    now = datetime.datetime.now()
    filename = "%d.%02d.%02d.%02d.%02d.%02d.jpg" % \
    (now.year,now.month,now.day,now.hour,now.minute,now.second)
    file = open("./" + filename, 'wb')

    # assumes first byte received is start of jpeg header FFD8
    data_last = 0
    while 1:    # this needed b/c serial seems to be buffered on sent/receipt
        if (serial.inWaiting() > 0):
            data = serial.read()
            file.write(data)
            if (data_last == b'\xFF' and data == b'\xD9'):
                break   # exit loop and close file on jpeg footer FFD9
            data_last = data

    pics += 1
    # close file
    file.close()
    print "%s written" % (filename)
