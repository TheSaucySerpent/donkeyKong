import pygame
from sprite import SpriteSheet

class Hammer(pygame.sprite.Sprite):

    def __init__(self,position):
        super().__init__()
        self.spritesheet = SpriteSheet("assets/sprite_sheet.png")
        self.image, _ = self.spritesheet.load_sprite((3,61),10,10)
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

        sound1 = pygame.mixer.Sound('assets/Bonus_sfx.wav')
        sound1.set_volume(0.1)
        sound1.play()

        pygame.mixer.music.unload()
        pygame.mixer.music.load("assets/Hammer_music.wav")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(start=3.8)

        pygame.mixer.music.queue("assets/level_music.wav")
        pygame.mixer.music.set_volume(0.5)

        self.kill()
        


    def draw(self,screen):
        screen.blit(self.image,self.position)
    
