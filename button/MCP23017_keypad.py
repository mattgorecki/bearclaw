from Adafruit_MCP230xx import Adafruit_MCP230XX
import time

class keypad(Adafruit_MCP230XX):
  INPUT = 0
  OUTPUT = 1
  HIGH = 1
  LOW = 0

  KEYPAD = [
    [1,2,3],
    [4,5,6],
    ['nope','nope',9],
    [7,8,0],
    ['#1','#2','#3','#4'],
    ['*1','*2','*3','*4']
  ]

  ROW = [0,1,2,3,7,9]
  COLUMN = [4,5,6,8]

  def __init__(self, address=0x20, num_gpios=16):
    self.mcp2 = Adafruit_MCP230XX(address, num_gpios)
    self.debounceDelay = 50
    self.lastDebounceTime = int(round(time.time() * 1000))
    self.lastKey = ''

  def rawKey(self):
    # Set all columns as output low
    for j in range(len(self.COLUMN)):
      self.mcp2.config(self.COLUMN[j], self.mcp2.OUTPUT)
      self.mcp2.output(self.COLUMN[j], self.LOW)

    # Set all rows as input
    for i in range(len(self.ROW)):
      self.mcp2.config(self.ROW[i], self.mcp2.INPUT)
      self.mcp2.pullup(self.ROW[i], True)

    # Scan rows for pushed key/button
    # valid rowVal" should be between 0 and 3 when a key is pressed. Pre-setting it to -1
    rowVal = -1
    for i in range(len(self.ROW)):
      tmpRead = self.mcp2.input(self.ROW[i])
      # print "Row %d: %d" % (i, tmpRead)
      if tmpRead == 0:
        rowVal = i

    # if rowVal is still "return" then no button was pressed and we can exit
    if rowVal == -1:
      self.exit()
      return

    # Convert columns to input
    for j in range(len(self.COLUMN)):
      self.mcp2.config(self.COLUMN[j], self.mcp2.INPUT)

    # Switch the i-th row found from scan to output
    self.mcp2.config(self.ROW[rowVal], self.mcp2.OUTPUT)
    self.mcp2.output(self.ROW[rowVal], self.HIGH)

    # Scan columns for still-pushed key/button
    colVal = -1
    for j in range(len(self.COLUMN)):
      tmpRead = self.mcp2.input(self.COLUMN[j])
      # print "Column %d: %d" % (j, tmpRead)
      if tmpRead == 1:
        colVal=j

    if colVal == -1:
      self.exit()
      return

    # Return the value of the key pressed if the debounce delay has been passed
    self.exit()
    return self.KEYPAD[rowVal][colVal]

  def getKey(self):
    keypressTime = int(round(time.time() * 1000))

    currentKey = self.rawKey()

    if ((keypressTime - self.lastDebounceTime) > self.debounceDelay) and (currentKey != self.lastKey):
      self.lastDebounceTime = keypressTime
      self.lastKey = currentKey
      return currentKey
    else:
      return False

  def exit(self):
    # Reinitialize all rows and columns as input before exiting
    for i in range(len(self.ROW)):
      self.mcp2.config(self.ROW[i], self.INPUT) 
    for j in range(len(self.COLUMN)):
      self.mcp2.config(self.COLUMN[j], self.INPUT)

if __name__ == '__main__':
  print 'Keypad Demo'
  # Initialize the keypad class
  kp = keypad()

  # Loop while waiting for a keypress
  while True:
    r = kp.getKey()
    # Print the result
    if r:
      print "Keypress: " + str(r)
