import pygame
pygame.init()

window = pygame.display.set_mode((320, 240))
pygame.display.set_caption('Bearclaw')

colour = pygame.Color('blue')

while True:
  pygame.draw.rect(window, colour, (0, 0, 100, 100))
  pygame.display.flip()
