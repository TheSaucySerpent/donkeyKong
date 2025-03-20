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
  
  def draw(self, screen, screen_height):
    for element in self.elements:
        sprite_key = element["sprite"]
        pos = element["pos"]
        scale = element["scale"]
        sprite = self.sprites[sprite_key]
        sprite = pygame.transform.scale(sprite, scale)

        
        # Convert Box2D position to Pygame screen coordinates
        # Since Box2D origin is at bottom-left of screen and
        # Pygame origin is at the top left of the screen
        sdl_x, sdl_y = int(pos[0]), int(pos[1])

        screen.blit(sprite, (sdl_x, sdl_y))