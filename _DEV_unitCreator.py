from secondary import new_unit
from unitClass import Unit

if __name__ == '__main__':
    unit = Unit()
    unit.name = 'warrior'
    unit.health = 3
    unit.movement_range = 3
    unit.attack_range = 1
    unit.image = f'.\\data\\units\\{unit.name}\\image.png'
    new_unit(unit)
