from stage import Stage
from characters.mario import Mario
from Box2D import b2World, b2EdgeShape
from conversions import *

def create_stage1():
    world = b2World(gravity=(0, -10), doSleep=False)
    stage = Stage()

    # create world boundaries
    world.CreateStaticBody(position=(0,0), 
                           shapes=b2EdgeShape(vertices=[(0, 0), (SCREEN_WIDTH, 0)]))
    world.CreateStaticBody(position=(0,0), 
                           shapes=b2EdgeShape(vertices=[(0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT)]))
    world.CreateStaticBody(position=(0,0), 
                           shapes=b2EdgeShape(vertices=[(0, 0), (0, SCREEN_HEIGHT)]))
    world.CreateStaticBody(position=(0,0), 
                           shapes=b2EdgeShape(vertices=[(SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)]))
    
        
    mario_x, mario_y = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    mario = Mario(mario_x, mario_y, world)

    return stage, {"mario": mario}, world
