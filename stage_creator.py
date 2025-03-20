from stage import Stage

def create_stage1():
    stage = Stage()

    flat_y = 700
    for i in range(4):
        stage.add_element("beam", (128*i, 700), (128, 32))
    # Second loop: beams going up the screen for the ramped part.
    # Start where the flat beams ended.
    start_x = 8 * 64  
    start_y = flat_y  
    # Change these values (delta_x and delta_y) to adjust the steepness of your ramp.
    delta_x = 64  
    delta_y = -9  # negative y moves upward in pygame

    for i in range(8):  # number of beams on the ramp
        stage.add_element("beam", (512 + i * delta_x, 700 + i * delta_y), (64,32))

    stage.add_element("oil_barrel", (50, 635)) # oil barrel on bottom left
    
    return stage

def create_stage2():
    stage = Stage()
    # Add different elements, for example:
    stage.add_element("beam", (400, 250), (128, 32))
    # You can build different layouts/stages as needed.
    return stage