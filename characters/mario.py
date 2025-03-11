import pygame
from spritesheet import SpriteSheet

class Mario:
  def __init__(self, x, y):
    self.spritesheet = SpriteSheet("assets/mario.png") # load sprite sheet
    self.image = self.spritesheet.get_sprite(0, 0, 32, 32) # get sprite
    self.x = x
    self.y = y
    self.speed = 5
  
  def handle_movement(self, keys):
    if keys[pygame.K_LEFT]:
      self.x -= self.speed
    if keys[pygame.K_RIGHT]:
      self.x += self.speed
  
  def draw(self, screen):
    screen.blit(self.image, (self.x, self.y))