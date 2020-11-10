def read_animal_text(filename):
    file = open(filename,"r+")
    content = file.read()
    animals = content.split("\n")
    animals = [item.lower() for item in animals]
    return animals