from game_defines import PPM, SCREEN_HEIGHT

def pixels_to_meters(pixels):
    """Convert pixels to meters"""
    return pixels / PPM

def meters_to_pixels(meters):
    """Convert meters to pixels"""
    return meters * PPM

def box2d_to_pygame(pos):
    """Convert Box2D world coordinates to Pygame screen coordinates"""
    return meters_to_pixels(pos[0]), SCREEN_HEIGHT - meters_to_pixels(pos[1])

def pygame_to_box2d(pos):
    """Convert Pygame screen coordinates to Box2D world coordinates"""
    return pixels_to_meters(pos[0]), pixels_to_meters(SCREEN_HEIGHT - pos[1])