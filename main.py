import pygame
import sys
from game_defines import SCREEN_WIDTH, SCREEN_HEIGHT
from stage import create_stages
from game_state import GameState
from characters.mario import Mario

FPS = 60

# initialize pygame & pygame mixer
pygame.mixer.pre_init(44100, -16, 2, 8192)
pygame.init()

# load the music file
pygame.mixer.music.load("assets/level_music.wav")
pygame.mixer.music.set_volume(0.5) # set the volume

# play the music infinitely
pygame.mixer.music.play(-1)

# create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Donkey Kong Arcade")

def new_game():
  stage1 = create_stages()[0]
  game_state = GameState() # initialze game state
  mario = Mario(120, SCREEN_HEIGHT - 100, stage1.world, game_state) # create Mario
  return stage1, game_state, mario


stage1, game_state, mario = new_game()

clock = pygame.time.Clock() # clock to track time
running = True # variable to control the game loop
while running:
  dt = clock.tick(FPS) / 1000.0

  # get pygame events
  for event in pygame.event.get():
    # handle quit event
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      # When game is over and space is pressed, restart the game.
      if game_state.game_over and event.key == pygame.K_SPACE:
          stage1, game_state, mario = new_game()
  
  keys = pygame.key.get_pressed() # get the pressed keys

  # Update game logic only if the game isn't over.
  if not game_state.game_over:
    mario.handle_movement(keys)
    stage1.world.Step(dt * 50, 6, 2)
    stage1.world.ClearForces()

  screen.fill((0, 0, 0))    # fill the screen (black background)
  stage1.draw(screen)       # draw stage
  game_state.draw(screen)   # draw game state
  mario.draw(screen) # draw Mario
  pygame.display.update()   # update the display

# gracefully quit pygame and exit program
pygame.quit()
sys.exit()