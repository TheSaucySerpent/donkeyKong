import pygame
from sprite import SpriteSheet
from Box2D import b2BodyDef, b2_dynamicBody, b2PolygonShape
from conversions import *

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

        # create Mario's physics body
        self.body = world.CreateDynamicBody(
            position=(x, y),
            type=b2_dynamicBody,
        )

        self.body.CreateFixture(
            shape=b2PolygonShape(box=(x / PPM, y / PPM)),
            density=1.0,
            friction=0.3,
            restitution=0.0,
        )

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
            self.body.ApplyLinearImpulse((0, 100), self.body.worldCenter, True)
            self.is_jumping = True
        
        self.update_animation() # update animation accordlingly

    def draw(self, screen):
        pos = box2d_to_sdl(self.body.position.x, self.body.position.y)
        screen.blit(self.image, pos)