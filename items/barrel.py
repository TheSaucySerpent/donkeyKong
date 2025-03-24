# Skyler Burden, Halie Numinen, Andrew Hua

import pygame
from sprite import SpriteSheet
from Box2D import b2_dynamicBody, b2PolygonShape
from conversions import *
from game_defines import *


class barrel(pygame.sprite.Sprite):

    def __init__(self, world, x, y):
        super().__init__()
        self.spritesheet = SpriteSheet("assets/sprite_sheet.png")
        self.image, _ = self.spritesheet.load_sprite((2,232),13,10)        
        self.collision = False
        self.rect = self.image.get_rect()
        self.frame_counter = 0

        #creating barrel dynamic body and applying a force
        box2d_x = x/PPM
        box2d_y = (SCREEN_HEIGHT-y)/ PPM

        self.barrel_start_pos_box2d = (box2d_x,box2d_y)
        self.body = world.CreateDynamicBody(
            position=(box2d_x, box2d_y),
            type=b2_dynamicBody,
        )
        self.body.ApplyLinearImpulse(impulse = (10,0), point=self.body.worldCenter, wake=True)
        self.fixture = self.body.CreateFixture(
            shape=b2PolygonShape(box=(self.width/2/PPM, self.height/2/PPM)),
            density=1.0,
            friction=0.0,
            restitution=0.0,
        )

    def update(self,Mario_rect):
        self.check_collision(Mario_rect)

    def check_collision(self, Mario_rect):
        if self.rect.colliderect(Mario_rect):
            self.on_collision()

    def on_collision(self):
        pass

    def draw(self,screen):
        screen.blit(self.image,self.position)

    def counter(self, frame_counter):
        self.frame_counter += 1
    
