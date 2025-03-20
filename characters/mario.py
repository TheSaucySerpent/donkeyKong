import pygame
from sprite import SpriteSheet
from Box2D import b2BodyDef, b2_dynamicBody, b2PolygonShape

# Conversion favor from Box2D meters to pixels
PIXELS_PER_METER = 30.0

# Constants for Mario
SPRITE_COORDS = {
    "idle":  (2, 1),
    "walk1": (18, 1),
    "walk2": (36, 1),
    "jump":  (55, 1),
}
MOVE_SPEED = 4

class Mario:
    def __init__(self, x, y, world):
        self.spritesheet = SpriteSheet("assets/sprites.png")  # load the spritesheet

        # load Mario's sprites
        self.mario_idle, self.mario_idle_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["idle"])
        self.mario_walk_1, self.mario_walk_1_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["walk1"])
        self.mario_walk_2, self.mario_walk_2_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["walk2"])
        self.mario_jump, self.mario_jump_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["jump"])

        # create a list of frames for animations
        self.mario_walk_animation = [self.mario_walk_1, self.mario_walk_2]
        self.mario_walk_animation_flipped = [self.mario_walk_1_flipped, self.mario_walk_2_flipped]

        # default image is the idle sprite
        self.image = self.mario_idle

        # movement/animation state
        self.is_facing_right = True
        self.is_walking = False
        self.is_jumping = False
        self.move_index = 0
        self.current_walk_frame = 0

        # Create a Box2d dynamic body for Mario
        # Convert the  initial pixel position to Box2D world coordinates
        self.body = world.CreateDynamicBody(position=(x / PIXELS_PER_METER, y / PIXELS_PER_METER))
        self.width = self.image.get_width() / PIXELS_PER_METER
        self.height = self.image.get_height() / PIXELS_PER_METER
        self.body.CreatePolygonFixture(box=(self.width, self.height), density=1.0, friction=0.3)

    def update_animation(self):
        # default to idle
        self.image = self.mario_idle if self.is_facing_right else self.mario_idle_flipped

        if self.is_walking:
            self.current_walk_frame += 1
            if self.current_walk_frame >= 5:
                self.current_walk_frame = 0
                self.move_index = (self.move_index + 1) % len(self.mario_walk_animation)
            self.image = (
                self.mario_walk_animation[self.move_index]
                if self.is_facing_right
                else self.mario_walk_animation_flipped[self.move_index]
            )
        if self.is_jumping:
            self.image = self.mario_jump if self.is_facing_right else self.mario_jump_flipped

    def handle_movement(self, keys):
        self.is_walking = False
        self.is_jumping = False

        # base horizontal speed
        velocity = self.body.linearVelocity

        if keys[pygame.K_LEFT]:
            self.body.linearVelocity = (-MOVE_SPEED, velocity.y)
            self.is_facing_right = False
            self.is_walking = True
        elif keys[pygame.K_RIGHT]:
            self.body.linearVelocity = (MOVE_SPEED, velocity.y)
            self.is_facing_right = True
            self.is_walking = True
        else:
            # add dampening so Mario slows down when not moving
            self.body.linearVelocity = (0, velocity.y)

        if keys[pygame.K_UP]:
            self.body.ApplyLinearImpulse((0, 10), self.body.worldCenter, True)
            self.is_jumping = True
        
        self.update_animation() # update animation accordlingly

    def draw(self, screen):
        # conver Box2D world coordinates back to pixel coordinates
        pos = self.body.position
        x = pos.x * PIXELS_PER_METER - self.image.get_width() / 2
        y = pos.y * PIXELS_PER_METER - self.image.get_height() / 2

        screen.blit(self.image, (x, y))
