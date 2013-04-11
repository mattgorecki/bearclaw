import os
import pygame
import time
import random

running = 1

class Bearclaw:
  screen = None;
          
  def __init__(self):
    "initializes a new pygame screen using the framebuffer"
    disp_no = os.getenv("DISPLAY")
    if disp_no:
      print "I'm running under X display = {0}".format(disp_no)

    # Check which frame buffer drivers are available
    # Start with fbcon since directfb hangs with composite output
    drivers = ['fbcon', 'directfb', 'svgalib']
    found = False
    for driver in drivers:
      # Make sure that SDL_VIDEODRIVER is set
      if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
        try:
          pygame.display.init()
        except pygame.error:
          print 'Driver: {0} failed.'.format(driver)
          continue
        found = True
        break

    if not found:
      raise Exception('No suitable video driver found!')

    size = (320,240)
    print "Framebuffer size: %d x %d" % (size[0], size[1])
    self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    # Clear the screen to start
    self.screen.fill((0, 0, 0))        

    # Initialise font support
    pygame.font.init()
    pygame.mouse.set_visible(False)

    # Render the screen
    pygame.display.update()

  def __del__(self):
    "Destructor to make sure pygame shuts down, etc."

  def event(self):
    return pygame.event.poll()
   
  def test(self):
    black = (0, 0, 0)

    myimage = pygame.image.load("2a8.png")
    imagerect = myimage.get_rect()

    self.screen.fill(black)
    self.screen.blit(myimage, imagerect)
    pygame.display.flip()

  def black(self):
    black = (0,0,0)
    self.screen.fill(black)
    pygame.display.update()

# Create an instance of the PyScope class
bearclaw = Bearclaw()

while running:
  event = bearclaw.event()
  if event.type == pygame.QUIT:
    running = 0

  bearclaw.test()
  time.sleep(2)
  bearclaw.black()
