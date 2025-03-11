import pygame
import sys
from characters.mario import Mario

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Donkey Kong")

# create Mario
mario = Mario(512, 359)

running = True # variable to control the game loop
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  
  keys = pygame.key.get_pressed() # get the pressed keys
  mario.handle_movement(keys) # handle Mario's movement

  screen.fill((0, 0, 0)) # fill the screen with black
  mario.draw(screen) # draw Mario

  pygame.display.update() # update the display
  pygame.time.Clock().tick(60) # limit the frame rate to 60 FPS

pygame.quit()
sys.exit()