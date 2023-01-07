import pygame.event

from secondary import new_unit
from secondary import load_image
from globals import MOVEMENT_TYPES, HOUSE_DAMAGED_EVENT
from unitClass import Wizard


if __name__ == '__main__':
    unit = Wizard()
    unit.name = 'wizard'
    unit.health = 3
    unit.movement_range = 3
    unit.attack_range = 2
    unit.image = f'.\\data\\units\\{unit.name}\\image.png'
    new_unit(unit)
