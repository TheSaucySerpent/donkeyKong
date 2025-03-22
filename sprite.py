import pygame

SPRITE_SCALE = (48, 48)  # (width, height) after scaling
SPRITE_WIDTH = 16        # original sprite width in the spritesheet
SPRITE_HEIGHT = 16       # original sprite height in the spritesheet

class SpriteSheet:
  def __init__(self, filename):
      self.spritesheet = pygame.image.load(filename).convert_alpha()
      self.cache = {}  # optional caching

  # helper function to extract a sprite from the spritesheet.
  def get_sprite(self, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))
    return sprite

  # load_sprite now uses get_sprite to extract the raw image, then scales and flips it.
  # pos is assumed to be grid coordinates that need conversion to pixel coordinates.
  def load_sprite(self, pos, sprite_width=SPRITE_WIDTH, sprite_height=SPRITE_HEIGHT, sprite_scale=SPRITE_SCALE):
    x, y = pos

    sprite = self.get_sprite(x, y, sprite_width, sprite_height) # extract the sprite
    sprite = pygame.transform.scale(sprite, sprite_scale)       # scale the sprite.
    flipped_sprite = pygame.transform.flip(sprite, True, False) # create a flipped sprite
    return sprite, flipped_sprite                               # return both sprites