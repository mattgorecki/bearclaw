import serial
import re
from time import sleep

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0)
rfidPattern = re.compile('[\W_]+')

while True:
  # Read data from RFID reader
  s = ser.read(ser.inWaiting())
  if len(s) > 0:
    print rfidPattern.sub('', s)

  # Listen for Exit Button input

  sleep(0.5)

ser.close()
