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

    def update(self,Mario_rect):
        self.check_collision(Mario_rect)

    def check_collision(self, Mario_rect):
        if self.rect.colliderect(Mario_rect):
            self.on_collision()

    def on_collision(self):
        pass


    def draw(self,screen):
        screen.blit(self.image,self.position)
    
