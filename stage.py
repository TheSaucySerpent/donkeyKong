import pygame
from sprite import SpriteSheet
from conversions import *

# Constants for Stages
SPRITE_COORDS = {
    "beam": (109, 215, 16, 7),
    "ladder": (40, 211, 10, 16),
    "oil_barrel": (145, 193, 16, 16),
    "upright_barrel": (112, 229, 10, 16)
}

class Stage:
  def __init__(self):
    self.spritesheet = SpriteSheet("assets/sprites.png")
    self.sprites = self.load_sprites()
    self.elements = [] # the elements of the stage
  
  def load_sprites(self):
    loaded_sprites = {}
    for name, (x, y, width, height) in SPRITE_COORDS.items():
      sprite, _ = self.spritesheet.load_sprite((x, y), width, height)
      loaded_sprites[name] = sprite
    return loaded_sprites
  
  def add_element(self, sprite_key, pos, scale=(48, 48)):
    self.elements.append({"sprite": sprite_key, "pos": pos, "scale": scale})
  
  def draw(self, screen):
    for element in self.elements:
      sprite_key = element["sprite"]
      pos = element["pos"]
      scale = element["scale"]
      sprite = self.sprites[sprite_key]
      sprite = pygame.transform.scale(sprite, scale)

      # Use the position from the element
      # Convert the position to SDL coordinates
      sdl_pos = box2d_to_sdl(pos[0], pos[1])
      
      # Center the sprite at the position
      rect = sprite.get_rect(center=sdl_pos)
      screen.blit(sprite, rect.topleft)
