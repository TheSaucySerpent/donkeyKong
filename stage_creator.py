from stage import Stage
from characters.mario import Mario
from Box2D import b2World, b2_staticBody, b2PolygonShape

PPM = 30  # Make sure this matches the conversion in mario.py

def create_stage1():
    # Create a Box2D world with gravity (e.g., gravity downwards)
    world = b2World(gravity=(0, -10), doSleep=True)

    stage = Stage()

    # Example: Create the flat beams.
    flat_y = 500  # pixel y-coordinate for the flat beams
    num_beams = 5
    
    for i in range(num_beams):
        x = i * 64  # pixel x-coordinate
        stage.add_element("beam", (x, flat_y), (64, 32))
        # Create a corresponding static body for each beam in Box2D.
        # Convert pixel coordinates to meters.
        beam_x = (x + 32) / PPM  # center of the beam in x
        beam_y = (flat_y + 16) / PPM  # center of the beam in y
        # Create a static body for the beam.
        world.CreateStaticBody(
            position=(beam_x, beam_y),
            shapes=b2PolygonShape(box=(32 / PPM, 16 / PPM))
        )

    # Example: Create the ramp beams.
    start_x = 5 * 64  
    start_y = flat_y  
    delta_x = 64  
    delta_y = -20

    for i in range(6):
        beam_x = start_x + i * delta_x
        beam_y = start_y + i * delta_y
        stage.add_element("beam", (beam_x, beam_y), (64, 32))
        # Create static bodies for ramp beams.
        body_x = (beam_x + 32) / PPM
        body_y = (beam_y + 16) / PPM
        world.CreateStaticBody(
            position=(body_x, body_y),
            shapes=b2PolygonShape(box=(32 / PPM, 16 / PPM))
        )

    # Create Mario using the physics world.
    mario = Mario(150, 635, world)
    
    # Return both the stage and a dictionary of dynamic entities, plus the Box2D world.
    return stage, {"mario": mario}, world

def create_stage2():
    stage = Stage()
    # Add different elements, for example:
    stage.add_element("beam", (400, 250), (128, 32))
    return stage