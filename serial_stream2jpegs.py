# Python 2 script receives a continuous stream of JPEG image binaries, 2 at a time, over USB serial from Arduino saving the files locally
import serial
import datetime
import os
import sys
import argparse

# parse command line options
parser = argparse.ArgumentParser(description='Receives binary jpeg images from serial')
parser.add_argument('-tty', '-t', required=False, default='/dev/tty.usbmodem1121181', help='Serial device')
parser.add_argument('-baud', '-b', type=int, required=False, default=115200, help='Serial port speed')
args = vars(parser.parse_args())

tty = args['tty']
baud = args['baud']

serial = serial.Serial(tty, baud, timeout=1)
snap = 1

# make a folder for these files to save to
now = datetime.datetime.now() # set time of 2 snapshot
path = "."
folder = "%s/%d.%02d.%02d.%02d.%02d.%02d" % \
        (path,now.year,now.month,now.day,now.hour,now.minute,now.second)
os.system("mkdir %s" % (folder))
print "folder %s created" % folder

first_run = 1

# loop continuously receiving multiple jpeg snapshot pairs
while 1:
    pic = 1
    print "SNAP %d!" % snap

    # make filename for new jpeg file
    now = datetime.datetime.now() # set time of 2 snapshot
    
    while pic <= 2:  # loop receiving 2 jpeg snapshot files
        if (pic == 1):
            filename = "%02d.%02d.%02d.A.jpg" % (now.hour,now.minute,now.second)
        elif (pic == 2):
            filename = "%02d.%02d.%02d.B.jpg" % (now.hour,now.minute,now.second)
        file = open(folder + "/" + filename, 'wb')

        # assumes first byte received is start of jpeg header FFD8
        data_last = 0
        while 1:    # this needed b/c serial seems to be buffered on sent/receipt
            if (serial.inWaiting() > 0):
                if (first_run == 1):
                    now = datetime.datetime.now()
                    if (pic == 1):
                        filename = "%02d.%02d.%02d.A.jpg" % (now.hour,now.minute,now.second)
                    elif (pic == 2):
                        filename = "%02d.%02d.%02d.B.jpg" % (now.hour,now.minute,now.second)
                    file = open(folder + "/" + filename, 'wb')
                    first_run = 0
                data = serial.read()
                file.write(data)
                if (data_last == b'\xFF' and data == b'\xD9'):
                    break   # exit loop and close file on jpeg footer FFD9
                data_last = data

        pic += 1
        # close file
        file.close()
        print "%s saved" % filename
        os.system("open " + folder + "/" + "%s" % (filename))
    snap += 1
