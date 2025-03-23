import pygame
import sys
from game_defines import SCREEN_WIDTH, SCREEN_HEIGHT
from stage import create_stages
from game_state import GameState
from characters.mario import Mario

FPS = 60
LEVEL_COMPLETE_DELAY = 2.0 # delay in seconds before moving to the next level

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
  stages = create_stages()
  current_stage = stages[0]
  game_state = GameState()  # initialize game state
  mario = Mario(200, SCREEN_HEIGHT-125, current_stage.world, game_state)  # create Mario
  return game_state, mario, stages, current_stage

current_stage_index = 0
game_state, mario, stages, current_stage = new_game()

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
          current_stage_index = 0
          game_state, mario, stages, current_stage = new_game()
  
  keys = pygame.key.get_pressed() # get the pressed keys

  # Update game logic only if the game isn't over.
  if not game_state.game_over:
    mario.handle_movement(keys)
    current_stage.world.Step(dt * 50, 6, 2)
    current_stage.world.ClearForces()

    # check if Mario is on Pauline's platform
    if mario.is_on_pauline_platform():
        if not game_state.level_complete:  # only execute this once when reaching the platform
            print("Level Complete!")
            level_complete_time = pygame.time.get_ticks() / 1000.0  # Get the current time

    # If the level is complete, check if the delay has passed
    if game_state.level_complete and \
    (pygame.time.get_ticks() / 1000.0 - level_complete_time) >= LEVEL_COMPLETE_DELAY:
      game_state.next_level()
      current_stage_index += 1  # move to the next stage
      if current_stage_index >= len(stages):
          # if the last stage is complete, reset to the first stage
          print("Congratulations! You've completed all levels! Restarting...")
          current_stage_index = 0
      current_stage = stages[current_stage_index]
      # create a new Mario with the new stage's world.
      mario = Mario(SCREEN_WIDTH / 2 - 50, 0, current_stage.world, game_state)

  screen.fill((0, 0, 0))     # fill the screen (black background)
  current_stage.draw(screen) # draw stage
  game_state.draw(screen)    # draw game state
  mario.draw(screen)         # draw Mario
  pygame.display.update()    # update the display

# gracefully quit pygame and exit program
pygame.quit()
sys.exit()