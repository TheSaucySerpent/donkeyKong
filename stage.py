import pygame
from sprite import SpriteSheet
from conversions import *
from Box2D import b2World, b2PolygonShape, b2EdgeShape
from game_defines import SCREEN_WIDTH, SCREEN_HEIGHT
from characters.mario import Mario
from enum import Enum

# the location of each sprite in the sprite sheet,
# along with the width and height of the sprite
SPRITE_COORDS = {
  "beam": (109, 215, 16, 7),
  "ladder": (40, 211, 10, 16),
  "oil_barrel": (145, 193, 16, 16),
  "upright_barrel": (112, 229, 10, 16)
}

# for creation of the beams
SLOPE = 2 
class SlopeDirection(Enum):
  NO_SLOPE = 0
  SLOPE_UP = 1
  SLOPE_DOWN = 2

class Stage:
  def __init__(self):
    self.spritesheet = SpriteSheet("assets/sprite_sheet.png")  # load the spritesheet
    self.sprites = self.load_sprites()                         # load the individual sprites
    self.elements = []                                         # the elements of the stage

    self.world = b2World(gravity=(0, -10), doSleep=False)      # create the physics world
    # create world boundaries
    self.world.CreateStaticBody(position=(0, 0), shapes=b2EdgeShape(vertices=[(0, 0), (SCREEN_WIDTH, 0)]))
    self.world.CreateStaticBody(position=(0, 0), shapes=b2EdgeShape(vertices=[(0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT)]))
    self.world.CreateStaticBody(position=(0, 0), shapes=b2EdgeShape(vertices=[(0, 0), (0, SCREEN_HEIGHT)]))
    self.world.CreateStaticBody(position=(0, 0), shapes=b2EdgeShape(vertices=[(SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)]))

    self.mario = None
  
  def get_world(self):
    return self.world

  def get_mario(self):
    return self.Mario

  def load_sprites(self):
    """load all of the sprites needed for stages"""
    loaded_sprites = {}
    for name, (x, y, width, height) in SPRITE_COORDS.items():
      sprite, _ = self.spritesheet.load_sprite((x, y), width, height) # don't need the flipped sprite for these
      loaded_sprites[name] = sprite
    return loaded_sprites
  
  def add_element(self, sprite_key, pos):
    self.elements.append({"sprite": sprite_key, "pos": pos})
  
  def add_static_object(self, key, x, y):
    dimensions = self.sprites[key].get_size()

    box2d_x = x/PPM
    box2d_y = (SCREEN_HEIGHT-y)/ PPM

    self.world.CreateStaticBody(
      position=(box2d_x, box2d_y),
      shapes=b2PolygonShape(box=(dimensions[0]/2/PPM, dimensions[1]/2/PPM))
    )
    self.add_element(key, (x, y))

  def create_beam_row(self, start_x, start_y, num_beams, slope_direction=SlopeDirection.NO_SLOPE):
    beam_width, beam_height = self.sprites["beam"].get_size()
    for i in range(num_beams):
      beam_x = start_x + i * beam_width

      # calculate beam_y based on slope direction
      if slope_direction == SlopeDirection.SLOPE_UP:
          beam_y = start_y - i * SLOPE # subtract becuase y decreases as you go up (pygame)
      elif slope_direction == SlopeDirection.SLOPE_DOWN:
          beam_y = start_y + i * SLOPE   # add because y increases as you go down (pygame)
      else:
          beam_y = start_y  # No slope
      
      self.add_static_object("beam", beam_x, beam_y)

    # return the x and y of the last beam created
    return beam_x, beam_y
  
  def draw(self, screen):
    """draw the stage and all of its elements"""
    for element in self.elements:
      sprite = self.sprites[element["sprite"]]
      screen.blit(sprite, element["pos"])
    self.mario.draw(screen)

def create_stages():
  stage1 = Stage()

  beam_width, beam_height = stage1.sprites["beam"].get_size()
  oil_barrel_width, oil_barrel_height = stage1.sprites["oil_barrel"].get_size()

  beam_x = 0
  beam_y = SCREEN_HEIGHT-50

  # first row of beams, half flat, half slope up
  beam_x, _ = stage1.create_beam_row(beam_x, beam_y, 8, SlopeDirection.NO_SLOPE)
  stage1.create_beam_row(beam_x+beam_width, beam_y, 8, SlopeDirection.SLOPE_UP)
  stage1.add_static_object("oil_barrel", beam_width, beam_y - oil_barrel_height)

  # second row of beams, all slope_down
  vertical_spacing = 80
  beam_y -= 100
  for i in range(5):
    if i % 2 == 0:
      beam_x = 0
      slope_direction = SlopeDirection.SLOPE_DOWN
      _, beam_y = stage1.create_beam_row(beam_x, beam_y, 15, slope_direction)

    else:
      beam_x = beam_width
      slope_direction = SlopeDirection.SLOPE_UP
      _, beam_y = stage1.create_beam_row(beam_x, beam_y, 15, slope_direction)
    
    beam_y -= vertical_spacing

  stage1.mario = Mario(beam_width * 3, SCREEN_HEIGHT - 100, stage1.world)

  return [stage1]