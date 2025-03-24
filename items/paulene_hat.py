# Skyler Burden, Halie Numinen, Andrew Hua

import pygame
from sprite import SpriteSheet

class Paulene_Hat(pygame.sprite.Sprite):

    def __init__(self,position):
        super().__init__()
        self.spritesheet = SpriteSheet("assets/sprite_sheet.png")
        self.image, _ = self.spritesheet.load_sprite((145,164),16,8)
        self.position = position
        self.collision = False
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def update(self,Mario,game_state):
        self.check_collision(Mario,game_state)

    def check_collision(self, Mario,game_state):
        if self.rect.colliderect(Mario.return_rect()):
            self.on_collision(Mario,game_state)

    def on_collision(self,Mario,game_state):

        bonus_sfx = pygame.mixer.Sound('assets/Bonus_sfx.wav')
        bonus_sfx.set_volume(0.1)
        bonus_sfx.play()
        game_state.add_score(500)

        self.kill()
        
    def draw(self,screen):
        screen.blit(self.image,self.position)
    
