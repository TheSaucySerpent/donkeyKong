from stage import Stage
from characters.mario import Mario
from Box2D import b2World, b2PolygonShape, b2EdgeShape
from conversions import *

SPRITE_DIMENSIONS = {
    "mario": (48, 48),
    "beam" : (48, 21),
    "oil_barrel": (48, 48),
    "upright_barrel": (30, 40),
    "ladder": (48, 60),
}

NUM_BEAMS = SCREEN_WIDTH // 48
SLOPE = 2

def add_oil_barrel(x, y, world, stage):
    world.CreateStaticBody(
        position=(x, y),
        shapes=b2PolygonShape(box=SPRITE_DIMENSIONS["oil_barrel"])
    )
    stage.add_element("oil_barrel", (x, y), SPRITE_DIMENSIONS["oil_barrel"])

def add_ladder(x, y, world, stage, dimensions=SPRITE_DIMENSIONS["ladder"]):
    world.CreateStaticBody(
        position=(x, y),
        shapes=b2PolygonShape(box=dimensions)
    )
    stage.add_element("ladder", (x, y), dimensions)

def create_stage1():
    world = b2World(gravity=(0, -10), doSleep=False) # create the physics world
    stage = Stage()                                  # create a new stage

    # create world boundaries
    world.CreateStaticBody(position=(0, 0), shapes=b2EdgeShape(vertices=[(0, 0), (SCREEN_WIDTH, 0)]))
    world.CreateStaticBody(position=(0, 0), shapes=b2EdgeShape(vertices=[(0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT)]))
    world.CreateStaticBody(position=(0, 0), shapes=b2EdgeShape(vertices=[(0, 0), (0, SCREEN_HEIGHT)]))
    world.CreateStaticBody(position=(0, 0), shapes=b2EdgeShape(vertices=[(SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)]))

    start_x, start_y = 0, 50
    beam_width, beam_height = SPRITE_DIMENSIONS["beam"]

    # create the first row (needs an extra beam to go outside the screen)
    for i in range(NUM_BEAMS + 1):
        beam_x = i * beam_width

        # first 7 beams are flat
        if i < 7:
            beam_y = start_y
        else:
            beam_y = start_y + (i - 7) * SLOPE

        world.CreateStaticBody(
            position=(beam_x, beam_y),
            shapes=b2PolygonShape(box=SPRITE_DIMENSIONS["beam"])
        )
        stage.add_element("beam", (beam_x, beam_y), SPRITE_DIMENSIONS["beam"])

    _, oil_barrel_height = SPRITE_DIMENSIONS["oil_barrel"]
    oil_barrel_x = start_x + beam_width
    oil_barrel_y = start_y + beam_height/2 + oil_barrel_height/2
    add_oil_barrel(oil_barrel_x, oil_barrel_y, world, stage)

    # create the second row
    start_x = 0
    start_y = 175

    _, ladder_height = SPRITE_DIMENSIONS["ladder"]
    ladder_x = SCREEN_WIDTH - beam_width * 2
    ladder_y = start_y - ladder_height - 10 
    add_ladder(ladder_x, ladder_y, world, stage)

    for i in range(NUM_BEAMS-1):
        beam_x = start_x + i * beam_width
        beam_y = start_y - SLOPE * (i + 1)

        world.CreateStaticBody(
            position=(beam_x, beam_y),
            shapes=b2PolygonShape(box=SPRITE_DIMENSIONS["beam"])
        )
        stage.add_element("beam", (beam_x, beam_y), SPRITE_DIMENSIONS["beam"])
    
    start_x = beam_width * 2
    start_y = start_y + 75
    for i in range(NUM_BEAMS - 1):
        beam_x = start_x + i * beam_width
        beam_y = start_y + SLOPE * (i + 1)

        world.CreateStaticBody(
            position=(beam_x, beam_y),
            shapes=b2PolygonShape(box=SPRITE_DIMENSIONS["beam"])
        )
        stage.add_element("beam", (beam_x, beam_y), SPRITE_DIMENSIONS["beam"])

    _, ladder_height = SPRITE_DIMENSIONS["ladder"]
    ladder_x = 0 + beam_width * 4
    ladder_y = start_y - ladder_height + 20
    add_ladder(ladder_x, ladder_y, world, stage, (SPRITE_DIMENSIONS["ladder"][0], SPRITE_DIMENSIONS["ladder"][1] + 10))
    
    ladder_x = beam_width * 10
    ladder_y = start_y - ladder_height + 20
    add_ladder(ladder_x, ladder_y, world, stage, (SPRITE_DIMENSIONS["ladder"][0], SPRITE_DIMENSIONS["ladder"][1] + 40))

    start_x = 0
    start_y = start_y + 125
    for i in range(NUM_BEAMS - 1):
        beam_x = start_x + i * beam_width
        beam_y = start_y - SLOPE * (i + 1)

        world.CreateStaticBody(
            position=(beam_x, beam_y),
            shapes=b2PolygonShape(box=SPRITE_DIMENSIONS["beam"])
        )
        stage.add_element("beam", (beam_x, beam_y), SPRITE_DIMENSIONS["beam"])

    ladder_x = beam_width * 7
    ladder_y = start_y - ladder_height
    add_ladder(ladder_x, ladder_y, world, stage, (SPRITE_DIMENSIONS["ladder"][0], SPRITE_DIMENSIONS["ladder"][1] + 20))

    ladder_x = SCREEN_WIDTH - beam_width * 2
    ladder_y = start_y - ladder_height
    add_ladder(ladder_x, ladder_y, world, stage, (SPRITE_DIMENSIONS["ladder"][0], SPRITE_DIMENSIONS["ladder"][1]))

    start_x = beam_width * 2
    start_y = start_y + 75
    for i in range(NUM_BEAMS - 1):
        beam_x = start_x + i * beam_width
        beam_y = start_y + SLOPE * (i + 1)
        world.CreateStaticBody(
            position=(beam_x, beam_y),
            shapes=b2PolygonShape(box=SPRITE_DIMENSIONS["beam"])
        )
        stage.add_element("beam", (beam_x, beam_y), SPRITE_DIMENSIONS["beam"]) 

    ladder_x = beam_width * 2
    ladder_y = start_y - ladder_height/2 - 10
    add_ladder(ladder_x, ladder_y, world, stage, (SPRITE_DIMENSIONS["ladder"][0], SPRITE_DIMENSIONS["ladder"][1]))

    ladder_x = beam_width * 10
    ladder_y = start_y - ladder_height/2 - 10
    add_ladder(ladder_x, ladder_y, world, stage, (SPRITE_DIMENSIONS["ladder"][0], SPRITE_DIMENSIONS["ladder"][1] + 30))

    start_y = start_y + 100
    for i in range(NUM_BEAMS - 1):
        beam_x = i * beam_width

        # first 7 beams are flat
        if i < 7:
            beam_y = start_y
        else:
            beam_y = start_y - (i - 7) * SLOPE

        world.CreateStaticBody(
            position=(beam_x, beam_y),
            shapes=b2PolygonShape(box=SPRITE_DIMENSIONS["beam"])
        )
        stage.add_element("beam", (beam_x, beam_y), SPRITE_DIMENSIONS["beam"])
    
    ladder_x = SCREEN_WIDTH - beam_width * 2
    ladder_y = start_y - ladder_height/2 - 10
    add_ladder(ladder_x, ladder_y, world, stage, (SPRITE_DIMENSIONS["ladder"][0], SPRITE_DIMENSIONS["ladder"][1]))

    start_x = beam_width * 7
    beam_y = start_y + 75
    for i in range(4):
        beam_x = start_x + i * beam_width

        world.CreateStaticBody(
            position=(beam_x, beam_y),
            shapes=b2PolygonShape(box=SPRITE_DIMENSIONS["beam"])
        )
        stage.add_element("beam", (beam_x, beam_y), SPRITE_DIMENSIONS["beam"])
    
    ladder_x = start_x + beam_width * 3
    ladder_y = beam_y - ladder_height/2 - 10
    add_ladder(ladder_x, ladder_y, world, stage, (SPRITE_DIMENSIONS["ladder"][0], SPRITE_DIMENSIONS["ladder"][1]))

    start_x = beam_width * 5
    beam_y -= 25
    for i in range(2):
        beam_x = start_x + i * beam_width

        world.CreateStaticBody(
            position=(beam_x, beam_y),
            shapes=b2PolygonShape(box=SPRITE_DIMENSIONS["beam"])
        )
        stage.add_element("beam", (beam_x, beam_y), SPRITE_DIMENSIONS["beam"])
    
    ladder_x = beam_width * 6
    ladder_y = beam_y + 50
    add_ladder(ladder_x, ladder_y, world, stage, (SPRITE_DIMENSIONS["ladder"][0] - 20, SPRITE_DIMENSIONS["ladder"][1] + 30))

    upright_barrel_width, upright_barrel_height = SPRITE_DIMENSIONS["upright_barrel"]
    for i in range(4):
        if i < 2:
            upright_barrel_x = 15 + upright_barrel_width * i 
            upright_barrel_y = beam_y -20
        else:
            upright_barrel_x = 15 + upright_barrel_width * (i - 2)
            upright_barrel_y = beam_y + upright_barrel_height/2

        world.CreateStaticBody(
            position=(upright_barrel_x, upright_barrel_y),
            shapes=b2PolygonShape(box=(upright_barrel_width, upright_barrel_height))
        )
        stage.add_element("upright_barrel", (upright_barrel_x, upright_barrel_y), SPRITE_DIMENSIONS["upright_barrel"])
        
    mario_x, mario_y = (140, 90)
    mario = Mario(mario_x, mario_y, world)

    return stage, {"mario": mario}, world
