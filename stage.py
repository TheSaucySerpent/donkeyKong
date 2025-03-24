# Skyler Burden, Halie Numinen, Andrew Hua

import pygame
from sprite import SpriteSheet
from conversions import *
from Box2D import b2World, b2PolygonShape, b2EdgeShape, b2CircleShape, b2Vec2
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
  "barrel": (2,232,13,10),
  "upright_barrel": (112, 229, 10, 16)
}

BARREL_SPEED = 5/PPM


# for creation of the beams
SLOPE = 1
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

    self.world = b2World(gravity=(0, -0.01), doSleep=False)      # create the physics world

    self.moving_platforms = []
    self.barrels = []

    # create world boundaries
    self.create_boundary_wall([(0, SCREEN_HEIGHT / PPM), (SCREEN_WIDTH / PPM, SCREEN_HEIGHT / PPM)],
                              TOP_BOUNDARY_CATEGORY_BITS)
    self.create_boundary_wall([(0, 0), (SCREEN_WIDTH / PPM, 0)],
                              BOTTOM_WORLD_BOUNDARY_CATEGORY_BITS)
    self.create_boundary_wall([(0, 0), (0, SCREEN_HEIGHT / PPM)],
                              LEFT_WORLD_BOUNDARY_CATEGORY_BITS)
    self.create_boundary_wall([(SCREEN_WIDTH / PPM, 0), (SCREEN_WIDTH / PPM, SCREEN_HEIGHT / PPM)],
                              RIGHT_WORLD_BOUNDARY_CATEGORY_BITS)
  
  def get_world(self):
    return self.world

  def load_sprites(self):
    """load all of the sprites needed for stages"""
    loaded_sprites = {}
    for name, (x, y, width, height) in SPRITE_COORDS.items():
      sprite, _ = self.spritesheet.load_sprite((x, y), width, height) # don't need the flipped sprite for these
      loaded_sprites[name] = sprite
    return loaded_sprites
  
  # create the boundary walls with category bits
  def create_boundary_wall(self, vertices, category_bits):
      wall_body = self.world.CreateStaticBody(shapes=b2EdgeShape(vertices=vertices))
      fixture = wall_body.fixtures[0]  # Get the default fixture created with the static body
      filterdata = fixture.filterData
      filterdata.categoryBits = category_bits
      fixture.filterData = filterdata

  
  def add_static_object(self, key, x, y, category_bits=GROUND_CATEGORY_BITS):
    dimensions = self.sprites[key].get_size()

    box2d_x = x/PPM
    box2d_y = (SCREEN_HEIGHT-y)/ PPM

    body = self.world.CreateStaticBody(
        position=(box2d_x, box2d_y),
        shapes=b2EdgeShape(vertices=[(-dimensions[0] / 2 / PPM, dimensions[1] / 2 / PPM), 
                                      (dimensions[0] / 2 / PPM, dimensions[1] / 2 / PPM)])
    )

    # apply collision filtering
    fixture = body.fixtures[0]
    filterdata = fixture.filterData
    filterdata.categoryBits = category_bits
    filterdata.maskBits = MARIO_CATEGORY_BITS | GROUND_CATEGORY_BITS
    fixture.filterData = filterdata

    # Store both the sprite key and the Box2D body for drawing
    self.elements.append({"sprite": key, "body": body})

  
  def add_kinematic_object(self, key, x, y, category_bits=GROUND_CATEGORY_BITS):
    dimensions = self.sprites[key].get_size()

    box2d_x = x/PPM
    box2d_y = (SCREEN_HEIGHT-y)/ PPM

    body = self.world.CreateKinematicBody(
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

    return body

  def create_beam_row(self, start_x, start_y, num_beams, slope_direction=SlopeDirection.NO_SLOPE, category_bits=GROUND_CATEGORY_BITS):
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
    return beam_x, beam_y,
  
  def create_moving_beam_row(self, start_x, start_y, num_beams, slope_direction=SlopeDirection.NO_SLOPE, category_bits=GROUND_CATEGORY_BITS):
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
      
      if i == 0:
         body = self.add_kinematic_object("beam", beam_x, beam_y, category_bits)
      else:
         self.add_kinematic_object("beam", beam_x, beam_y, category_bits)

    # return the x and y of the last beam created
    return beam_x, beam_y, body
  
  def add_barrel(self, x, y):
    # convert screen coordinates to Box2D coordinates
    box2d_x = x / PPM
    box2d_y = (SCREEN_HEIGHT - y) / PPM

    # get the radius
    radius = self.sprites["barrel"].get_size()[0] / 2

    # create the barrel as a dynamic body
    barrel_body = self.world.CreateDynamicBody(position=(box2d_x, box2d_y))
    barrel_body.linearVelocity = BARREL_SPEED * b2Vec2(1, 0)

    # create a circular shape for the barrel
    barrel_fixture = barrel_body.CreateFixture(
        shape=b2CircleShape(radius=radius / PPM),  # Convert radius to Box2D units
        density=5.0,
        friction=0.8, 
        restitution=0.1
    )

    # Apply collision filtering
    filterdata = barrel_fixture.filterData
    filterdata.categoryBits = BARREL_CATEGORY_BITS  # set the category for barrels
    filterdata.maskBits = (MARIO_CATEGORY_BITS | GROUND_CATEGORY_BITS | TOP_BOUNDARY_CATEGORY_BITS |
                           BOTTOM_WORLD_BOUNDARY_CATEGORY_BITS | LEFT_WORLD_BOUNDARY_CATEGORY_BITS | RIGHT_WORLD_BOUNDARY_CATEGORY_BITS)
    barrel_fixture.filterData = filterdata

    # store the barrel's information for drawing
    self.elements.append({"sprite": "barrel", "body": barrel_body})
    self.barrels.append(barrel_body)

    return barrel_body
  
  def move_barrels(self):
    for barrel in self.barrels:
        # check for boundary collisions
        for contact_edge in barrel.contacts:
            contact = contact_edge.contact
            if contact.touching:
                if contact.fixtureA.body == barrel:
                    other_fixture = contact.fixtureB
                else:
                    other_fixture = contact.fixtureA

                if other_fixture.filterData.categoryBits == LEFT_WORLD_BOUNDARY_CATEGORY_BITS:
                  barrel.linearVelocity = BARREL_SPEED * b2Vec2(1, 0)
                elif other_fixture.filterData.categoryBits == RIGHT_WORLD_BOUNDARY_CATEGORY_BITS:
                  barrel.linearVelocity = -BARREL_SPEED * b2Vec2(1, 0)

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
    
    ladder_width, ladder_height = self.sprites["ladder"].get_size()

    ladder_x = beam_x + ladder_width/2
    ladder_y = beam_y + ladder_height/2
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

  def update_platform_movement(self):
     for moving_platform in self.moving_platforms:
         moving_platform.move_platform()

class Moving_Platform_obj:
    def __init__(self, limit, body, speed):
        self.moving_right = True
        self.left_limit, self.right_limit = limit
        self.body = body
        self.speed = speed
        
    def move_platform(self):
        # Instead of directly modifying position, use linear velocity
        if self.body.position[0] > self.right_limit:
            self.moving_right = False
        elif self.body.position[0] < self.left_limit:
            self.moving_right = True
            
        # Clear existing velocity
        self.body.linearVelocity = (0, 0)
        
        # Apply new velocity
        if self.moving_right:
            self.body.linearVelocity = (self.speed, 0)
        else:
            self.body.linearVelocity = (-self.speed, 0)


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

  # add hammer item
  stage1.item_sprites.add(Hammer((200,SCREEN_HEIGHT-325)))
  stage1.add_barrel(100, 100)


  stage2 = Stage(donkey_kong_pos=(85,23),paulene_pos=(245,15),mario_pos=(100,625))
  beam_width, beam_height = stage2.sprites["beam"].get_size()
  beam_x = 0
  beam_y = SCREEN_HEIGHT-50

  # Start Beam
  beam_x, _ = stage2.create_beam_row(beam_x, beam_y, 4, SlopeDirection.NO_SLOPE)

  # Replace this beam with moving platform going left and right
  _, _, move_plat1 = stage2.create_moving_beam_row(210, beam_y, 1, SlopeDirection.NO_SLOPE)


  stage2.create_beam_row(600,beam_y, 5, SlopeDirection.NO_SLOPE)

  # First floor ladder 
  ladder_x = beam_width * 13
  ladder_y = SCREEN_HEIGHT - 90
  stage2.create_ladder(ladder_x, ladder_y, double_ladder=True)
  ladder_y = SCREEN_HEIGHT - 185
  stage2.create_ladder(ladder_x, ladder_y, double_ladder=False)

  stage2.create_ladder(440, 200, double_ladder=True)

  stage2.create_ladder(50, 440, double_ladder=True)
  stage2.create_ladder(50, 340, double_ladder=True)

  stage2.create_beam_row(600,beam_y- 170, 5, SlopeDirection.NO_SLOPE)

  # Should be moving platforms
  _, _, move_plat2 = stage2.create_moving_beam_row(300,beam_y- 170, 1, SlopeDirection.NO_SLOPE)
  _, _, move_plat3 = stage2.create_moving_beam_row(200,beam_y -400, 1, SlopeDirection.NO_SLOPE)

  stage2.create_beam_row(0,beam_y -400, 5, SlopeDirection.NO_SLOPE)


  stage2.create_beam_row(600,beam_y- 400, 12, SlopeDirection.NO_SLOPE)

  stage2.create_beam_row(0,beam_y- 170, 6, SlopeDirection.NO_SLOPE)
  stage2.create_pauline_platform(beam_width*5, 70)
  stage2.create_beam_row(0, beam_y-510, 10, SlopeDirection.SLOPE_DOWN)

  stage2.item_sprites.add(Paulene_Hat((600,210)))
  stage2.create_stacked_barrels(oil_barrel_width, 100)

  move_plat_1 = Moving_Platform_obj((5,18),move_plat1,0.05)
  move_plat_2 = Moving_Platform_obj((7,18),move_plat2,0.05)
  move_plat_3 = Moving_Platform_obj((6,18),move_plat3,0.05)
  stage2.moving_platforms.append(move_plat_1)
  stage2.moving_platforms.append(move_plat_2)
  stage2.moving_platforms.append(move_plat_3)


  return [stage1, stage2]