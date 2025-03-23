import pygame
import sys
from game_defines import SCREEN_WIDTH, SCREEN_HEIGHT
from stage import create_stages

FPS = 60

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Donkey Kong Arcade")

stage1 = create_stages()[0]

clock = pygame.time.Clock() # clock to track time
running = True # variable to control the game loop
while running:
  dt = clock.tick(FPS) / 1000.0

  # get pygame events
  for event in pygame.event.get():
    # handle quit event
    if event.type == pygame.QUIT:
      running = False
  
  keys = pygame.key.get_pressed() # get the pressed keys

  stage1.mario.handle_movement(keys) # handle Mario's movement

  # update the physics world
  stage1.world.Step(dt * 50, 6, 2)
  stage1.world.ClearForces()

  screen.fill((0, 0, 0))    # fill the screen (black background)
  stage1.draw(screen)       # draw stage
  stage1.mario.draw(screen) # draw Mario
  stage1.paulene.draw(screen) # draw Paulene
  stage1.donkey_kong.draw(screen) # draw Donkey Kong

  stage1.item_sprites.update(stage1.mario.return_rect())
  stage1.item_sprites.draw(screen)
  
  pygame.display.update()   # update the display

# gracefully quit pygame and exit program
pygame.quit()
sys.exit()