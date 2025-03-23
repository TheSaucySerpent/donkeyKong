import pygame
from sprite import SpriteSheet

class Paulene:
    def __init__(self,position):
        self.spritesheet = SpriteSheet("assets/sprite_sheet.png") 

        self.paulene_idle_sprite_one,self.paulene_idle_sprite_one_flipped  = self.spritesheet.load_sprite((0,148),width=16,height=22,scale=2)
        self.paulene_idle_sprite_two, self.paulene_idle_sprite_two_flipped  = self.spritesheet.load_sprite((19,148),16,22,2)

        self.paulene_idle = [self.paulene_idle_sprite_one,self.paulene_idle_sprite_two]

        self.help_text, _ = self.spritesheet.load_sprite((91,183),24,8,2)

        self.position = position
        self.help_position = (position[0]+ 30, position[1] - 10)
        self.image = self.paulene_idle_sprite_one

        self.call_help = False

        # Index to figure out when to switch animations
        self.anim_frame_index = 0

        # Index to flip through the different idle animations
        self.anim_help_index = 0
        
    
    def animate(self):
        self.anim_frame_index += 1

        call_help_frame_end = 360
        call_help_frame_start = 240
        
        if self.anim_frame_index > call_help_frame_end:
            self.anim_frame_index = 0
            self.anim_help_index = 0
            self.call_help = False

        elif self.anim_frame_index > call_help_frame_start:
            self.call_help = True
            if self.anim_frame_index % 20 == 0:
             self.anim_help_index = (self.anim_help_index + 1) % 2
             self.image = self.paulene_idle[self.anim_help_index]
             

    def draw(self,screen):
        self.animate()
        if self.call_help:
            screen.blit(self.help_text,self.help_position)
        screen.blit(self.image, self.position)
        

