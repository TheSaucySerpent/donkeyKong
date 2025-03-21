import pygame
import sys
from stage_creator import create_stage1
from conversions import *

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Donkey Kong")

# create stage and characters (initially only 1 stage, will add more later)
stage, characters, world = create_stage1()

running = True # variable to control the game loop
while running:
  # get pygame events
  for event in pygame.event.get():
    # handle quit event
    if event.type == pygame.QUIT:
      running = False
  
  keys = pygame.key.get_pressed() # get the pressed keys

  characters["mario"].handle_movement(keys) # handle Mario's movement

  # update the physics world
  world.Step(1.0 / 50.0, 6, 2)
  world.ClearForces()

  screen.fill((0, 0, 0)) # fill the screen (black background)
  stage.draw(screen) # draw stage
  
  # Draw all characters
  for character in characters.values():
    character.draw(screen)

  pygame.display.update() # update the display
  pygame.time.Clock().tick(FPS) # limit the frame rate to 60 FPS

# gracefully quit pygame and exit program
pygame.quit()
sys.exit()