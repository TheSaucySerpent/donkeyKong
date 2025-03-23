import pygame
from sprite import SpriteSheet
from Box2D import b2_dynamicBody, b2PolygonShape
from conversions import *
from game_defines import MARIO_CATEGORY_BITS, GROUND_CATEGORY_BITS, LADDER_CATEGORY_BITS

# Constants for Mario
SPRITE_COORDS = {
    "idle":  (2, 1),
    "walk1": (18, 1),
    "walk2": (36, 1),
    "jump":  (55, 1),
    "death1": (0,37),
    "death2": (18,37),
    "death3": (36,37),
    "death4": (54,37),
    "death5": (72,37),
}
MOVE_SPEED = 5

class Mario:
    def __init__(self, x, y, world):
        self.spritesheet = SpriteSheet("assets/sprite_sheet.png")  # load the spritesheet

        # load Mario's sprites
        self.mario_idle, self.mario_idle_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["idle"])
        self.mario_walk_1, self.mario_walk_1_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["walk1"])
        self.mario_walk_2, self.mario_walk_2_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["walk2"])
        self.mario_jump, self.mario_jump_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["jump"])

        # Death sprites
        self.mario_death_1,self.mario_death_1_flipped  = self.spritesheet.load_sprite(SPRITE_COORDS["death1"])
        self.mario_death_2,self.mario_death_2_flipped  = self.spritesheet.load_sprite(SPRITE_COORDS["death2"])
        self.mario_death_3,self.mario_death_3_flipped  = self.spritesheet.load_sprite(SPRITE_COORDS["death3"])
        self.mario_death_4,self.mario_death_4_flipped  = self.spritesheet.load_sprite(SPRITE_COORDS["death4"])
        self.mario_death_5,self.mario_death_5_flipped  = self.spritesheet.load_sprite(SPRITE_COORDS["death5"])

        # create a list of frames for animations
        self.mario_walk_animation = [self.mario_walk_1, self.mario_walk_2]
        self.mario_walk_animation_flipped = [self.mario_walk_1_flipped, self.mario_walk_2_flipped]

        self.mario_death_animation = [self.mario_death_1,self.mario_death_2,self.mario_death_3,
                                      self.mario_death_4,self.mario_death_5]
        self.mario_death_animation_flipped = [self.mario_death_1_flipped,self.mario_death_2_flipped,
                                              self.mario_death_3_flipped,self.mario_death_4_flipped,
                                              self.mario_death_5_flipped]

        # default image is the idle sprite
        self.image = self.mario_idle
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.hammer_position = (0,0)

        # movement/animation state
        self.is_facing_right = True
        self.is_walking = False
        self.is_jumping = False
        self.is_climbing = False
        self.is_pulling_up = False
        self.is_dead = False
        self.is_grounded = False
        self.move_index = 0
        self.current_walk_frame = 0
        self.current_death_frame = 0

        box2d_x = x/PPM
        box2d_y = (SCREEN_HEIGHT-y)/ PPM

        # create Mario's physics body
        self.body = world.CreateDynamicBody(
            position=(box2d_x, box2d_y),
            type=b2_dynamicBody,
        )
        self.fixture = self.body.CreateFixture(
            shape=b2PolygonShape(box=(self.width/2/PPM, self.height/2/PPM)),
            density=1.0,
            friction=0.0,
            restitution=0.0,
        )

        self.fixture.categoryBits = MARIO_CATEGORY_BITS
        self.fixture.maskBits = GROUND_CATEGORY_BITS | LADDER_CATEGORY_BITS
    
    def is_on_ground(self):
        for contact_edge in self.body.contacts:
            contact = contact_edge.contact
            if contact.touching:
                # Check if Mario is touching something **below** him
                if contact.fixtureA.body == self.body:
                    other_body = contact.fixtureB.body
                else:
                    other_body = contact.fixtureA.body

                # Ensure the object isn't another dynamic body (like a barrel)
                if other_body.type != b2_dynamicBody:
                    return True
        return False
    
    def is_on_ladder(self):
        # Iterate over all contacts on Mario's body and check for ladder contact
        for contact_edge in self.body.contacts:
            contact = contact_edge.contact
            if contact.touching:
                # Identify the other fixture in the collision
                if contact.fixtureA.body == self.body:
                    other_fixture = contact.fixtureB
                else:
                    other_fixture = contact.fixtureA

                # Check if the other fixture belongs to the ladder
                if other_fixture.filterData.categoryBits == LADDER_CATEGORY_BITS:
                    return True
        return False

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

        if self.climbing:
            pass
        if self.is_pulling_up:
            pass

        if self.is_dead:
            self.body.linearVelocity = (0,0)
            frame_duration = 30
            self.current_death_frame += 1
            if self.current_death_frame > (frame_duration * 6) - 1:
                self.current_death_frame = 0
                self.is_dead = False
            elif self.current_death_frame > frame_duration * 3:
                self.image = (self.mario_death_animation[4]
                                if self.is_facing_right
                                else self.mario_death_animation_flipped[4]
                        )
            else:
                current_frame = int(self.current_death_frame/ 5) % 3
                self.image = (self.mario_death_animation[int(current_frame)]
                              if self.is_facing_right
                              else self.mario_death_animation_flipped[int(current_frame)])


    def handle_movement(self, keys):
        self.is_walking = False
        self.is_jumping = False

        # Update grounded state
        self.is_grounded = self.is_on_ground()

        velocity = self.body.linearVelocity

        if keys[pygame.K_LEFT]:
            self.body.linearVelocity = (-MOVE_SPEED / PPM, velocity.y)
            self.is_facing_right = False
            self.is_walking = True
        elif keys[pygame.K_RIGHT]:
            self.body.linearVelocity = (MOVE_SPEED / PPM, velocity.y)
            self.is_facing_right = True
            self.is_walking = True
        else:
            self.body.linearVelocity = (0, velocity.y)

        if keys[pygame.K_UP] and self.is_grounded:  # Jump only if on ground
            self.body.ApplyLinearImpulse((0, 15 * self.body.mass), self.body.worldCenter, True)
            self.is_jumping = True

        if keys[pygame.K_DOWN]:
            self.is_dead = True
        
        # print("Grounded:", self.is_grounded)
        # print("Velocity:", self.body.linearVelocity)

        # will later want to add handling for climbing
        if self.is_on_ladder():
            print("On ladder!")

        self.update_animation()

    def draw(self, screen):
        # Convert Box2D coordinates back to screen coordinates
        pos = box2d_to_pygame((self.body.position.x, self.body.position.y))
        rect = self.image.get_rect(center=pos)
        screen.blit(self.image, rect.topleft)
        # print(f"Mario's position: {pos}")

        

    def return_rect(self):
        pos = box2d_to_pygame((self.body.position.x, self.body.position.y))
        return   self.image.get_rect(center=pos)