import pygame
import sys
from characters.mario import Mario
from stage_creator import create_stage1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Donkey Kong")

# create stage and characters
stage, characters, world = create_stage1()

running = True # variable to control the game loop
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  
  keys = pygame.key.get_pressed() # get the pressed keys

  characters["mario"].handle_movement(keys) # handle Mario's movement

  # Step the Box2D world simulation
  world.Step(1/60.0, 6, 2)

  screen.fill((0, 0, 0)) # fill the screen with black
  stage.draw(screen) # draw stage
  
  # Draw all characters
  for character in characters.values():
    character.draw(screen)

  pygame.display.update() # update the display
  pygame.time.Clock().tick(FPS) # limit the frame rate to 60 FPS

pygame.quit()
sys.exit()