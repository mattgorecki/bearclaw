#!/usr/bin/python2
import serial
import re, sys, signal, os, time, datetime
import RPi.GPIO as GPIO
import daemon
import daemon.pidfile
import db

print "Welcome to the Bearclaw.py"

BITRATE = 9600
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Lock the door on boot
GPIO.output(7, GPIO.HIGH)

pidfile = daemon.pidfile.PIDLockFile("/var/run/bearclaw.pid")

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
'840034D6CEA8', # Ryan Carsten fob
]

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

if __name__ == '__main__':
  #with daemon.DaemonContext(pidfile=pidfile, working_directory='/opt/bearclaw'):
    buffer = ''
    ser = serial.Serial('/dev/ttyUSB0', BITRATE, timeout=0)
    rfidPattern = re.compile(b'[\W_]+')
    signal.signal(signal.SIGINT, signal_handler)

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
            unlock_door(10)
            db.Log(
              event = "authorized",
              key_id = match,
              event_time = datetime.datetime.now()
            ).save()
          else:
            print 'unauthorized card'
            db.Log(
              event = "unauthorized",
              key_id = match,
              event_time = datetime.datetime.now()
            ).save()

        # Clear buffer
        buffer = ''
        lines = ''

      # Listen for Exit Button input
      if not GPIO.input(3):
        print "button pressed"
        unlock_door(5)
        db.Log(
          event = "exit_button",
          key_id = "exit_button",
          event_time = datetime.datetime.now()
        ).save()

      time.sleep(0.1)
