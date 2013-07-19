from Adafruit_MCP230xx import Adafruit_MCP230XX
import time

INPUT = True
OUTPUT = False

mcp = Adafruit_MCP230XX(busnum = 1, address = 0x20, num_gpios = 16)

mcp.config(0, OUTPUT)

while (True):
  mcp.output(0, 1)  # Pin 0 High
  time.sleep(0.5)
  mcp.output(0, 0)  # Pin 0 Low
  time.sleep(0.5)
