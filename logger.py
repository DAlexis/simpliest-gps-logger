#!/usr/bin/python2

import serial
from time import gmtime, strftime, sleep
import sys
import signal, os

print "Starting GPS logger"

port            = "/dev/ttyUSB0"
directory       = "./"
filenamePrefix  = "gps_track_"
filenameSuffix  = ".txt"

ser = serial.Serial()
ser.baudrate = 4800
ser.port = port

filename = directory + filenamePrefix + strftime("%Y-%m-%d_%H:%M:%S", gmtime()) + filenameSuffix

print "Writing data to " + filename + "."
outFile = open(filename, "w")

print "Opening port " + port + "..."
ser.open()

def interruptHandler(signum, frame):
    print 'Interruption handling...'
    outFile.close()
    ser.close()
    sys.exit(1)

signal.signal(signal.SIGINT, interruptHandler)

while True:
    line = ser.readline();
    fields = line.split(",");
    if fields[0] == "$GPGGA":
        timeStr = fields[1][0:2] + "-" + fields[1][2:4] + "-" + fields[1][4:10]
        print "Time: " + timeStr + ", Height: " + fields[9] + " m"
    outFile.write(line)
    

if not ser.isOpen():
    print "Cannot open port, sorry."
    outFile.close()
    sys.exit(1)

outFile.close()
ser.close()
