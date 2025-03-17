import pygame
from spritesheet import SpriteSheet

class Mario:
  def __init__(self, x, y):
    self.spritesheet = SpriteSheet("assets/sprites.png") # load sprite sheet


    self.mario_idle = self.spritesheet.get_sprite(2, 1, 16, 16)  # get sprite
    self.mario_idle = pygame.transform.scale(self.mario_idle, (64, 64)) # scale sprite
    self.mario_idle_flipped = SpriteSheet.flip_image(self.mario_idle)

    # Mario Walk Sprites
    self.mario_walk_1 = self.spritesheet.get_sprite(18, 1, 16, 16)
    self.mario_walk_1 = pygame.transform.scale(self.mario_walk_1, (64, 64)) # scale sprite
    self.mario_walk_1_flipped = SpriteSheet.flip_image(self.mario_walk_1)

    self.mario_walk_2 = self.spritesheet.get_sprite(36, 1, 16, 16)
    self.mario_walk_2 = pygame.transform.scale(self.mario_walk_2, (64, 64)) # scale sprite
    self.mario_walk_2_flipped = SpriteSheet.flip_image(self.mario_walk_2)

    self.mario_walk_animation = [self.mario_walk_1,self.mario_walk_2]
    self.mario_walk_animation_flipped = [self.mario_walk_1_flipped,self.mario_walk_2_flipped]

    self.mario_current_walk_frame = 0
    self.mario_walk_frames = 5
    
    self.mario_is_facing_right = True
    self.mario_is_walking = False

    self.move_index = 0

    self.image = self.mario_idle

    self.x = x
    self.y = y
    self.speed = 5


  
  def animation(self):
    if self.mario_is_walking:
      self.mario_current_walk_frame += 1
      if self.mario_current_walk_frame >= self.mario_walk_frames:
        self.mario_current_walk_frame = 0
        self.move_index += 1
        self.move_index %= 2
      
      if self.mario_is_facing_right:
        self.image = self.mario_walk_animation[self.move_index]
      else:
        self.image = self.mario_walk_animation_flipped[self.move_index]
    else:
      if self.mario_is_facing_right: 
        self.image = self.mario_idle
      else:
        self.image = self.mario_idle_flipped
      


  def handle_movement(self, keys):
    self.mario_is_walking = False

    if keys[pygame.K_LEFT]:
      self.x -= self.speed
      self.mario_is_facing_right = False
      self.mario_is_walking = True

    if keys[pygame.K_RIGHT]:
      self.x += self.speed
      self.mario_is_facing_right = True
      self.mario_is_walking = True
    

  def draw(self, screen):
    screen.blit(self.image, (self.x, self.y))