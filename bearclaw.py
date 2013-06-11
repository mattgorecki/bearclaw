#!/usr/bin/python
import serial
import re, sys, signal, os, time
import RPi.GPIO as GPIO
from couchdbkit import *

print "Welcome to the Bearclaw.py"

BITRATE = 9600
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

CARDS = [
'060090840715', # Matt Gorecki card
'840034BD3E33', # Matt Gorecki fob
'6A003E3A2C42', # Suzy Williams card
'840034D5DDB8', # Suzy Williams fob
'6A003E6F556E', # Paul Williams card
'840034CD324F', # Paul Williams fob
'6A003E61AC99', # Marla Jo Gorecki card
'6A003E247E0E', # Kathy Carrette card
'6A003E77BD9E', # Kevin Hamm card
'6A003E7BB19E', # Grant Austin card
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
  time.sleep(duration)
  print "Locking the door"
  GPIO.output(7, GPIO.HIGH)

signal.signal(signal.SIGINT, signal_handler)

ser = serial.Serial('/dev/ttyUSB0', BITRATE, timeout=0)
rfidPattern = re.compile(b'[\W_]+')
buffer = ''

while True:
  # Read data from RFID reader
  buffer = buffer + ser.read(ser.inWaiting())
  if '\n' in buffer:
    lines = buffer.split('\n')
    last_received = lines[-2]
    match = rfidPattern.sub('', last_received)

    if match:
      print match
      if match in CARDS:
        print 'card authorized'
        with open('/opt/bearclaw/access_log', 'a') as f:
          f.write('%s::%s::authorized\n' % (time.strftime("%a, %d %b %Y %H:%M:%S %z", time.gmtime()), match))
      	unlock_door(10)
      else:
        print 'unauthorized card'
        with open('/opt/bearclaw/error_log', 'a') as f:
          f.write('%s::%s::unauthorized\n' % (time.strftime("%a, %d %b %Y %H:%M:%S %z", time.gmtime()), match))

    # Clear buffer
    buffer = ''
    lines = ''

  # Listen for Exit Button input
  if not GPIO.input(3):
    print "button pressed"
    unlock_door(5)

  time.sleep(0.1)
