import pygame

SPRITE_WIDTH = 16  # original sprite width in the spritesheet
SPRITE_HEIGHT = 16 # original sprite height in the spritesheet

class SpriteSheet:
  def __init__(self, filename):
      self.spritesheet = pygame.image.load(filename).convert_alpha() # load the spritesheet
      self.width = 0
      self.height = 0

  def load_sprite(self, pos, width=SPRITE_WIDTH, height=SPRITE_HEIGHT, scale=3):
    """load the sprite and return it alongside a flipped version"""
    x, y = pos

    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))         # extract the sprite
    sprite = pygame.transform.scale(sprite, (width*scale, height*scale)) # scale the sprite.
    flipped_sprite = pygame.transform.flip(sprite, True, False)          # create a flipped sprite

    self.width = sprite.get_width()
    self.height = sprite.get_height()

    return sprite, flipped_sprite