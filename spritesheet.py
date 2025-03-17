import pygame

class SpriteSheet:
  def __init__(self, filename):
    self.spritesheet = pygame.image.load(filename).convert_alpha()

  def get_sprite(self, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))
    return sprite
  
  def flip_image(image):
    return pygame.transform.flip(image,True, False)