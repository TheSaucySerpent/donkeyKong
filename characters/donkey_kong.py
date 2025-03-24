# Skyler Burden, Halie Numinen, Andrew Hua

import pygame
from sprite import SpriteSheet

class Donkey_Kong:
    def __init__(self,position,stage):
        self.spritesheet = SpriteSheet("assets/sprite_sheet.png") 
        self.scale = 3.2

        self.dk_idle, _ = self.spritesheet.load_sprite((5,258),width=41,height=32,scale=(self.scale, self.scale))
        
        self.dk_barrel_throw_left, self.dk_barrel_throw_right = self.spritesheet.load_sprite((0,292),44,32,(self.scale, self.scale))
        self.dk_barrel_throw_front, _ = self.spritesheet.load_sprite((54,292),41,32,(self.scale,self.scale))

        self.dk_barrel_throw = [self.dk_barrel_throw_left, self.dk_barrel_throw_front, self.dk_barrel_throw_right]
        self.dk_barrel, _ = self.spritesheet.load_sprite((72,232),17,10,(3.6,3.6))
        self.stage = stage
        self.position = position
        self.barrel_position = (position[0] + 34,position[1] + 60)
        self.image = self.dk_idle
        self.freeze = False


        # Index to figure out when to switch animations
        self.anim_frame_index = 0
        self.throw_animation_index = 0

        
    
    def animate(self):
        self.anim_frame_index += 1

        barrel_throw_start_frame = 120
        barrel_throw_end_frame = 400 - (barrel_throw_start_frame+1)
        
        
        if self.anim_frame_index > barrel_throw_end_frame:
            self.anim_frame_index = 0
            self.throw_animation_index = 0
            self.image = self.dk_idle
            

        elif self.anim_frame_index > barrel_throw_start_frame:
            if self.anim_frame_index % 40 == 0:
             self.image = self.dk_barrel_throw[self.throw_animation_index]
             self.throw_animation_index = (self.throw_animation_index + 1) % 3
             if self.throw_animation_index == 0:
                 self.stage.donkey_kong_throw()
             

    def draw(self,screen):
        if not self.freeze:
            self.animate()
        screen.blit(self.image, self.position)
        if self.throw_animation_index == 2:
            screen.blit(self.dk_barrel,self.barrel_position)
        

