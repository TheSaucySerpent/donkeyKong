from stage import Stage

def create_stage1():
    stage = Stage()

    for i in range(15):
        stage.add_element("beam", (128*i, 700), (128, 32))

    stage.add_element("oil_barrel", (25, 635)) # oil barrel on bottom left
    
    return stage

def create_stage2():
    stage = Stage()
    # Add different elements, for example:
    stage.add_element("beam", (400, 250), (128, 32))
    # You can build different layouts/stages as needed.
    return stage