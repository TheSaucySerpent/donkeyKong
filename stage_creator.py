from stage import Stage
from characters.mario import Mario
from Box2D import b2World, b2_staticBody, b2PolygonShape
from box2d_helper import pixels_to_meters

def create_stage1():
    # Create a Box2D world with gravity (downward)
    world = b2World(gravity=(0, -10), doSleep=False)

    stage = Stage()
    
    for i in range(5):
        x = i * 64
        y = 600
        stage.add_element("beam", (x, y), (64, 32))

        # Convert to meters for Box2D
        beam_x, beam_y = pixels_to_meters(x, y)

        # Create a static body for Box2D
        world.CreateStaticBody(
            position=(beam_x, beam_y),
        )

    # # Ramp Beams
    # start_x = 5 * 64  
    # start_y = flat_y  
    # delta_x = 64  
    # delta_y = -20  

    # for i in range(6):
    #     beam_x = start_x + i * delta_x
    #     beam_y = start_y + i * delta_y
    #     stage.add_element("beam", (beam_x, beam_y), (64, 32))  # Keep pixels

    #     # Convert to meters for Box2D
    #     body_x, body_y = pixels_to_meters(beam_x + 32, beam_y + 16)

    #     # Create static bodies for Box2D
    #     world.CreateStaticBody(
    #         position=(body_x, body_y),
    #         shapes=b2PolygonShape(box=(32 / PPM, 16 / PPM))
    #     )

    # Create Mario using Box2D
    mario_x, mario_y = (150, 584)  # Convert to meters
    mario = Mario(mario_x, mario_y, world)  # Convert back to pixels

    return stage, {"mario": mario}, world
