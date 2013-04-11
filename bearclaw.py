import serial
import re
from time import sleep

bitrate = 9600

ser = serial.Serial('/dev/ttyUSB0', bitrate, timeout=0)
rfidPattern = re.compile('[\W_]+')

while True:
  # Read data from RFID reader
  s = ser.read(ser.inWaiting())
  #s = ser.read(12)
  if len(s) > 0:
    print rfidPattern.sub('', s)

  # Listen for Exit Button input

  sleep(2)

ser.close()
