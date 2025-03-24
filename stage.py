import pygame
from sprite import SpriteSheet
from conversions import *
from Box2D import b2World, b2PolygonShape, b2EdgeShape
from game_defines import *
from characters.mario import Mario
from characters.paulene import Paulene
from characters.donkey_kong import Donkey_Kong
from items.hammer import Hammer
from items.paulene_hat import Paulene_Hat
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
SLOPE = 0
class SlopeDirection(Enum):
  NO_SLOPE = 0
  SLOPE_UP = 1
  SLOPE_DOWN = 2

class Stage:
  def __init__(self,donkey_kong_pos, paulene_pos,mario_pos):
    self.spritesheet = SpriteSheet("assets/sprite_sheet.png")  # load the spritesheet
    self.sprites = self.load_sprites()                         # load the individual sprites
    self.elements = []                                         # the elements of the stage

  
    self.mario_start_pos = mario_pos
    self.donkey_kong = Donkey_Kong(donkey_kong_pos)
    self.paulene = Paulene(paulene_pos)
    self.item_sprites = pygame.sprite.Group()

    self.world = b2World(gravity=(0, -10), doSleep=False)      # create the physics world
    # create world boundaries
    self.world.CreateStaticBody(position=(0, 0), shapes=b2EdgeShape(vertices=[(0, 0), (SCREEN_WIDTH, 0)]))
    self.world.CreateStaticBody(position=(0, 0), shapes=b2EdgeShape(vertices=[(0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT)]))
    self.world.CreateStaticBody(position=(0, 0), shapes=b2EdgeShape(vertices=[(0, 0), (0, SCREEN_HEIGHT)]))
    self.world.CreateStaticBody(position=(0, 0), shapes=b2EdgeShape(vertices=[(SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)]))
  
  def get_world(self):
    return self.world

  def load_sprites(self):
    """load all of the sprites needed for stages"""
    loaded_sprites = {}
    for name, (x, y, width, height) in SPRITE_COORDS.items():
      sprite, _ = self.spritesheet.load_sprite((x, y), width, height) # don't need the flipped sprite for these
      loaded_sprites[name] = sprite
    return loaded_sprites
  
  def add_static_object(self, key, x, y, category_bits=GROUND_CATEGORY_BITS):
    dimensions = self.sprites[key].get_size()

    box2d_x = x/PPM
    box2d_y = (SCREEN_HEIGHT-y)/ PPM

    body = self.world.CreateStaticBody(
      position=(box2d_x, box2d_y),
      shapes=b2PolygonShape(box=(dimensions[0]/2/PPM, dimensions[1]/2/PPM))
    )

    # apply collision filtering
    fixture = body.fixtures[0]
    filterdata = fixture.filterData
    filterdata.categoryBits = category_bits
    filterdata.maskBits = MARIO_CATEGORY_BITS | GROUND_CATEGORY_BITS
    fixture.filterData = filterdata

    # Store both the sprite key and the Box2D body for drawing
    self.elements.append({"sprite": key, "body": body})

  def create_beam_row(self, start_x, start_y, num_beams, slope_direction=SlopeDirection.NO_SLOPE, category_bits=GROUND_CATEGORY_BITS,SLOPE = 0):
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
      
      self.add_static_object("beam", beam_x, beam_y, category_bits)

    # return the x and y of the last beam created
    return beam_x, beam_y

  def create_ladder(self, x, y, double_ladder=False):
    def add_ladder(x_pos, y_pos):
        ladder_width, ladder_height = self.sprites["ladder"].get_size()

        box2d_x = x_pos / PPM
        box2d_y = (SCREEN_HEIGHT - y_pos) / PPM

        # Create the ladder as a static body
        ladder_body = self.world.CreateStaticBody(position=(box2d_x, box2d_y))
        ladder_fixture = ladder_body.CreateFixture(
            shape=b2PolygonShape(box=(ladder_width / 2 / PPM, ladder_height / 2 / PPM)),
            isSensor=True
        )

        # Add collision filtering
        filterdata = ladder_fixture.filterData
        filterdata.categoryBits = LADDER_CATEGORY_BITS
        filterdata.maskBits = MARIO_CATEGORY_BITS | GROUND_CATEGORY_BITS
        ladder_fixture.filterData = filterdata

        self.elements.append({"sprite": "ladder", "body": ladder_body})

    # Create the first ladder
    add_ladder(x, y)

    # Create the second ladder if double_ladder is True
    if double_ladder:
        add_ladder(x, y - self.sprites["ladder"].get_size()[1])  # Stack on top of the first ladder

  def create_pauline_platform(self, x, y):
    beam_width, _ = self.sprites["beam"].get_size()
    beam_x, beam_y = self.create_beam_row(x, y, 3, SlopeDirection.NO_SLOPE, PAULINE_PLATFORM_CATEGORY_BITS)
    
    ladder_x = beam_x + beam_width
    ladder_y = beam_y + self.sprites["ladder"].get_size()[1] / 2
    self.create_ladder(ladder_x, ladder_y, double_ladder=True)

  def create_stacked_barrels(self, x, y):
    upright_barrel_width, upright_barrel_height = self.sprites["upright_barrel"].get_size()

    for row in range(2):
      for col in range(2):
        barrel_x = x + col * upright_barrel_width
        barrel_y = y - row * upright_barrel_height
        self.add_static_object("upright_barrel", barrel_x, barrel_y)
  
  def draw(self, screen):
    """Draw the stage elements based on their hitboxes."""
    for element in self.elements:
        sprite = self.sprites[element["sprite"]]
        # Convert the body's position (center) from Box2D to screen coordinates
        pos = box2d_to_pygame((element["body"].position.x, element["body"].position.y))
        rect = sprite.get_rect(center=pos)
        screen.blit(sprite, rect.topleft)

    self.paulene.draw(screen)
    self.donkey_kong.draw(screen)
    self.item_sprites.draw(screen)

  def update_items(self,Mario,game_state):
    self.item_sprites.update(Mario,game_state)


def create_stages():
  stage1 = Stage(donkey_kong_pos=(85,23),paulene_pos=(245,15),mario_pos=(200, SCREEN_HEIGHT-85))

  beam_width, beam_height = stage1.sprites["beam"].get_size()
  oil_barrel_width, oil_barrel_height = stage1.sprites["oil_barrel"].get_size()

  beam_x = 0
  beam_y = SCREEN_HEIGHT-50

  # first row of beams, half flat, half slope up
  beam_x, _ = stage1.create_beam_row(beam_x, beam_y, 8, SlopeDirection.NO_SLOPE)
  stage1.create_beam_row(beam_x+beam_width, beam_y, 8, SlopeDirection.SLOPE_UP)
  stage1.add_static_object("oil_barrel", beam_width, beam_y - beam_height/2 - oil_barrel_height/2)

  # create slanted beams (alternating slope directions)
  vertical_spacing = 100
  beam_y -= 125
  for i in range(4):
    if i % 2 == 0:
      beam_x = 0
      slope_direction = SlopeDirection.SLOPE_DOWN
      _, beam_y = stage1.create_beam_row(beam_x, beam_y, 14, slope_direction)

    else:
      beam_x = beam_width*2
      slope_direction = SlopeDirection.SLOPE_UP
      _, beam_y = stage1.create_beam_row(beam_x, beam_y, 15, slope_direction)
    
    beam_y -= vertical_spacing
  
  # create final row (which holds Donkey Kong) - half flat, half slope down
  beam_x = 0
  beam_y += 10
  beam_x, _ = stage1.create_beam_row(beam_x, beam_y, 9, SlopeDirection.NO_SLOPE)
  stage1.create_beam_row(beam_x+beam_width, beam_y, 5, SlopeDirection.SLOPE_DOWN)

  # create upright barrels next to Donkey Kong
  oil_barrel_width, upright_barrel_height = stage1.sprites["upright_barrel"].get_size()
  stage1.create_stacked_barrels(oil_barrel_width, beam_y - beam_height/2 - upright_barrel_height/2)
  
  # create ladders

  # first floor ladders
  ladder_x = beam_width * 13
  ladder_y = SCREEN_HEIGHT - 90
  stage1.create_ladder(ladder_x, ladder_y, double_ladder=True)
  
  # second floor ladders
  ladder_x = beam_width * 3
  ladder_y -= 110
  stage1.create_ladder(ladder_x, ladder_y, double_ladder=True)
  ladder_x = beam_width * 8
  stage1.create_ladder(ladder_x, ladder_y, double_ladder=True)

  # third floor ladders
  ladder_x = beam_width * 9
  ladder_y -= 100
  stage1.create_ladder(ladder_x, ladder_y, double_ladder=True)
  ladder_x = beam_width * 13
  stage1.create_ladder(ladder_x, ladder_y, double_ladder=True)

  # fourth floor ladders
  ladder_x = beam_width * 4
  ladder_y -= 100
  stage1.create_ladder(ladder_x, ladder_y, double_ladder=True)

  # fifth floor ladders
  ladder_x = beam_width * 13
  ladder_y -= 100
  stage1.create_ladder(ladder_x, ladder_y, double_ladder=True)

  # create Pauline platform
  stage1.create_pauline_platform(beam_width*5, 70)

  stage1.item_sprites.add(Hammer((300,600)))


  stage2 = Stage(donkey_kong_pos=(85,23),paulene_pos=(245,15),mario_pos=(100,625))
  beam_width, beam_height = stage2.sprites["beam"].get_size()
  beam_x = 0
  beam_y = SCREEN_HEIGHT-50

  # Start Beam
  beam_x, _ = stage2.create_beam_row(beam_x, beam_y, 4, SlopeDirection.NO_SLOPE)

  # Replace this beam with moving platform going left and right
  stage2.create_beam_row(220, beam_y, 2, SlopeDirection.NO_SLOPE)


  stage2.create_beam_row(600,beam_y, 4, SlopeDirection.NO_SLOPE)

  # First floor ladder 
  ladder_x = beam_width * 13
  ladder_y = SCREEN_HEIGHT - 90
  stage2.create_ladder(ladder_x, ladder_y, double_ladder=True)
  ladder_y = SCREEN_HEIGHT - 185
  stage2.create_ladder(ladder_x, ladder_y, double_ladder=False)

  stage2.create_ladder(440, 200, double_ladder=True)

  stage2.create_ladder(50, 440, double_ladder=True)
  stage2.create_ladder(50, 340, double_ladder=True)

  stage2.create_beam_row(600,beam_y- 170, 4, SlopeDirection.NO_SLOPE)

  # Should be moving platforms
  stage2.create_beam_row(300,beam_y- 170, 2, SlopeDirection.NO_SLOPE)
  stage2.create_beam_row(200,beam_y -400, 2, SlopeDirection.NO_SLOPE)


  stage2.create_beam_row(0,beam_y -400, 2, SlopeDirection.NO_SLOPE)


  stage2.create_beam_row(600,beam_y- 400, 12, SlopeDirection.NO_SLOPE)

  stage2.create_beam_row(0,beam_y- 170, 2, SlopeDirection.NO_SLOPE)
  stage2.create_pauline_platform(beam_width*5, 70)
  stage2.create_beam_row(0, beam_y-510, 10, SlopeDirection.SLOPE_DOWN)

  stage2.item_sprites.add(Paulene_Hat((600,210)))
  stage2.create_stacked_barrels(oil_barrel_width, 100)


  return [stage1, stage2]