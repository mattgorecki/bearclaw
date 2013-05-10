import serial
import re, sys, signal
from time import sleep
import RPi.GPIO as GPIO
from couchdbkit import *

print "Welcome to the Bearclaw.py"

BITRATE = 9600
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

CARDS = [
'060090840715', # Matt card
'840034BD3E33', # Matt fob
'6A003E3A2C42', # Suzy card
'840034D5DDB8', # Suzy fob
'6A003E6F556E', # Paul card
'840034CD324F', # Paul fob
'6A003E61AC99', # Marla Jo card
'6A003E247E0E', # Kathy card
'6A003E77BD9E', # Kevin card
]

# Lock the door on boot
GPIO.output(7, GPIO.HIGH)

def signal_handler(signal, frame):
  print "Closing Bearclaw"
  GPIO.output(7, GPIO.LOW)  # Unlock the door on program exit
  GPIO.cleanup()
  ser.close()
  sys.exit(0)

def unlock_door(duration):
  print "Unlocking door for %d seconds" % duration
  GPIO.output(7, GPIO.LOW)
  sleep(duration)
  print "Locking the door"
  GPIO.output(7, GPIO.HIGH)

signal.signal(signal.SIGINT, signal_handler)

ser = serial.Serial('/dev/ttyUSB0', BITRATE, timeout=0)
rfidPattern = re.compile(b'[\W_]+')

while True:
  # Read data from RFID reader
  s = ser.read(ser.inWaiting())
  if len(s) > 0:
    match = rfidPattern.sub('', s)
    if match:
      print match
      if match in CARDS:
        print 'card authorized'
      	unlock_door(10)
      else:
        print 'unauthorized card'

  # Listen for Exit Button input
  if not GPIO.input(3):
    print "button pressed"
    unlock_door(5)

  sleep(0.1)
