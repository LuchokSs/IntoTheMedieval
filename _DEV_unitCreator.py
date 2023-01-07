import pygame.event

from secondary import new_unit
from secondary import load_image
from globals import MOVEMENT_TYPES, HOUSE_DAMAGED_EVENT
from unitClass import Tower


if __name__ == '__main__':
    unit = Tower()
    unit.name = 'tower'
    unit.health = 4
    unit.movement_range = 0
    unit.attack_range = 6
    unit.image = f'.\\data\\units\\{unit.name}\\image.png'
    new_unit(unit)
