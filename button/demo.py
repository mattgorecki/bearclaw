from MCP23017_keypad import keypad

# Initialize the keypad class
kp = keypad()

def digit():
  # Loop while waiting for a keypress
  while True:
    key = kp.getKey()
    if key:
      return key

print "Please enter a 4 digit code: "

# Getting digit 1, printing it, then sleep to allow the next digit press.
d1 = digit()
print d1

d2 = digit()
print d2

d3 = digit()
print d3

d4 = digit()
print d4

# printing out the assembled 4 digit code.
print "You Entered %s%s%s%s "%(d1,d2,d3,d4)
