# Skyler Burden, Halie Numinen, Andrew Hua

import pygame
from sprite import SpriteSheet
from Box2D import b2_dynamicBody, b2PolygonShape
from conversions import *
from game_defines import *

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
    "ladderclimb": (91,1),

    "Hammer_up_idle": (2,19),
    "Hammer_up_walk1": (37,19),
    "Hammer_up_walk2": (72,19),

    "Hammer_down_idle": (20,19),
    "Hammer_down_walk1": (55,19),
    "Hammer_down_walk2": (90,19),

}
MOVE_SPEED = 5

class Mario:
    def __init__(self, x, y, world, game_state):
        self.game_state = game_state
        self.spritesheet = SpriteSheet("assets/sprite_sheet.png")  # load the spritesheet

        # load Mario's sprites
        self.mario_idle, self.mario_idle_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["idle"])
        self.mario_walk_1, self.mario_walk_1_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["walk1"])
        self.mario_walk_2, self.mario_walk_2_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["walk2"])
        self.mario_jump, self.mario_jump_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["jump"])

        self.mario_ladder_climb, self.mario_ladder_climb_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["ladderclimb"])




        # Death sprites
        self.mario_death_1,self.mario_death_1_flipped  = self.spritesheet.load_sprite(SPRITE_COORDS["death1"])
        self.mario_death_2,self.mario_death_2_flipped  = self.spritesheet.load_sprite(SPRITE_COORDS["death2"])
        self.mario_death_3,self.mario_death_3_flipped  = self.spritesheet.load_sprite(SPRITE_COORDS["death3"])
        self.mario_death_4,self.mario_death_4_flipped  = self.spritesheet.load_sprite(SPRITE_COORDS["death4"])
        self.mario_death_5,self.mario_death_5_flipped  = self.spritesheet.load_sprite(SPRITE_COORDS["death5"])

        # Mario Hammer version
        self.mario_hammer_up_idle,self.mario_hammer_up_idle_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["Hammer_up_idle"])
        self.mario_hammer_up_walk_1, self.mario_hammer_up_walk_1_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["Hammer_up_walk1"])
        self.mario_hammer_up_walk_2, self.mario_hammer_up_walk_2_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["Hammer_up_walk2"])

        self.mario_hammer_down_idle,self.mario_hammer_down_idle_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["Hammer_down_idle"])
        self.mario_hammer_down_walk_1, self.mario_hammer_down_walk_1_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["Hammer_down_walk1"])
        self.mario_hammer_down_walk_2, self.mario_hammer_down_walk_2_flipped = self.spritesheet.load_sprite(SPRITE_COORDS["Hammer_down_walk2"])



        # Mario Hammer Sprites (The actual hammer object)
        self.hammer_up, self.hammer_up_flipped = self.spritesheet.load_sprite((3,61),10,10)
        self.hammer_down, self.hammer_down_flipped = self.spritesheet.load_sprite((18,61),17,9)
        self.hammer_up_flash, self.hammer_up_flash_flipped  = self.spritesheet.load_sprite((39,61),10,10)
        self.hammer_down_flash, self.hammer_down_flash_flipped = self.spritesheet.load_sprite((54,61),17,9)


        # create a list of frames for animations
        self.mario_walk_animation = [self.mario_walk_1, self.mario_walk_2]
        self.mario_walk_animation_flipped = [self.mario_walk_1_flipped, self.mario_walk_2_flipped]

        self.mario_death_animation = [self.mario_death_1,self.mario_death_2,self.mario_death_3,
                                      self.mario_death_4,self.mario_death_5]
        self.mario_death_animation_flipped = [self.mario_death_1_flipped,self.mario_death_2_flipped,
                                              self.mario_death_3_flipped,self.mario_death_4_flipped,
                                              self.mario_death_5_flipped]
        
        self.mario_climb_animation = [self.mario_ladder_climb, self.mario_ladder_climb_flipped]

        self.mario_hammer_idle_anim = [self.mario_hammer_up_idle,self.mario_hammer_down_idle]
        self.mario_hammer_idle_flipped_anim =[self.mario_hammer_up_idle_flipped,self.mario_hammer_down_idle_flipped]

        self.mario_hammer_up_walk_anim = (self.mario_hammer_up_walk_1,self.mario_hammer_up_walk_2)
        self.mario_hammer_up_walk_anim_flipped = (self.mario_hammer_up_walk_1_flipped,self.mario_hammer_up_walk_2_flipped)

        self.mario_hammer_down_walk_anim = (self.mario_hammer_down_walk_1,self.mario_hammer_down_walk_2)
        self.mario_hammer_down_walk_anim_flipped = (self.mario_hammer_down_walk_1_flipped,self.mario_hammer_down_walk_2_flipped)
        

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
        self.is_moving_on_ladder = False
        self.is_dead = False
        self.is_grounded = False
        self.has_hammer = False
        self.move_index = 0
        self.current_walk_frame = 0
        self.current_death_frame = 0
        self.current_climb_frame = 0
        self.current_hammer_frame = 0
        self.lock_direction = False

        # for testing
        self.just_climbed = False
        self.climb_cooldown = 0

        box2d_x = x/PPM
        box2d_y = (SCREEN_HEIGHT-y)/ PPM

        self.mario_start_pos_box2d = (box2d_x,box2d_y)
        

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
                    other_fixture = contact.fixtureB
                else:
                    other_body = contact.fixtureA.body
                    other_fixture = contact.fixtureA

                # Ensure the object isn't another dynamic body (like a barrel)
                # make sure the other object is below Mario (so that he can't cling to the ceiling)
                if (other_body.type != b2_dynamicBody and 
                    other_body.position.y < self.body.position.y and 
                    other_fixture.filterData.categoryBits == GROUND_CATEGORY_BITS):
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
    
    def is_on_pauline_platform(self):
        for contact_edge in self.body.contacts:
            contact = contact_edge.contact
            if contact.touching:
                # Determine the other body in contact
                if contact.fixtureA.body == self.body:
                    other_fixture = contact.fixtureB
                else:
                    other_fixture = contact.fixtureA

                # Check if the other fixture belongs to Pauline's platform
                if other_fixture.filterData.categoryBits == PAULINE_PLATFORM_CATEGORY_BITS:
                    return True
        return False

    def update_animation(self):
        # default to idle
        self.image = self.mario_idle if self.is_facing_right else self.mario_idle_flipped
        if self.has_hammer:
            self.is_climbing = False
            self.is_jumping = False
            self.current_hammer_frame += 1
            hammer_index = int(self.current_hammer_frame/5) % 2
            hammer_movement = int(self.current_hammer_frame/10) % 2
            if self.is_walking:
                if hammer_movement == 1:
                    self.image = (self.mario_hammer_up_walk_anim[hammer_index]
                    if self.is_facing_right
                    else self.mario_hammer_up_walk_anim_flipped[hammer_index])
                else:
                    self.image = (self.mario_hammer_down_walk_anim[hammer_index]
                                  if self.is_facing_right
                                  else self.mario_hammer_down_walk_anim_flipped[hammer_index]
                                  )
            else:
                if hammer_movement == 1:
                    self.image = (self.mario_hammer_idle_anim[0]
                                if self.is_facing_right 
                                else self.mario_hammer_idle_flipped_anim[0])
                else:
                    self.image = (self.mario_hammer_idle_anim[1]
                                if self.is_facing_right 
                                else self.mario_hammer_idle_flipped_anim[1])

            if self.current_hammer_frame > 720:
                self.has_hammer = False

        elif self.is_walking:
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

        if self.is_climbing:
            if self.is_moving_on_ladder:
                self.current_climb_frame += 1
            
            current_climb_frame = int(self.current_climb_frame/ 7) % 2
            self.image = self.mario_climb_animation[current_climb_frame]

        if self.is_pulling_up:
            pass

        if self.is_dead:
            self.body.linearVelocity = (0,0)
            frame_duration = 45
            self.lock_direction = True
            if self.current_death_frame == 0:
                pygame.mixer.music.unload()
                death_sound = pygame.mixer.Sound('assets/death.wav')
                death_sound.set_volume(0.1)
                death_sound.play()

            self.current_death_frame += 1
            if self.current_death_frame > (frame_duration * 6) - 1:
                self.current_death_frame = 0
                self.is_dead = False

                # Sets Mario back to the start
                self.lock_direction = False
                self.is_facing_right = True
                self.send_mario_to_start()

                pygame.mixer.music.load("assets/level_music.wav")
                pygame.mixer.music.set_volume(0.5) # set the volume
                pygame.mixer.music.play(-1)



            elif self.current_death_frame > frame_duration * 3:
                self.image = (self.mario_death_animation[4]
                                if self.is_facing_right
                                else self.mario_death_animation_flipped[4]
                        )
            elif self.current_death_frame < frame_duration * 2 - 20:
                pass
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
            self.is_walking = True
            if not self.lock_direction:
                self.is_facing_right = False

        elif keys[pygame.K_RIGHT]:
            self.body.linearVelocity = (MOVE_SPEED / PPM, velocity.y)
            self.is_walking = True

            if not self.lock_direction:
                self.is_facing_right = True
        else:
            self.body.linearVelocity = (0, velocity.y)

        if self.is_on_ladder():
            self.body.gravityScale = 0  # Disable gravity while climbing
            self.fixture.sensor = True  # Disable physical collision

            if keys[pygame.K_UP]:
                self.body.linearVelocity = (velocity.x, MOVE_SPEED / PPM)  # Move up
                self.is_climbing = True
                self.is_moving_on_ladder = True
            elif keys[pygame.K_DOWN]:
                self.body.linearVelocity = (velocity.x, -MOVE_SPEED / PPM)  # Move down
                self.is_climbing = True
                self.is_moving_on_ladder = True
            else:
                self.body.linearVelocity = (velocity.x, 0)  # Stop vertical movement
                self.is_moving_on_ladder = False
            
            self.just_climbed = True  # Set the flag when Mario is climbing
            self.climb_cooldown = 10  # Set cooldown (frames)

        else:
            self.is_climbing = False
            self.body.gravityScale = 1  # Restore gravity
            self.fixture.sensor = False  # Re-enable physical collision

            if self.climb_cooldown > 0:
                self.climb_cooldown -= 1  # Countdown the cooldown timer
            else:
                self.just_climbed = False  # Reset flag after cooldown

        # Prevent instant jump if just climbed
        if keys[pygame.K_UP] and self.is_grounded and not self.just_climbed:
            self.body.ApplyLinearImpulse((0, 15 * self.body.mass), self.body.worldCenter, True)
            self.is_jumping = True

        # if keys[pygame.K_DOWN] and not self.is_dead:
        #     self.game_state.lose_life()
        #     self.is_dead = True
        
        # print("Grounded:", self.is_grounded)
        # print("Velocity:", self.body.linearVelocity)

        # will later want to add handling for climbing
        if self.is_on_ladder():
            print("On ladder!")
        if self.is_on_pauline_platform():
            print("On Pauline's platform!")
            self.game_state.level_complete = True

        self.update_animation()

    def draw(self, screen):
        # Convert Box2D coordinates back to screen coordinates
        pos = box2d_to_pygame((self.body.position.x, self.body.position.y))
        rect = self.image.get_rect(center=pos)
        screen.blit(self.image, rect.topleft)

        if self.has_hammer:
            if int(self.current_hammer_frame/10) % 2:
                if self.is_facing_right:
                    hammer_pos = (rect.topleft[0] + 5, rect.topleft[1] - 30)
                    screen.blit(self.hammer_up, hammer_pos)
                else:
                    hammer_pos = (rect.topleft[0] + 12, rect.topleft[1] - 30)
                    screen.blit(self.hammer_up_flipped, hammer_pos)
                
            else:
                if self.is_facing_right:
                    hammer_pos =(rect.topleft[0] + 40, rect.topleft[1] + 16)
                    screen.blit(self.hammer_down, hammer_pos)
                else:
                    hammer_pos =(rect.topleft[0] - 40, rect.topleft[1] + 16)
                    screen.blit(self.hammer_down_flipped, hammer_pos)
        # print(f"Mario's position: {pos}")

    
    def change_mario_start_position(self,x,y):
        box2d_x = x/PPM
        box2d_y = (SCREEN_HEIGHT-y)/ PPM
        self.mario_start_pos_box2d = (box2d_x,box2d_y)

    def send_mario_to_start(self):
        self.body.position = self.mario_start_pos_box2d

    def return_rect(self):
        pos = box2d_to_pygame((self.body.position.x, self.body.position.y))
        return self.image.get_rect(center=pos)
    
    def activate_mario_hammer_time(self):
        self.has_hammer = True
        print(True)

