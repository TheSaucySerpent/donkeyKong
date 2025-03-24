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

    def update(self, Mario, game_state):
        self.check_collision(Mario)

    def check_collision(self, Mario):
        if self.rect.colliderect(Mario.return_rect()):
            self.on_collision(Mario)

    def on_collision(self,Mario):
        bonus_sfx = pygame.mixer.Sound('assets/Bonus_sfx.wav')
        bonus_sfx.set_volume(0.1)
        bonus_sfx.play()

        pygame.mixer.music.unload()
        pygame.mixer.music.load("assets/Hammer_music.wav")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(start=3.8)

        pygame.mixer.music.queue("assets/level_music.wav")
        pygame.mixer.music.set_volume(0.5)

        Mario.activate_mario_hammer_time()

        self.kill()
        


    def draw(self,screen):
        screen.blit(self.image,self.position)
    
