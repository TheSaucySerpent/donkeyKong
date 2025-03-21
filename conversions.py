SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PPM = 32

def box2d_to_sdl(x, y):
    return int(x), SCREEN_HEIGHT - int(y)
