import pygame
from sprite import SpriteSheet

# Constants for Stages
SPRITE_COORDS = {
    "beam": (109, 215, 16, 7),
    "ladder": (40, 211, 10, 16),
    "oil_barrel": (145, 193, 16, 16),
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
  
  def add_element(self, sprite_key, pos, scale=(64, 64)):
    self.elements.append({"sprite": sprite_key, "pos": pos, "scale": scale})
  
  def draw(self, screen):
      for element in self.elements:
          sprite_key = element["sprite"]
          center = element["pos"]  # Center-based position.
          scale = element["scale"]
          sprite = self.sprites[sprite_key]
          sprite = pygame.transform.scale(sprite, scale)

          # Convert center position to top-left by subtracting half of the scale dimensions.
          top_left = (int(center[0] - scale[0] / 2), int(center[1] - scale[1] / 2))
          screen.blit(sprite, top_left)
