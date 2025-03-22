SCREEN_WIDTH = 768
SCREEN_HEIGHT = 700
FPS = 60
PPM = 32

def box2d_to_sdl(x, y):
    return int(x), SCREEN_HEIGHT - int(y)

def pixels_to_meters(pixels):
    return pixels / PPM