from stage import Stage

def create_stage1():
    stage = Stage()
    stage.add_element("beam", (300, 200), (128, 32))
    stage.add_element("beam", (275, 140), (128, 32))
    stage.add_element("oil_barrel", (250, 150))
    return stage

def create_stage2():
    stage = Stage()
    # Add different elements, for example:
    stage.add_element("beam", (400, 250), (128, 32))
    # You can build different layouts/stages as needed.
    return stage